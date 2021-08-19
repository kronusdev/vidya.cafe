from flask import request
from files.__main__ import app


@app.post("/ko-fi")
def kofi():
	print(request.headers)
	print(request.json)
	print(request.data)
	print(request.form)
	return "OK", 200
