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

		user=args[0]
		if not user.discord_id:
			return


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

def send_message(message):
	url=f"https://discordapp.com/api/channels/850266802449678366/messages"
	headers = {"Authorization": f"Bot {BOT_TOKEN}"}
	data={"content": message}
	requests.post(url, headers=headers, data=data)