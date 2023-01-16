
document.addEventListener('DOMContentLoaded', function(){
	console.log("WOrking")
	const menu = document.querySelector('#mobile-menu');
	const links = document.querySelector('#navigation');

	menu.addEventListener('click', function() {
		console.log("Activate menu")
		menu.classList.toggle('is-active');
		links.classList.toggle('active');
	})

});