import qrcode
import io
import time
import traceback
import sys
from datetime import datetime

from files.classes.user import ViewerRelationship
from files.helpers.alerts import *
from files.helpers.sanitize import *
from files.helpers.markdown import *
from files.mail import *
from flask import *
from files.__main__ import app, limiter
from files.helpers.steam import get_steam_info, get_steam_games
# from pusher_push_notifications import PushNotifications, PusherAuthError

site = environ.get("DOMAIN").strip()

# PUSHER_KEY = environ.get("PUSHER_KEY", "").strip()

# beams_client = PushNotifications(
# 		instance_id='9a1835db-8f76-4c65-b444-cb61af126521',
# 		secret_key=PUSHER_KEY,
# )
@app.get("/leaderboard")
@auth_desired
def leaderboard(v):
	if v and v.is_banned and not v.unban_utc:return render_template("seized.html")
	users = g.db.query(User).options(lazyload('*'))
	users1 = users.order_by(User.coins.desc()).limit(25).all()
	users2 = users.order_by(User.stored_subscriber_count.desc()).limit(10).all()
	users3 = users.order_by(User.post_count.desc()).limit(10).all()
	users4 = users.order_by(User.comment_count.desc()).limit(10).all()
	return render_template("leaderboard.html", v=v, users1=users1, users2=users2, users3=users3, users4=users4)

@app.get("/@<username>/css")
def get_css(username):
	user = get_user(username)
	if user.css: css = user.css
	else: css = ""
	resp=make_response(css)
	resp.headers.add("Content-Type", "text/css")
	return resp

@app.get("/@<username>/profilecss")
def get_profilecss(username):
	user = get_user(username)
	if user.profilecss: profilecss = user.profilecss
	else: profilecss = ""
	resp=make_response(profilecss)
	resp.headers.add("Content-Type", "text/css")
	return resp

@app.post("/@<username>/reply/<id>")
@auth_required
def messagereply(v, username, id):

	if v.zzz:
		abort(418)

	message = request.form.get("message", "")[:1000].strip()
	user = get_user(username)
	message = message.replace("\n", "\n\n").replace("\n\n\n\n\n\n", "\n\n").replace("\n\n\n\n", "\n\n").replace("\n\n\n", "\n\n")

	# check existing
	existing = g.db.query(Comment).join(CommentAux).filter(Comment.author_id == v.id,
															Comment.sentto == user.id,
															CommentAux.body == message,
															).options(contains_eager(Comment.comment_aux)).first()
	if existing: return redirect('/notifications?all=true')

	with CustomRenderer() as renderer: text_html = renderer.render(mistletoe.Document(message))
	text_html = sanitize(text_html, linkgen=True, noimages=True)
	parent = get_comment(int(id), v=v)
	new_comment = Comment(author_id=v.id,
							parent_submission=None,
							parent_comment_id=id,
							level=parent.level + 1,
							sentto=user.id
							)
	g.db.add(new_comment)
	g.db.flush()
	new_aux = CommentAux(id=new_comment.id, body=message, body_html=text_html)
	g.db.add(new_aux)
	notif = Notification(comment_id=new_comment.id, user_id=user.id)
	g.db.add(notif)
	g.db.commit()
	return redirect('/notifications?all=true')

@app.get("/songs/<id>")
def songs(id):
	try: id = int(id)
	except: return '', 400
	user = g.db.query(User).filter_by(id=id).first()
	return send_from_directory('/songs/', f'{user.song}.mp3')

@app.post("/subscribe/<post_id>")
@auth_required
def subscribe(v, post_id):
	new_sub = Subscription(user_id=v.id, submission_id=post_id)
	g.db.add(new_sub)
	g.db.commit()
	return "", 204
	
@app.post("/unsubscribe/<post_id>")
@auth_required
def unsubscribe(v, post_id):
	sub=g.db.query(Subscription).filter_by(user_id=v.id, submission_id=post_id).first()
	g.db.delete(sub)
	return "", 204

@app.post("/@<username>/message")
@limiter.limit("10/hour")
@auth_required
def message2(v, username):

	if v.zzz:
		abort(418)

	user = get_user(username, v=v)
	if user.is_blocking: return {"error": "You're blocking this user."}, 403
	if user.is_blocked: return {"error": "This user is blocking you."}, 403
	message = request.form.get("message", "")[:1000].strip()

	message = message.replace("\n", "\n\n").replace("\n\n\n\n\n\n", "\n\n").replace("\n\n\n\n", "\n\n").replace("\n\n\n", "\n\n")

	# check existing
	existing = g.db.query(Comment).join(CommentAux).filter(Comment.author_id == v.id,
															Comment.sentto == user.id,
															CommentAux.body == message,
															).options(contains_eager(Comment.comment_aux)).first()
	if existing: return redirect('/notifications?all=true')

	send_pm(v.id, user, message)
	
	# try:
	# 	beams_client.publish_to_interests(
	# 		interests=[str(user.id)],
	# 		publish_body={
	# 			'web': {
	# 				'notification': {
	# 					'title': f'New message from @{v.username}',
	# 					'body': message,
	# 					'deep_link': f'https://{site}/notifications',
	# 				},
	# 			},
	# 		},
	# 	)
	# except PusherAuthError as e:
	# 	sys.stderr.write(traceback.format_exc())
	# 	sys.stderr.flush()

	return redirect('/notifications?all=true')

@app.get("/2faqr/<secret>")
@auth_required
def mfa_qr(secret, v):
	x = pyotp.TOTP(secret)
	qr = qrcode.QRCode(
		error_correction=qrcode.constants.ERROR_CORRECT_L
	)
	qr.add_data(x.provisioning_uri(v.username, issuer_name=app.config["SITE_NAME"]))
	img = qr.make_image(fill_color="#000000", back_color="white")

	mem = io.BytesIO()

	img.save(mem, format="PNG")
	mem.seek(0, 0)
	return send_file(mem, mimetype="image/png", as_attachment=False)


@app.get("/is_available/<name>")
@auth_desired
def api_is_available(name, v):

	name=name.strip()

	if len(name)<3 or len(name)>25:
		return {name:False}
		
	name=name.replace('_','\_')

	x= g.db.query(User).options(
		lazyload('*')
		).filter(
		or_(
			User.username.ilike(name),
			User.original_username.ilike(name)
			)
		).first()

	if x:
		return {name: False}
	else:
		return {name: True}


@app.get("/id/<id>")
def user_id(id):

	user = get_account(int(id))
	return redirect(user.url)
		
@app.get("/u/<username>")
def redditor_moment_redirect(username):
	return redirect(f"/@{username}")

@app.get("/@<username>/followers")
@auth_required
def followers(username, v):
	if v and v.is_banned and not v.unban_utc: return render_template("seized.html")

	u = get_user(username, v=v)
	users = [x.user for x in u.followers]
	return render_template("followers.html", v=v, u=u, users=users)

@app.get("/views")
@auth_required
def visitors(v):
	if v.admin_level < 1 and not v.patron: return render_template("errors/patron.html", v=v)
	viewers=sorted(v.viewers, key = lambda x: x.last_view_utc, reverse=True)
	return render_template("viewers.html", v=v, viewers=viewers)

@app.get("/@<username>/strikes")
@auth_required
def strikes(username, v):
	if v and v.is_banned and not v.unban_utc: return render_template("seized.html")

	u = get_user(username, v=v)
	strikes = [x.strike for x in u.strikes]
	return render_template("strikes.html", v=v, u=u, strikes=strikes)

@app.get("/@<username>")
@auth_desired
def u_username(username, v=None):
	if v and v.is_banned and not v.unban_utc: return render_template("seized.html")

	# username is unique so at most this returns one result. Otherwise 404

	# case insensitive search

	u = get_user(username, v=v)
	# check for wrong cases

	if username != u.username:
		return redirect(request.path.replace(username, u.username))

	if u.reserved:
		if request.headers.get("Authorization"): return {"error": f"That username is reserved for: {u.reserved}"}
		else: return render_template("userpage_reserved.html", u=u, v=v)

	# viewers
	if v and u.id != v.id:
		view = g.db.query(ViewerRelationship).filter(
			and_(
				ViewerRelationship.viewer_id == v.id,
				ViewerRelationship.user_id == u.id
			)
		).first()

		if view:
			view.last_view_utc = g.timestamp
		else:
			view = ViewerRelationship(user_id = u.id,
									  viewer_id = v.id)

		g.db.add(view)

		
	if u.is_private and (not v or (v.id != u.id and v.admin_level < 3)):
		
		# paidrent = False
		# if v and u.id == 253:
		# 	if int(time.time()) - v.rent_utc < 600: paidrent = True
		# 	elif request.args.get("rent") == "true" and v.coins > 500:
		# 		v.coins -= 500
		# 		v.rent_utc = int(time.time())
		# 		g.db.add(v)
		# 		u.coins += 500
		# 		g.db.add(u)
		# 		send_notification(1, u, f"@{v.username} has paid rent!")
		# 		paidrent = True

		# if not paidrent:

		if request.headers.get("Authorization"): return {"error": "That userpage is private"}
		else: return render_template("userpage_private.html", u=u, v=v)


	if u.is_blocking and (not v or v.admin_level < 3):
		if request.headers.get("Authorization"): return {"error": f"You are blocking @{u.username}."}
		else: return render_template("userpage_blocking.html", u=u, v=v)


	if u.is_blocked and (not v or v.admin_level < 3):
		if request.headers.get("Authorization"): return {"error": "This person is blocking you."}
		else: return render_template("userpage_blocked.html", u=u, v=v)


	sort = request.args.get("sort", "new")
	t = request.args.get("t", "all")
	page = int(request.args.get("page", "1"))
	page = max(page, 1)

	ids = u.userpagelisting(v=v, page=page, sort=sort, t=t)

	# we got 26 items just to see if a next page exists
	next_exists = (len(ids) == 26)
	ids = ids[:25]

   # If page 1, check for sticky
	if page == 1:
		sticky = []
		sticky = g.db.query(Submission).filter_by(is_pinned=True, author_id=u.id).all()
		if sticky:
			for p in sticky:
				ids = [p.id] + ids

	listing = get_posts(ids, v=v)
	try:
		steam_info = get_steam_info(u)
	except:
		steam_info = ""
	
	if u.unban_utc:
		if request.headers.get("Authorization"): {"data": [x.json for x in listing]}
		else: return render_template("userpage.html",
												unban=u.unban_string,
												u=u,
												v=v,
												listing=listing,
												page=page,
												sort=sort,
												t=t,
												time=time.time(),
												next_exists=next_exists,
												steam=steam_info,
												is_following=(v and u.has_follower(v)))



	if request.headers.get("Authorization"): return {"data": [x.json for x in listing]}
	else: return render_template("userpage.html",
									u=u,
									v=v,
									listing=listing,
									page=page,
									sort=sort,
									t=t,
									time=time.time(),
									next_exists=next_exists,
									steam=steam_info,
									is_following=(v and u.has_follower(v)))



@app.get("/@<username>/comments")
@auth_desired
def u_username_comments(username, v=None):
	if v and v.is_banned and not v.unban_utc: return render_template("seized.html")

	# username is unique so at most this returns one result. Otherwise 404

	# case insensitive search

	user = get_user(username, v=v)

	# check for wrong cases

	if username != user.username: return redirect(f'{user.url}/comments')

	u = user

	if u.reserved:
		if request.headers.get("Authorization"): return {"error": f"That username is reserved for: {u.reserved}"}
		else: return render_template("userpage_reserved.html",
												u=u,
												v=v,
												time=time.time())


	if u.is_private and (not v or (v.id != u.id and v.admin_level < 3)):
		# paidrent = False
		# if v and u.id == 253:
		# 	if int(time.time()) - v.rent_utc < 600: paidrent = True
		# 	elif request.args.get("rent") == "true" and v.coins > 500:
		# 		v.coins -= 500
		# 		v.rent_utc = int(time.time())
		# 		g.db.add(v)
		# 		u.coins += 500
		# 		g.db.add(u)
		# 		send_notification(1, u, f"@{v.username} has paid rent!")
		# 		paidrent = True

		# if not paidrent:
		if request.headers.get("Authorization"): return {"error": "That userpage is private"}
		else: return render_template("userpage_private.html",
													u=u,
													v=v,
													time=time.time())

	if u.is_blocking and (not v or v.admin_level < 3):
		if request.headers.get("Authorization"): return {"error": f"You are blocking @{u.username}."}
		else: return render_template("userpage_blocking.html",
													u=u,
													v=v,
													time=time.time())

	if u.is_blocked and (not v or v.admin_level < 3):
		if request.headers.get("Authorization"): return {"error": "This person is blocking you."}
		else: return render_template("userpage_blocked.html",
													u=u,
													v=v,
													time=time.time())


	page = int(request.args.get("page", "1"))
	sort=request.args.get("sort","new")
	t=request.args.get("t","all")

	ids = user.commentlisting(
		v=v, 
		page=page,
		sort=sort,
		t=t,
		)

	# we got 26 items just to see if a next page exists
	next_exists = (len(ids) == 26)
	ids = ids[:25]

	listing = get_comments(ids, v=v)

	is_following = (v and user.has_follower(v))

	try:
		steam_info = get_steam_info(u)
	except:
		steam_info = ""

	if request.headers.get("Authorization"): return {"data": [c.json for c in listing]}
	else: return render_template("userpage_comments.html", steam=steam_info,u=user, v=v, listing=listing, page=page, sort=sort, t=t,next_exists=next_exists, is_following=is_following, standalone=True, time=time.time())

@app.get("/@<username>/info")
@auth_desired
def u_username_info(username, v=None):

	user=get_user(username, v=v)

	if user.is_blocking:
		return {"error": "You're blocking this user."}, 401
	elif user.is_blocked:
		return {"error": "This user is blocking you."}, 403

	return user.json


@app.post("/follow/<username>")
@auth_required
def follow_user(username, v):

	target = get_user(username)

	if target.id==v.id: return {"error": "You can't follow yourself!"}, 400

	# check for existing follow
	if g.db.query(Follow).filter_by(user_id=v.id, target_id=target.id).first(): abort(409)

	new_follow = Follow(user_id=v.id, target_id=target.id)
	g.db.add(new_follow)

	target.stored_subscriber_count = g.db.query(Follow).filter_by(target_id=target.id).count()
	g.db.add(target)

	existing = g.db.query(Notification).filter_by(followsender=v.id, user_id=target.id).first()
	if not existing: send_follow_notif(v.id, target.id, f"@{v.username} has followed you!")
	return "", 204


@app.post("/unfollow/<username>")
@auth_required
def unfollow_user(username, v):

	target = get_user(username)

	# check for existing follow
	follow = g.db.query(Follow).filter_by(user_id=v.id, target_id=target.id).first()

	if not follow: abort(409)

	g.db.delete(follow)
	target.stored_subscriber_count = g.db.query(Follow).filter_by(target_id=target.id).count()
	g.db.add(target)

	existing = g.db.query(Notification).filter_by(followsender=v.id, user_id=target.id).first()
	if not existing: send_unfollow_notif(v.id, target.id, f"@{v.username} has unfollowed you!")
	return "", 204


@app.route("/uid/<id>/pic/profile")
@limiter.exempt
def user_profile_uid(id):
	try: id = int(id)
	except:
		try: id = int(id, 36)
		except: abort(404)
	x=get_account(id)
	return redirect(x.profile_url)


@app.get("/@<username>/saved/posts")
@auth_required
def saved_posts(v, username):

	page=int(request.args.get("page",1))

	ids=v.saved_idlist(page=page)

	next_exists=len(ids)==26

	ids=ids[:25]

	listing = get_posts(ids, v=v)
	try:
		steam_info = get_steam_info(v)
	except:
		steam_info = ""

	if request.headers.get("Authorization"): return {"data": [x.json for x in listing]}
	else: return render_template("userpage.html",
											u=v,
											v=v,
											listing=listing,
											page=page,
											next_exists=next_exists,
											time=time.time(),
											steam=steam_info,
											)


@app.get("/@<username>/saved/comments")
@auth_required
def saved_comments(v, username):

	page=int(request.args.get("page",1))

	ids=v.saved_comment_idlist(page=page)

	next_exists=len(ids)==26

	ids=ids[:25]

	listing = get_comments(ids, v=v)

	try:
		steam_info = get_steam_info(v)
	except:
		steam_info = ""
	if request.headers.get("Authorization"): return {"data": [x.json for x in listing]}
	else: return render_template("userpage_comments.html",
											u=v,
											v=v,
											listing=listing,
											page=page,
											next_exists=next_exists,
											standalone=True,
											time=time.time(),
											steam=steam_info)
