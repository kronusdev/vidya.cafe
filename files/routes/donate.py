from os import environ
from files.classes.donation import Donation
from flask import request
from files.__main__ import app
import json

@app.get("/ko-fi")
@app.post("/ko-fi")
def kofi():

	if request.args.get('token') != environ.get("KOFI_WEBHOOK_TOKEN"): return "OK", 200

	data_json = request.form['data']
	data = json.loads(data_json)

	donation = Donation(
		amount = int(float(data['amount'])),
		currency = data['currency'],
		purchase_id = data['kofi_transaction_id'],
		purchase_email = data['email'],
		data = data_json,
		payment_company = "kofi"
	)

	g.db.add(donation)
	g.db.commit()


	return "OK", 200
