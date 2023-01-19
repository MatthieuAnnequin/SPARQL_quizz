# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
import random
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

def create_team_query(league):
  start_query_team = """SELECT DISTINCT ?item ?itemLabel WHERE {
    ?item wdt:P31 wd:Q476028.
    ?item wdt:P118 ?league
    """
  filter_team =  """FILTER (?league = wd:{0})
  """
  end_query_team = """
    BIND(RAND() AS ?random)
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  }
  ORDER BY ?random
  LIMIT 25"""
  query_team = start_query_team + filter_team.format(league) + end_query_team
  return query_team

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def create_player_query(club):
  start_query = '''SELECT DISTINCT ?item ?itemLabel ?team ?pays_de_nationalité_sportive ?pays_de_nationalité_sportiveLabel ?date_de_naissance ?pays_de_citoyenneté ?pays_de_citoyennetéLabel WHERE{
    ?item wdt:P106 wd:Q937857.
    ?item wdt:P569 ?date FILTER (?date > "1995-01-01T00:00:00Z"^^xsd:dateTime) .
    ?item wdt:P54 ?team.'''
  filter =  '''FILTER (?team = wd:{0})
  '''
  end_query =  '''SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  OPTIONAL { ?item wdt:P1532 ?pays_de_nationalité_sportive. }
  OPTIONAL { ?item wdt:P569 ?date_de_naissance. }
  OPTIONAL { ?item wdt:P27 ?pays_de_citoyenneté. }
  }
  LIMIT 30'''
  query_player = start_query + filter.format(club) + end_query
  return query_player

def list_q(result_query):
  list_q = list()
  for result in result_query["results"]["bindings"]:
      list_q.append((result['itemLabel']['value'], result['item']['value'].split("/")[-1]))
  return list_q

def get_player_id():
  leagues = ["Q9448", "Q13394", "Q82595", "Q324867", "Q15804"]
  random_league = random.choice(leagues)
  query_team = create_team_query(random_league)
  result_team_query = get_results(endpoint_url, query_team)

  clubs_id = list_q(result_team_query)

  random_club = random.choice(clubs_id)
  random_club_name = random_club[0]
  random_club_id = random_club[1]
  query_player = create_player_query(random_club_id)
  result_query_player = get_results(endpoint_url, query_player)
  
  list_players = list()
  for result in result_query_player["results"]["bindings"]:
       list_players.append(result)
  
  random_player = random.choice(list_players)
  random_player_id = random_player['item']['value'].split("/")[-1]
  random_player_name = random_player['itemLabel']['value']
  random_player_birth = random_player['date_de_naissance']['value']
  try:
    random_player_country = random_player['pays_de_nationalité_sportiveLabel']['value']
    random_player_country_id = random_player['pays_de_nationalité_sportive']['value'].split("/")[-1]
  except:
    random_player_country = random_player['pays_de_citoyennetéLabel']['value']
    random_player_country_id = random_player['pays_de_citoyenneté']['value'].split("/")[-1]
  return random_player_id, random_player_name, random_player_birth, random_player_country, random_player_country_id, random_club_id, random_club_name









