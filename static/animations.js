$('.hover_box').click(function(){


	if($(this).hasClass('hb_many')){
		$(this).toggleClass('hover_box_selected')
	} else {
		$(this).toggleClass('hover_box_selected')
		$(this).siblings().removeClass('hover_box_selected')
		$(this).parent().siblings().children().removeClass('hover_box_selected')
	}

	var test = $(this).find("h6")
	var text = test[0]['textContent']

	if ($(this).hasClass('hb_many')){
		var nearest_input = $(this).find('.hidden_input');
	} else if ($(this).hasClass('multi_row')){
		var nearest_input = $(this).parentsUntil('.grandparent').find('.hidden_input')
		console.log(nearest_input)
	} else {
		var nearest_input = $(this).parent().find('.hidden_input');
	}

	if ($(this).hasClass('hover_box_selected')){	
		nearest_input.val(text)
	} else {
		nearest_input.val("")
	}


})

var i = 1
$(".edit_products").click(function(e){


	if ($(this).hasClass("add_product")){
		i++
		$('.input_table').append("<tr class='table_row'><td><input type='text' name='product_" + i + "_name' placeholder='product name " + i + "'></td><td><input type='text' name='p" + i + "_category' placeholder='details'></td><td><input type='text' name='p" + i + "_cogs' placeholder='$0.00'></td><td><input type='text' name='p" + i + "_sales_price' placeholder='$0.00'></td><td><input type='text' name='p" + i + "_qty_sold' placeholder='0'></td><td><input type='text' name='p" + i + "_est_unique_buyers' placeholder='0'></td><tr>")
	} else if ($(this).hasClass('remove_product')){
		if (i > 1){
			i--
		}
		var last = $('.table_row').last()
		last.remove()
	}
	$('.product_len').val(i)
		
})



$(document).ready(function(){
	var submenu_count = $('.step').length
	
	var width = (1/submenu_count*100)-1

	console.log(width)

	$('.step').css('width', width+"%")

})











