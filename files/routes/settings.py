from __future__ import unicode_literals
from files.helpers.alerts import *
from files.helpers.sanitize import *
from files.helpers.filters import filter_comment_html
from files.helpers.markdown import *
from files.helpers.discord import remove_user, set_nick
from files.mail import *
from files.__main__ import app, cache
import youtube_dl
from .front import frontlist
import time
import re

valid_username_regex = re.compile("^[a-zA-Z0-9_\-]{3,25}$")
valid_title_regex = re.compile("^((?!<).){3,100}$")
valid_password_regex = re.compile("^.{8,100}$")

YOUTUBE_KEY = environ.get("YOUTUBE_KEY").strip()
COINS_NAME = environ.get("COINS_NAME").strip()
STEAM_KEY = environ.get("STEAM_KEY",'').strip()

@app.post("/settings/profile")
@auth_required
@validate_formkey
def settings_profile_post(v):
	updated = False

	if request.values.get("background", v.background) != v.background:
		updated = True
		v.background= request.values.get("background", None)

	if request.values.get("slurreplacer", v.slurreplacer) != v.slurreplacer:
		updated = True
		v.slurreplacer = request.values.get("slurreplacer", None) == 'true'

	if request.values.get("hidevotedon", v.hidevotedon) != v.hidevotedon:
		updated = True
		v.hidevotedon = request.values.get("hidevotedon", None) == 'true'

	if request.values.get("newtab", v.newtab) != v.newtab:
		updated = True
		v.newtab = request.values.get("newtab", None) == 'true'

	if request.values.get("newtabexternal", v.newtabexternal) != v.newtabexternal:
		updated = True
		v.newtabexternal = request.values.get("newtabexternal", None) == 'true'

	if request.values.get("oldreddit", v.oldreddit) != v.oldreddit:
		updated = True
		v.oldreddit = request.values.get("oldreddit", None) == 'true'

	if request.values.get("over18", v.over_18) != v.over_18:
		updated = True
		v.over_18 = request.values.get("over18", None) == 'true'

	if request.values.get("private", v.is_private) != v.is_private:
		updated = True
		v.is_private = request.values.get("private", None) == 'true'
		v.show_activity = False
	
	if request.values.get("activity", v.show_activity) != v.show_activity:
		updated = True
		v.show_activity = request.values.get("activity", None) == 'true'

	if request.values.get("animatedname", v.animatedname) != v.animatedname:
		if v.animatedname == False:
			users = g.db.query(User.id).options(lazyload('*')).order_by(User.coins.desc()).limit(25).all()
			users = [x[0] for x in users]
			if v.id not in users: return {"error": "You must be in the top 25 leaderboard or be a patron to apply an animated name!"}, 403
		updated = True
		v.animatedname = request.values.get("animatedname", None) == 'true'

	if request.values.get("nofollow", v.is_nofollow) != v.is_nofollow:
		updated = True
		v.is_nofollow = request.values.get("nofollow", None) == 'true'

	if request.values.get("bio"):
		bio = request.values.get("bio")[:1500]

		if bio == v.bio:
			return render_template("settings_profile.html",
								   v=v,
								   error="You didn't change anything")

		for i in re.finditer('^(https:\/\/.*\.(png|jpg|jpeg|gif|PNG|JPG|JPEG|GIF))', bio, re.MULTILINE): bio = bio.replace(i.group(1), f'![]({i.group(1)})')
		bio = bio.replace("\n", "\n\n").replace("\n\n\n\n\n\n", "\n\n").replace("\n\n\n\n", "\n\n").replace("\n\n\n", "\n\n")
		with CustomRenderer() as renderer: bio_html = renderer.render(mistletoe.Document(bio))
		bio_html = sanitize(bio_html, linkgen=True)

		# Run safety filter
		bans = filter_comment_html(bio_html)

		if bans:
			ban = bans[0]
			reason = f"Remove the {ban.domain} link from your bio and try again."
			if ban.reason:
				reason += f" {ban.reason}"

			#auto ban for digitally malicious content
			if any([x.reason==4 for x in bans]):
				v.ban(days=30, reason="Digitally malicious content is not allowed.")
			return {"error": reason}, 401

		v.bio = bio
		v.bio_html=bio_html
		g.db.add(v)
		return render_template("settings_profile.html",
							   v=v,
							   msg="Your bio has been updated.")

	if request.values.get("filters"):

		filters=request.values.get("filters")[:1000].strip()

		if filters==v.custom_filter_list:
			return render_template("settings_profile.html",
								   v=v,
								   error="You didn't change anything")

		v.custom_filter_list=filters
		g.db.add(v)
		return render_template("settings_profile.html",
							   v=v,
							   msg="Your custom filters have been updated.")



	defaultsortingcomments = request.values.get("defaultsortingcomments")
	if defaultsortingcomments:
		if defaultsortingcomments in ["new", "old", "controversial", "top", "bottom", "random"]:
			v.defaultsortingcomments = defaultsortingcomments
			updated = True
		else:
			abort(400)

	defaultsorting = request.values.get("defaultsorting")
	if defaultsorting:
		if defaultsorting in ["hot", "new", "old", "comments", "controversial", "top", "bottom", "random", "active"]:
			v.defaultsorting = defaultsorting
			updated = True
		else:
			abort(400)

	defaulttime = request.values.get("defaulttime")
	if defaulttime:
		if defaulttime in ["hour", "day", "week", "month", "year", "all"]:
			v.defaulttime = defaulttime
			updated = True
		else:
			abort(400)

	theme = request.values.get("theme")
	if theme:
		v.theme = theme
		if theme == "coffee": v.themecolor = "805ad5"
		elif theme == "4chan": v.themecolor = "38a169"
		elif theme =="hackernews": v.themecolor = "ff6600"
		elif theme == "win98": 
			v.themecolor = "00007b"
			v.background = "/assets/images/custombackgrounds/other/bg-5"

		g.db.add(v)
		return "", 204

	if updated:
		g.db.add(v)

		return {"message": "Your settings have been updated."}

	else:
		return {"error": "You didn't change anything."}, 400

@app.post("/changelogsub")
@auth_required
@validate_formkey
def changelogsub(v):
	v.changelogsub = not v.changelogsub
	g.db.add(v)

	cache.delete_memoized(frontlist)

	return "", 204

@app.post("/settings/sidebar_settings")
@auth_required
@validate_formkey
def sidebar_settings(v):
	if not v.sidebar_settings:
		sidebar_settings = json.loads("{}")
	else:
		sidebar_settings = json.loads(v.sidebar_settings)
	
	if request.values.get("custom_feed_tag"):
		sidebar_settings['custom_feed_tag'] = request.values.get("custom_feed_tag").strip()
	v.sidebar_settings = sidebar_settings
	g.db.add(v)
	return redirect("/")

@app.post("/settings/namecolor")
@auth_required
@validate_formkey
def namecolor(v):
	color = str(request.form.get("color", "")).strip()
	if color not in ['ff66ac','805ad5','62ca56','38a169','80ffff','2a96f3','eb4963','ff0000','f39731','30409f','3e98a7','e4432d','7b9ae4','ec72de','7f8fa6', 'f8db58', 'ffffff', 'ff6600', '00007b']: abort(400)
	v.namecolor = color
	g.db.add(v)
	return redirect("/settings/profile")

@app.post("/settings/themecolor")
@auth_required
@validate_formkey
def themecolor(v):
	themecolor = str(request.form.get("themecolor", "")).strip()
	if themecolor not in ['ffffff', '47a3ff','805ad5','62ca56','38a169','80ffff','2a96f3','eb4963','ff0000','f39731','adf1d2','3e98a7','e4432d','7b9ae4','ec72de','7f8fa6', 'f8db58', 'ff6600', '00007b']: abort(400)
	v.themecolor = themecolor
	g.db.add(v)
	return redirect("/settings/profile")

@app.post("/settings/titlecolor")
@auth_required
@validate_formkey
def titlecolor(v):
	titlecolor = str(request.form.get("titlecolor", "")).strip()
	if titlecolor not in ['ff66ac','805ad5','62ca56','38a169','80ffff','2a96f3','eb4963','ff0000','f39731','30409f','3e98a7','e4432d','7b9ae4','ec72de','7f8fa6', 'f8db58', 'ffffff', 'ff6600', '00007b']: abort(400)
	v.titlecolor = titlecolor
	g.db.add(v)
	return redirect("/settings/profile")

@app.post("/settings/set_steam")
@auth_required
@validate_formkey
def set_steam(v):
	steam_id = str(request.form.get("steam_id", "")).strip()
	v.steam_id = steam_id
	g.db.add(v)
	return redirect("/settings/profile")

@app.post("/settings/security")
@auth_required
@validate_formkey
def settings_security_post(v):
	if request.form.get("new_password"):
		if request.form.get(
				"new_password") != request.form.get("cnf_password"):
			return redirect("/settings/security?error=" +
							escape("Passwords do not match."))

		if not re.match(valid_password_regex, request.form.get("new_password")):
			#print(f"signup fail - {username } - invalid password")
			return redirect("/settings/security?error=" +
							escape("Password must be between 8 and 100 characters."))

		if not v.verifyPass(request.form.get("old_password")):
			return render_template(
				"settings_security.html", v=v, error="Incorrect password")

		v.passhash = v.hash_password(request.form.get("new_password"))

		g.db.add(v)

		return redirect("/settings/security?msg=" +
						escape("Your password has been changed."))

	if request.form.get("new_email"):

		if not v.verifyPass(request.form.get('password')):
			return redirect("/settings/security?error=" +
							escape("Invalid password."))

		new_email = request.form.get("new_email","").strip()
		#counteract gmail username+2 and extra period tricks - convert submitted email to actual inbox
		if new_email.endswith("@gmail.com"):
			gmail_username=new_email.split('@')[0]
			gmail_username=gmail_username.split("+")[0]
			gmail_username=gmail_username.replace('.','')
			new_email=f"{gmail_username}@gmail.com"
		if new_email == v.email:
			return redirect("/settings/security?error=" +
							escape("That email is already yours!"))

		# check to see if email is in use
		existing = g.db.query(User).filter(User.id != v.id,
										   func.lower(User.email) == new_email.lower()).first()
		if existing:
			return redirect("/settings/security?error=" +
							escape("That email address is already in use."))

		url = f"https://{app.config['SERVER_NAME']}/activate"

		now = int(time.time())

		token = generate_hash(f"{new_email}+{v.id}+{now}")
		params = f"?email={quote(new_email)}&id={v.id}&time={now}&token={token}"

		link = url + params

		send_mail(to_address=new_email,
				  subject="Verify your email address.",
				  html=render_template("email/email_change.html",
									   action_url=link,
									   v=v)
				  )

		return redirect("/settings/security?msg=" + escape(
			"Check your email and click the verification link to complete the email change."))

	if request.form.get("2fa_token", ""):

		if not v.verifyPass(request.form.get('password')):
			return redirect("/settings/security?error=" +
							escape("Invalid password or token."))

		secret = request.form.get("2fa_secret")
		x = pyotp.TOTP(secret)
		if not x.verify(request.form.get("2fa_token"), valid_window=1):
			return redirect("/settings/security?error=" +
							escape("Invalid password or token."))

		v.mfa_secret = secret
		g.db.add(v)

		return redirect("/settings/security?msg=" +
						escape("Two-factor authentication enabled."))

	if request.form.get("2fa_remove", ""):

		if not v.verifyPass(request.form.get('password')):
			return redirect("/settings/security?error=" +
							escape("Invalid password or token."))

		token = request.form.get("2fa_remove")

		if not v.validate_2fa(token):
			return redirect("/settings/security?error=" +
							escape("Invalid password or token."))

		v.mfa_secret = None
		g.db.add(v)

		return redirect("/settings/security?msg=" +
						escape("Two-factor authentication disabled."))

@app.post("/settings/add_ko-fi_email")
@auth_required
@validate_formkey
def add_kofi_email(v):
	new_email = request.form.get("new_email","").strip()
	#counteract gmail username+2 and extra period tricks - convert submitted email to actual inbox
	if new_email.endswith("@gmail.com"):
		gmail_username=new_email.split('@')[0]
		gmail_username=gmail_username.split("+")[0]
		gmail_username=gmail_username.replace('.','')
		new_email=f"{gmail_username}@gmail.com"
	if new_email == v.kofi_email:
		return redirect("/settings/security?error=" +
						escape("That email is already yours!"))

	# check to see if email is in use
	existing = g.db.query(User).filter(User.id != v.id,
										func.lower(User.kofi_email) == new_email.lower()).first()
	if existing:
		return redirect("/settings/security?error=" +
						escape("That email address is already in use."))

	url = f"https://{app.config['SERVER_NAME']}/verify_ko-fi"

	now = int(time.time())

	token = generate_hash(f"{new_email}+{v.id}+{now}")
	params = f"?email={quote(new_email)}&id={v.id}&time={now}&token={token}"

	link = url + params

	send_mail(to_address=new_email,
				subject="Verify your email address.",
				html=render_template("email/email_add_ko-fi.html",
									action_url=link,
									v=v)
				)

	return redirect("/settings/security?msg=" + escape(
		f"Check your email and click the verification link to complete the email change."))


@app.post("/settings/add_xbox_gamertag")
@auth_required
def add_xbox_gamertag(v):

	gamertag = request.form.get("gamertag", "").strip()

	# suffix is required (for adding other people on Xbox)
	if len(gamertag.split("#")) == 1:
		return redirect("/settings/profile?error=" + 
			escape("Please add your Gamertag Suffix"))
	
	# suffix can only be numeric
	if not gamertag.split("#")[1].isdigit():
		return redirect("/settings/profile?error=" + 
			escape("Gamertag Suffix must be all numbers"))

	# suffix can't be more than 5 digits
	if len(gamertag.split("#")[1]) > 5:
		return redirect("/settings/profile?error=" + 
			escape("Gamertag Suffix cannot be more than 5 digits"))

	# gamertag can't be more than 15 digits
	if len(gamertag.split("#")[0]) > 15:
		return redirect("/settings/profile?error=" +
			escape("Gamertag must be less than 15 characters."))
	
	# gamertag can only have 1 space
	gtag_arr = gamertag.split(" ")
	if len(gtag_arr) > 2:
		return redirect("/settings/profile?error=" +
			escape("Gamertag can only have a single space."))

	# gamertag cannot start or end with a space, cannot start with a number
	first_char = gamertag.split("#")[0][0]
	last_char = gamertag.split("#")[0][-1] 
	if first_char.isdigit():
		return redirect("/settings/profile?error=" + 
			escape("Gamertag cannot start with a number."))
	if first_char == " " or last_char == " ":
		return redirect("/settings/profile?error=" + 
			escape("Gamertag cannot start or end with a space."))
	
	user = g.db.query(User).filter(User.id==v.id).first()
	if not user:
		abort(404)
	
	user.xbox_gamertag = gamertag

	g.db.add(user)
	g.db.commit()

	return render_template("settings_profile.html", v=v, msg="Xbox Gamertag updated.")

@app.post("/settings/add_psn_name")
@auth_required
def add_psn_name(v):

	psn_name = request.form.get("psn_name", "").strip()

	psn_arr = [ch for ch in psn_name]

	# name has to be between 3 and 16 characters
	if len(psn_name) < 3 or len(psn_name) > 16:
		return redirect("/settings/profile?error=" + 
			escape("PSN Name must be between 3 and 16 characters."))
	
	# it has to start with a character
	if psn_name[0].isdigit():
		return redirect("/settings/profile?error=" + 
			escape("PSN Name needs to start with a letter."))
	
	# no spaces
	if len(psn_name.split(" ")) > 1:
		return redirect("/settings/profile?error=" + 
			escape("PSN Name cannot contain a space."))
	
	# only numbers, hypens, dashes, and letters
	for c in psn_arr:
		if not c.isalpha():
			if not c.isdigit():
				if c != "_" or c != "-":
					return redirect("/settings/profile?error=" + 
						escape("PSN Name can only contain characters, numbers, hyphens, and dashes"))

	user = g.db.query(User).filter(User.id==v.id).first()
	if not user:
		abort(404)
	
	user.playstation_name = psn_name

	g.db.add(user)
	g.db.commit()

	return render_template("settings_profile.html", v=v, msg="PSN Name updated.")
	
@app.post("/settings/add_switch_friend_code")
@auth_required
def add_steam_friend_code(v):
	
	switch_code = request.form.get("switch_code", "").strip()
	
	if len(switch_code) != 12:
		return redirect("/settings/profile?error=" +
						escape("Friend Code must be 12 digits in length."))
	
	if not switch_code.isdigit():
				return redirect("/settings/profile?error=" +
						escape("Friend Code must be numbers only, no letters."))

	formatted_code = f"SW-{switch_code[0:4]}-{switch_code[4:8]}-{switch_code[8:12]}"

	user = g.db.query(User).filter(User.id==v.id).first()
	if not user:
		abort(404)

	user.switch_code = formatted_code

	g.db.add(user)
	g.db.commit()

	return render_template("settings_profile.html", v=v, msg="Switch Friend Code updated.")

@app.post("/settings/log_out_all_others")
@auth_required
@validate_formkey
def settings_log_out_others(v):

	submitted_password = request.form.get("password", "")

	if not v.verifyPass(submitted_password):
		return render_template("settings_security.html",
							   v=v, error="Incorrect Password"), 401

	# increment account's nonce
	v.login_nonce += 1

	# update cookie accordingly
	session["login_nonce"] = v.login_nonce

	g.db.add(v)

	return render_template("settings_security.html", v=v,
						   msg="All other devices have been logged out")


@app.post("/settings/images/profile")
@auth_required
@validate_formkey
def settings_images_profile(v):

	if request.content_length > 16 * 1024 * 1024:
		g.db.rollback()
		abort(413)

	if request.headers.get("cf-ipcountry") == "T1": return "Image uploads are not allowed through TOR.", 403
	highres = upload_file(request.files["profile"])
	if not highres: abort(400)
	imageurl = upload_file(resize=True)
	if not imageurl: abort(400)
	v.highres = highres
	v.profileurl = imageurl
	g.db.add(v)

	return render_template("settings_profile.html", v=v, msg="Profile picture successfully updated.")


@app.post("/settings/images/banner")
@auth_required
@validate_formkey
def settings_images_banner(v):
	if request.content_length > 16 * 1024 * 1024:
		g.db.rollback()
		abort(413)

	if request.headers.get("cf-ipcountry") == "T1": return "Image uploads are not allowed through TOR.", 403
	imageurl = upload_file(request.files["banner"])
	if imageurl:
		v.bannerurl = imageurl
		g.db.add(v)

	return render_template("settings_profile.html", v=v, msg="Banner successfully updated.")


@app.post("/settings/delete/profile")
@auth_required
@validate_formkey
def settings_delete_profile(v):

	v.profileurl = None
	g.db.add(v)
	return render_template("settings_profile.html", v=v,
						   msg="Profile picture successfully removed.")

@app.post("/settings/delete/banner")
@auth_required
@validate_formkey
def settings_delete_banner(v):

	v.bannerurl = None
	g.db.add(v)

	return render_template("settings_profile.html", v=v,
						   msg="Banner successfully removed.")


@app.post("/settings/read_announcement")
@auth_required
@validate_formkey
def update_announcement(v):

	v.read_announcement_utc = int(time.time())
	g.db.add(v)

	return "", 204


@app.get("/settings/blocks")
@auth_required
def settings_blockedpage(v):
	if v and v.is_banned and not v.unban_utc: return render_template("seized.html")

	#users=[x.target for x in v.blocked]

	return render_template("settings_blocks.html",
						   v=v)

@app.get("/settings/css")
@auth_required
def settings_css_get(v):
	if v and v.is_banned and not v.unban_utc: return render_template("seized.html")

	return render_template("settings_css.html", v=v)

@app.post("/settings/css")
@auth_required
def settings_css(v):
	css = request.form.get("css").replace('\\', '')[:50000]
	v.css = css
	g.db.add(v)
	return render_template("settings_css.html", v=v)

@app.get("/settings/profilecss")
@auth_required
def settings_profilecss_get(v):
	if v and v.is_banned and not v.unban_utc: return render_template("seized.html")
	if v.coins < 1000 and not v.patron: return f"You must have +1000 {COINS_NAME} or be a patron to set profile css."
	return render_template("settings_profilecss.html", v=v)

@app.post("/settings/profilecss")
@auth_required
def settings_profilecss(v):
	if v.coins < 1000 and not v.patron: return f"You must have +1000 {COINS_NAME} or be a patron to set profile css."
	profilecss = request.form.get("profilecss").replace('\\', '')[:50000]
	v.profilecss = profilecss
	g.db.add(v)
	return render_template("settings_profilecss.html", v=v)

@app.post("/settings/block")
@auth_required
@validate_formkey
def settings_block_user(v):

	user = get_user(request.values.get("username"), graceful=True)

	if not user:
		return {"error": "That user doesn't exist."}, 404

	if user.id == v.id:
		return {"error": "You can't block yourself."}, 409

	if v.has_block(user):
		return {"error": f"You have already blocked @{user.username}."}, 409

	if user.id == 1:
		return {"error": "You can't block @files."}, 409

	new_block = UserBlock(user_id=v.id,
						  target_id=user.id,
						  )
	g.db.add(new_block)



	existing = g.db.query(Notification).filter_by(blocksender=v.id, user_id=user.id).first()
	if not existing: send_block_notif(v.id, user.id, f"@{v.username} has blocked you!")

	if request.args.get("notoast"): return "", 204

	if v.admin_level == 1: return {"message": f"@{user.username} banned!"}

	cache.delete_memoized(frontlist)

	return {"message": f"@{user.username} blocked."}


@app.post("/settings/unblock")
@auth_required
@validate_formkey
def settings_unblock_user(v):

	user = get_user(request.values.get("username"))

	x = v.has_block(user)

	if not x: abort(409)

	g.db.delete(x)



	existing = g.db.query(Notification).filter_by(unblocksender=v.id, user_id=user.id).first()
	if not existing: send_unblock_notif(v.id, user.id, f"@{v.username} has unblocked you!")

	if request.args.get("notoast"): return "", 204

	if v.admin_level == 1: return {"message": f"@{user.username} unbanned!"}

	cache.delete_memoized(frontlist)

	return {"message": f"@{user.username} unblocked."}


@app.get("/settings/apps")
@auth_required
def settings_apps(v):
	if v and v.is_banned and not v.unban_utc: return render_template("seized.html")

	return render_template("settings_apps.html", v=v)


@app.post("/settings/remove_discord")
@auth_required
@validate_formkey
def settings_remove_discord(v):

	if v.admin_level>1:
		return render_template("settings_filters.html", v=v, error="Admins can't disconnect Discord.")

	remove_user(v)

	v.discord_id=None
	g.db.add(v)
	g.db.commit()

	return redirect("/settings/profile")

@app.get("/settings/content")
@auth_required
def settings_content_get(v):
	if v and v.is_banned and not v.unban_utc: return render_template("seized.html")

	return render_template("settings_filters.html", v=v)

@app.post("/settings/name_change")
@auth_required
@validate_formkey
def settings_name_change(v):

	new_name=request.form.get("name").strip()

	#make sure name is different
	if new_name==v.username:
		return render_template("settings_profile.html",
						   v=v,
						   error="You didn't change anything")

	#verify acceptability
	if not re.match(valid_username_regex, new_name):
		return render_template("settings_profile.html",
						   v=v,
						   error=f"This isn't a valid username.")

	#verify availability
	name=new_name.replace('_','\_')

	x= g.db.query(User).options(
		lazyload('*')
		).filter(
		or_(
			User.username.ilike(name),
			User.original_username.ilike(name)
			)
		).first()

	if x and x.id != v.id:
		return render_template("settings_profile.html",
						   v=v,
						   error=f"Username `{new_name}` is already in use.")

	v=g.db.query(User).with_for_update().options(lazyload('*')).filter_by(id=v.id).first()

	v.username=new_name
	v.name_changed_utc=int(time.time())

	set_nick(v, new_name)

	g.db.add(v)
	g.db.commit()

	return redirect("/settings/profile")

@app.post("/settings/song_change")
@auth_required
@validate_formkey
def settings_song_change(v):
	song=request.form.get("song").strip()

	if song == "" and v.song and path.isfile(f"/songs/{v.song}.mp3") and g.db.query(User).filter_by(song=v.song).count() == 1:
		os.remove(f"/songs/{v.song}.mp3")
		v.song=None
		g.db.add(v)
		return redirect("/settings/profile")

	song = song.replace("https://music.youtube.com", "https://youtube.com")
	if song.startswith(("https://www.youtube.com/watch?v=", "https://youtube.com/watch?v=", "https://m.youtube.com/watch?v=")):
		id = song.split("v=")[1]
	elif song.startswith("https://youtu.be/"):
		id = song.split("https://youtu.be/")[1]
	else:
		return render_template("settings_profile.html",
					v=v,
					error=f"Not a youtube link.")

	if "?" in id: id = id.split("?")[0]
	if "&" in id: id = id.split("&")[0]

	if path.isfile(f'/songs/{id}.mp3'):
		v.song=id
		g.db.add(v)
		g.db.commit()
		return redirect("/settings/profile")


	req = requests.get(f"https://www.googleapis.com/youtube/v3/videos?id={id}&key={YOUTUBE_KEY}&part=contentDetails").json()
	try: duration = req['items'][0]['contentDetails']['duration']
	except:
		print(req)
		abort(400)
	if "H" in duration:
		return render_template("settings_profile.html",
					v=v,
					error=f"Duration of the video must not exceed 10 minutes.")

	if "M" in duration:
		duration = int(duration.split("PT")[1].split("M")[0])
		if duration > 10:
			return render_template("settings_profile.html",
						v=v,
						error=f"Duration of the video must not exceed 10 minutes.")


	if v.song and path.isfile(f"/songs/{v.song}.mp3") and g.db.query(User).filter_by(song=v.song).count() == 1:
		os.remove(f"/songs/{v.song}.mp3")

	ydl_opts = {
		'outtmpl': '/songs/%(title)s.%(ext)s',
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		try: ydl.download([f"https://youtube.com/watch?v={id}"])
		except Exception as e:
			print(e)
			return render_template("settings_profile.html",
						   v=v,
						   error=f"Age-restricted videos aren't allowed.")

	files = os.listdir("/songs/")
	paths = [path.join("/songs/", basename) for basename in files]
	songfile = max(paths, key=path.getctime)
	os.rename(songfile, f"/songs/{id}.mp3")

	v.song=id
	g.db.add(v)

	return redirect("/settings/profile")

@app.post("/settings/title_change")
@auth_required
@validate_formkey
def settings_title_change(v):

	if v.flairchanged: abort(403)

	new_name=request.form.get("title").strip()

	#verify acceptability
	if not re.match(valid_title_regex, new_name):
		return render_template("settings_profile.html",
						   v=v,
						   error=f"This isn't a valid flair.")

	#make sure name is different
	if new_name==v.customtitle:
		return render_template("settings_profile.html",
						   v=v,
						   error="You didn't change anything")

	v.customtitleplain = new_name
	new_name = sanitize(new_name, flair=True)

	v = g.db.query(User).with_for_update().options(lazyload('*')).filter_by(id=v.id).first()
	v.customtitle = new_name

	g.db.add(v)
	g.db.commit()

	return redirect("/settings/profile")

@app.post("/settings/badges")
@auth_required
@validate_formkey
def settings_badge_recheck(v):

	v.refresh_selfset_badges()

	return {"message":"Badges Refreshed"}
