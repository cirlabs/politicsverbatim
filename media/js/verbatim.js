$(document).ready(function() {
	$('#more-tweets').click(function() {
		$('#tweet-rail').animate({height: $('#tweet-rail ul').height() - 6, overflow:'visible'}, 800, 'linear');
	});
});
