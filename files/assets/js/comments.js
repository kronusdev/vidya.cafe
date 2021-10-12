function post_comment(fullname){
	var form = new FormData();
	
	form.append('formkey', formkey());
	form.append('parent_fullname', fullname);
	form.append('submission', document.getElementById('reply-form-submission-'+fullname).value);
	form.append('body', document.getElementById('reply-form-body-'+fullname).value);
	form.append('file', document.getElementById('file-upload-reply-'+fullname).files[0]);
	var xhr = new XMLHttpRequest();
	xhr.open("post", "/comment");
	xhr.withCredentials=true;
	xhr.onload=function(){
		if (xhr.status==200) {
			commentForm=document.getElementById('comment-form-space-'+fullname);
			commentForm.innerHTML = JSON.parse(xhr.response.replace(/data-src/g, 'src'))['html'];
// 			commentForm=document.getElementById('comment-text-'+id);
// 			commentForm.innerHTML=JSON.parse(xhr.response)["html"];
// 			document.getElementById('cancel-edit-'+id).click()
// 			
// 			var successToast = bootstrap.Toast(document.getElementById('toast-comment-success'))
// 			successToast.show()
			
		}
		else {
			var myToast = new bootstrap.Toast(document.getElementById('toast-post-success'));
			myToast.hide();
			var myToast = new bootstrap.Toast(document.getElementById('toast-post-error'));
			myToast.show();
			document.getElementById("comment-error-text").textContent = "Error. Please try again later.";
		}
	}
	xhr.send(form)
	
	document.getElementById('save-reply-to-'+fullname).classList.add('disabled');
	
}

function herald_comment(cid){

	var xhr = new XMLHttpRequest();
	xhr.open("post", "/admin/distinguish_comment/"+cid);
	
	var form = new FormData();
	
	form.append('formkey', formkey());
	
	xhr.withCredentials=true;
	xhr.onload=function(){
		if (xhr.status==200) {
			comment=document.getElementById('comment-'+cid+'-only');
			comment.innerHTML=JSON.parse(xhr.response)["html"];
		}
		else {
			var commentError = document.getElementById("comment-error-text");
			document.getElementById('toast-comment-success').toast('dispose');
			document.getElementById('toast-comment-error').toast('dispose');
			document.getElementById('toast-comment-error').toast('show');
			commentError.textContent = JSON.parse(xhr.response)["error"];
		}
	}
	xhr.send(form)
	
}

function comment_edit(id){
	
	var commentError = document.getElementById("comment-error-text");
	
	var form = new FormData();
	
	form.append('formkey', formkey());
	form.append('body', document.getElementById('comment-edit-body-'+id).value);
	form.append('file', document.getElementById('file-edit-reply-'+id).files[0]);
	
	var xhr = new XMLHttpRequest();
	xhr.open("post", "/edit_comment/"+id);
	xhr.withCredentials=true;
	xhr.onload=function(){
		if (xhr.status==200 || xhr.status==204) {
			commentForm=document.getElementById('comment-text-'+id);
			commentForm.innerHTML=JSON.parse(xhr.response)["html"];
			document.getElementById('cancel-edit-'+id).click()
			//$('#toast-comment-success').toast('dispose');
			//$('#toast-comment-error').toast('dispose');
			//$('#toast-comment-success').toast('show');
			var successToast = bootstrap.Toast(document.getElementById('toast-comment-success'))
			successToast.show()
		}
		else {
			//$('#toast-comment-success').toast('dispose');
			//$('#toast-comment-error').toast('dispose');
			//$('#toast-comment-error').toast('show');
			var errorToast = bootstrap.Toast(document.getElementById('toast-comment-error'))
			errorToast.show()
			commentError.textContent = JSON.parse(xhr.response)["error"];
		}
	}
	xhr.send(form)
	
} 

// Toggle comment collapse

function collapse_comment(comment_id) {
	
	var comment = "comment-" + comment_id;
	
	document.getElementById(comment).classList.toggle("collapsed");
	
};

// Comment edit form

function toggleEdit(id){
	comment=document.getElementById("comment-text-"+id);
	form=document.getElementById("comment-edit-"+id);
	box=document.getElementById('edit-box-comment-'+id);
	actions = document.getElementById('comment-' + id +'-actions');
	
	comment.classList.toggle("d-none");
	form.classList.toggle("d-none");
	actions.classList.toggle("d-none");
	autoExpand(box);
};

//comment modding
function removeComment(post_id) {
	url="/ban_comment/"+post_id
	
	callback=function(){
		document.getElementById("comment-"+post_id+"-only").classList.add("banned");
		
		button=document.getElementById("moderate-"+post_id);
		button.onclick=function(){approveComment(post_id)};
		button.innerHTML='<i class="fas fa-clipboard-check"></i>Approve'
	}
	post(url, callback, "Comment has been removed.")
};

function approveComment(post_id) {
	url="/unban_comment/"+post_id
	
	callback=function(){
		document.getElementById("comment-"+post_id+"-only").classList.remove("banned");
		
		button=document.getElementById("moderate-"+post_id);
		button.onclick=function(){removeComment(post_id)};
		button.innerHTML='<i class="fas fa-trash-alt"></i>Remove'
	}
	
	post(url, callback, "Comment has been approved.")
}

function admin_comment(cid){
	
	
	var xhr = new XMLHttpRequest();
	xhr.open("post", "/distinguish_comment/"+cid);
	
	var form = new FormData();
	
	form.append('formkey', formkey());
	
	xhr.withCredentials=true;
	xhr.onload=function(){
		if (xhr.status==200) {
			comment=document.getElementById('comment-'+cid+'-only');
			comment.innerHTML=JSON.parse(xhr.response)["html"];
		}
		else {
			var commentError = document.getElementById("comment-error-text");
			$('#toast-comment-success').toast('dispose');
			$('#toast-comment-error').toast('dispose');
			$('#toast-comment-error').toast('show');
			commentError.textContent = JSON.parse(xhr.response)["error"];
		}
	}
	xhr.send(form)
}

// Flag Comment

function report_commentModal(id, author) {
	
	document.getElementById("comment-author").textContent = author;
	
	//offtopic.disabled=true;
	
	document.getElementById("reportCommentButton").onclick = function() {
		
		this.innerHTML='<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Reporting comment';
		this.disabled = true;
		var xhr = new XMLHttpRequest();
		xhr.open("POST", '/flag/comment/'+id, true);
		var form = new FormData()
		form.append("formkey", formkey());
		form.append("reason", document.getElementById("reason-comment").value);
		
		xhr.withCredentials=true;
		
		xhr.onload=function() {
			document.getElementById("reportCommentFormBefore").classList.add('d-none');
			document.getElementById("reportCommentFormAfter").classList.remove('d-none');
		};
		
		xhr.onerror=function(){alert(errortext)};
		xhr.send(form);
	}
	
};

document.getElementById('reportCommentModal').on('hidden.bs.modal', function () {
	
	var button = document.getElementById("reportCommentButton");
	
	var beforeModal = document.getElementById("reportCommentFormBefore");
	var afterModal = document.getElementById("reportCommentFormAfter");
	
	button.innerHTML='Report comment';
	button.disabled= false;
	afterModal.classList.add('d-none');
	
	if ( beforeModal.classList.contains('d-none') ) {
		beforeModal.classList.remove('d-none');
	}
	
});
