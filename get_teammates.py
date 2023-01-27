import sys
import random
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def extract_id(item):
    #extract the id of the time spent by the player at the club
    return item['item']['value'].split('/statement/')[1]

def get_clubs(player_id):
    
    query_1 = f'''SELECT ?item ?itemLabel ?p
        WHERE {{ 
            wd:{player_id} p:P54 ?item
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
        
        ORDER BY str(?p)
    '''

    results = get_results(endpoint_url, query_1)
    clubs = results['results']['bindings']
    club_ids = list(map(extract_id,clubs))
    for club_id in club_ids:
        query_2 = f'''
                SELECT ?item ?p ?pLabel WHERE {{
                    wds:{club_id} ?item ?p.
                    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
                }}
                ORDER BY ?item
            '''
        results_2 = get_results(endpoint_url, query_2)["results"]["bindings"]
        #Get the club id and the start and end date when the player was at the club
        club = results_2[0]['p']['value'].split('/entity/')[1]
        start_date, end_date = None, None
        for item in results_2:
            if 'qualifier/P580' in item['item']['value'] and 'http://' not in item['p']['value']:
                start_date = item['p']['value']
            if 'qualifier/P582' in item['item']['value'] and 'http://' not in item['p']['value']:
                end_date = item['p']['value']
    return club, start_date, end_date

def to_datetime(date):
    return datetime.strptime(date.split('T')[0], '%Y-%m-%d')

def are_teammates(start_date_1, start_date_2, end_date_1, end_date_2):
    if not start_date_1 or not start_date_2:
        return False
    d11 = to_datetime(start_date_1)
    d12 = to_datetime(start_date_2)
    d21 = None if not end_date_1 else to_datetime(end_date_1)
    d22 = None if not end_date_2 else to_datetime(end_date_2)
    return d11 != d21 and d12 != d22 and (not ((d21 and d21 <= d12) or (d22 and d22 <= d11)))

#only if start_date!=end_date
def get_teammates(player_id, club_id, player_start_date, player_end_date):
    teammates = []
    query = f'''SELECT DISTINCT ?item ?itemLabel WHERE {{
      ?item wdt:P21 wd:Q6581097.
      ?item wdt:P106 wd:Q937857.
      ?item wdt:P54 wd:{club_id} .
      ?item wdt:P569 ?date FILTER (?date > "1990-01-01T00:00:00Z"^^xsd:dateTime) .
      FILTER(?item != wd:{player_id}) .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    '''
    results = get_results(endpoint_url, query)
    players = results['results']['bindings']
    for player in players:
        club, start_date, end_date = get_clubs(player['item']['value'].split('/entity/')[1])
        if (club == club_id and are_teammates(start_date, player_start_date, end_date, player_end_date)):
            print(player)
            teammates.append(player)
    return teammates


#get_clubs('Q21621995')
import time
start_time = time.time()
get_teammates('Q180305','Q180305', '2015-01-01T00:00:00Z', '2018-01-01T00:00:00Z')
print("--- %s seconds ---" % (time.time() - start_time))



















