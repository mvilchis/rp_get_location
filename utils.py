#! /usr/bin/env python
# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import os
import re
import time
from nltk.corpus import stopwords

###############     Constants date     ########################
NUMBERS = {'primero':1, 'segundo':2, 'tercero':3, 'cuarto':4,
           'uno':1, 'dos':2, 'tres':3, 'cuatro':4, 'cinco':5,
           'seis':6, 'siete':7, 'ocho':8, 'nueve':9, 'diez':10,
           'once':11, 'doce':12, 'trece':13, 'catorce':14, 'quince':15,
           'dieciseis':16, 'diecisiete':17, 'dieciocho':18,
           'diecinueve':19,'veinte':20, 'ventiuno':21, 'veintidos':22,
           'veintitres':23, 'veinticuatro':24, 'veinticinco':25,
           'veintiseis':26, 'veintisiete':27, 'veintiocho':28,
           'veintinueve':29, 'treinta':30, 'treinta y uno':31}

MONTHS = {'ene':1, 'enero':1,
         'feb': 2, 'febrero':2,
         'mar': 3, 'marzo':3,
         'abr': 4, 'abril':4,
         'may': 5, 'mayo':5,
         'jun': 6, 'junio':6,
         'jul': 7, 'julio':7,
         'agto': 8, 'agosto':8,
         'sep': 9, 'septiembre':9,
         'oct': 10, 'octubre':10,
         'nov': 11, 'noviembre':11,
         'dic': 12, 'diciembre':12  }

############### Constants elasticsearch #######################
REQUEST_STRING= "es.search(index= 'fechas', body = {'query' : {'fuzzy': {'name': {'value':'%s', 'fuzziness':5}}}})"
DAY=0
MONTH=1
YEAR = 2
HITS_KEY = 'hits'
SOURCE_KEY = '_source'
ERROR='error'


elastic_port = int(os.getenv('ELASTIC_PORT',9200))
elastic_ip = os.getenv('ELASTIC_IP','127.0.0.1')
elasticsearch_url = "{ip}:{port}"
es = Elasticsearch([elasticsearch_url.format(ip=elastic_ip, port=elastic_port)])



#Method that intent search the pattern used, first will search locally,
# if not find a pattern then ask to elasticsearch server
def search_item(item):
    global es
    has_prefix = [MONTHS[key] for key in MONTHS if item.startswith(key)]
    if not item.isdigit():
        if item in NUMBERS.keys():
            final_item = NUMBERS[item]
        elif item in MONTHS.keys():
            final_item = MONTHS[item]
        elif len(has_prefix) == 1:
            final_item = has_prefix[0]
        else:
            ##Check the hit
            result = es.search(index= 'fechas',
            body ={'query' : {'match':  {'name': {'query':str(item),'fuzziness':'AUTO' }}}})
            print (result)
            hits = result[HITS_KEY][HITS_KEY]
            if hits:
                final_item = hits[0][SOURCE_KEY]['number']
            else:
                final_item = ERROR
    else: # Is digit, asume the numer is correct
        return item
    return final_item


def parse_list(date_list):
    if len(date_list) == 2:
        year = int(time.strftime("%Y"))
    else:
        year = int(search_item(date_list[YEAR]))

    ## we assume (3 feb 2016) or (3 02 16) or (tres febrero dosmildieciseis)
    day = search_item(date_list[DAY])
    month = search_item(date_list[MONTH])
    if day != ERROR and month != ERROR and year != ERROR:
        if year <= 100: ##User give us two digits
            if year <= 50:
               year += 2000
            else:
               year += 1900
        return str(day) + "/"+str(month) +"/"+ str(year)
    print ("%s %s %s" %(day, month, year))
    return ERROR


def parse_date(date):
    date_str = str(date).lower()
    #remove punctuation and split into seperate words
    date_words = re.findall(r'\w+', date_str,flags = re.UNICODE | re.LOCALE)
    clean_date = list(filter(lambda x: x not in stopwords.words('spanish'),date_words))
    if (len(clean_date) == 3 or len(clean_date) == 2):
        final_date = parse_list(clean_date)
        if final_date != ERROR:
            return final_date

    #Maybe rapidpro can parse date
    return date
