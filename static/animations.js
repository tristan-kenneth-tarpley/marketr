$('.hover_box').click(function(){


	if($(this).hasClass('hb_many')){

		$(this).toggleClass('hover_box_selected')

	} else {

		$(this).toggleClass('hover_box_selected')
		$(this).siblings().removeClass('hover_box_selected')
		$(this).parent().siblings().children().removeClass('hover_box_selected')


	}


})


$(document).ready(function(){
	var submenu_count = $('.step').length
	
	var width = (1/submenu_count*100)-1

	console.log(width)

	$('.step').css('width', width+"%")

})