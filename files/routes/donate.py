from flask import request
from files.__main__ import app
import json

@app.get("/ko-fi")
@app.post("/ko-fi")
def kofi():
	print(request.form['data'])
	print(json.loads(request.form['data']))
	return "OK", 200
