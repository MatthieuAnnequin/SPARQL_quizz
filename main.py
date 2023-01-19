from select_random_player import get_player_id
from request_similar import get_similar_players

import random


# player_id, player_name, player_birth, player_country, player_country_id, club_id, club_name = get_player_id()
# birth_year = int(player_birth.split('-')[0])
# print("Which player born in " + str(birth_year) + ", played for " + club_name + " and for " + player_country + "?")
# possibilities = get_similar_players(player_id, club_id, player_country_id, birth_year)
# player_1 = possibilities[0]['itemLabel']['value']
# player_2 = possibilities[1]['itemLabel']['value']
# player_3 = possibilities[2]['itemLabel']['value']

# print(player_1, player_2, player_3, player_name)


def get_question():
    player_id, player_name, player_birth, player_country, player_country_id, club_id, club_name = get_player_id()
    birth_year = int(player_birth.split('-')[0])
    question = "Which player born in " + str(birth_year) + ", played for " + club_name + " and for " + player_country + "?"
    possibilities = get_similar_players(player_id, club_id, player_country_id, birth_year)
    player_1 = possibilities[0]['itemLabel']['value']
    player_2 = possibilities[1]['itemLabel']['value']
    player_3 = possibilities[2]['itemLabel']['value']
    
    L = [x['itemLabel']['value'] for x in possibilities]
    L.append(player_name)
    
    random.shuffle(L)
    
    dic_out = {
           'question': question,
            'optionA': L[0],
            'optionB': L[1],
            'optionC': L[2],
            'optionD': L[3],
            'correctOption': "optionD"
        }
    
    for k in list(dic_out):
        if dic_out[k]==player_name:
            dic_out['correctOption']=k
    
    return dic_out