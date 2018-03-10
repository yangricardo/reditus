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


def search_process_test(cod_process):
    return sc.process_dict.get(cod_process) if cod_process in sc.process_dict else {}

def index_view(request):
    try:
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                process_data = search_process_test(form.cleaned_data['search_field'])

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
    # try:
    #     process_data = search_process_test(cod)
    #     similar_data = get_similar_data(process_data)
    #     # if bool(process_data):
        #     serventia = process_data.get('serventia')
        #     comarca = process_data.get('comarca')
        #     df = get_similar_data
        #     process = df['processo'][int(index)]
        #     process_contestacao_url = process_data.get('process_url')
        #     sentence = df['sentenca'][int(index)]
        #     similar = re.search(r"\d{4}\.\d{3}\.\d{6}-\d",df['similar_processo'][int(index)]).group(0)
        #     author = re.search(r"(autor|Autor|AUTOR|Autora|autora|AUTORA)(\s*:\s*)(\w.+)+",sentence).group(3) if re.search(r"(autor|Autor|AUTOR|Autora|autora|AUTORA)(\s*:\s*)(\w.+)+[^\n]",sentence) else ""
        #     similar_atual = re.search(r"\d{5,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}",sentence).group(0) if re.search(r"\d{5,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}",sentence) else ""
        #     reu = re.search(r"(reu|Reu|Réu|réu|REU|RÉU|RÉ|Ré|ré)(\s*:\s*)(\w.+)+",sentence).group(3) if re.search(r"(reu|Reu|Réu|réu|REU|RÉU|RÉ|Ré|ré)(\s*:\s*)(\w.+)+[^\n]",sentence) else ""
        #     similar_contestacao_url = "http://gedweb.tjrj.jus.br/gedcacheweb/default.aspx?gedid="+df['similar_file'][int(index)]
        #     process_movimento_url = "http://www4.tjrj.jus.br/consultaProcessoWebV2/consultaMov.do?v=2&numProcesso="+process+"&acessoIP=internet&tipoUsuario="
        #     similar_movimento_url = "http://www4.tjrj.jus.br/consultaProcessoWebV2/consultaMov.do?v=2&numProcesso="+similar+"&acessoIP=internet&tipoUsuario="
        #     similaridade = df['similaridade'][int(index)]

        #     similar_processes = list(process_data.get('similar_processo').items())

            
        #     pages = df['processo'].count()-1
            
        #     has_previous = True if int(index) > 0 else False
        #     has_next = True if int(index) < pages else False
        #     previousIndex = int(index)-1 if int(index) > 0 else 0
        #     nextIndex = int(index)+1 if int(index) < pages else pages
        #     #return render(request, 'search/sentenca.html', {'process': process,'sentence':sentence,'similar':similar,'author':author,'reu':reu, 'pages':pages, 'previousindex':previousIndex,'nextindex':nextIndex })
        #     return render(request, 'search/sentenca.html', {'cod':cod, 'index':index ,'process': process,'process_contestacao_url':process_contestacao_url,'sentence':sentence,'similar':similar,'similaridade':similaridade,'similar_atual':similar_atual,'similar_processes':similar_processes,'author':author,'reu':reu,'similar_contestacao_url':similar_contestacao_url,'similar_movimento_url':similar_movimento_url,'process_movimento_url':process_movimento_url,'serventia':serventia,'comarca':comarca,'pages':pages, 'previousindex':previousIndex,'nextindex':nextIndex,'has_previous':has_previous,'has_next':has_next  })
    #     return render(request, 'search/sentenca.html')
    # except:
    #     error = True
    #     return render(request, 'search/sentenca.html',{'error':error } )

    process_data = search_process_test(cod)
    similar_data = get_similar_data(process_data.get('hash_processes'))

    return render(request,'search/sentenca.html')



def get_similar_data(hash_processes):
    regex_file = re.compile(r"similar_to_([0-9A-Z]+)\.csv")
    path = os.path.join(settings.BASE_DIR, 'static/data/similar_data/'),

    process_data = pd.DataFrame()

    for hash_process in hash_processes:
        csv = join(path[0], "similar_to_{}.csv".format(hash_process))
        data = pd.read_csv(csv, sep=";" ,encoding = 'latin1')
        data = data[~data['sentenca'].str.contains('Homologo|HOMOLOGO|homologo|homologa-se|Homologa-se|Projeto em Revisão')]
        data = data[data['similar_processo'] != data['processo']]
        process_data = data if process_data.empty else process_data.append(data)

    process_data = process_data.sort_values(by=['similaridade'],ascending=False)
    process_data = process_data.reset_index(drop=True)
    print(process_data)

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
