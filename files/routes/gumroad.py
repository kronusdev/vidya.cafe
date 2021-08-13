from flask import *
from files.__main__ import app


@app.post("/gumroad")
def gumroad():

	data = request.json

	print(data)
	print(request.data)

	return "OK", 200