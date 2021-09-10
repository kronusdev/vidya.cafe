from os import environ, path
from .get import *
from files.__main__ import app, cache
import time

@app.template_filter("total_users")
@cache.memoize(timeout=60)
def total_users(x):

	return db.query(User).filter_by(is_banned=0).count()


@app.template_filter("source_code")
@cache.memoize(timeout=60 * 60 * 24)
def source_code(file_name):

	return open(path.expanduser('~') + '/files/' +
				file_name, mode="r+").read()


@app.template_filter("full_link")
def full_link(url):

	return f"https://{app.config['SERVER_NAME']}{url}"


@app.template_filter("env")
def env_var_filter(x):

	x = environ.get(x, 1)

	try:
		return int(x)
	except BaseException:
		try:
			return float(x)
		except BaseException:
			return x


@app.template_filter("js_str_escape")
def js_str_escape(s):

	s = s.replace("'", r"\'")

	return s


@app.template_filter("app_config")
def app_config(x):
	return app.config.get(x)

@app.template_filter("post_embed")
def crosspost_embed(url):

    matches = re.match(post_regex, url)

    b36id = matches.group(1)

    p = get_post(b36id, v=g.v, graceful=True)

    if not p or p.is_deleted or p.is_banned or not p.is_public:
        return ""

    return render_template(
        "embeds/post.html",
        listing=[p],
        v=g.v
        )


@app.template_filter('to_hours')
def unix_to_hours(s):
	if(s>0):
		return round((time.time() - s)/3600, 1)
	else:
		return 0
    #return time.ctime(s) # datetime.datetime.fromtimestamp(s)
