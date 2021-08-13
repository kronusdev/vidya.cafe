from files.__main__ import app
from flask import *

@app.post("/gumroad_ping")
def gumroad():

	data = request.json

	print(data)
	print(request.data)

	return "OK", 200