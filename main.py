from select_random_player import get_player_id
from request_similar import get_similar_players

player_id, player_name, player_birth, player_country, player_country_id, club_id, club_name = get_player_id()
birth_year = int(player_birth.split('-')[0])
print("Which player born in " + str(birth_year) + ", played for " + club_name + " and for " + player_country + "?")
possibilities = get_similar_players(player_id, club_id, player_country_id, birth_year)
player_1 = possibilities[0]['itemLabel']['value']
player_2 = possibilities[1]['itemLabel']['value']
player_3 = possibilities[2]['itemLabel']['value']

print(player_1, player_2, player_3, player_name)
