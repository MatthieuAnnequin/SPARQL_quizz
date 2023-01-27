#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 11:32:22 2023

@author: valentin
"""

import sys
import random

from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """

SELECT DISTINCT ?item ?itemLabel WHERE {
  ?item wdt:P106 wd:Q937857.
  ?item wdt:P569 ?date FILTER (?date > "1980-01-01T00:00:00Z"^^xsd:dateTime) .
  ?item wdt:P54 wd:Q18716 .
  ?item wdt:P54 wd:Q132885 .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}

"""

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()




def get_similar_players(good_player_id, club_id, country_id, birth_year):
    start_year = str(birth_year)
    end_year = str(birth_year+1)
    
    # similar birth date and club
    query_1 = f'''SELECT DISTINCT ?item ?itemLabel WHERE {{
      ?item wdt:P21 wd:Q6581097.
      ?item wdt:P106 wd:Q937857.
      ?item wdt:P569 ?date FILTER (?date > "{start_year}-01-01T00:00:00Z"^^xsd:dateTime) .
      ?item wdt:P569 ?date FILTER (?date < "{end_year}-01-01T00:00:00Z"^^xsd:dateTime) .
      ?item wdt:P54 wd:{club_id} .
      FILTER(?item != wd:{good_player_id}) .
      MINUS{{?item wdt:P1532 wd:{country_id}}} .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    '''

    js = get_results(endpoint_url, query_1)
    L_1 = js['results']['bindings']
    
    
    #similar club and country
    query_2 = f'''SELECT DISTINCT ?item ?itemLabel WHERE {{
      ?item wdt:P21 wd:Q6581097.
      ?item wdt:P106 wd:Q937857.
      ?item wdt:P54 wd:{club_id} .
      ?item wdt:P1532 wd:{country_id} .
      FILTER(?item != wd:{good_player_id}) .
      ?item wdt:P569 ?date FILTER (?date < "{start_year}-01-01T00:00:00Z"^^xsd:dateTime || ?date > "{end_year}-01-01T00:00:00Z"^^xsd:dateTime) .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    '''
    
    js = get_results(endpoint_url, query_2)
    L_2 = js['results']['bindings']

    
    
    # similar country and birth date
    query_3 = f'''SELECT DISTINCT ?item ?itemLabel WHERE {{
      ?item wdt:P21 wd:Q6581097.
      ?item wdt:P106 wd:Q937857.
      ?item wdt:P569 ?date FILTER (?date > "{start_year}-01-01T00:00:00Z"^^xsd:dateTime) .
      ?item wdt:P569 ?date FILTER (?date < "{end_year}-01-01T00:00:00Z"^^xsd:dateTime) .
      ?item wdt:P1532 wd:{country_id} .
      FILTER(?item != wd:{good_player_id}) .
      MINUS{{?item wdt:P54 wd:{club_id}}} .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    '''
    
    js = get_results(endpoint_url, query_3)
    L_3 = js['results']['bindings']
    
    
    try:
        J1 = random.choice(L_1)
    except:
        J1 =  {'item': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q1835'},
          'itemLabel': {'xml:lang': 'en',
           'type': 'literal',
           'value': "Zinedine Zidane"}}
    try:
        J2 = random.choice(L_2)
    except:
        J2 =  {'item': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q615'},
          'itemLabel': {'xml:lang': 'en',
           'type': 'literal',
           'value': "Lionel Messi"}}
    try:
        J3 = random.choice(L_3)
    except:
        J2 =  {'item': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q142794'},
          'itemLabel': {'xml:lang': 'en',
           'type': 'literal',
           'value': "Neymar"}}
    
    
    
    return J1,J2,J3



















