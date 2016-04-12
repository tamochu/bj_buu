$(function() {
	$("form").on('submit', function(){
		$(this).find('input:submit').attr('disabled', 'disabled').val('‘—M’†');
	});
	
	$(".namelink").on('click', function(){
		location.href = "profile.cgi?id=" + $(this).attr('data-id');
	});
});