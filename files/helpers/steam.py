from files.__main__ import cache, environ, requests
from flask import *

STEAM_KEY = environ.get('STEAM_KEY','').strip()

def get_steam_games(u):
	steam_id = u.steam_id
	steam_api_owned_games = requests.get(f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_KEY}&steamid={steam_id}&format=json").json()['response']
	owned_games = [""]
	for game in range(steam_api_owned_games['game_count']):
		owned_games.append(appid_to_details(steam_api_owned_games['games'][game]['appid']))
	return owned_games

@cache.memoize(timeout=300)
def get_steam_info(u):
	steam_id = u.steam_id
	steam_api_response = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_KEY}&steamids={steam_id}").json()['response']['players'][0]
	player_level = requests.get(f"https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key={STEAM_KEY}&steamid={steam_id}").json()['response']['player_level']

	try:
		current_game = steam_api_response['gameextrainfo']
	except:
		current_game = ""
	try:
		current_game_bg = appid_to_details(steam_api_response['gameid'])['background']
	except:
		current_game_bg = "https://community.cloudflare.steamstatic.com/public/images//skin_1/forum_op_gradient.png?v=3"
	try:
		current_game_image = appid_to_details(steam_api_response['gameid'])['image']
	except:
		current_game_image = ""
	persona_state = steam_api_response['personastate']
	try:
		last_log_off = steam_api_response['lastlogoff']
	except:
		last_log_off = 0
	avatar = steam_api_response['avatar']
	persona_name = steam_api_response['personaname']
	profile_url = steam_api_response['profileurl']
	time_created = steam_api_response['timecreated']

	return {'current_game': current_game, 'last_log_off': last_log_off, 'persona_state': persona_state, 'avatar':avatar, 'persona_name':persona_name, 'profile_url':profile_url, 'time_created':time_created, 'player_level': player_level, 'current_game_bg': current_game_bg, 'current_game_image': current_game_image}

def appid_to_details(app_id):
	app_details = requests.get(f"https://store.steampowered.com/api/appdetails/?appids={app_id}").json()
	try:
		name = app_details[f'{app_id}']['data']['name'],
		image = app_details[f'{app_id}']['data']['header_image'].replace("\\", ""),
		background = app_details[f'{app_id}']['data']['background'].replace("\\", "")
	except:
		name = "Game Not Found"
		image = f"App_id={app_id}"
		background = ""
			
	return {'name': name, 'image': image, 'background': background}

