from django.shortcuts import render, get_object_or_404, redirect
from .forms import SearchForm
from django.views.generic.edit import FormView
from .apps import SearchConfig as sc
import pandas as pd
import numpy as np
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
    try:
        process_data = search_process_test(cod)
        
        if bool(process_data):
            serventia = process_data.get('serventia')
            comarca = process_data.get('comarca')
            df = process_data.get('data')
            process = df['processo'][int(index)]
            sentence = df['sentenca'][int(index)]
            similar = re.search(r"\d{4}\.\d{3}\.\d{6}-\d",df['similar_processo'][int(index)]).group(0)
            author = re.search(r"(autor|Autor|AUTOR|Parte Autora)(\s*:\s*)(\w.+)+",sentence).group(3) if re.search(r"(autor|Autor|AUTOR|Parte Autora)(\s*:\s*)(\w.+)+[^\n]",sentence) else ""
            similar_atual = re.search(r"\d{5,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}",sentence).group(0) if re.search(r"\d{5,7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}",sentence) else ""
            reu = re.search(r"(reu|Reu|Réu|réu|REU|RÉU|Parte RÉ|Parte Ré)(\s*:\s*)(\w.+)+",sentence).group(3) if re.search(r"(reu|Reu|Réu|réu|REU|RÉU|Parte RÉ|Parte Ré)(\s*:\s*)(\w.+)+[^\n]",sentence) else ""
            url = "http://gedweb.tjrj.jus.br/gedcacheweb/default.aspx?gedid="+df['similar_file'][int(index)]
            similaridade = df['similaridade'][int(index)]

            similar_processes = list(process_data.get('similar_processo').items())
            
            pages = df['processo'].count()-1
            
            has_previous = True if int(index) > 0 else False
            has_next = True if int(index) < pages else False
            previousIndex = int(index)-1 if int(index) > 0 else 0
            nextIndex = int(index)+1 if int(index) < pages else pages
            #return render(request, 'search/sentenca.html', {'process': process,'sentence':sentence,'similar':similar,'author':author,'reu':reu, 'pages':pages, 'previousindex':previousIndex,'nextindex':nextIndex })
            return render(request, 'search/sentenca.html', {'cod':cod, 'index':index ,'process': process,'sentence':sentence,'similar':similar,'similaridade':similaridade,'similar_atual':similar_atual,'similar_processes':similar_processes,'author':author,'reu':reu,'url':url,'serventia':serventia,'comarca':comarca,'pages':pages, 'previousindex':previousIndex,'nextindex':nextIndex,'has_previous':has_previous,'has_next':has_next  })
        
        return render(request, 'search/sentenca.html')
    except:
        error = True
        return render(request, 'search/sentenca.html',{'error':error } )



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
