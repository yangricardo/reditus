from django.shortcuts import render, get_object_or_404, redirect
from .forms import SearchForm
from django.views.generic.edit import FormView
from .apps import SearchConfig as sc
import pandas as pd
from django.core.paginator import Paginator

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
            df = pd.concat([df,sc.data_processes_dict.get(process_keys_list[i])])  
    
    return df
#end of complete_process_data    

def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            process_keys_list = search_process(form.cleaned_data['search_field'])
            if process_keys_list != False:
                return redirect('processo' ,form.cleaned_data['search_field'])
            else:
                error = True
                return render(request, 'search/index.html',{'form': form, 'error':error } )
    else:
        form = SearchForm()
        return render(request, 'search/index.html',{'form': form } )

def showSentences(request,cod):
    process_keys_list = search_process(cod)
    if process_keys_list != False:
        data = complete_process_data(cod)
        paginator = Paginator(data, 1)
        return render(request, 'search/sentenca.html', )
    else:
        error = True
        return render(request, 'search/sentenca.html',{'error':error } )
    
