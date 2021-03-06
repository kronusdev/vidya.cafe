from files.helpers.wrappers import *
from files.helpers.get import *
import time
from files.__main__ import app, cache
from files.classes import *

@app.get("/post/")
def slash_post():
	return redirect("/")

# this is a test

def get_user_notifications(v, page, all_, messages, posts):
	page = int(request.args.get('page', 1))
	all_ = request.args.get('all', False)
	messages = request.args.get('messages', False)
	posts = request.args.get('posts', False)
	if messages:
		if v.admin_level == 6: comments = g.db.query(Comment).filter(or_(Comment.author_id==v.id, Comment.sentto==v.id, Comment.sentto==0)).filter(Comment.parent_submission == None).order_by(Comment.created_utc.desc()).offset(25 * (page - 1)).limit(26).all()
		else: comments = g.db.query(Comment).filter(or_(Comment.author_id==v.id, Comment.sentto==v.id)).filter(Comment.parent_submission == None).order_by(Comment.created_utc.desc()).offset(25 * (page - 1)).limit(26).all()
		next_exists = (len(comments) == 26)
		comments = comments[:25]
	elif posts:
		cids = v.notification_subscriptions(page=page, all_=all_)
		next_exists = (len(cids) == 26)
		cids = cids[:25]
		comments = get_comments(cids, v=v)
	else:
		cids = v.notification_commentlisting(page=page, all_=all_)
		next_exists = (len(cids) == 26)
		cids = cids[:25]
		comments = get_comments(cids, v=v)

	listing = []
	for c in comments:
		c._is_blocked = False
		c._is_blocking = False
		if c.parent_submission and c.parent_comment and c.parent_comment.author_id == v.id:
			while c.parent_comment:
				parent = c.parent_comment
				if c not in parent.replies2:
					parent.replies2 = parent.replies2 + [c]
					parent.replies = parent.replies2
				c = parent
			if c not in listing:
				listing.append(c)
				c.replies = c.replies2
		elif c.parent_submission and c not in listing:
			listing.append(c)
		else:
			if c.parent_comment:
				while c.level > 1:
					c = c.parent_comment

			if c not in listing:
				listing.append(c)
	return {"listing": listing, "next_exists": next_exists}

@app.get("/notifications")
@auth_required
def notifications(v):

	if v and v.is_banned and not v.unban_utc: return render_template("seized.html")

	page = int(request.args.get('page', 1))
	all_ = request.args.get('all', False)
	messages = request.args.get('messages', False)
	posts = request.args.get('posts', False)
	listing = get_user_notifications(v, page, all_, messages, posts)
	return render_template("notifications.html",
						   v=v,
						   notifications=listing['listing'],
						   next_exists=listing['next_exists'],
						   page=page,
						   standalone=True,
						   render_replies=True,
						   is_notification_page=True,
						   time=time.time())

@cache.memoize(timeout=1500)
def frontlist(v=None, feed="vidya", sort="hot", t="all", tag="all", show_sticky=True, page=1, posts_per_page=25, filter_words='', **kwargs):
	# vidya, cafe and all
	if feed != "all":
		posts = g.db.query(Submission).options(lazyload('*')).filter_by(is_banned=False,stickied=False,private=False,feed=feed).filter(Submission.deleted_utc == 0)
	else:
		posts = g.db.query(Submission).options(lazyload('*')).filter_by(is_banned=False,stickied=False,private=False).filter(Submission.deleted_utc == 0)

	if v and v.admin_level == 0:
		blocking = g.db.query(
			UserBlock.target_id).filter_by(
			user_id=v.id).subquery()
		blocked = g.db.query(
			UserBlock.user_id).filter_by(
			target_id=v.id).subquery()
		posts = posts.filter(
			Submission.author_id.notin_(blocking),
			Submission.author_id.notin_(blocked)
		)
	
	if (tag == "changelog"):
		posts = posts.filter(Submission.tag == tag, User.admin_level > 0)
	elif (tag == "all"):
		posts = posts
	else:
		posts = posts.filter(Submission.tag == tag)

	if (not ((v and v.changelogsub))) and tag != "changelog":
		posts=posts.filter(not_(Submission.tag == "changelog"))

	if v and filter_words:
		for word in filter_words:
			posts=posts.filter(not_(Submission.title.ilike(f'%{word}%')))

	if t != 'all':
		cutoff = 0
		now = int(time.time())
		if t == 'hour':
			cutoff = now - 3600
		elif t == 'day':
			cutoff = now - 86400
		elif t == 'week':
			cutoff = now - 604800
		elif t == 'month':
			cutoff = now - 2592000
		elif t == 'year':
			cutoff = now - 31536000
		posts = posts.filter(Submission.created_utc >= cutoff)

	gt = kwargs.get("gt")
	lt = kwargs.get("lt")

	if gt:
		posts = posts.filter(Submission.created_utc > gt)

	if lt:
		posts = posts.filter(Submission.created_utc < lt)

	if sort == "hot":
		posts = sorted(posts.all(), key=lambda x: x.hotscore, reverse=True)
	elif sort == "new":
		posts = posts.order_by(Submission.created_utc.desc()).all()
	elif sort == "old":
		posts = posts.order_by(Submission.created_utc.asc()).all()
	elif sort == "controversial":
		posts = sorted(posts.all(), key=lambda x: x.score_disputed, reverse=True)
	elif sort == "top":
		posts = sorted(posts.all(), key=lambda x: x.score, reverse=True)
	elif sort == "bottom":
		posts = sorted(posts.all(), key=lambda x: x.score)
	elif sort == "comments":
		posts = sorted(posts.all(), key=lambda x: x.comment_count, reverse=True)
	elif sort == "active":
		posts = sorted(posts.all(), key=lambda x: x.score_active, reverse=True)
	elif sort == "random":
		posts = posts.all()
		posts = random.sample(posts, k=len(posts))
	else:
		abort(400)

	firstrange = posts_per_page * (page - 1)
	#secondrange = firstrange+1000
	secondrange = firstrange+posts_per_page
	posts = posts[firstrange:secondrange]

	if v and v.hidevotedon: posts = [x for x in posts if x.voted == 0]

	if page == 1 and show_sticky: posts = g.db.query(Submission).filter_by(stickied=True).all() + posts

	if random.random() < 0.02:
		for post in posts:
			if post.author and post.author.shadowbanned:
				rand = random.randint(500,1400)
				vote = Vote(user_id=rand,
					vote_type=random.choice([-1, 1]),
					submission_id=post.id)
				g.db.add(vote)
				try: g.db.flush()
				except: g.db.rollback()
				post.upvotes = g.db.query(Vote).filter_by(submission_id=post.id, vote_type=1).count()
				post.views = post.views + random.randint(7,10)
				g.db.add(post)

	posts = [x for x in posts if not (x.author and x.author.shadowbanned) or (v and v.id == x.author_id)][:posts_per_page+1]

	return [x.id for x in posts]


def get_frontpage(v, request, feed):
	if(v):
		v.last_active = time.time();
	if v and v.is_banned and not v.unban_utc: return render_template("seized.html")

	try: page = int(request.args.get("page") or 1)
	except: abort(400)

	# prevent invalid paging
	page = max(page, 1)

	if v:
		defaultsorting = v.defaultsorting
		defaulttime = v.defaulttime
	else:
		defaultsorting = "active"
		defaulttime = "all"
	frontpage_tag=request.args.get("frontpage_tag", "all")
	sort=request.args.get("sort", defaultsorting)
	t=request.args.get('t', defaulttime)
	# front page
	ids = frontlist(sort=sort,
					tag=frontpage_tag,
					page=page,
					t=t,
					v=v,
					gt=int(request.args.get("utc_greater_than", 0)),
					lt=int(request.args.get("utc_less_than", 0)),
					filter_words=v.filter_words if v else [],
					feed=feed,
					show_sticky=True
					)

	# check existence of next page
	next_exists = (len(ids) == 26)
	ids = ids[:25]

	# check if ids exist
	posts = get_posts(ids, v=v)
	
	custom_feed_page = int(request.args.get("custom_feed_page") or 1)
	custom_feed_page = max(custom_feed_page, 1)
	try:
		sidebar_settings = json.loads(v.sidebar_settings)
	except:
		sidebar_settings = ""
	try:
		custom_feed_sort=sidebar_settings['custom_feed_sort']
	except:
		custom_feed_sort="new"
	try:
		custom_feed_time=sidebar_settings['custom_feed_time']
	except:
		custom_feed_time="all"
	# sidebar
	# CUSTOM FEED
	custom_feed_posts = ""
	custom_feed_next_exists = ""
	custom_feed_tag = "all"
	
	if v:
		try:
			custom_feed_tag = sidebar_settings['custom_feed_tag']
		except:
			custom_feed_tag = "all"
			
		ids = frontlist(v=v, feed="all", sort=custom_feed_sort, t=custom_feed_time, tag=custom_feed_tag, show_sticky=False, page=custom_feed_page, posts_per_page=10)

		# check existence of next page
		custom_feed_next_exists = (len(ids) == 11)
		custom_feed_ids = ids

		# check if ids exist
		custom_feed_posts = get_posts(custom_feed_ids, v=v)
		last_comments_output = get_recent_posts(v)
	
	# SIDEBAR NOTIFICATIONS
	sidebar_notif_page = int(request.args.get("sidebar_notif_page") or 1)
	sidebar_notif_page = max(sidebar_notif_page, 1)
	if v:
		sidebar_notif_feed_cids = v.notification_commentlisting(sidebar_notif_page, True, True)
		sidebar_notif_feed_next_exists = (len(sidebar_notif_feed_cids) == 26)
		sidebar_notif_feed_cids = sidebar_notif_feed_cids[:25]
		sidebar_notif_feed = get_comments(sidebar_notif_feed_cids, v=v)
	else:
		sidebar_notif_feed = ""
		sidebar_notif_feed_next_exists = False
	sidebar_notif_feed_page = int(request.args.get("sidebar_notif_feed_page") or 1)
	sidebar_notif_feed_page = max(custom_feed_page, 1)



	if request.headers.get("Authorization"): return {"data": [x.json for x in posts], "next_exists": next_exists}
	else: return render_template("home.html", 
								v=v, 
								listing=posts, 
								next_exists=next_exists, 
								sort=sort, 
								t=t, 
								page=page, 
								frontpage_tag=frontpage_tag,
								custom_feed_next_exists=custom_feed_next_exists, 
								sidebar_listing=custom_feed_posts, 
								custom_feed_page=custom_feed_page,
								custom_feed_tag=custom_feed_tag,
								custom_feed_time=custom_feed_time,
								custom_feed_sort=custom_feed_sort,
								sidebar_notif_feed=sidebar_notif_feed,
								sidebar_notif_feed_next_exists=sidebar_notif_feed_next_exists,
								sidebar_notif_feed_page=sidebar_notif_feed_page,
								sidebar_settings=sidebar_settings,
								time=time.time(),
								feed=feed)


@app.get("/")
@auth_desired
def frontpage_vidya(v):
	return get_frontpage(v=v, request=request, feed="vidya")
@app.get("/cafe")
@auth_desired
def frontpage_cafe(v):
	return get_frontpage(v=v, request=request, feed="cafe")

@app.get("/changelog")
@auth_desired
def changelog(v):
	if v and v.is_banned and not v.unban_utc: return render_template("seized.html")

	page = int(request.args.get("page") or 1)
	page = max(page, 1)

	sort=request.args.get("sort", "new")
	t=request.args.get('t', "all")
	
	ids = frontlist(v=v, feed="all", sort=sort, t=t, tag="changelog", show_sticky=False, page=page)
	# check existence of next page
	next_exists = (len(ids) == 26)
	ids = ids

	# check if ids exist
	posts = get_posts(ids, v=v)

	if request.headers.get("Authorization"): return {"data": [x.json for x in posts], "next_exists": next_exists}
	else: return render_template("changelog.html", v=v, listing=posts, next_exists=next_exists, sort=sort, t=t, page=page, time=time.time())


@app.get("/random")
@auth_desired
def random_post(v):
	if v and v.is_banned and not v.unban_utc: return render_template("seized.html")

	x = g.db.query(Submission).filter(Submission.deleted_utc == 0, Submission.is_banned == False)

	total = x.count()
	n = random.randint(0, total - 1)

	post = x.order_by(Submission.id.asc()).offset(n).limit(1).first()
	return redirect(post.permalink)

@cache.memoize(600)
def comment_idlist(page=1, v=None, nsfw=False, sort="new", t="all", **kwargs):

	posts = g.db.query(Submission).options(lazyload('*'))

	posts = posts.subquery()

	comments = g.db.query(Comment).options(lazyload('*'))

	if v and v.admin_level <= 3:
		blocking = g.db.query(
			UserBlock.target_id).filter_by(
			user_id=v.id).subquery()
		blocked = g.db.query(
			UserBlock.user_id).filter_by(
			target_id=v.id).subquery()

		comments = comments.filter(
			Comment.author_id.notin_(blocking),
			Comment.author_id.notin_(blocked)
		)

	if not v or not v.admin_level >= 3:
		comments = comments.filter_by(is_banned=False).filter(Comment.deleted_utc == 0)

	comments = comments.join(posts, Comment.parent_submission == posts.c.id)

	now = int(time.time())
	if t == 'hour':
		cutoff = now - 3600
	elif t == 'day':
		cutoff = now - 86400
	elif t == 'week':
		cutoff = now - 604800
	elif t == 'month':
		cutoff = now - 2592000
	elif t == 'year':
		cutoff = now - 31536000
	else:
		cutoff = 0
	comments = comments.filter(Comment.created_utc >= cutoff)

	if sort == "new":
		comments = comments.order_by(Comment.created_utc.desc()).all()
	elif sort == "old":
		comments = comments.order_by(Comment.created_utc.asc()).all()
	elif sort == "controversial":
		comments = sorted(comments.all(), key=lambda x: x.score_disputed, reverse=True)
	elif sort == "top":
		comments = sorted(comments.all(), key=lambda x: x.score, reverse=True)
	elif sort == "bottom":
		comments = sorted(comments.all(), key=lambda x: x.score)

	firstrange = 25 * (page - 1)
	secondrange = firstrange+100
	comments = comments[firstrange:secondrange]

	comments = [x.id for x in comments if not (x.author and x.author.shadowbanned) or (v and v.id == x.author_id)]

	return comments[:26]

@app.get("/comments")
@auth_desired
def all_comments(v):
	if v and v.is_banned and not v.unban_utc: return render_template("seized.html")

	page = int(request.args.get("page", 1))

	sort=request.args.get("sort", "new")
	t=request.args.get("t", "all")

	idlist = comment_idlist(v=v,
							page=page,
							sort=sort,
							t=t,
							)

	comments = get_comments(idlist, v=v)

	next_exists = len(idlist) == 26

	idlist = idlist[:25]

	if request.headers.get("Authorization"): return {"data": [x.json for x in comments]}
	else: return render_template("home_comments.html", v=v, sort=sort, t=t, page=page, comments=comments, standalone=True, next_exists=next_exists, time=time.time())
