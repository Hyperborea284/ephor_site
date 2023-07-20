from summarizer import Summarizer
from spacy import displacy
import spacy
from polyglot.detect import Detector
import subprocess
import os
import re
import pandas as pd
import string
import nltk
from nltk import *
from nltk.tokenize import word_tokenize
from tabulate import tabulate
from operator import itemgetter
from langdetect import detect


@staticmethod
def entities(texto):
    lang_code = detect(texto)
    if lang_code == 'en':
        lang_code_short = 'english'
        lang_code_full = 'en_core_web_sm'

    elif lang_code == 'pt':
        lang_code_short = 'portuguese'
        lang_code_full = 'pt_core_news_sm'
    else:
        pass

    ent_list = []
    pln = spacy.load(lang_code_full)
    documento = pln(texto)
    for entidade in documento.ents:
        ent_list.append([entidade.text, entidade.label_])

    return ent_list, lang_code, lang_code_short, lang_code_full

@staticmethod
def idiom(form, name):
    with open(f"{name}.txt", "w") as text_file:
        text_file.write(f"{form.cleaned_data['content']}\n\n")
        text_file.close()
        ent_list, lang_code, lang_code_short, lang_code_full = entities(form.cleaned_data['content'])
        barplot_size = form.cleaned_data["barplot_size"]
    os.remove(f"{name}.txt")

@staticmethod
def bert_sumarizar(form):
    sumarizador = Summarizer()
    resumo = sumarizador(form.cleaned_data['content'])
    return resumo

@staticmethod
def cleaner(text, lang_code_short):
    text_0 = word_tokenize(text)
    stopwords = set(nltk.corpus.stopwords.words(lang_code_short))
    string_better = string.punctuation + '`' + '”' + "'" + " '" + "''" + "``" + ")." + ".)." + ".:" + ".)" \
                                       + "]:" + "[:" + ":]" + ":[" + '©' + "'–" + '//' + '/' + "'-" + "!" \
                                       + "?" + ".," + "." + "," + "“"

    filtered_word_0 = [word.lower() for word in text_0 if (word.lower() not in stopwords) and (word.lower() not in string_better)]
    filtered_word_1 = [re.sub('[0-9]', '', i) for i in filtered_word_0]

    for i in filtered_word_1:
        if(len(i) >= 2):
            continue
        elif(len(i) == 0):
            filtered_word_1.remove(i)
        else:
            filtered_word_1.remove(i)

    output_bi = list(nltk.bigrams(filtered_word_1))
    output_tri = list(nltk.trigrams(filtered_word_1))

    return output_tri, output_bi, filtered_word_1

@staticmethod
def proto(filtered_word_1):
    # constrói dicionário beta contendo o termo e a frequencia
    beta = {}
    for i in filtered_word_1:
        if i not in beta:
            beta[i] = (1)
        else:
            beta[i] += (1)
    
    # constrói dicionário charlie contendo o termo e a ordenação
    charlie = {}
    for i in filtered_word_1:
        charlie[i] = [o for o, x in enumerate(filtered_word_1) if x == i]
    
    delta = sorted(beta.items(), key=lambda item: item[1], reverse=True)
    echo = sorted(charlie.items(), key=lambda item: item[1], reverse=True)
    
    alt_freq_bai_ord = (pd.concat([pd.Series(dict(delta)),pd.Series(dict(echo))],axis=1).reset_index().values.tolist())

    for i in range(len(alt_freq_bai_ord)):
        ome = sum(alt_freq_bai_ord[i][2])/(len(alt_freq_bai_ord[i][2]))
        alt_freq_bai_ord[i].insert(3, ome)

    bai_freq_alt_ord = sorted(sorted(alt_freq_bai_ord, key=lambda x: x[2][0], reverse=True), key = lambda x: x[1])
    alt_freq_alt_ord = sorted(sorted(alt_freq_bai_ord, key=lambda x: x[2][0], reverse=True), key = lambda x: x[1], reverse=True)
    bai_freq_bai_ord = sorted(sorted(alt_freq_bai_ord, key=lambda x: x[2][0]), key = lambda x: x[1])

    return alt_freq_bai_ord, bai_freq_alt_ord, alt_freq_alt_ord, bai_freq_bai_ord
