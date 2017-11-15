#! /usr/bin/env python
# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import os
import re
import time
import unidecode
import json, requests,codecs

###############     Constants date     ########################
ESTADOS= {"1":{"nombre":"Aguascalientes", "clave":"01"}
         ,"2":{"nombre":"Baja California", "clave":"02"}
         ,"3":{"nombre":"Baja California Sur", "clave":"03"}
         ,"4":{"nombre":"Campeche", "clave":"04"}
         ,"5":{"nombre":"Coahuila", "clave":"05"}
         ,"6":{"nombre":"Colima", "clave":"06"}
         ,"7":{"nombre":"Chiapas", "clave":"07"}
         ,"8":{"nombre":"Chihuahua", "clave":"08"}
         ,"9":{"nombre":"Ciudad de México", "clave":"09"}
         ,"10":{"nombre":"Durango", "clave":"10"}
         ,"11":{"nombre":"Guanajuato", "clave":"11"}
         ,"12":{"nombre":"Guerrero", "clave":"12"}
         ,"13":{"nombre":"Hidalgo", "clave":"13"}
         ,"14":{"nombre":"Jalisco", "clave":"14"}
         ,"15":{"nombre":"México", "clave":"15"}
         ,"16":{"nombre":"Michoacán", "clave":"16"}
         ,"17":{"nombre":"Morelos", "clave":"17"}
         ,"18":{"nombre":"Nayarit", "clave":"18"}
         ,"19":{"nombre":"Nuevo León", "clave":"19"}
         ,"20":{"nombre":"Oaxaca", "clave":"20"}
         ,"21":{"nombre":"Puebla", "clave":"21"}
         ,"22":{"nombre":"Querétaro", "clave":"22"}
         ,"23":{"nombre":"Quintana Roo", "clave":"23"}
         ,"24":{"nombre":"San Luis Potosí", "clave":"24"}
         ,"25":{"nombre":"Sinaloa", "clave":"25"}
         ,"26":{"nombre":"Sonora", "clave":"26"}
         ,"27":{"nombre":"Tabasco", "clave":"27"}
         ,"28":{"nombre":"Tamaulipas", "clave":"28"}
         ,"29":{"nombre":"Tlaxcala", "clave":"29"}
         ,"30":{"nombre":"Veracruz", "clave":"30"}
         ,"31":{"nombre":"Yucatán", "clave":"31"}
         ,"32":{"nombre":"Zacatecas", "clave":"32"}
         ,"9_1": {"nombre":"Distrito Federal", "clave": "09"}
         ,"15_1":{"nombre":"Estado de México", "clave": "15"}}

ESTADOS_ABBREVIATION = {
           "1":{"nombre":"Ags", "clave":"01"}
          ,"2":{"nombre":"BC", "clave":"02"}
          ,"3":{"nombre":"BCS", "clave":"03"}
          ,"4":{"nombre":"Camp", "clave":"04"}
          ,"5":{"nombre":"Coah", "clave":"05"}
          ,"6":{"nombre":"Col", "clave":"06"}
          ,"7":{"nombre":"Chis", "clave":"07"}
          ,"8":{"nombre":"Chih", "clave":"08"}
          ,"9":{"nombre":"CDMX", "clave":"09"}
          ,"10":{"nombre":"Dgo", "clave":"10"}
          ,"11":{"nombre":"Gto", "clave":"11"}
          ,"12":{"nombre":"Gro", "clave":"12"}
          ,"13":{"nombre":"Hgo", "clave":"13"}
          ,"14":{"nombre":"Jal", "clave":"14"}
          ,"15":{"nombre":"Méx", "clave":"15"}
          ,"16":{"nombre":"Mich", "clave":"16"}
          ,"17":{"nombre":"Mor", "clave":"17"}
          ,"18":{"nombre":"Nay", "clave":"18"}
          ,"19":{"nombre":"NL", "clave":"19"}
          ,"20":{"nombre":"Oax", "clave":"20"}
          ,"21":{"nombre":"Pue", "clave":"21"}
          ,"22":{"nombre":"Qro", "clave":"22"}
          ,"23":{"nombre":"QRoo", "clave":"23"}
          ,"24":{"nombre":"SLP", "clave":"24"}
          ,"25":{"nombre":"Sin", "clave":"25"}
          ,"26":{"nombre":"Son", "clave":"26"}
          ,"27":{"nombre":"Tab", "clave":"27"}
          ,"28":{"nombre":"Tamps", "clave":"28"}
          ,"29":{"nombre":"Tlax", "clave":"29"}
          ,"30":{"nombre":"Ver", "clave":"30"}
          ,"31":{"nombre":"Yuc", "clave":"31"}
          ,"32":{"nombre":"Zac", "clave":"32"}
          ,"9_1": {"nombre":"DF", "clave": "09"}
          ,"15_1":{"nombre":"Edomex", "clave": "15"}
          ,"23_1":{"nombre":"QR", "clave": "23"}}

MUNICIPIOS = json.load(codecs.open('data/municipios.json', 'r', 'utf-8-sig'))
COLONIAS = json.load(codecs.open('data/colonias.json', 'r', 'utf-8-sig'))

############### Constants elasticsearch #######################
HITS_KEY = 'hits'
SOURCE_KEY = '_source'
ERROR='error'


elastic_port = int(os.getenv('ELASTIC_PORT',9200))
elastic_ip = os.getenv('ELASTIC_IP','127.0.0.1')
elasticsearch_url = "{ip}:{port}"
es = Elasticsearch([elasticsearch_url.format(ip=elastic_ip, port=elastic_port)])

#Method that intent search the pattern used, first will search locally,
# if not find a pattern then ask to elasticsearch server
def parse_col(mun, item):
    item = item.lower()
    mun = str(mun)

    has_prefix = [value["col_name"] for value in COLONIAS if value["mun"] == mun and value["col_name"].lower().startswith(item)]
    is_correct = [value["col_name"] for value in COLONIAS if value["mun"] == mun and item == value["col_name"].lower()
                                                   or item == unidecode.unidecode(value["col_name"].lower())]
    if  len(is_correct) == 1:
        return is_correct[0]
    elif len(has_prefix) == 1:
        return has_prefix[0]
    else:
        ##Check the hit
        result = es.search(index= 'colonias',doc_type=mun,
                            body ={'query' : {'match':  {'nombre': {'query':str(item),'fuzziness':'AUTO',  }}}})
        hits = result[HITS_KEY][HITS_KEY]
        if hits:
            return hits[0][SOURCE_KEY]["nombre"]

    return item


#Method that intent search the pattern used, first will search locally,
# if not find a pattern then ask to elasticsearch server
def parse_mun(edo_cve, mun):
    item = mun.lower()
    edo_cve = str(int(edo_cve))

    has_prefix = [value for value in MUNICIPIOS[edo_cve] if value.lower().startswith(item)]
    is_correct = [value for value in MUNICIPIOS[edo_cve] if item == value.lower()
                                                 or item == unidecode.unidecode(value.lower())]
    if  len(is_correct) == 1:
        estado_item = is_correct[0]
        return estado_item
    elif len(has_prefix) == 1:
        estado_item = has_prefix[0]
        return estado_item
    else:
        ##Check the hit
        result = es.search(index= 'municipios',doc_type=edo_cve,
                            body ={'query' : {'match':  {'nombre': {'query':str(item),'fuzziness':'AUTO',  }}}})
        hits = result[HITS_KEY][HITS_KEY]
        if hits:
           return hits[0][SOURCE_KEY]["nombre"]
    return item



#Method that intent search the pattern used, first will search locally,
# if not find a pattern then ask to elasticsearch server
def parse_edo(item):
    item = item.lower()
    #Abbreviation
    has_prefix_ab = [ESTADOS_ABBREVIATION[key] for key in ESTADOS_ABBREVIATION.keys()
                             if ESTADOS_ABBREVIATION[key]["nombre"].lower().startswith(item)]
    is_correct_ab = [ESTADOS_ABBREVIATION[key] for key in ESTADOS_ABBREVIATION.keys()
                             if item == ESTADOS_ABBREVIATION[key]["nombre"].lower()
                             or item == unidecode.unidecode(ESTADOS_ABBREVIATION[key]["nombre"].lower())]
    has_prefix = [ESTADOS[key] for key in ESTADOS.keys() if ESTADOS[key]["nombre"].lower().startswith(item)]
    is_correct = [ESTADOS[key] for key in ESTADOS.keys() if item == ESTADOS[key]["nombre"].lower()
                                                 or item == unidecode.unidecode(ESTADOS[key]["nombre"].lower())]
    if  len(is_correct) == 1:
        estado_item = is_correct[0]
        return estado_item["nombre"], estado_item["clave"]
    elif len(has_prefix) == 1:
        estado_item = has_prefix[0]
        return estado_item["nombre"], estado_item["clave"]
    if  len(is_correct_ab) == 1:
        estado_item = is_correct_ab[0]
        return estado_item["nombre"], estado_item["clave"]
    elif len(has_prefix_ab) == 1:
        estado_item = has_prefix_ab[0]
        return estado_item["nombre"], estado_item["clave"]
    else:
        ##Check the hit
        result = es.search(index= 'estados',
                           body ={'query' : {'match':  {'nombre': {'query':str(item),'fuzziness':'AUTO' }}}})
        hits = result[HITS_KEY][HITS_KEY]
        if hits:
           return hits[0][SOURCE_KEY]["nombre"],hits[0][SOURCE_KEY]["clave"]

    return item,0


##########################################
#         Normalize state name           #
##########################################
def correct_edo(nombre):
    nombre_str = str(nombre).lower()
    return parse_edo(nombre_str)


##########################################
#          Normalize mun name            #
##########################################
def correct_mun(edo, nombre):
    nombre_str = str(nombre).lower()
    return parse_mun(edo.lower(),nombre_str)

##########################################
#          Normalize col name            #
##########################################
def correct_col(mun, nombre):
    nombre_str = str(nombre).lower()
    return parse_col(mun.lower(),nombre_str)

##########################################
#       Search corner base on municipio  #
##########################################
def get_location_with_corner_municipio(municipio,street_a, street_b):
     standard_street_a = street_a.replace(" ", "+")
     standard_street_b = street_b.replace(" ", "+")
     mun = municipio.replace(" ", "+")
     base_url  = "https://maps.googleapis.com/maps/api/geocode/json?address="
     address = (mun +',+' + standard_street_a  + '+%26+' + standard_street_b)
     full_url = base_url + address
     r = requests.get(full_url)
     result_dic = r.json()
     if 'results' in result_dic:
         if result_dic['results']:
             if 'geometry' in result_dic['results'][0]:
                 return result_dic['results'][0]['geometry']['location']
     return {"lat": None, "lng": None}
