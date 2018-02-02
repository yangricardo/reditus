from django.shortcuts import render, get_object_or_404, redirect
from .forms import SearchForm
from django.views.generic.edit import FormView
from .apps import SearchConfig as sc
import pandas as pd
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import re

def search_process(process):
    return sc.known_process_dict.get(process) if process in sc.known_process_dict else False
#end of search_process

def search_process_hash(process):
    return sc.data_processes_dict.get(process) if process in sc.data_processes_dict else False
#end of search_process_hash

def complete_process_data(process):
    #obtem a lista de hashes para os dados de sentenças
    process_keys_list = search_process(process)
    
    #inicializa o dataframe de retorno
    df = sc.data_processes_dict.get(process_keys_list[0])   
    
    #caso haja mais de uma referencia ao codigo do process(hash), 
    #concatena os diferentes hashes
    if len(process_keys_list) > 1:
        for i in range(1,len(process_keys_list)):
            #df = pd.concat( [df, sc.data_processes_dict.get(process_keys_list[i])] )  
            df.append(sc.data_processes_dict.get(process_keys_list[i]))
    return df
#end of complete_process_data    

def index(request):
    try:
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                process_keys_list = search_process(form.cleaned_data['search_field'])
                if process_keys_list != False:
                    return redirect('processo' ,form.cleaned_data['search_field'],0)
                else:
                    error = True
                    return render(request, 'search/index.html',{'form': form, 'error':error } )
        else:
            form = SearchForm()
            return render(request, 'search/index.html',{'form': form } )
    except:
        error = True
        return render(request, 'search/index.html',{'form': form, 'error':error } )

def showSentences(request,cod, index):
    process_keys_list = search_process(cod)

    try:
        if process_keys_list != False:
            data = complete_process_data(cod)
            print(data)
            process = data['processo'][int(index)]
            sentence = data['sentenca'][int(index)]
            similar = re.search(r"[0-9]{4}\.[0-9]{3}\.[0-9]{6}-[0-9]",data['similar_processo'][int(index)]).group(0)
            author = re.search(r"(autor|Autor)(\s*:\s*)(\w.+)+",sentence).group(3) if re.search(r"(autor|Autor)(\s*:\s*)(\w.+)+[^\n]",sentence) else ""
            reu = re.search(r"(reu|Reu|Réu|réu)(\s*:\s*)(\w.+)+",sentence).group(3) if re.search(r"(reu|Reu|Réu|réu)(\s*:\s*)(\w.+)+[^\n]",sentence) else ""

            #pages = [ i for i in range(data['processo'].count()) ]
            pages = data['processo'].count()-1
            print(pages)
            
            has_previous = True if int(index) > 0 else False
            has_next = True if int(index) < pages else False
            previousIndex = int(index)-1 if int(index) > 0 else 0
            nextIndex = int(index)+1 if int(index) < pages else pages
            #return render(request, 'search/sentenca.html', {'process': process,'sentence':sentence,'similar':similar,'author':author,'reu':reu, 'pages':pages, 'previousindex':previousIndex,'nextindex':nextIndex })
            return render(request, 'search/sentenca.html', {'cod':cod, 'index':index ,'process': process,'sentence':sentence,'similar':similar,'author':author,'reu':reu, 'pages':pages, 'previousindex':previousIndex,'nextindex':nextIndex,'has_previous':has_previous,'has_next':has_next  })
        
    except:
        error = True
        return render(request, 'search/sentenca.html',{'error':error } )