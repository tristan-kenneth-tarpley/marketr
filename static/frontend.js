$(document).ready(function() {

	console.log('document is loaded')

	$.get('/onload', function(data){
		text = data
		header = text + "'s dashboard"
		$('.dash-select').text(header)
		console.log(text)
	})

})

