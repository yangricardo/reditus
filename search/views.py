from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .forms import SearchForm
from .models import Process, ProcessFile, Character, ProcessCharacter
from django.views.generic.edit import FormView
from .apps import SearchConfig as sc
import pandas as pd
import numpy as np
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from operator import itemgetter
import os
from reditus import settings
from os.path import isfile, join
import re


def index_view(request):
    try:
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                process = get_list_or_404(ProcessFile,cod=form.cleaned_data['search_field'])
                return redirect('processo' ,form.cleaned_data['search_field'],0)
            else: 
                raise Exception()
        form = SearchForm()
        return render(request, 'search/index.html',{'form': form } )
    except:
        error = True
        return render(request, 'search/index.html',{'form': form, 'error':error } )


def process_view(request,cod, index):
# try:
    process = get_object_or_404(Process,cod=cod)
    similars_files = get_list_or_404(ProcessFile,cod=cod)
    similars_data = get_similar_data(similars_files)
    
    #dados do processo
    process_serventia = process.serventia
    process_comarca = process.comarca

    process_movimento_url = "http://www4.tjrj.jus.br/consultaProcessoWebV2/consultaMov.do?v=2&numProcesso={}&acessoIP=internet&tipoUsuario=".format(process)
    process_contestacao_url = "http://gedweb.tjrj.jus.br/gedcacheweb/default.aspx?gedid={}".format(similars_data['constestacao_buscado'][int(index)])
    process_inicial_url = "http://gedweb.tjrj.jus.br/gedcacheweb/default.aspx?gedid={}".format(similars_data['inicial_buscado'][int(index)])

    #dados do similar
    similar_cod = re.search(r"\d{4}\.\d{3}\.\d{6}-\d",similars_data['similar_processo'][int(index)]).group(0)

    similar_metadata = get_object_or_404(Process,cod=similar_cod)
    similar_serventia = similar_metadata.serventia
    similar_comarca = similar_metadata.comarca

    similar_sentence = similars_data['sentenca'][int(index)]
    
    similar_atual_cod = re.search(r"\d{5,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{3,4}",similar_sentence).group(0) if re.search(r"\d{5,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{3,4}",similar_sentence) else ""
    
    similar_author = get_list_or_404(ProcessCharacter,process__cod=similar_cod,typerel='A')[0].character.name[:60]
    similar_reu = get_list_or_404(ProcessCharacter,process__cod=similar_cod,typerel='P')[0].character.name[:60]

    similar_movimento_url = "http://www4.tjrj.jus.br/consultaProcessoWebV2/consultaMov.do?v=2&numProcesso={}&acessoIP=internet&tipoUsuario=".format(similar_cod)
    similar_contestacao_url = "http://gedweb.tjrj.jus.br/gedcacheweb/default.aspx?gedid={}".format(similars_data['similar_file'][int(index)])
    similar_inicial_url = "http://gedweb.tjrj.jus.br/gedcacheweb/default.aspx?gedid={}".format(similars_data['similar_init'][int(index)])

    similar_percentage = similars_data['similaridade'][int(index)]
    
    similars_processes = []
    for i, row in similars_data.iterrows():
        if re.search(r"\d{4}\.\d{3}\.\d{6}-\d",row['similar_processo']).group(0) not in similars_processes: 
            similars_processes.append(
                (
                    re.search(r"\d{4}\.\d{3}\.\d{6}-\d",row['similar_processo']).group(0),
                    "http://gedweb.tjrj.jus.br/gedcacheweb/default.aspx?gedid={}".format(row['similar_file']),
                    row['similaridade'],
                )
            ) 

    similars_processes = sorted(list(set(similars_processes)),key=itemgetter(2), reverse=True)

    #paginação
    pages = similars_data['processo'].count()-1

    has_previous = True if int(index) > 0 else False
    has_next = True if int(index) < pages else False
    previousIndex = int(index)-1 if int(index) > 0 else 0
    nextIndex = int(index)+1 if int(index) < pages else pages

    return render(request, 'search/sentenca.html', {
        'cod':cod,'process_serventia':process_serventia,'process_comarca':process_comarca,'process_movimento_url':process_movimento_url,'process_inicial_url':process_inicial_url,'process_contestacao_url':process_contestacao_url,'similar_cod':similar_cod,'similar_atual_cod':similar_atual_cod,'similar_serventia':similar_serventia, 'similar_comarca':similar_comarca,'similar_sentence':similar_sentence,'similar_author':similar_author,'similar_reu':similar_reu,'similar_movimento_url':similar_movimento_url,'similar_inicial_url':similar_inicial_url,'similar_contestacao_url':similar_contestacao_url,'similar_percentage':similar_percentage,'similars_processes':similars_processes,'pages':pages, 'previousindex':previousIndex,'nextindex':nextIndex,'has_previous':has_previous,'has_next':has_next, 'index':index
        })
# except:
#     error = True
#     return render(request, 'search/sentenca.html', {'error':error})
        


def get_similar_data(hash_processes):
    regex_file = re.compile(r"similar_to_([0-9A-Z]+)\.csv")
    path = os.path.join(settings.BASE_DIR, 'static/data/similar_data/similares_const/'),

    process_data = pd.DataFrame()

    for hash_process in hash_processes:
        csv = join(path[0], "similar_to_{}.csv".format(hash_process))
        data = pd.read_csv(csv, sep=";" ,encoding = 'latin1')
        data = data[~data['sentenca'].str.contains('Homologo|HOMOLOGO|homologo|homologa-se|Homologa-se|Projeto em Revisão')]
        data = data[data['similar_processo'] != data['processo']]
        data['contestacao_processo'] = hash_process
        process_data = data if process_data.empty else process_data.append(data)
    
    process_data = process_data.sort_values(by=['similaridade'],ascending=False)
    process_data = process_data.reset_index(drop=True)
    return process_data