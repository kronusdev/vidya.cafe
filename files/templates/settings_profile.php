{% extends "settings.html" %}

{% block pagetitle %}Profile Settings - {{"SITE_NAME" | app_config}}{% endblock %}

{% block content %}
{% include "emoji_modal.html" %}
{% include "gif_modal.html" %}

<?php
	require 'steamauth/steamauth.php';
?>

<div class="row">

	<div class="col col-lg-10">

		<div class="settings">



			<div class="card-blank rounded">
				<h2 class="h5 card-header" name="referral">Theme</h2>
					<div class="body d-lg-flex border-bottom">
						<div class="title w-lg-25">
							<label for="theme">Website Theme</label>
						</div>

						<div class="body w-lg-100">
							<p>Change the theme for the website.</p>
							<div class="input-group mb2">
								<select id='theme' class="form-control" form="profile-settings" name="theme" onchange="post('/settings/profile?theme='+document.getElementById('theme').value, function(){window.location.reload(true);})">
								 {% for entry in ["dark", "light", "coffee", "tron", "hackernews", "4chan", "blur", "win98", "midnight"] %}
									 <option value="{{entry}}" {% if v.theme==entry %} selected {% endif %}>
										{{entry}}
									</option>
								{% endfor %}
							 </select>
							</div>
							{% if v.theme == "blur" %}
								<div class="text-small text-muted mt-3">This theme won't work for most firefox users. To make it work, see <a href="https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter#browser_compatibility">the mozilla developers website</a> and follow the instructions to turn it on (click small triangle under "Firefox")</div>
							{% endif %}
						</div>
				</div>
					<div class="body d-lg-flex border-bottom">
						<div class="title w-lg-25">
							<label for="themecolor">Theme Color</label>
						</div>
				<div class="d-flex">

					 <form action="/settings/themecolor" id="themecolor-form" method="post" class="color-picker" style="line-height: 0">
							<input type="hidden" name="formkey" value="{{v.formkey}}">

							{% for themecolor in ['47a3ff','805ad5','62ca56','38a169','80ffff','2a96f3','eb4963','ff0000','f39731','adf1d2','3e98a7','e4432d','7b9ae4','ec72de','7f8fa6', 'f8db58', 'ffffff', 'ff6600', '00007b'] %}
							<input type="radio" name="themecolor" id="themecolor-{{themecolor}}" value="{{themecolor}}" {% if v.themecolor == themecolor %}checked{% endif %} onclick="document.getElementById('themecolor-form').submit()"/>
							<label class="color-radio" for="themecolor-{{themecolor}}">
								<span style="background-color: #{{themecolor}}">
								{% if v.themecolor.lower() == themecolor %}
									<i class="fas fa-check text-white"></i>
								{% else %}
									&nbsp;
								{% endif %}
								</span>
							</label>
							{% endfor %}

					</form>

				</div>

				</div>
					<div class="body d-lg-flex border-bottom">
					<div class="title w-lg-25">
						<label for="theme">Website Backgrounds</label>
					</div>
						<div class="body w-lg-100">
							<script>
								function updatebgselection(){
								var bgselector = document.getElementById("backgroundSelector");
								var selection = bgselector.options[bgselector.selectedIndex].text;

								//var paragraph = document.getElementById("testp");
								//paragraph.innerHTML = selection;

								const backgrounds = [
									{
										folder: "fantasy",
										backgrounds:
										[
											"bg-1",
											"bg-2",
											"bg-3",
											"bg-4",
										]
									},
									{
										folder: "solarpunk",
										backgrounds:
										[
											"bg-1",
											"bg-2",
											"bg-3",
											"bg-4",
											"bg-5",
											"bg-6",
											"bg-7",
											"bg-8",
											"bg-9",
											"bg-10",
											"bg-11",
											"bg-12",
											"bg-13",
											"bg-14",
											"bg-15",
											"bg-16",
											"bg-17",
											"bg-18",
											"bg-19",
										]
									},
									{
										folder: "other",
										backgrounds:
										[
											"bg-1",
											"bg-2",
											"bg-3",
											"bg-4",
											"bg-5",
										]
									},
									{
									folder: "pixelart",
									backgrounds:
									[
										"bg-1",
										"bg-2",
										"bg-3",
										"bg-4",
										"bg-5",
										"bg-6",
										"bg-7",
									]
									}
								]
									let bgContainer = document.getElementById(`bgcontainer`);
									let str = '';
									let bgsToDisplay = backgrounds[bgselector.selectedIndex].backgrounds;
									let bgsDir = backgrounds[bgselector.selectedIndex].folder;
									for (i=0; i < bgsToDisplay.length; i++) {
										let onclickPost = "/assets/images/custombackgrounds/" + bgsDir + "/" + bgsToDisplay[i];
										str += `<button class="btn btn-secondary m-1 p-0" style="width:15rem; overflow: hidden;"><img style="padding:0.25rem; width: 15rem" src="/assets/images/custombackgrounds/${bgsDir}/${bgsToDisplay[i]}" alt="${bgsToDisplay[i]}-background" onclick="post('/settings/profile?background=${onclickPost}', function(){window.location.reload(true);})"/></button>`;
									}
									bgContainer.innerHTML = str;
								}
							</script>
							<p>Change the background for the website.</p>
							<div class="input-group mb2">
									<select id='backgroundSelector' class="form-control" form="profile-settings" name="background" onchange="updatebgselection();">
									{% for entry in ["fantasy", "solarpunk", "other", "pixelart"] %}
										<option value="{{entry}}">
											{{entry}}
										</option>
									{% endfor %}
								</select>
							</div>
							<div class="d-flex mt-2">
								<!--<input class="btn btn-primary ml-auto" value="Load Backgrounds" onclick="updatebgselection();">-->
								<a class="btn btn-primary ml-auto" id="loadBackgrounds" href="javascript:void(0)" onclick="updatebgselection()">Load Backgrounds</a>
							</div>
							<div id="bgcontainer"></div>

						</div>
				</div>
			</div>

			<div class="card-blank rounded">
				<h2 class="h5 card-header">Profile Picture</h2>
				<div class="d-flex">

					<div class="title w-lg-25 text-md-center">
						<img src="{{v.profile_url}}" class="profile-pic-75">
					</div>

					<div class="body w-lg-100 my-auto">

						<div class="d-flex">

							<div>

								<form action="/settings/images/profile" method="post" enctype="multipart/form-data">
									<input type="hidden" name="formkey" value="{{v.formkey}}">
									<label class="btn btn-secondary text-capitalize mr-2 mb-0">
										Update<input type="file" hidden name="profile" onchange="form.submit()">
									</label>
								</form>

							</div>

							{% if v.profileurl %}
							<div>
								<form action="/settings/delete/profile" method="post">
									<input type="hidden" name="formkey" value="{{v.formkey}}">
									<button type="submit" value="Delete" class="btn btn-link fa-lg"><i class="far fa-trash-alt text-danger"></i></button>
								</form>
							</div>
							{% endif %}

						</div>

						<div class="text-small-extra text-muted mt-3">JPG, PNG, GIF files are supported. Max file size is 16 MB.</div>

					</div>

				</div>

			</div>

			<div class="card-blank rounded">
				<h2 class="h5 card-header">Profile Banner</h2>
				<div class="d-flex">

					<div class="title w-lg-75 text-md-center">
						<img src="{{v.banner_url}}" class="banner-pic-135">
					</div>

					<div class="body w-lg-100 my-auto">

						<div class="d-flex">

							<div>

								<form action="/settings/images/banner" method="post" enctype="multipart/form-data">
									<input type="hidden" name="formkey" value="{{v.formkey}}">
									<label class="btn btn-secondary text-capitalize mr-2 mb-0">
										Update<input type="file" hidden name="banner" onchange="form.submit()">
									</label>
								</form>

							</div>

							<div>

								{% if v.bannerurl %}
								<form action="/settings/delete/banner" method="post">
									<input type="hidden" name="formkey" value="{{v.formkey}}">
									<button type="submit" value="Delete" class="btn btn-link fa-lg"><i class="far fa-trash-alt text-danger"></i></button>
								</form>{% endif %}

							</div>

						</div>

						<div class="text-small-extra text-muted mt-3">JPG, PNG, GIF files are supported. Max file size is 16 MB.</div>

					</div>

				</div>

			</div>

			<div class="card-blank rounded">
			<div class="card-header">
				<h2 class="h5" id="referral" name="referral">Referrals</h2>
				<p class="text-small text-muted">Invite a friend.</p>
			</div>
				<div class="d-lg-flex">

					<div class="title w-lg-25">
						<label for="referral_code">Referral code</label>
					</div>

					<div class="body w-lg-100">

						<div class="input-group">

							<input type="text" readonly="" class="form-control copy-link" id="referral_code" value="{{request.host_url}}signup?ref={{v.username}}" data-clipboard-text="{{request.host_url}}signup?ref={{v.username}}">

							<span class="input-group-append" data-toggle="tooltip" data-placement="top" title="You have referred {{v.referral_count}} user{{'s' if v.referral_count != 1 else ''}} so far. {% if v.referral_count==0 %}¯\_(ツ)_/¯{% elif v.referral_count>10%}Wow!{% endif %}">
								<span class="input-group-text text-primary border-0">
									<i class="far fa-user mr-1" aria-hidden="true"></i>{{v.referral_count}}</span>
								</span>

							</div>

							<div class="text-small-extra text-muted mt-3">Share this link with a friend. {% if v.referral_count==0 %} When they sign up, you'll get the bronze recruitment badge. <a href="/badges">Learn more.</a>{% elif v.referral_count<10 %} When you refer 10 friends, you'll receive the silver recruitment badge. <a href="/badges">Learn more.</a>{% elif v.referral_count<100 %} When you refer 100 friends, you'll receive the gold recruitment badge. <a href="/badges">Learn more</a>.{% endif %}</div>

							</div>

						</div>

					</div>

					  <div class="card-blank rounded">
						<div class="card-header">
							<h2 class="h5" name="referral">Linked Accounts</h2>
							<p class="text-small text-muted">Manage your connections to other services.</p>
						</div>
						<div class="d-lg-flex">

						  <div class="title w-lg-25">
							<label>Discord</label>
						  </div>

						  <div class="body w-lg-100">

							{% if v.discord_id %}
							<form action="/settings/remove_discord" method="post">
							  <input type="hidden" name="formkey" value="{{v.formkey}}">
							  <input type="submit" class="btn btn-secondary text-capitalize mr-2 mb-0 mt-2" value="Disconnect Discord">
							</form>

							<div class="text-small-extra text-muted mt-3">Disconnecting your Discord account will remove you from the {{"SITE_NAME" | app_config}} Discord server.</div>
							{% else %}
							<a href="/discord" class="btn btn-primary">Link Discord</a>
							<div class="text-small-extra text-muted mt-3">Link your Discord account to join the {{"SITE_NAME" | app_config}} Discord server.</div>
							{% endif %}

						  </div>

						</div>

						<div class="body d-lg-flex border-bottom">

							<label for="bio" class="text-black w-lg-25">Steam</label>
							<div class="w-lg-100">
							<?php
								if(!isset($_SESSION['steam_id'])){
									loginbutton("rectangle"); //display login button
								}
								else 
								{
									logoutbutton(); //display logout button
								}
							?>
							</div>
						</div>
					  </div>



					<div class="card-blank rounded">
						<div class="card-header">
							<h2 class="h5" name="referral">RSS Feed</h2>
							<p class="text-small text-muted">Subscribe to the {{"SITE_NAME" | app_config}} RSS feed.</p>
						</div>
						<div class="d-lg-flex">

							<div class="body w-lg-100">

								<input type="text" readonly="" class="form-control copy-link" id="rss_feed" value="{{('/rss/hot/all') | full_link}}" data-clipboard-text="{{('/rss/hot/all') | full_link}}">

								<div class="text-small-extra text-muted mt-3">You can change the feed by replacing "hot" with whatever sorting you want and "all" with whatever time filter you want.</div>

							</div>

						</div>

					</div>

						<div class="card-blank rounded">
							<div class="card-header">
								<h2 class="h5" id="bio" name="bio">Your Profile</h2>
								<p class="text-small text-muted">Edit how others see you on {{"SITE_NAME" | app_config}}.</p>
							</div>
							<div class="body d-lg-flex border-bottom">

								<label for="bio" class="text-black w-lg-25">Username</label>

								<div class="w-lg-100">
									<p>Your original username will always stay reserved for you: <code>{{v.original_username}}</code></p>


									<form action="/settings/name_change" method="post">
										<input type="hidden" name="formkey" value="{{v.formkey}}">
										<input type="text" name="name" class="form-control" value="{{v.username}}">
										<small>3-25 characters, including letters, numbers, _ , and -</small>
										<div class="d-flex mt-2">
											<input class="btn btn-primary ml-auto" type="submit" value="Change Display Name">
										</div>
									</form>
								</div>

							</div>

<!--							<div class="body d-lg-flex border-bottom">

								<label for="bio" class="text-black w-lg-25">Profile Anthem</label>

								<div class="w-lg-100">
									<p>Must be a youtube video link.</p>

									<form action="/settings/song_change" method="post">
										<input type="hidden" name="formkey" value="{{v.formkey}}">
										<input type="text" name="song" class="form-control" value="{% if v.song %}https://youtu.be/{{v.song}}{% endif %}" placeholder='Enter a youtube video link here' >
										<br><small>In some browsers, users have to click at least once anywhere in the profile page for the anthem to play.</small>
										<div class="d-flex mt-2">
											<input class="btn btn-primary ml-auto" type="submit" value="Change Profile Anthem">
										</div>
									</form>
								</div>

							</div>
-->
							<div class="body d-lg-flex border-bottom">

								<label for="bio" class="text-black w-lg-25">Name Color</label>

								<div class="d-flex">

									<form action="/settings/namecolor" id="color-form" method="post" class="color-picker" style="line-height: 0">
											<input type="hidden" name="formkey" value="{{v.formkey}}">

											{% for color in ['ff66ac','805ad5','62ca56','38a169','80ffff','2a96f3','eb4963','ff0000','f39731','30409f','3e98a7','e4432d','7b9ae4','ec72de','7f8fa6', 'f8db58', 'ffffff', 'ff6600', '00007b'] %}
											<input type="radio" name="color" id="color-{{color}}" value="{{color}}" {% if v.namecolor == color %}checked{% endif %} onclick="document.getElementById('color-form').submit()"/>
											<label class="color-radio" for="color-{{color}}">
												<span style="background-color: #{{color}}">
												{% if v.namecolor.lower() == color %}
													<i class="fas fa-check text-white"></i>
												{% else %}
													&nbsp;
												{% endif %}
												</span>
											</label>
											{% endfor %}

									</form>

								</div>

							</div>


						<!--	<div class="body d-lg-flex border-bottom">

								<label for="bio" class="text-black w-lg-25">Animated Username</label>

								<div class="w-lg-100">

									<div class="custom-control custom-switch">
										<input type="checkbox" class="custom-control-input" id="animatedname" name="animatedname"{% if v.animatedname%} checked{% endif %} onchange="post_toast('/settings/profile?animatedname='+document.getElementById('animatedname').checked)">
										<label class="custom-control-label" for="animatedname"></label>
									</div>

									<span class="text-small-extra text-muted">Enable animated username (only available to users in the {{"COINS_NAME" | app_config}} leaderboard and patrons)</span>
								</div>

							</div>
						-->

							{% if not v.flairchanged %}
							<div class="body d-lg-flex border-bottom">

								<label for="bio" class="text-black w-lg-25">Flair</label>

								<div class="w-lg-100">

									<form id="profile-settings" action="/settings/title_change" method="post">
										<input type="hidden" name="formkey" value="{{v.formkey}}">
										<input id="customtitlebody" type="text" name="title" class="form-control" placeholder='Enter a flair here' value="{% if v.customtitleplain %}{{v.customtitleplain}}{% endif %}">
										<div class="d-flex mt-2">
											<small class="format"><i class="btn btn-secondary format d-inline-block m-0 fas fa-smile-beam" onclick="loadEmojis('customtitlebody')" aria-hidden="true" data-toggle="modal" data-target="#emojiModal" data-toggle="tooltip" data-placement="bottom"  title="Add Emoji"></i></small>
											&nbsp;&nbsp;&nbsp;
											<small>Limit of 100 characters</small>
											<input class="btn btn-primary ml-auto" id="titleSave" type="submit" value="Change Flair">
										</div>
									</form>
								</div>

							</div>
							{% endif %}

							<div class="body d-lg-flex border-bottom">

							 <label for="bio" class="text-black w-lg-25">Flair Color</label>

							<div class="d-flex">

								 <form action="/settings/titlecolor" id="titlecolor-form" method="post" class="color-picker" style="line-height: 0">
										<input type="hidden" name="formkey" value="{{v.formkey}}">

										{% for titlecolor in ['ff66ac','805ad5','62ca56','38a169','80ffff','2a96f3','eb4963','ff0000','f39731','30409f','3e98a7','e4432d','7b9ae4','ec72de','7f8fa6', 'f8db58', 'ffffff', 'ff6600', '00007b'] %}
										<input type="radio" name="titlecolor" id="titlecolor-{{titlecolor}}" value="{{titlecolor}}" {% if v.titlecolor == titlecolor %}checked{% endif %} onclick="document.getElementById('titlecolor-form').submit()"/>
										<label class="color-radio" for="titlecolor-{{titlecolor}}">
											<span style="background-color: #{{titlecolor}}">
											{% if v.titlecolor.lower() == titlecolor %}
												<i class="fas fa-check text-white"></i>
											{% else %}
												&nbsp;
											{% endif %}
											</span>
										</label>
										{% endfor %}

								</form>

							</div>

							</div>

							<div class="body d-lg-flex border-bottom">

								<label for="bio" class="text-black w-lg-25">Bio</label>

								<div class="w-lg-100">


									<form id="profile-bio" action="/settings/profile" method="post">
										<input type="hidden" name="formkey" value="{{v.formkey}}">
										<div class="input-group mb-2">
											<textarea class="form-control rounded" id="bio-text" aria-label="With textarea"
											placeholder="Tell the community a bit about yourself."
											rows="3" name="bio" form="profile-bio" maxlength="1500">{{v.bio}}</textarea>
										</div>

										<div class="d-flex">
											<pre class="btn btn-secondary format d-inline-block m-0 fas fa-bold" aria-hidden="true" onclick="makeBold('bio-text')" data-toggle="tooltip" data-placement="bottom" title="Bold"></pre>
											&nbsp;
											<pre class="btn btn-secondary format d-inline-block m-0 fas fa-italic" aria-hidden="true" onclick="makeItalics('bio-text')" data-toggle="tooltip" data-placement="bottom" title="Italicize"></pre>
											&nbsp;
											<pre class="btn btn-secondary format d-inline-block m-0 fas fa-quote-right" aria-hidden="true" onclick="makeQuote('bio-text')" data-toggle="tooltip" data-placement="bottom" title="Quote"></pre>
											&nbsp;
											<pre style="line-height:1;" class="btn btn-secondary format d-inline-block m-0 font-weight-bolder text-uppercase" onclick="commentForm('bio-text');getGif()" aria-hidden="true" data-toggle="modal" data-target="#gifModal" data-toggle="tooltip" data-placement="bottom" title="Add GIF">GIF</pre>
											&nbsp;
											<pre class="btn btn-secondary format d-inline-block m-0 fas fa-smile-beam" onclick="loadEmojis('bio-text')" aria-hidden="true" data-toggle="modal" data-target="#emojiModal" data-toggle="tooltip" data-placement="bottom" title="Add Emoji"></pre>
											&nbsp;
										</div>

										<pre></pre>

										<div class="d-flex">
											<small>Limit of 1500 characters</small>
											<input class="btn btn-primary ml-auto" id="bioSave" type="submit" value="Save Changes">
										</div>
									</form>
								</div>

							</div>

							<div class="body d-lg-flex border-bottom">
								<label class="text-black w-lg-25">Badges</label>

								<div class="w-lg-100">
									<p>Profile badges show off all of your site achievements. If your badges look not quite up to date, use this tool to refresh them.</p>
									<div class="d-flex">
										<a class="btn btn-primary ml-auto" id="badgeUpdate" href="javascript:void(0)" onclick="post_toast('/settings/badges')">Refresh badges</a>
									</div>

							 </div>

						 </div>
						 </div>
						<div class="card-blank rounded">
							<div class="card-header">
								<h2 class="h5" id="bio" name="bio">Privacy Toggles</h2>
								</div>
						 <div class="body d-lg-flex border-bottom">

							<div class="title w-lg-25">
								<label for="privateswitch">Private Mode</label>
							</div>

							<div class="body w-lg-100">

								<div class="custom-control custom-switch">
									<input type="checkbox" class="custom-control-input" id="privateswitch" name="private"{% if v.is_private%} checked{% endif %} onchange="post_toast('/settings/profile?private='+document.getElementById('privateswitch').checked)">
									<label class="custom-control-label" for="privateswitch"></label>
								</div>

								<span class="text-small-extra text-muted">This will hide your post and comment history from others. We will also ask search engines to not index your profile page. (Your content will still be accessible via direct link.). It will also turn off showing the activity status by default </span>

							</div>

						</div>
						<div class="body d-lg-flex border-bottom">

							<div class="title w-lg-25">
								<label for="activityswitch">Show Activity Status</label>
							</div>

							<div class="body w-lg-100">

								<div class="custom-control custom-switch">
									<input type="checkbox" class="custom-control-input" id="activityswitch" name="activity"{% if v.show_activity%} checked{% endif %} onchange="post_toast('/settings/profile?activity='+document.getElementById('activityswitch').checked)">
									<label class="custom-control-label" for="activityswitch"></label>
								</div>

								<span class="text-small-extra text-muted">This will hide your online status (green dot next to the username)</span>

							</div>

						</div>
						 <div class="body d-lg-flex border-bottom">

							<div class="title w-lg-25">
								<label for="nofollowswitch">Disable Subscriptions</label>
							</div>

							<div class="body w-lg-100">

								<div class="custom-control custom-switch">
									<input type="checkbox" class="custom-control-input" id="nofollowswitch" name="nofollow"{% if v.is_nofollow%} checked{% endif %} onchange="post_toast('/settings/profile?nofollow='+document.getElementById('nofollowswitch').checked)">
									<label class="custom-control-label" for="nofollowswitch"></label>
								</div>

								<span class="text-small-extra text-muted">Prevent other users from following you.</span>

							</div>

						</div>
						</div>
					</div>
					</div>

				</div>

		</div>

	</div>

</div>

</div>

{% endblock %}
