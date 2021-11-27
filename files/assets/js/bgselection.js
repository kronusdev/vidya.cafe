function updatebgselection(make_post){
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
			"bg-5",
			"bg-6"
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
			"bg-6",
			"bg-7"
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
		"bg-8"
	]
	}
]
	let bgContainer = document.getElementById(`bgcontainer`);
	let str = '';
	let bgsToDisplay = backgrounds[bgselector.selectedIndex].backgrounds;
	let bgsDir = backgrounds[bgselector.selectedIndex].folder;
	if (make_post == true) {
		for (i=0; i < bgsToDisplay.length; i++) {
			let onclickPost = "/assets/images/custombackgrounds/" + bgsDir + "/" + bgsToDisplay[i];
			str += `<button class="button m-1 p-0" style="width:15rem; overflow: hidden;"><img style="padding:0.25rem; width: 15rem" src="/assets/images/custombackgrounds/${bgsDir}/${bgsToDisplay[i]}" alt="${bgsToDisplay[i]}-background" onclick="post('/settings/profile?background=${onclickPost}', function(){window.location.reload(true);})"/></button>`;
		}
	}else {
		for (i=0; i < bgsToDisplay.length; i++) {
			let onclickPost = "/assets/images/custombackgrounds/" + bgsDir + "/" + bgsToDisplay[i];
			property = `'url(${onclickPost})'`
			
// 			onclick="function(){document.getElementById('frontpage').style.setProperty('background-image', ${property})})
			
			str += `<div onclick="document.getElementById('frontpage').style.setProperty('background-image', ${property}); document.getElementById('bginput').value = '${onclickPost}'" class="button m-1 p-0" style="width:15rem; overflow: hidden;"><img style="padding:0.25rem; width: 15rem" src="/assets/images/custombackgrounds/${bgsDir}/${bgsToDisplay[i]}" alt="${bgsToDisplay[i]}-background"></div>`;
			
		}
	}
	bgContainer.innerHTML = str;
}
function postBgUrl(){
	post('/settings/profile?background_url='+document.getElementById("background_url_field").value, function(){window.location.reload(true);})
}

