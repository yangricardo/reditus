from django.apps import AppConfig
from reditus import settings

import pandas as pd
import os
from os import listdir
from os.path import isfile, join
import re

class SearchConfig(AppConfig):
    name = 'search'

    known_process_dict = {}
    data_processes_dict = {} 
    processes_meta_dict = {}

    def build_processes_dict(self):
        regex_file = re.compile(r"similar_to_([0-9A-Z])+\.csv")

        path = os.path.join(settings.BASE_DIR, 'static/data/similares_const/'),
        
        #cria a lista com o nome de todos os arquivos do diretorio que se adequam ao regex_file
        onlyfiles = [ f for f in listdir(path[0]) if isfile(join(path[0], f)) and regex_file.match(f) ]

        for f in onlyfiles:
            re_process = re.compile(r"[0-9]{7}-[0-9]{2}\.[0-9]{4}\.[0-9]\.[0-9]{2}\.[0-9]{4}")
            re_autor = re.compile(r"(autor|Autor)(\s*:\s*)(\w.+)+[^\n]")
            re_reu = re.compile(r"(reu|Reu|Réu|réu)(\s*:\s*)(\w.+)+[^\n]")

            #le os dados do arquivo csv
            value = pd.read_csv(path[0] + f, sep=";" ,encoding = 'latin1') 
            #armazena o numero do processo do arquivo csv
            process = value['processo'][0]
            #armazena o numero do hash do arquivo do processo
            process_hash = re.search(r"([0-9A-Z])+",f).group(0)
            #cria a chave composta por: processo + similar_file_number

            #caso a chave do processo não seja conhecida pelo dicionario,
            if value['processo'][0] not in self.known_process_dict:
                #cria a lista de chaves processos    
                self.known_process_dict.update({process: [process_hash] })
            else:
                #caso exista, atualiza a lista de chaves
                self.known_process_dict.get(process).append(process_hash)

            self.data_processes_dict.update({process_hash: value})   

        #build dos dados de comarca com base nos arquivos do elastic search

        regex_file = re.compile(r"elasticinput_([0-9A-Z])+\.csv")
        
        path = os.path.join(settings.BASE_DIR, 'static/data/data_tj/'),
        #cria a lista com o nome de todos os arquivos do diretorio que se adequam ao regex_file
        onlyfiles = [ f for f in listdir(path[0]) if isfile(join(path[0], f)) and regex_file.match(f) ]
        
        for f in onlyfiles:
            
            #le os dados do arquivo csv
            df = pd.read_csv(path[0] + f, sep=";" ,encoding = 'latin1') 
            #armazena o numero do processo do arquivo csv
            
            for index, row in df.iterrows():
                COD_PROC = row['COD_PROC']
                Serventia = row['Serventia']
                COMARCA = row['COMARCA']
                if COD_PROC not in self.processes_meta_dict:
                    self.processes_meta_dict.update(
                            { COD_PROC : (Serventia,COMARCA) }
                    )
    #end of build_processes_dict    

    def ready(self):
        self.build_processes_dict()
        print('Processos Carregados...')