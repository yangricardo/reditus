import pandas as pd
from os import listdir
from os.path import isfile, join
import re

known_process_dict = {}
data_processes_dict = {} 
similar_processes_dict = {}

processes_meta_dict = {}


def build_processes_dict_elastic():
    regex_file = re.compile(r"elasticinput_([0-9A-Z])+\.csv")
    
    path = '//Users/mac/Documents/reditus/reditus/static/data/data_tj/'
    #cria a lista com o nome de todos os arquivos do diretorio que se adequam ao regex_file
    onlyfiles = [ f for f in listdir(path) if isfile(join(path, f)) and regex_file.match(f) ]
    
    for f in onlyfiles:
        
        #le os dados do arquivo csv
        df = pd.read_csv(path + f, sep=";" ,encoding = 'latin1') 
        #armazena o numero do processo do arquivo csv
        
        for index, row in df.iterrows():
            COD_PROC = row['COD_PROC']
            Serventia = row['Serventia']
            COMARCA = row['COMARCA']
            if COD_PROC not in processes_meta_dict:
                processes_meta_dict.update(
                        { COD_PROC : (Serventia,COMARCA) }
                )
#end of build_processes_dict_elastic

def build_processes_dict():
    regex_file = re.compile(r"similar_to_([0-9A-Z])+\.csv")
    
    path = '//Users/mac/Documents/reditus/reditus/static/data/similares_const/'
    #cria a lista com o nome de todos os arquivos do diretorio que se adequam ao regex_file
    onlyfiles = [ f for f in listdir(path) if isfile(join(path, f)) and regex_file.match(f) ]
    
    for f in onlyfiles:
        re_process = re.compile(r"[0-9]{7}-[0-9]{2}\.[0-9]{4}\.[0-9]\.[0-9]{2}\.[0-9]{4}")
        re_autor = re.compile(r"(autor|Autor)(\s*:\s*)(\w.+)+[^\n]")
        re_reu = re.compile(r"(reu|Reu|Réu|réu)(\s*:\s*)(\w.+)+[^\n]")
        
        #le os dados do arquivo csv
        value = pd.read_csv(path + f, sep=";" ,encoding = 'latin1') 
        #armazena o numero do processo do arquivo csv
        process = value['processo'][0]
        print(process)
        #armazena o numero do hash do arquivo do processo
        process_hash = re.search(r"([0-9A-Z])+",f).group(0)
        #cria a chave composta por: processo + similar_file_number
    
        #caso a chave do processo não seja conhecida pelo dicionario,
        if value['processo'][0] not in known_process_dict:
           #cria a lista de chaves processos    
           known_process_dict.update({process: [process_hash] })
        else:
           #caso exista, atualiza a lista de chaves
           known_process_dict.get(process).append(process_hash)
       
        data_processes_dict.update({process_hash: value})   
#end of build_processes_dict    

def compute_similar_process_dict(df):
    for index, row in df.iterrows():
        process = row["processo"]
        similar_file = row["similar_file"]
        similar_process = re.search(r"[0-9]{4}\.[0-9]{3}\.[0-9]{6}-[0-9]",row["similar_processo"]).group(0)
        if similar_process not in similar_processes_dict:
            similar_processes_dict.update({similar_process : [ (similar_file, process) ]})
        else:
            value = (similar_file, process) 
            if not search_tuple(value, similar_processes_dict.get(similar_process)):
                similar_processes_dict.get(similar_process).append( (similar_file, process) )
#end of compute_similar_process_dict

def search_tuple(tup,lst):
    ret = False
    for t in lst:
        if t == tup:
            ret = True
    return ret
# end of search_tuple


def search_process(process):
    return known_process_dict.get(process) if process in known_process_dict else False
#end of search_process

def search_process_hash(process):
    return data_processes_dict.get(process) if process in data_processes_dict else False
#end of search_process_hash

def complete_process_data(process):
    #obtem a lista de hashes para os dados de sentenças
    process_keys_list = search_process(process)
    
    #inicializa o dataframe de retorno
    df = data_processes_dict.get(process_keys_list[0])   
    
    #caso haja mais de uma referencia ao codigo do process(hash), 
    #concatena os diferentes hashes
    if len(process_keys_list) > 1:
        for i in range(1,len(process_keys_list)):
            df = pd.concat([df,data_processes_dict.get(process_keys_list[i])])  
            print(df['processo'][0])
    return df
#end of complete_process_data    
    

def print_all_similar_process(process):
    print("- Processos similares ao de numero: "+ str(process[0]) + "\n")
    for p in data_process['similar_processo']:
        similar_process_key = re.search(r"[0-9]{4}\.[0-9]{3}\.[0-9]{6}\-[0-9]", p).group(0)
        print("- - Buscando dados do processo similar: "+ similar_process_key)
        similar_process = search_process(similar_process_key)
        if similar_process != False:
            print(complete_process_data(similar_process))
        else:
            print("- - - processo de numero "+ similar_process_key + " não encontrado")
#end of print_all_similar_process
            
def print_all_similar_process_hash(process):
    print("- Processos similares ao de numero: "+ str(process[0]) + "\n")
    for sp, sf  in data_process['similar_processo'], data_process['similar_file']:
        similar_process_key = re.search(r"[0-9]{4}\.[0-9]{3}\.[0-9]{6}\-[0-9]", sp).group(0)
        print("- - Buscando dados do processo similar: "+ similar_process_key)
        similar_process = search_process_hash(sf)
        if similar_process != False:
            print(complete_process_data(similar_process))
        else:
            print("- - - processo de numero "+ similar_process_key + " não encontrado")
#end of print_all_similar_process

    
build_processes_dict()

print(search_process("2016.001.261711-1"))
complete_process_data("2016.001.261711-1")

process_keys_list = search_process("2016.001.261711-1")
data_process = complete_process_data("2016.001.261711-1")
print_all_similar_process("2016.001.261711-1")

import time
for p in known_process_dict.items():
    print_all_similar_process(p)
    time.sleep(1)
    
len(known_process_dict.keys())

data_process['re_processo'] = re.search("(autor|Autor)(\s*:\s*)(\w.+)+[^\\n]", data_process['sentenca'][18].to_string()).group(3)

search_process_hash("000468C40707FD667E0F22D2B5C3FC9758CFC504571C3751")
compute_similar_process_dict(data_processes_dict["0004CADF0A424659663AF0E115BD2D45CD44C50550152510"])


