//email change

// Show confirm password field when user clicks email box
document.addEventListener("DOMContentLoaded", function(){
	document.getElementById('new_email').addEventListener('input', function () {

		var id = document.getElementById("email-password");
		var id2 = document.getElementById("email-password-label");
		var id3 = document.getElementById("emailpasswordRequired");

		id.classList.remove("d-none");
		id2.classList.remove("d-none");
		id3.classList.remove("d-none");

	});

	// 2FA toggle modal

	document.getElementById('2faModal').addEventListener('hidden.bs.modal', function () {

		var box = document.getElementById("2faToggle");
		
		box.checked = !box.checked;

	});


	//Email verification text

	function emailVerifyText() {

		document.getElementById("email-verify-text").innerHTML = "Verification email sent! Please check your inbox.";

	}
})
