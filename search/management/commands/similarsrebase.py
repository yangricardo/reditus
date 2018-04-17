from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_list_or_404
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
    help = 'Rebase the similar files references of processes on database'

    def clearsimilars(self):
        ProcessFile.objects.all().delete()
    #end of cleardatabase

    def similarrebase(self):
        regex_file = re.compile(r"similar_to_([0-9A-Z]+)\.csv")
        path = os.path.join(settings.BASE_DIR, 'data/similar_data/similares_const/'),
        #cria a lista com o nome de todos os arquivos do diretorio que se adequam ao regex_file
        try:
            similarfiles = get_list_or_404(ProcessFile)
            similarfiles = [ file.id for file in similarfiles ]
            similarfiles = set(similarfiles)
            onlyfiles = [ f for f in listdir(path[0]) if isfile(join(path[0], f)) and regex_file.match(f) ]
            onlyfiles = [ f for f in onlyfiles if regex_file.match(f).group(1) not in similarfiles ]
            print(onlyfiles)
        except:
            onlyfiles = [ f for f in listdir(path[0]) if isfile(join(path[0], f)) and regex_file.match(f) ]
        print("Lendo arquivos de similares do diretorio: {}".format(path[0]))

        for f in onlyfiles:
            data = pd.read_csv(path[0] + f, sep=";" ,encoding = 'latin1')
            cod_process = data['processo'][0]
            id_file = regex_file.match(f).group(1)
            del data
            try:
                process = Process.objects.get(cod=cod_process)
                try:
                    ProcessFile.objects.get(id=id_file,cod=process)
                except ObjectDoesNotExist:
                    ProcessFile.objects.create(id=id_file,cod=process)
                    print('Arquivo Similar ao processo {} de id {} cadastrado'.format(process,id_file))
            except ObjectDoesNotExist:
                continue
    #end of rebasedabase


    def handle(self, *args, **options):
        print("Apagando dados de processos similares armazenados...")
        self.clearsimilars()
        print("Dados antigos de processos processos similares apagados.")
        self.similarrebase()
        print("Cadastro de referencias de processos similares finalizado.")
        
        