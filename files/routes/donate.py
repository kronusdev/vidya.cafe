from os import environ
from files.__main__ import *
import json
from files.classes.donation import Donation
from files.helpers.security import *
from files.helpers.wrappers import *


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
	donor_badge = g.db.query(BadgeDef).filter_by(icon="donator.png").first()
	granted_badge = Badge(
		badge_id = donor_badge.id,
		user_id = g.db.query(User).filter_by(kofi_email=data['email']).id,
		description = f"Donated {amount}{currency} - Thanks a lot!"
	)
	g.db.add(donation)
	g.db.commit()

	return "OK", 200

@app.get("/verify_ko-fi")
@auth_desired
def verify_kofi(v):

	email = request.args.get("email", "")
	id = request.args.get("id", "")
	timestamp = int(request.args.get("time", "0"))
	token = request.args.get("token", "")

	if int(time.time()) - timestamp > 3600:
		return render_template("message.html", v=v, title="Verification link expired.",
							   message="That link has expired. Visit your settings to send yourself another verification email."), 410

	#if not validate_hash(f"{email}+{id}+{timestamp}", token):
	#	abort(403)

	user = g.db.query(User).filter_by(id=id).first()
	if not user:
		abort(404)

	if user.kofi_verified and user.kofi_email == email:
		return render_template("message_success.html", v=v,
							   title="Email already verified.", message="Email already verified."), 404

	user.kofi_email = email
	user.kofi_verified = True

	g.db.add(user)

	return render_template("message_success.html", v=v, title="Ko-fi Email verified.", message=f"Your ko-fi email {email} has been verified. Thank you.")