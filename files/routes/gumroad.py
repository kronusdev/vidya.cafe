from files.__main__ import app
from flask import *

@app.post("/gumroad")
def gumroad():

	data = request.json

	print(data)

	return "OK", 200