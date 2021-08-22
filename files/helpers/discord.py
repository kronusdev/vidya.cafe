from os import environ
import requests
import threading

SERVER_ID = environ.get("DISCORD_SERVER_ID",'').strip()
CLIENT_ID = environ.get("DISCORD_CLIENT_ID",'').strip()
CLIENT_SECRET = environ.get("DISCORD_CLIENT_SECRET",'').strip()
BOT_TOKEN = environ.get("DISCORD_BOT_TOKEN",'').strip()
AUTH = environ.get("DISCORD_AUTH",'').strip()

ROLES={
	"linked":  "849621030926286920",
	"admin": "846509661288267776",
	"feedback": "850716291714383883",
	"newuser": "854783259229421589",
	"norep": "850971811918512208",
	}

def discord_wrap(f):

	def wrapper(*args, **kwargs):

		thread=threading.Thread(target=f, args=args, kwargs=kwargs)
		thread.start()

	wrapper.__name__=f.__name__
	return wrapper



@discord_wrap
def add_role(user, role_name):
	role_id = ROLES[role_name]
	url = f"https://discordapp.com/api/guilds/{SERVER_ID}/members/{user.discord_id}/roles/{role_id}"
	headers = {"Authorization": f"Bot {BOT_TOKEN}"}
	requests.put(url, headers=headers)

@discord_wrap
def delete_role(user, role_name):
	role_id = ROLES[role_name]
	url = f"https://discordapp.com/api/guilds/{SERVER_ID}/members/{user.discord_id}/roles/{role_id}"
	headers = {"Authorization": f"Bot {BOT_TOKEN}"}
	requests.delete(url, headers=headers)

@discord_wrap
def remove_user(user):
	url=f"https://discordapp.com/api/guilds/{SERVER_ID}/members/{user.discord_id}"
	headers = {"Authorization": f"Bot {BOT_TOKEN}"}
	requests.delete(url, headers=headers)

@discord_wrap
def set_nick(user, nick):
	url=f"https://discordapp.com/api/guilds/{SERVER_ID}/members/{user.discord_id}"
	headers = {"Authorization": f"Bot {BOT_TOKEN}"}
	data={"nick": nick}
	requests.patch(url, headers=headers, json=data)



# discord_wrap breaks this lol
def get_discord_info():
	url=f"https://discordapp.com/api/users/291956736787742721"
	
	headers = {'Authorization': f"Bot ODMyMjIzMzg3NzMyMTQ4MjQ0.YHgqbQ.Y0IpiyJ7CjdVm_ehQ5WuPoAWMnQ"}
	discord_user = requests.get(url, headers=headers).json()
	avatar_hash = discord_user['avatar']
	avatar_url=f"https://cdn.discordapp.com/avatars/291956736787742721/{avatar_hash}.png"
	try: 
		banner_hash = discord_user['banner']
		banner_url=f"https://cdn.discordapp.com/banners/291956736787742721/{banner_hash}.png"
	except:
		banner_url = ""
	username = discord_user['username']
	digits = discord_user['discriminator']

	return {'username': username, 'digits': digits, 'avatar_url': avatar_url, 'banner_url': banner_url}

def send_message(message):
	url=f"https://discordapp.com/api/channels/850266802449678366/messages"
	headers = {"Authorization": f"Bot {BOT_TOKEN}"}
	data={"content": message}
	requests.post(url, headers=headers, data=data)