// fix for links
$(document).on('click', 'a.disabled', function(event) {
	event.preventDefault();
	return false;
});

$(document).on('click', 'li.disabled > a', function(event) {
	event.preventDefault();
});