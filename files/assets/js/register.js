function register_text_expands(){
	var textexpands = document.getElementsByClassName('text-expand')

	for(var i = 0; i < textexpands.length; i++){
		textexpands[i].addEventListener('click', function(event){
			if (event.which != 1) {
				return
			};
			id=this.dataset.id;
			
			document.getElementById('post-text-'+id).classList.toggle('d-none');
			document.getElementsByClassName('text-expand-icon-'+id).classList.toggle('fa-expand-alt');
			document.getElementsByClassName('text-expand-icon-'+id).classList.toggle('fa-compress-alt');
			
		}, false)
	}
}

function register_votes() {
	var upvoteButtons = document.getElementsByClassName('upvote-button')
	
	var voteDirection = 0
	
	for (var i = 0; i < upvoteButtons.length; i++) {
		upvoteButtons[i].addEventListener('click', upvote, false);
		upvoteButtons[i].addEventListener('keydown', function(event) {
			if (event.keyCode === 13) {
				upvote(event)
			}
		}, false)
	};
}

function register_image_expands(){
	var imageexpands = document.getElementsByClassName('expandable-image')
	for(var i = 0; i < imageexpands.length; i++){
		imageexpands[i].addEventListener('click', function(event) {
	if (event.which != 1) {
		return
	}
	event.preventDefault();
	
	var url= this.data('url');
	
	expandDesktopImage(url,url);
	})}

}
document.addEventListener("DOMContentLoaded", function(){
	boxes = document.getElementsByTagName('textarea')
	for(i = 0; i < boxes.length; i+=1){
		boxes[i].addEventListener('keydown', function(e) {
			if (e.key == 'Tab') {
				e.preventDefault();
				var start = this.selectionStart;
				var end = this.selectionEnd;
				
				// set textarea value to: text before caret + tab + text after caret
				this.value = this.value.substring(0, start) +
				"\t" + this.value.substring(end);
				
				// put caret at right position again
				this.selectionStart =
				this.selectionEnd = start + 1;
			}
		});
	}
});


document.addEventListener("DOMContentLoaded", function(){
	var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
	tooltipTriggerList.map(function(element){
		return new bootstrap.Tooltip(element);
	});
});
