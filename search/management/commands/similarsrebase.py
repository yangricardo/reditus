from django.core.management.base import BaseCommand, CommandError
from search.models import Process, ProcessFile
from search.apps import SearchConfig as sc
from reditus import settings
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
import os
from os import listdir
from os.path import isfile, join
import re
import sys
import pandas as pd

class Command(BaseCommand):
    help = 'Rebase the similar files references on database'

    def cleardatabase(self):
        ProcessFile.objects.all().delete()
        Process.objects.all().delete()
    #end of cleardatabase

    def rebasedatabase(self):
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
                
                try:
                    Process.objects.get(cod=cod_process)
                except ObjectDoesNotExist:
                    Process.objects.create(cod=cod_process,serventia=serventia,comarca=comarca)
                    print('{} cadastrado'.format(cod_process))
       


    #end of rebasedabase


    def handle(self, *args, **options):
        print("Apagando dados de processos armazenados...")
        self.cleardatabase()
        print("Dados antigos de processos apagados.")
        self.rebasedatabase()
        
        