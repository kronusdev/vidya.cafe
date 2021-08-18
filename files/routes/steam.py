from files.mail import *
from files.__main__ import app, limiter
from files.helpers.alerts import *
from files.helpers.security import generate_hash
import hashlib
import hmac
import subprocess
import threading

site = environ.get("DOMAIN").strip()
STEAM_KEY = environ.get("STEAM_KEY").strip()

@app.get("/steam")
@auth_desired
def steam(v):
    now = int(time.time())
    state=generate_hash(f"{now}+{v.id}+discord")
    state=f"{now}.{state}"
    return redirect(f"https://steamcommunity.com/oauth/login?response_type=token&client_id={STEAM_KEY}&state={state}")

@app.get("/steam_redirect")
@auth_desired
def steam_redirect(v):
    print("LMAO")
