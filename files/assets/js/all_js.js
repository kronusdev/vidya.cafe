// Using mouse

document.body.addEventListener('mousedown', function() {
	document.body.classList.add('using-mouse');
});

document.body.addEventListener('keydown', function(event) {
	if (event.keyCode === 9) {
		document.body.classList.remove('using-mouse');
	}
});

//GIFS

	// Identify which comment form to insert GIF into

	var commentFormID;

	function commentForm(form) {
		commentFormID = form;
	};


	// Insert EMOJI markdown into comment box function

	function getEmoji(searchTerm, form) {

		var emoji = ' :'+searchTerm+': '
			
		var commentBox = document.getElementById(form);

		var old	= commentBox.value;

		commentBox.value = old + emoji;

	}

	function loadEmojis(form, isUpdate) {

		const emojis = [
		{
			type:'classic',
			emojis: ['dollar', '2thumbsup', 'thumbsup','aliendj','ambulance','angry','angrywhip','argue','aroused','ashamed','badass','banana', 'birthday', 'band','banghead','batman','bigeyes','bite','blind','blowkiss','blush','bong','bounce','bow','breakheart','bs','cartwheel','cat','celebrate','chainsaw','cheers','clap','cold','confused','crazyeyes','cry','cthulhu','cute','D','daydream','ddr','deadpool','devilsmile','diddle','die','distress','disturbing','dizzy','domo','doughboy','drink','drool','dudeweedlmao','edward','electro','elephant','embarrassed','emo','emo2','evil','evilclown','evilgrin','facepalm','fap','flamethrower','flipbird','flirt','frown','gasp','glomp','go','gooby','grr','gtfo','guitar','haha','handshake','happydance','headbang','heart','heartbeat','hearts','highfive','hmm','hmph','holdhands','horny', 'awooga', 'hug','hugging','hugs','hump','humpbed','hysterical','ily','inlove','jason','jawdrop','jedi','jester','kaboom','kick','kiss','kitty','laughchair','lick','link','lol','lolbeat','loving','makeout','medal','megaman','megamanguitar','meow','metime','mooning','mummy','na','nauseous','nervous','ninja','nod','nono','omg','onfire','ooo','orly','p','paddle','panda','pandabutt','paranoid','party','pat','peek','pikachu','pimp','plzdie','poke','popcorn','pout','probe','puke','punch','quote','raccoon','roar','rofl','roflmao','rolleyes','sad','sadeyes','sadhug','samurai','sarcasm','scoot','scream','shmoopy','shrug','skull','slap','slapfight','sleepy','smackfish','smackhead','smh','smile','smoke','sonic','spank','sparta','sperm','spiderman','stab','star','stare','stfu','suicide','surprisehug','suspicious','sweat','swordfight','taco','talk2hand','tantrum','teehee','lurk', 'thinking','threesome','throw','throwaway','tickle','typing', 'computerpunch','uhuh','vampbat','viking','violin','vulgar','wah','wat','whip','whipping','wink','witch','wizard','woah','worm','woo','work','worship','wow','XD','yay','zzz']
		},
		{
			type:'marsey',
			emojis: ['marseylong1', 'marseylong2', 'marseylong3', 'marseyjam','marseyhmm','marseyhmmm','marseythonk',
					 'marseyworried','marseysus','marsey4chan','marseyandmarcus','marseybluecheck','marseybong','marseybooba',
					 'marseyconfused','marseydespair','marseylizard','marseyowow','marseyproctologist','marseyvaxmaxx','marseyxd',
					 'marsoyhype','marmsey','marsey1984','marseyakshually','marseycope','marseydeux','marseydoomer','marseyflamewar',
					 'marseyfug','marseygasp','marseyglow','marseyhacker','marseyking','marseylifting','marseymanlet','marseymouse',
					 'marseynpc','marseypainter','marseypeacekeeper','marseypickle','marseypipe','marseypirate','marseypope','marseyrat',
					 'marseyrick','marseyseethe','marseysneed','marseytroll','marsoy','marseyasian','marseyburger','marseyfacepalm',
					 'marseygrilling','marseyjanny','marseyrentfree','marseyretard','marseysadcat','marseysick','marseysmug', 'marseysipping',
					 'marseyjamming','marseyangel','marseyblowkiss','marseycry','marseydead','marseyexcited','marseygift','marseyinabox',
					 'marseylaugh','marseylove','marseymad','marseyparty','marseyrain','marseyreading','marseyready','marseysad','marseyscarf',
					 'marseyshook','marseysleep','marseythumbsup','marseywave', 'marsey69', 'marseynut', 'marseyglam', 'marseycowboy', 'marseypat',
					 'marseypanties', 'marseybingus', 'marseydepressed', 'marseyagree', 'marseybane', 'marseyboomer', 'marseybux', 'marseycapy',
					 'marseycool', 'marseydisagree', 'marseydragon', 'marseyghost', 'marseygivecrown', 'marseyjapanese', 'marseynightmare', 'marseyno', 'marseynooo',
					 'marseyoctopus', 'marseypanda', 'marseypenguin', 'marseypretty', 'marseypumpking', 'marseyrage', 'marseyramen', 'marseyshark', 'marseyskeletor',
					 'marseysmirk', 'marseysombrero', 'marseyspirit', 'marseystars', 'marseystein', 'marseysweating', 'marseytwerking', 'marseyvampire', 'marseyvaporwave',
					 'marseyvibing', 'marseywarhol', 'marseywinner', 'marseywise', 'marseywolf', 'marseywtf', 'marseywut', 'marseyyawn', 'marseyyes', 'marseyyikes', 'marseyzombie', 'marseyzwei',
					 'marseychristmasbulb', 'marseyelf', 'marseyreindeer', 'marseyreindeer2', 'marseyreindeer3', 'marseysanta', 'marseysanta2', 'marseysnow', 'marseysnowman']
		},
		{
			type:'rage',
			emojis: ['troll','bitchplease','cerealguypart2','challengeaccepted','contentiouscereal','cryingatcuteness',
			'derp','derpcornsyrup','derpcrying','derpcute','derpdumb','derpeuphoria','derpinahd','derpinapokerface','derpinasnickering',
			'derpprocessing','derprealization','derpsnickering','derptalking','derpthinking','derpthumbsup','derpunimpressed','derpwhy',
			'donotwant','epicfacefeatures','fancywithwine','fffffffuuuuuuuuuuuu','flipthetable','foreveralone','foreveralonehappy','hewillnever',
			'idontknow','interuptedreading','iseewhatyoudidthere','killherkillher','ledesire','leexcited','legenius','lelolidk','lemiddlefinger',
			'lemindblown','leokay','lepanicrunning','lepokerface','lepokerface2','lerageface','leseriousface','likeaboss','lolface','longwhiskers',
			'manymiddlefingers','megusta','motherfucker','motherofgod','mysides','ohgodwhy','pervertedspiderman','picard','ragestrangle','rukiddingme',
			'tfwyougettrolled','trollolol','truestorybro','xallthey']
		},
		{
			type:'pepe',
			emojis: ['peepopog','peepojam','peepoknife','peepoking','peepodrink','peepolook','peepopeek','peepolove','peepopet','peepopoggers','peepocool','peepohappy','peepoclap','peepocross','peepowholesome','peepoblanket','peepoface','peepopogchamp','peepowtf','peepoyes','peepoascended','peepothink','peepocoffe','peepocoffe2']
		}
		]
		let search_bar = document.getElementById("emoji_search");
		let search_container = document.getElementById('emoji-tab-search')

		if(search_bar.value == ""){
			for (i=0; i < emojis.length; i++) {

				let container = document.getElementById(`EMOJIS_${emojis[i].type}`)
				let str = ''
				let arr = emojis[i].emojis

				for (j=0; j < arr.length; j++) {
					if(arr[j].match(search_bar.value)){
						str += `<button class="button m-1 px-0" onclick="getEmoji(\'${arr[j]}\', \'${form}\')" style="width:60px; overflow: hidden;" data-bs-toggle="tooltip" title=":${arr[j]}:" delay:="0"><img width=50 src="/assets/images/emojis/${arr[j]}.gif" alt="${arr[j]}-emoji"/></button>`;
					}
				}

				container.innerHTML = str
				search_container.innerHTML = ""
			}
		}else{
		 	let str = ''
		 	for (i=0; i < emojis.length; i++) {
		 		let arr = emojis[i].emojis
				let container = document.getElementById(`EMOJIS_${emojis[i].type}`)
		 		for (j=0; j < arr.length; j++) {
		 			if(arr[j].match(search_bar.value.toLowerCase())){
		 			str += `<button class="button m-1 px-0" onclick="getEmoji(\'${arr[j]}\', \'${form}\')" style="width:60px; overflow: hidden;" data-bs-toggle="tooltip" title=":${arr[j]}:" delay:="0"><img width=50 src="/assets/images/emojis/${arr[j]}.gif" alt="${arr[j]}-emoji"/></button>`;
		 			}
		 		}
				container.innerHTML = ""
		 	}
		 	search_container.innerHTML = str
		}
		search_bar.oninput = function(){loadEmojis(form, true);};
	}


	function getGif(searchTerm) {

		if (searchTerm !== undefined) {
			document.getElementById('gifSearch').value = searchTerm;
		}
		else {
			document.getElementById('gifSearch').value = null;
		}

			// load more gifs div
			var loadGIFs = document.getElementById('gifs-load-more');

			// error message div
			var noGIFs = document.getElementById('no-gifs-found');

			// categories div
			var cats = document.getElementById('GIFcats');

			// container div
			var container = document.getElementById('GIFs');

			// modal body div
			var modalBody = document.getElementById('gif-modal-body')

			// UI buttons
			var backBtn = document.getElementById('gifs-back-btn');
// 			var cancelBtn = document.getElementById('gifs-cancel-btn');

			container.innerHTML = '';

			if (searchTerm == undefined) {
				container.innerHTML = '<div class="card" onclick="getGif(\'agree\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Agree</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/wGhYz3FHaRJgk/200w_d.gif"> </div> <div class="card" onclick="getGif(\'laugh\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Laugh</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/O5NyCibf93upy/200w_d.gif"> </div> <div class="card" onclick="getGif(\'confused\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Confused</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/3o7btPCcdNniyf0ArS/200w_d.gif"> </div> <div class="card" onclick="getGif(\'sad\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Sad</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/ISOckXUybVfQ4/200w_d.gif"> </div> <div class="card" onclick="getGif(\'happy\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Happy</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/XR9Dp54ZC4dji/200w_d.gif"> </div> <div class="card" onclick="getGif(\'awesome\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Awesome</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/3ohzdIuqJoo8QdKlnW/200w_d.gif"> </div> <div class="card" onclick="getGif(\'yes\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Yes</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/J336VCs1JC42zGRhjH/200w_d.gif"> </div> <div class="card" onclick="getGif(\'no\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">No</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/1zSz5MVw4zKg0/200w_d.gif"> </div> <div class="card" onclick="getGif(\'love\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Love</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/4N1wOi78ZGzSB6H7vK/200w_d.gif"> </div> <div class="card" onclick="getGif(\'please\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Please</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/qUIm5wu6LAAog/200w_d.gif"> </div> <div class="card" onclick="getGif(\'scared\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Scared</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/bEVKYB487Lqxy/200w_d.gif"> </div> <div class="card" onclick="getGif(\'angry\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Angry</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/12Pb87uq0Vwq2c/200w_d.gif"> </div> <div class="card" onclick="getGif(\'awkward\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Awkward</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/unFLKoAV3TkXe/200w_d.gif"> </div> <div class="card" onclick="getGif(\'cringe\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Cringe</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/1jDvQyhGd3L2g/200w_d.gif"> </div> <div class="card" onclick="getGif(\'omg\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">OMG</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/3o72F8t9TDi2xVnxOE/200w_d.gif"> </div> <div class="card" onclick="getGif(\'why\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Why</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/1M9fmo1WAFVK0/200w_d.gif"> </div> <div class="card" onclick="getGif(\'gross\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Gross</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/pVAMI8QYM42n6/200w_d.gif"> </div> <div class="card" onclick="getGif(\'meh\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #ffffff;font-weight: bold;">Meh</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/xT77XTpyEzJ4OJO06c/200w_d.gif"> </div>'
				backBtn.innerHTML = null;
// 				cancelBtn.innerHTML = null;
				noGIFs.innerHTML = null;
				loadGIFs.innerHTML = null;
			} else {
				backBtn.innerHTML = '<button class="btn btn-link pl-0 pr-3" id="gifs-back-btn" onclick="getGif();"><i class="fas fa-long-arrow-left text-muted"></i></button>';

// 				cancelBtn.innerHTML = '<button class="btn btn-link pl-3 pr-0" id="gifs-cancel-btn" onclick="getGif();"><i class="fas fa-times text-muted"></i></button>';

				let gifs = [];
				let apiKey = tenor_api_key();
				let lmt = 25;
				let url = "https://g.tenor.com/v1/search/?q=" + searchTerm + "&key=" + apiKey + "&limit=" + lmt;
				fetch(url)
				.then(response => {
					return response.json();
				})
				.then(json => {
					let results = json.results.map(function(obj) {
						return {
							id: obj.id,
							preview: obj.media[0].tinygif.url,
							url: obj.media[0].gif.url,
							source: obj.url,
							bgColor: obj.bg_color
						}
					});
					
					gifs = results

					// loop for fetching mutliple GIFs and creating the card divs
					if (gifs.length) {
						for (var i = 0; i < gifs.length; i++) {
							container.innerHTML += ('<div class="card bg-white" style="overflow: hidden" data-bs-dismiss="modal" aria-label="Close" onclick="insertGIF(\'' + gifs[i].url + '\',\'' + commentFormID + '\')"><div class="gif-cat-overlay"></div><img class="img-fluid" src="' + gifs[i].preview + '"></div>');
							noGIFs.innerHTML = null;
							loadGIFs.innerHTML = '<div class="text-center py-3"><div class="mb-3"><i class="fad fa-grin-beam-sweat text-primary" style="font-size: 3.5rem;"></i></div><p class="font-weight-bold text-black mb-0">Thou&#39;ve reached the end of the list!</p></div>';
						}
					} else {
						noGIFs.innerHTML = '<div class="text-center py-3 mt-3"><div class="mb-3"><i class="fad fa-frown text-primary" style="font-size: 3.5rem;"></i></div><p class="font-weight-bold text-black mb-0">Aw shucks. No GIFs found...</p></div>';
						container.innerHTML = null;
						loadGIFs.innerHTML = null;
					}
				})
				.catch(err => alert(err));
			};
		}
	// Insert GIF markdown into comment box function

	function insertGIF(url,form) {

		var gif = "![](" + url +")";

		var commentBox = document.getElementById(form);

		var old	= commentBox.value;

		commentBox.value = old + gif;

	}

	// When GIF keyboard is hidden, hide all GIFs TODO-fix (what's .on) or remove

// 	document.getElementById('gifModal').on('hidden.bs.modal', function (e) {
// 
// 		document.getElementById('gifSearch').value = null;
// 
// 		// load more gifs div
// 
// 		var loadGIFs = document.getElementById('gifs-load-more');
// 
// 		// no GIFs div
// 
// 		var noGIFs = document.getElementById('no-gifs-found');
// 
// 		// container div
// 
// 		var container = document.getElementById('GIFs');
// 
// 		// UI buttons
// 
// 		var backBtn = document.getElementById('gifs-back-btn');
// 
// 		var cancelBtn = document.getElementById('gifs-cancel-btn');
// 
// 		// Remove inner HTML from container var
// 
// 		container.innerHTML = '<div class="card" onclick="getGif(\'agree\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Agree</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/wGhYz3FHaRJgk/200w_d.gif"> </div> <div class="card" onclick="getGif(\'laugh\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Laugh</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/O5NyCibf93upy/200w_d.gif"> </div> <div class="card" onclick="getGif(\'confused\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Confused</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/3o7btPCcdNniyf0ArS/200w_d.gif"> </div> <div class="card" onclick="getGif(\'sad\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Sad</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/ISOckXUybVfQ4/200w_d.gif"> </div> <div class="card" onclick="getGif(\'happy\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Happy</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/XR9Dp54ZC4dji/200w_d.gif"> </div> <div class="card" onclick="getGif(\'awesome\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Awesome</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/3ohzdIuqJoo8QdKlnW/200w_d.gif"> </div> <div class="card" onclick="getGif(\'yes\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Yes</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/J336VCs1JC42zGRhjH/200w_d.gif"> </div> <div class="card" onclick="getGif(\'no\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">No</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/1zSz5MVw4zKg0/200w_d.gif"> </div> <div class="card" onclick="getGif(\'love\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Love</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/4N1wOi78ZGzSB6H7vK/200w_d.gif"> </div> <div class="card" onclick="getGif(\'please\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Please</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/qUIm5wu6LAAog/200w_d.gif"> </div> <div class="card" onclick="getGif(\'scared\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Scared</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/bEVKYB487Lqxy/200w_d.gif"> </div> <div class="card" onclick="getGif(\'angry\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Angry</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/12Pb87uq0Vwq2c/200w_d.gif"> </div> <div class="card" onclick="getGif(\'awkward\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Awkward</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/unFLKoAV3TkXe/200w_d.gif"> </div> <div class="card" onclick="getGif(\'cringe\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Cringe</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/1jDvQyhGd3L2g/200w_d.gif"> </div> <div class="card" onclick="getGif(\'omg\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">OMG</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/3o72F8t9TDi2xVnxOE/200w_d.gif"> </div> <div class="card" onclick="getGif(\'why\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Why</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/1M9fmo1WAFVK0/200w_d.gif"> </div> <div class="card" onclick="getGif(\'gross\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Gross</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/pVAMI8QYM42n6/200w_d.gif"> </div> <div class="card" onclick="getGif(\'meh\');" style="overflow: hidden;"> <div class="gif-cat-overlay"> <div style="position: relative;top: 50%;transform: translateY(-50%);color: #cfcfcf;font-weight: bold;">Meh</div> </div> <img class="img-fluid" src="https://media.giphy.com/media/xT77XTpyEzJ4OJO06c/200w_d.gif"> </div>'
// 
// 		// Hide UI buttons
// 
// 		backBtn.innerHTML = null;
// 
// 		cancelBtn.innerHTML = null;
// 
// 		// Remove inner HTML from no gifs div
// 
// 		noGIFs.innerHTML = null;
// 
// 		// Hide no more gifs div
// 
// 		loadGIFs.innerHTML = null;
// 
// 	});


//iOS webapp stuff

(function(document,navigator,standalone) {
						// prevents links from apps from oppening in mobile safari
						// this javascript must be the first script in your <head>
						if ((standalone in navigator) && navigator[standalone]) {
							var curnode, location=document.location, stop=/^(a|html)$/i;
							document.addEventListener('click', function(e) {
								curnode=e.target;
								while (!(stop).test(curnode.nodeName)) {
									curnode=curnode.parentNode;
								}
										// Condidions to do this only on links to your own app
										// if you want all links, use if('href' in curnode) instead.
										if('href' in curnode && ( curnode.href.indexOf('http') || ~curnode.href.indexOf(location.host) ) ) {
											e.preventDefault();
											location.href = curnode.href;
										}
									},false);
						}
					})(document,window.navigator,'standalone');






// Search Icon
// Change navbar search icon when form is in focus, active states
// TODO - can get rid of this question mark?
// $(".form-control").focus(function () {
// 	$(this).prev('.input-group-append').removeClass().addClass('input-group-append-focus');
// 	$(this).next('.input-group-append').removeClass().addClass('input-group-append-focus');
// });
// 
// $(".form-control").focusout(function () {
// 	$(this).prev('.input-group-append-focus').removeClass().addClass('input-group-append');
// 	$(this).next('.input-group-append-focus').removeClass().addClass('input-group-append');
// });
// 
// //spinner effect
// 
// $(document).ready(function() {
// 	$('#login').submit(function() {
// 			// disable button
// 			$("#login_button").prop("disabled", true);
// 			// add spinner to button
// 			$("#login_button").html('<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Signing in');
// 		});
// });
// 
// $(document).ready(function() {
// 	$('#signup').submit(function() {
// 			// disable button
// 			$("#register_button").prop("disabled", true);
// 			// add spinner to button
// 			$("#register_button").html('<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Registering');
// 		});
// });
// 
// 
// $('.mention-user').click(function (event) {
// 
// 	if (event.which != 1) {
// 		return
// 	}
// 
// 	event.preventDefault();
// 
// 	window.location.href='/@' + $(this).data('original-name');
// 
// });
