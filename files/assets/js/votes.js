function upvote(event) {
	
	var type = event.target.dataset.contentType;
	var id = event.target.dataset.idUp;
	
	var upvoteButton = document.getElementsByClassName(type + '-' + id + '-up');
	var scoreText = document.getElementsByClassName(type + '-score-' + id);
	
	for (var j = 0; j < upvoteButton.length  && j < scoreText.length; j++) {
		
		var thisUpvoteButton = upvoteButton[j];
		var thisScoreText = scoreText[j];
		var thisScore = Number(thisScoreText.textContent);
		
		if (thisUpvoteButton.classList.contains('active')) {
			thisUpvoteButton.classList.remove('active')
			thisScoreText.textContent = thisScore - 1
			voteDirection = "0"
		} else {
			thisUpvoteButton.classList.add('active')
			thisScoreText.textContent = thisScore + 1
			voteDirection = "1"
		}
		
		if (thisUpvoteButton.classList.contains('active')) {
			thisScoreText.classList.add('score-up')
			thisScoreText.classList.remove('score')
		} else {
			thisScoreText.classList.add('score')
			thisScoreText.classList.remove('score-up')	
		}
	}
	
	post_toast("/vote/" + type + "/" + id + "/" + voteDirection);
	
}

