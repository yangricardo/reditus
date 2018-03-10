from django.shortcuts import render, get_object_or_404, redirect
from .forms import SearchForm
from django.views.generic.edit import FormView
from .apps import SearchConfig as sc
import pandas as pd
import numpy as np
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import os
from reditus import settings
from os.path import isfile, join
import re


def search_process_metadata(cod_process):
    return sc.process_dict.get(cod_process) if cod_process in sc.process_dict else {}

def index_view(request):
    try:
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                process_data = search_process_metadata(form.cleaned_data['search_field'])

                if bool(process_data):
                    return redirect('processo' ,form.cleaned_data['search_field'],0)
                else:
                    raise Exception()
            else: 
                raise Exception()
        form = SearchForm()
        return render(request, 'search/index.html',{'form': form } )
    except:
        error = True
        return render(request, 'search/index.html',{'form': form, 'error':error } )


def process_view(request,cod, index):
    #try:
    process_data = search_process_metadata(cod)
    if bool(process_data):
        similars_data = get_similar_data(process_data.get('hash_processes'))
        #dados do processo
        process_serventia = process_data.get('serventia')
        process_comarca = process_data.get('comarca')

        process_movimento_url = "http://www4.tjrj.jus.br/consultaProcessoWebV2/consultaMov.do?v=2&numProcesso={}&acessoIP=internet&tipoUsuario=".format(cod)
        process_contestacao_url = "http://gedweb.tjrj.jus.br/gedcacheweb/default.aspx?gedid={}".format(similars_data['contestacao_processo'][int(index)])

        #dados do similar
        similar_cod = re.search(r"\d{4}\.\d{3}\.\d{6}-\d",similars_data['similar_processo'][int(index)]).group(0)

        similar_metadata = search_process_metadata(similar_cod)
        similar_serventia = similar_metadata.get('serventia')
        similar_comarca = similar_metadata.get('comarca')

        similar_sentence = similars_data['sentenca'][int(index)]
        
        similar_atual_cod = re.search(r"\d{5,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{3,4}",similar_sentence).group(0) if re.search(r"\d{5,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{3,4}",similar_sentence) else ""
        similar_author = re.search(r"(autor|Autor|AUTOR|Autora|autora|AUTORA)(\s*:\s*)(\w.+)+",similar_sentence).group(3) if re.search(r"(autor|Autor|AUTOR|Autora|autora|AUTORA)(\s*:\s*)(\w.+)+[^\n]",similar_sentence) else ""
        similar_reu = re.search(r"(reu|Reu|Réu|réu|REU|RÉU|RÉ|Ré|ré)(\s*:\s*)(\w.+)+",similar_sentence).group(3) if re.search(r"(reu|Reu|Réu|réu|REU|RÉU|RÉ|Ré|ré)(\s*:\s*)(\w.+)+[^\n]",similar_sentence) else ""

        similar_movimento_url = "http://www4.tjrj.jus.br/consultaProcessoWebV2/consultaMov.do?v=2&numProcesso={}&acessoIP=internet&tipoUsuario=".format(similar_cod)
        similar_contestacao_url = "http://gedweb.tjrj.jus.br/gedcacheweb/default.aspx?gedid={}".format(similars_data['similar_file'][int(index)])

        print(similar_movimento_url)
        print(similar_contestacao_url)

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

        #paginação
        pages = similars_data['processo'].count()-1

        has_previous = True if int(index) > 0 else False
        has_next = True if int(index) < pages else False
        previousIndex = int(index)-1 if int(index) > 0 else 0
        nextIndex = int(index)+1 if int(index) < pages else pages

        return render(request, 'search/sentenca.html', {
            'cod':cod,'process_serventia':process_serventia,'process_comarca':process_comarca,'process_movimento_url':process_movimento_url,'process_contestacao_url':process_contestacao_url,'similar_cod':similar_cod,'similar_atual_cod':similar_atual_cod,'similar_serventia':similar_serventia, 'similar_comarca':similar_comarca,'similar_sentence':similar_sentence,'similar_author':similar_author,'similar_reu':similar_reu,'similar_movimento_url':similar_movimento_url,'similar_contestacao_url':similar_contestacao_url,'similar_percentage':similar_percentage,'similars_processes':similars_processes,'pages':pages, 'previousindex':previousIndex,'nextindex':nextIndex,'has_previous':has_previous,'has_next':has_next, 'index':index
            })
    # except:
    #     error = True
    #     return render(request, 'search/sentenca.html',{'error':error } )


def get_similar_data(hash_processes):
    regex_file = re.compile(r"similar_to_([0-9A-Z]+)\.csv")
    path = os.path.join(settings.BASE_DIR, 'static/data/similar_data/'),

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

class Process(object):
    cod = ""
    similar = ""
    similar_atual = ""
    sentence = ""
    author = ""
    reu = ""
    data = ""
    url = ""

    def __init__(self, cod, data):
        self.cod = cod
        self.similar = re.search(r"\d{4}\.\d{3}\.\d{6}-\d",data['similar_processo']).group(0)
        self.cod = data['processo']
        self.sentence = data['sentenca']
        self.similar = re.search(r"\d{4}\.\d{3}\.\d{6}-\d",data['similar_processo']).group(0)
        self.author = re.search(r"(autor|Autor)(\s*:\s*)(\w.+)+",sentence).group(3) if re.search(r"(autor|Autor)(\s*:\s*)(\w.+)+[^\n]",sentence) else ""
        self.similar_atual = re.search(r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}",sentence).group(0) if re.search(r"\d{6}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}",sentence) else ""
        self.reu = re.search(r"(reu|Reu|Réu|réu)(\s*:\s*)(\w.+)+",sentence).group(3) if re.search(r"(reu|Reu|Réu|réu)(\s*:\s*)(\w.+)+[^\n]",sentence) else ""
