from flask import request
from files.__main__ import app

@app.get("/ko-fi")
@app.post("/ko-fi")
def kofi():
	print(request.form['data'])
	return "OK", 200
