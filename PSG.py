# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
import random
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

leagues = ["Q9448", "Q13394", "Q82595", "Q324867", "Q15804"]
random_league = random.choice(leagues)

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

query_team = start_query_team + filter_team.format(random_league) + end_query_team

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query_team)

clubs = list()
for result in results["results"]["bindings"]:
    clubs.append(result['item']['value'].split("/")[-1])

#print(clubs_francais)
random_club = random.choice(clubs)

start_query = '''SELECT DISTINCT ?item ?itemLabel ?team WHERE{
  ?item wdt:P106 wd:Q937857.
  ?item wdt:P569 ?date FILTER (?date > "1995-01-01T00:00:00Z"^^xsd:dateTime) .
  ?item wdt:P54 ?team.'''
filter =  '''FILTER (?team = wd:{0})
'''
end_query =  '''SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
LIMIT 30'''

query_test = start_query + filter.format(random_club) + end_query
result_joueur = get_results(endpoint_url, query_test)
print(result_joueur)

for result in result_joueur["results"]["bindings"]:
    print(result)