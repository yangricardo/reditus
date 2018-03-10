from django.apps import AppConfig
from reditus import settings

import pandas as pd
import os
from os import listdir
from os.path import isfile, join
import re
import sys

class SearchConfig(AppConfig):
    name = 'search'

    process_dict = {}

    '''
        process_dict = {
            cod_proc : {
                'cod_process':str(cod_process) ,
                'hash_processes':[ str(hash_processes) ], 
                'serventia' : str(serventia)
                'comarca' : str(comarca)
            }
        }
    '''

    def build_process_dict(self):
        regex_file = re.compile(r"similar_to_([0-9A-Z]+)\.csv")
        path = os.path.join(settings.BASE_DIR, 'static/data/similar_data/'),
        #cria a lista com o nome de todos os arquivos do diretorio que se adequam ao regex_file
        onlyfiles = [ f for f in listdir(path[0]) if isfile(join(path[0], f)) and regex_file.match(f) ]
        print("Lendo arquivos de similares do diretorio: {}".format(path[0]))
        # for f in onlyfiles:
        #     data = pd.read_csv(path[0] + f, sep=";" ,encoding = 'latin1')
            
        #     data = data[~data['sentenca'].str.contains('Homologo|HOMOLOGO|homologo|homologa-se|Homologa-se|Projeto em Revisão')]
        #     data = data[data['similar_processo'] != data['processo']]
            
        #     data = data.reset_index(drop=True)

        #     cod_process = data['processo'][0]

        #     if cod_process not in self.process_dict:
        #         self.process_dict.update({cod_process : {'data':data, 'similar_processo':{} }})
        #     else:
        #         self.process_dict.get(cod_process).get('data').append(data)

        #     for index, row in self.process_dict.get(cod_process).get('data').iterrows():
        #         similar = re.search(r"[0-9]{4}\.[0-9]{3}\.[0-9]{6}-[0-9]",row['similar_processo']).group(0)

        #         if similar not in self.process_dict.get(cod_process).get('similar_processo'):
        #             similar_url = "http://gedweb.tjrj.jus.br/gedcacheweb/default.aspx?gedid="+row['similar_file']
        #             self.process_dict.get(cod_process).get('similar_processo').update({similar : (similar,similar_url,row['similaridade']) })

        #     process_url = "http://gedweb.tjrj.jus.br/gedcacheweb/default.aspx?gedid="+re.search(r"similar_to_([0-9A-Z]+)\.csv",path[0] + f).group(1)
        #     self.process_dict.get(cod_process).update({'process_url':process_url})

        for f in onlyfiles:
            data = pd.read_csv(path[0] + f, sep=";" ,encoding = 'latin1')
            cod_process = data['processo'][0]
            hash_process = regex_file.match(f).group(1)

            if cod_process not in self.process_dict:
                self.process_dict.update({
                    cod_process: {
                        'cod_process':cod_process ,
                        'hash_processes':[hash_process], 
                        } 
                    })
            else:
                self.process_dict.get(cod_process).get('hash_processes').append(hash_process)

        regex_file = re.compile(r"elasticinput_([0-9A-Z])+\.csv")
        path = os.path.join(settings.BASE_DIR, 'static/data/elastic_data/'),
        #cria a lista com o nome de todos os arquivos do diretorio que se adequam ao regex_file
        onlyfiles = [ f for f in listdir(path[0]) if isfile(join(path[0], f)) and regex_file.match(f) ]       
        print("Lendo metadados do diretorio: {}".format(path[0]))         
        for f in onlyfiles:
            #le os dados do arquivo csv
            df = pd.read_csv(path[0] + f, sep=";" ,encoding = 'latin1') 
            #armazena o numero do processo do arquivo csv
            for index, row in df.iterrows():
                cod_process = row['COD_PROC']
                serventia = row['Serventia']
                comarca = row['COMARCA']
                if cod_process in self.process_dict:
                    self.process_dict.get(cod_process).update(
                        { 
                            'serventia':serventia,
                            'comarca': comarca,
                        }
                    )

        print(self.process_dict)
    #end of build_process_dict    

    def ready(self):
        print("Carregando dados dos processos...")
        self.build_process_dict()
        print('Códigos de Processos Carregados:')
        print(self.process_dict.keys())
        print("{} bytes ocupados em memória".format(sys.getsizeof(self.process_dict)))