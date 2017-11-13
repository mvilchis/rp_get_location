#! /usr/bin/env python
# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import os
import json


############### Constants Elasticsearch configuration ####################
INDEX_SETTINGS = { "settings":{
                        "analysis": {
                            "filter": {
                                "dbl_metaphone"  : {  "type":"phonetic","encoder": "double_metaphone","languageset":"spanish"}
                            },
                            "analyzer": {
                                "dbl_metaphone": { "tokenizer": "standard", "filter":    "dbl_metaphone"}
                            }
                        }
                    }
                }


############### Constants to index data #######################
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

with open('data/municipios.json') as data_file:
     MUNICIPIOS = json.load(data_file)


################# Index data ######################
def main():
    elastic_port = int(os.getenv('ELASTIC_PORT',9200))
    elastic_ip = os.getenv('ELASTIC_IP','localhost')
    elasticsearch_url = "{ip}:{port}"
    es = Elasticsearch([elasticsearch_url.format(ip=elastic_ip, port=elastic_port)])
    #Clean last index, and create the same index
    es.indices.delete(index='estados', ignore=[400, 404])
    es.indices.create(index = 'estados', body = INDEX_SETTINGS)

    es.indices.delete(index='municipios', ignore=[400, 404])
    es.indices.create(index = 'municipios', body = INDEX_SETTINGS)

    for key in ESTADOS.keys():
        value = ESTADOS[key]
        es.index(index = 'estados', doc_type = 'estado', body = {'nombre':value["nombre"], 'clave': value["clave"]})
    for key in ESTADOS_ABBREVIATION.keys():
        value = ESTADOS_ABBREVIATION[key]
        es.index(index = 'estados', doc_type = 'estado', body = {'nombre':value["nombre"], 'clave': value["clave"]})
    for key in MUNICIPIOS.keys():
        for value in MUNICIPIOS[key]:
            es.index(index = 'municipios', doc_type = key, body = {'nombre':value})

main()
