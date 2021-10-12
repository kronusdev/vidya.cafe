//POST

function post(url, callback, errortext) {
	var xhr = new XMLHttpRequest();
	xhr.open("POST", url, true);
	var form = new FormData()
	form.append("formkey", formkey());
	xhr.withCredentials=true;
	xhr.onerror=function() { alert(errortext); };
	xhr.onload = function() {
		if (xhr.status >= 200 && xhr.status < 300) {
			callback();
		} else {
			xhr.onerror();
		}
	};
	xhr.send(form);
};

function post_toast(url, callback) {
	var xhr = new XMLHttpRequest();
	xhr.open("POST", url, true);
	var form = new FormData()
	form.append("formkey", formkey());
	xhr.withCredentials=true;
	
	xhr.onload = function() {
		if (xhr.status==204) {}
		else if (xhr.status >= 200 && xhr.status < 300) {
// 			$('#toast-post-success').toast('dispose');
			var successToast = new bootstrap.Toast(document.getElementById('toast-post-success'));
			successToast.show();
			document.getElementById('toast-post-success-text').innerText = JSON.parse(xhr.response)["message"];
			callback(xhr)
			return true
			
		} else if (xhr.status >= 300 && xhr.status < 400) {
			window.location.href = JSON.parse(xhr.response)["redirect"]
		} else {
			data=JSON.parse(xhr.response);
			
			var successToast = new bootstrap.Toast(document.getElementById('toast-post-error'))
			successToast.show();
			document.getElementById('toast-post-error-text').innerText = data["error"];
			return false
			
		}
	};
	
	xhr.send(form);
	
}

// Mobile bottom navigation bar

window.onload = function () {
	var prevScrollpos = window.pageYOffset;
	window.onscroll = function () {
		var currentScrollPos = window.pageYOffset;
		
		var topBar = document.getElementById("fixed-bar-mobile");
		
		var bottomBar = document.getElementById("mobile-bottom-navigation-bar");
		
		var dropdown = document.getElementById("mobileSortDropdown");
		
		var navbar = document.getElementById("navbar");
		
		if (bottomBar != null) {
			if (prevScrollpos > currentScrollPos && (window.innerHeight + currentScrollPos) < (document.body.offsetHeight - 65)) {
				bottomBar.style.bottom = "0px";
			} 
			else if (currentScrollPos <= 125 && (window.innerHeight + currentScrollPos) < (document.body.offsetHeight - 65)) {
				bottomBar.style.bottom = "0px";
			}
			else if (prevScrollpos > currentScrollPos && (window.innerHeight + currentScrollPos) >= (document.body.offsetHeight - 65)) {
				bottomBar.style.bottom = "-50px";
			}
			else {
				bottomBar.style.bottom = "-50px";
			}
		}
		
		// Execute if bottomBar exists
		
		if (topBar != null && dropdown != null) {
			if (prevScrollpos > currentScrollPos) {
				topBar.style.top = "48px";
				navbar.classList.remove("shadow");
			} 
			else if (currentScrollPos <= 125) {
				topBar.style.top = "48px";
				navbar.classList.remove("shadow");
			}
			else {
				topBar.style.top = "-48px";
				dropdown.classList.remove('show');
				navbar.classList.add("shadow");
			}
		}
		prevScrollpos = currentScrollPos;
	}
}

// tooltips

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
	return new bootstrap.Tooltip(tooltipTriggerEl)
})

// Expand Images on Desktop

function expandDesktopImage(image, link) {
	
	// Link text
	
	var linkText = document.getElementById("desktop-expanded-image-link");
	var imgLink = document.getElementById("desktop-expanded-image-wrap-link");
	
	var inlineImage = document.getElementById("desktop-expanded-image");
	
	inlineImage.src = image.replace("100w.gif", "giphy.gif");
	linkText.href = image;
	imgLink.href=image;
	
	linkText.textContent = 'View original';
};

function block_user() {
	
	var exileForm = document.getElementById("exile-form");
	
	var exileError = document.getElementById("toast-error-message");
	
	var usernameField = document.getElementById("exile-username");
	
	var isValidUsername = usernameField.checkValidity();
	
	username = usernameField.value;
	
	if (isValidUsername) {
		
		var xhr = new XMLHttpRequest();
		xhr.open("post", "/settings/block");
		xhr.withCredentials=true;
		f=new FormData();
		f.append("username", username);
		f.append("formkey", formkey());
		xhr.onload=function(){
			if (xhr.status<300) {
				window.location.reload(true);
			}
			else {
				$('#toast-exile-error').toast('dispose');
				$('#toast-exile-error').toast('show');
				exileError.textContent = JSON.parse(xhr.response)["error"];
			}
		}
		xhr.send(f)
	}
	
}
