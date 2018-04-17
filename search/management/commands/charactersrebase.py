from django.core.management.base import BaseCommand, CommandError
from search.models import Process, ProcessFile, Character, ProcessCharacter
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
    help = 'Rebase the metadata`s processes references on database'

    def cleardatabase(self):
        ProcessCharacter.objects.all().delete()
        Character.objects.all().delete()
    #end of cleardatabase

    def charactersrebase(self):
        path = os.path.join(settings.BASE_DIR, 'static/data/elastic_data/'),
        regex_file = re.compile(r"Personagem\d{4}\.csv")
        
        onlyfiles = [ f for f in listdir(path[0]) if isfile(join(path[0], f)) and regex_file.match(f) ]  

        for f in onlyfiles:
            #le os dados do arquivo csv
            df = pd.read_csv(path[0] + f, sep=";" ,encoding = 'latin1',usecols=['P__COD_PERS','P__NOME']) 
            for index, row in df.iterrows():
                cod = row['P__COD_PERS']
                name = row['P__NOME']
                try:
                    Character.objects.get(id=cod)
                except ObjectDoesNotExist:
                    Character.objects.create(id=cod,name=name)
                    print('{} - {} cadastrado'.format(cod, name))
            print('{} completado'.format(f))
            del df
    # end of charactersrebase

    def processcharactersrebase(self):
        path = os.path.join(settings.BASE_DIR, 'static/data/elastic_data/'),
        regex_file = re.compile(r"PersonagemProcesso\d{4}\.csv")
        
        onlyfiles = [ f for f in listdir(path[0]) if isfile(join(path[0], f)) and regex_file.match(f) ]  
        print(onlyfiles)
        for f in onlyfiles:
            #le os dados do arquivo csv
            df = pd.read_csv(path[0] + f, sep=";" ,encoding = 'latin1',usecols=['PP__COD_PROC','PP__COD_PERS','PP__TIP_POLO']) 
            df = df.dropna(axis=0, how='any')

            for index, row in df.iterrows():
                processcod = row['PP__COD_PROC']
                charactercod = row['PP__COD_PERS']
                typerel = row['PP__TIP_POLO']

                try:
                    ProcessCharacter.objects.get(process_cod=processcod,character_cod=charactercod)
                except ObjectDoesNotExist:
                    try:
                        process = Process.objects.get(cod=processcod)
                        character = Character.objects.get(id=charactercod)
                        ProcessCharacter.objects.create(process_cod=process,character_cod=character,typerel=typerel)
                        print(process,character)
                    except ObjectDoesNotExist:
                        continue
            print('{} completado'.format(f))
            del df
    # end of charactersrebase


    def handle(self, *args, **options):
        self.cleardatabase()
        self.charactersrebase()
        self.processcharactersrebase()