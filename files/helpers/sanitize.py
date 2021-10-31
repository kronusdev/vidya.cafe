import bleach
from bs4 import BeautifulSoup
from bleach.linkifier import LinkifyFilter
from urllib.parse import ParseResult, urlunparse, urlencode, urlparse, parse_qs
from functools import partial
from .get import *
from os import path

site = environ.get("DOMAIN").strip()

_allowed_tags = tags = ['b',
						'blockquote',
						'br',
						'code',
						'del',
						'em',
						'h1',
						'h2',
						'h3',
						'h4',
						'h5',
						'h6',
						'hr',
						'i',
						'li',
						'ol',
						'p',
						'pre',
						'strong',
						'sub',
						'sup',
						'table',
						'tbody',
						'th',
						'thead',
						'td',
						'tr',
						'ul',
						'marquee',
						'a',
						'img',
						'span',
						]

no_images = ['b',
			'blockquote',
			'br',
			'code',
			'del',
			'em',
			'h1',
			'h2',
			'h3',
			'h4',
			'h5',
			'h6',
			'hr',
			'i',
			'li',
			'ol',
			'p',
			'pre',
			'strong',
			'sub',
			'sup',
			'table',
			'tbody',
			'th',
			'thead',
			'td',
			'tr',
			'ul',
			'marquee',
			'a',
			'span']

_allowed_attributes = {
	'*': ['href', 'style', 'src', 'class', 'title', 'rel', 'data-original-name']
	}

_allowed_protocols = [
	'http', 
	'https'
	]

_allowed_styles =[
	'color',
	'font-weight',
	'margin-bottom'
]

# filter to make all links show domain on hover


def a_modify(attrs, new=False):

	raw_url=attrs.get((None, "href"), None)
	if raw_url:
		parsed_url = urlparse(raw_url)

		domain = parsed_url.netloc
		attrs[(None, "target")] = "_blank"
		if domain and not domain.endswith(domain):
			attrs[(None, "rel")] = "nofollow noopener"

			# Force https for all external links in comments
			# (Website already forces its own https)
			new_url = ParseResult(scheme="https",
								  netloc=parsed_url.netloc,
								  path=parsed_url.path,
								  params=parsed_url.params,
								  query=parsed_url.query,
								  fragment=parsed_url.fragment)

			attrs[(None, "href")] = urlunparse(new_url)

	return attrs






_clean_wo_links = bleach.Cleaner(tags=_allowed_tags,
								 attributes=_allowed_attributes,
								 protocols=_allowed_protocols,
								 )

_clean_w_links = bleach.Cleaner(tags=_allowed_tags,
								attributes=_allowed_attributes,
								protocols=_allowed_protocols,
								styles=_allowed_styles,
								filters=[partial(LinkifyFilter,
												 skip_tags=["pre"],
												 parse_email=False,
												 callbacks=[a_modify]
												 )
										 ]
								)


def sanitize(text, linkgen=False, flair=False, noimages=False, polls=False):

	text = text.replace("\ufeff", "").replace("m.youtube.com", "youtube.com")
	
	if noimages:
		text = bleach.Cleaner(tags=no_images, 
							  attributes=_allowed_attributes,
							  protocols=_allowed_protocols,
							  styles=_allowed_styles,
							  filters=[partial(LinkifyFilter,
							  				   skip_tags=["pre"],
											   parse_email=False,
											   callbacks=[a_modify]
											   )
											]	
										).clean(text)
	if linkgen:
		sanitized = _clean_w_links.clean(text)

		#soupify
		soup = BeautifulSoup(sanitized, features="html.parser")

		#img elements - embed
		for tag in soup.find_all("img"):

			url = tag.get("src", "")
			if not url: continue
			netloc = urlparse(url).netloc

			domain = get_domain(netloc)

			if "profile-pic-20" not in tag.get("class", ""):
				#print(tag.get('class'))
				# set classes and wrap in link

				tag["rel"] = "nofollow"
				tag["style"] = "max-height: 100px; max-width: 100%;"
				tag["class"] = "in-comment-image rounded-sm my-2"

				link = soup.new_tag("a")
				link["href"] = tag["src"]
				link["rel"] = "nofollow noopener"
				link["target"] = "_blank"

				link["onclick"] = f"expandDesktopImage('{tag['src']}');"
				link["data-toggle"] = "modal"
				link["data-target"] = "#expandImageModal"

				tag.wrap(link)

		#disguised link preventer
		for tag in soup.find_all("a"):

			if re.match("https?://\S+", str(tag.string)):
				try:
					tag.string = tag["href"]
				except:
					tag.string = ""

		#clean up tags in code
		for tag in soup.find_all("code"):
			tag.contents=[x.string for x in tag.contents if x.string]

		#whatever else happens with images, there are only two sets of classes allowed
		for tag in soup.find_all("img"):
			if 'profile-pic-20' not in tag.attrs.get("class",""):
				tag.attrs['class']="in-comment-image rounded-sm my-2"

		#table format
		for tag in soup.find_all("table"):
			tag.attrs['class']="table table-striped"

		for tag in soup.find_all("thead"):
			tag.attrs['class']="bg-primary text-white"


		sanitized = str(soup)

	else:
		sanitized = _clean_wo_links.clean(text)
	
	start = '&lt;s&gt;'
	end = '&lt;/s&gt;' 
	if start in sanitized and end in sanitized and start in sanitized.split(end)[0] and end in sanitized.split(start)[1]: 			sanitized = sanitized.replace(start, '<span class="spoiler">').replace(end, '</span>')
	#emojis
	if flair: emojisize = 20
	else: emojisize = 30
	for i in re.finditer(':(.{1,30}?):', sanitized):
		if path.isfile(f'./files/assets/images/emojis/{i.group(1)}.gif'):
			sanitized = sanitized.replace(f':{i.group(1)}:', f'<img data-bs-toggle="tooltip" title="{i.group(1)}" delay="0" height={emojisize} src="https://{site}/assets/images/emojis/{i.group(1)}.gif"<span>')
	# urls
	sanitized = sanitized.replace("https://www.", "https://").replace("https://youtu.be/", "https://youtube.com/embed/").replace("https://music.youtube.com/watch?v=", "https://youtube.com/embed/").replace("/watch?v=", "/embed/").replace("https://open.spotify.com/", "https://open.spotify.com/embed/").replace("https://streamable.com/", "https://streamable.com/e/").replace("https://youtube.com/shorts/", "https://youtube.com/embed/")
	
	for i in re.finditer('<a href="(https://(streamable|youtube).com/(e|embed)/.*?)"', sanitized):
		url = i.group(1)
		replacing = f'<a href="{url}" rel="nofollow noopener" target="_blank">{url}</a>'
		htmlsource = f'<div style="padding-top:5px; padding-bottom: 10px;"><iframe frameborder="0" src="{url}?controls=0"></iframe></div>'
		sanitized = sanitized.replace(replacing, htmlsource)
		
	for i in re.finditer('<a href="(https://open.spotify.com/embed/.*?)"', sanitized):
		url = i.group(1)
		replacing = f'<a href="{url}" rel="nofollow noopener" target="_blank">{url}</a>'
		htmlsource = f'<iframe src="{url}" width="100%" height="80" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>'
		sanitized = sanitized.replace(replacing, htmlsource)

	sanitized = sanitized.replace("https://mobile.twitter.com", "https://twitter.com")

	for rd in ["https://reddit.com/", "https://new.reddit.com/", "https://www.reddit.com/", "https://redd.it/"]:
		sanitized = sanitized.replace(rd, "https://old.reddit.com/")

	for i in re.finditer('(/comments/.*?)"', sanitized):
		url = i.group(1)
		p = urlparse(url).query
		p = parse_qs(p)

		if 'sort' not in p:
			p['sort'] = ['controversial']

		url_noquery = url.split('?')[0]
		sanitized = sanitized.replace(url, f"{url_noquery}?{urlencode(p, True)}")

	return sanitized
