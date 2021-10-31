from os import environ, path
from .get import *
from files.__main__ import app, cache
import time
import re

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
def post_embed(url):
	regex = "/\/([0-9].)$/gm"
	post_id = re.match(re.compile(regex), url).group(1)
	p = get_post(post_id)
	return render_template(
		"embeds/post.html",
		p=p, 
		time=time.time()
	)

@app.template_filter('to_hours')
def unix_to_hours(s):
	if(s>0):
		return round((time.time() - s)/3600, 1)
	else:
		return 0
    #return time.ctime(s) # datetime.datetime.fromtimestamp(s)

@app.template_filter('as_json')
def str_as_json(s):
	return json.loads(s)

@app.template_filter('len')
def lengg(a):
	return len(a)

@app.template_filter('darken_hex')
@cache.memoize(timeout=60 * 60 * 24)
def darken_hex(s):
    """ takes a color like #87c95f and produces a lighter or darker variant """  
    if len(s) != 6:  
        raise Exception("Passed %s into color_variant(), needs to be in 87c95f format." % hex_color)
    rgb_hex = [s[x:x+2] for x in [0, 2, 4]]
    new_rgb_int = [int(hex_value, 16) + -40 for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255
    # hex() produces "0x88", we want just "88"
    if(len(hex(new_rgb_int[0])) != 4):
        print("0" + hex(new_rgb_int[0])[2:])
        R = "0" + hex(new_rgb_int[0])[2:]
    else:
        R = hex(new_rgb_int[0])[2:]
        
    
    if(len(hex(new_rgb_int[1])) != 4):
        print("0" + hex(new_rgb_int[1])[2:])
        G = "0" + hex(new_rgb_int[1])[2:]
    else:
        G = hex(new_rgb_int[1])[2:]
    
    if(len(hex(new_rgb_int[2])) != 4):
        print("0" + hex(new_rgb_int[2])[2:])
        B = "0" + hex(new_rgb_int[2])[2:]
    else:
        B = hex(new_rgb_int[2])[2:]
        
    return R + G + B

