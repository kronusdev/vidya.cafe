// Post edit form

function togglePostEdit(id){
	
	body=document.getElementById("post-body");
	title=document.getElementById("post-title");
	form=document.getElementById("edit-post-body-"+id);
	box=document.getElementById("post-edit-box-"+id);
	box2=document.getElementById("post-edit-box2-"+id);
	
	body.classList.toggle("d-none");
	title.classList.toggle("d-none");
	form.classList.toggle("d-none");
	autoExpand(box);
	autoExpand(box2);
}; 

// Flag Submission

report_postModal = function(id, author) {
	
	document.getElementById("post-author").textContent = author;
	
	submitbutton=document.getElementById("reportPostButton");
	
	submitbutton.onclick = function() {
		
		this.innerHTML='<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Reporting post';
		this.disabled = true;
		
		var xhr = new XMLHttpRequest();
		xhr.open("POST", '/flag/post/'+id, true);
		var form = new FormData()
		form.append("formkey", formkey());
		form.append("reason", document.getElementById("reason").value);
		
		xhr.withCredentials=true;
		
		xhr.onload=function() {
			document.getElementById("reportPostFormBefore").classList.add('d-none');
			document.getElementById("reportPostFormAfter").classList.remove('d-none');
		};
		
		xhr.onerror=function(){alert(errortext)};
		xhr.send(form);
		
	}
};
document.addEventListener("DOMContentLoaded", function(){
	document.getElementById('reportPostModal').addEventListener('hidden.bs.modal', function () {
		
		var button = document.getElementById("reportPostButton");
		
		var beforeModal = document.getElementById("reportPostFormBefore");
		var afterModal = document.getElementById("reportPostFormAfter");
		
		button.innerHTML='Report post';
		button.disabled= false;
		
		afterModal.classList.add('d-none');
		
		if ( beforeModal.classList.contains('d-none') ) {
			beforeModal.classList.remove('d-none');
		}
		
	});
})
