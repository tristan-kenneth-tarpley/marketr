function init_admin(){


	  $.get('/admin_availability',function(data){
	  	data = JSON.parse(data)
	  	for(var i = 0; i<data.length; i++){

	  		if(data[i]['email'] == $('#email').val()){

	  			$('.availability').text('Email is taken.  Please try another.')
	  			$('.availability').css('visibility', 'visible')
				$('.create_button').attr('disabled','disabled');
	  			return false

	  		} else {

	  			$('.availability').text('username is available!')
	  			$('.availability').css('visibility', 'visible')

				$('.create_button').prop('disabled', false);

	  		}

	  	}
	  })

	  $('.headers').click(function(){
	  	$(this).find("span").addClass('blue')
	  	$('.headers').not(this).find("span").removeClass('blue')
	  })

}


function smilesMapper(name){
	var path = "/static/assets/img/"
	var map = {
		"bing": "Bing.png",
		"google": "GoogleAds.png",
		"linkedin": "Linkedin.png",
		"instagram": "Instagram.png",
		"amazon": "Amazon.png",
		"twitter": "twitter.png",
		"snapchat": "Snapchat.png",
		"youtube": "YouTube.png",
		"yelp": "Yelp.png",
		"facebook": "Facebook.png"
	}

	var url = path + map[name]

	return url
}



function init_create_account(){

	$('.create_button').prop('disabled', true);
	function delay(callback, ms) {
		var timer = 0;

		return function() {
	    	var context = this, args = arguments;
	    	clearTimeout(timer);
	    	timer = setTimeout(function () {
				callback.apply(context, args);
	   		}, ms || 0);
		};
	}

	$('#email').keyup(delay(function (e) {



	  $.get('/availability',function(data){
	  	data = JSON.parse(data)
	  	for(var i = 0; i<data.length; i++){

	  		if(data[i]['email'] == $('#email').val()){

	  			$('.availability').text('Email is taken.  Please try another.')
	  			$('.availability').css('visibility', 'visible')
				$('.create_button').attr('disabled','disabled');
	  			return false

	  		} else {

	  			$('.availability').text('username is available!')
	  			$('.availability').css('visibility', 'visible')

				$('.create_button').prop('disabled', false);

	  		}

	  	}
	  })

	  var testEmail = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i;

	  if (testEmail.test($('#email').val())){
	  	$('.format').text(' ')
	  } else {
	  	$('.format').text('invalid email format')
	  }

	}, 1000));


}


var i = 1
$(".edit_products").click(function(e){


	if ($(this).hasClass("add_product")){
		i++

		var data = $('.data-row').last().clone()
		var item_1_name = `product_name[${i}]`
		data.find('#item-1').attr("name", item_1_name)
		var placeholder = `name ${i}`
		data.find('#item-1').attr('placeholder', placeholder)

		var item_2_name = `p_category[${i}]`
		data.find('#item-2').attr("name", item_2_name)

		var item_3_name = `cogs[${i}]`
		data.find('#item-3').attr("name", item_3_name)

		var item_4_name = `sales_price[${i}]`
		data.find('#item-4').attr("name", item_4_name)

		var item_5_name = `price_model[${i}]`
		data.find('#item-5').attr("name", item_5_name)

		var item_6_name = `qty_sold[${i}]`
		data.find('#item-6').attr("name", item_6_name)

		var item_7_name = `est_unique_buyers[${i}]`
		data.find('#item-7').attr("name", item_7_name)

		$('.input_table').append(data)

	} else if ($(this).hasClass('remove_product')){
		if (i > 1){
			var last = $('.data-row').last()
			last.remove()
			i--
		}
	}
	$('.product_len').val(i)
		
})



function init_products(){
	function load_product_list(){
		$.get("/load_product_list",function(results){
			var results = JSON.parse(results)

			for (var i=0;i<results.length;i++){
				var current_name = results[i]['name']
				$('.product_prev_container').append(`<div class='col-lg-3 col-md-3 col-sm-3 product_container'><p>${results[i]['name']}</p></div>`)
			}

			$('.product_container:nth-of-type(1)').addClass('product_container_active')
			$('#product-name').text(results[0]['name'])

			$('#p_id').val(results[0]['p_id'])

			localStorage.setItem('results', JSON.stringify(results));
			
		})
	}

	// new Cleave('.cogs', {
	//     numeral: true,
	//     prefix: '$'
	// });
	// new Cleave('.price', {
	//     numeral: true,
	//     prefix: '$'
	// });


	load_product_list()
	$("#wogf").click(function(){
		$("#warranties_or_guarantee_freeform").focus()
	})
	$('.form-radio').click(function(){
		console.log($(this).val())
	})

	var it = 0 

	$('.p_form_submit').click(function(){

		let local_results = localStorage.getItem('results');
		const results = JSON.parse(local_results)
	
		let p_value = $("#p_id").val()
		console.log(p_value)
		let complexity = $('input[name=complexity]').val()
		let price = $('input[name=price]').val()
		let product_or_service = $('input[name=product_or_service]').val()
		let frequency_of_use = $('input[name=frequency_of_use]').val()
		let frequency_of_purchase = $('input[name=frequency_of_purchase]').val()
		let value_prop = $('input[name=value_prop]').val()
		let warranties_or_guarantee = $('input[name=warranties_or_guarantee]').val()
		let warranties_or_guarantee_freeform = $('textarea[name=warranties_or_guarantee_freeform]').val()
		let num_skus = $('input[name=num_skus]').val()
		let level_of_customization = $('input[name=level_of_customization]').val()

		const length = results.length

		const args = { complexity: complexity, price: price, product_or_service: product_or_service, frequency_of_use: frequency_of_use, frequency_of_purchase: frequency_of_purchase, value_prop: value_prop, warranties_or_guarantee: warranties_or_guarantee, warranties_or_guarantee_freeform: warranties_or_guarantee_freeform, num_skus: num_skus, level_of_customization: level_of_customization, p_id: p_value }
		for (let key in args) {
			if (args[key] == undefined || args[key] == ""){
				args[key] = "n/a"
			}
		}
		console.log(args)
		$.post("/product_submit", args )

		it++

		if (it < length){

			$('#product-name').text(results[it]['name'])
			console.log(results[it]['name'])
			let p_value = $("#p_id").val()

			
			$('.product_container').not('.product_container:nth-of-type(' + (it+1) + ')').removeClass('product_container_active')
			$('.product_container:nth-of-type(' + (it+1) + ')').addClass('product_container_active')


			var p_id = results[it]['p_id']
			$('#p_id').val(p_id)
		} else {
			$('.card-body').addClass("hidden")
			$('.p_form_submit').addClass('hidden')
			$('.final').removeClass('hidden')
			$('.product_prev_container').addClass("hidden")
			$('.hide_on_end').addClass('hidden')
			$(".change_on_submit").html("<h5>Nice! Let's keep going.</h5>")
		}

	   $("html, body").animate({ scrollTop: 0 }, "slow");
		$('textarea').val("")
		$('.hover_box').removeClass('hover_box_selected')


		// $('input:checked').prop('checked', false)
	})
}


function load_sales_cycle(data, callback){

	var awareness = data.filter(function(item){
	    return item.stage == "awareness";         
	});
	var evaluation = data.filter(function(item){
	    return item.stage == "evaluation";         
	});
	var conversion = data.filter(function(item){
	    return item.stage == "conversion";         
	});
	var retention = data.filter(function(item){
	    return item.stage == "retention";         
	});
	var referral = data.filter(function(item){
	    return item.stage == "referral";         
	});

	var stages = [awareness, evaluation, conversion, retention, referral]

	function get_length(step){
		var length = step.length
		return length
	}
	$('.stage_container input').not('.first').addClass('hide')

	for (var i=0;i<stages.length;i++){
		var length = get_length(stages[i])
		for (var x=0;x<stages[i].length;x++){
			var toShow = $(".stage_container." + stages[i][x]['stage'] + " input").slice(0, length)
			toShow.removeClass('hide')
			if (toShow.val() !== stages[i][x]['tactic']){
				toShow.eq(x).val(stages[i][x]['tactic'])
			}
		}
	}
	callback()		
}


function init_sales_cycle(){
	$('.left_stage').addClass("stages")
	$('.right_stage').addClass('stages')
	

	$('.stage_container input').keydown(function(event){

	    var keycode = (event.keyCode ? event.keyCode : event.which);

	    if(keycode == '13'){
	        event.preventDefault()

		    if($(document.activeElement).is(':last-child')){
	    		if($(document.activeElement).val() == ''){
		    		alert('You have to enter a value');
		    	} else {
		    		if($(document.activeElement).hasClass('last')){
						$(document.activeElement).blur()
			    	} else if ($(document.activeElement).parent().siblings().find('input:first-child').hasClass('hide')) {
		    			$(document.activeElement).parent().siblings().find('input:first-child').removeClass('hide')
		    			$(document.activeElement).parent().siblings().find('input:first-child').focus()
			    	}
		    	}
		    } else {
		    	
		    	if($(document.activeElement).val() == ''){
		    		alert('You have to enter a value');
		    	} else if ($(document.activeElement).nextAll("input").eq(0).hasClass('hide')) {
		    		$(document.activeElement).nextAll("input").eq(0).removeClass('hide')
		    		$(document.activeElement).nextAll('.x').eq(0).removeClass("hide")
		    		$(document.activeElement).nextAll().eq(0).focus()
		    	}

		    }
		} else if (keycode == '8' || keycode == '46'){
			
			if ($(document.activeElement).val() == '' && !$(document.activeElement).hasClass("first") && !$(document.activeElement).is(':first-child')){
				event.preventDefault()
				$(document.activeElement).addClass('hide')
				$(document.activeElement).prevAll().eq(0).focus()
				$(document.activeElement).next().val("")
			}

		}


		$('.x').click(function() {
			$(this).prev().val('')
			$(this).prev().addClass('invisible')
		})


	    var awareness_tags = [
			"Website",
			"Physical storefront",
			"Amazon",
			"Google shopping",
			"Etsy",
			"Articles",
			"eBook",
			"TV ads",
			"Radio ads",
			"Podcast ads",
			"Online ads",
			"Shelf-space in other stores",
			"Tradeshows",
			"How-to-videos",
			"Cross promotion",
			"Referrals / word-of-mouth",
			"Signage (incl. billboards)",
			"Direct mailers",
			"Email newsletter"
	    ];
	    $( ".awareness input" ).autocomplete({
	      source: awareness_tags
	    });

	    var evaluation_tags = [
			'Competitive comparison',
			'Feature list',
			'Data sheet',
			'Case study',
			'Testimonials',
			'Webinar',
			'Online reviews',
			'FAQ',
			'Samples',
			'Demo video'
	    ]
	    $( ".evaluation input" ).autocomplete({
	      source: evaluation_tags
	    });


	    var conversion_tags = [
			'Free trial',
			'Pricing page',
			'Live demo',
			'Consultation',
			'Estimate / quote',
			'Coupon',
			'Call-to-action',
			'Re-targeting',
			'Sales call follow-up',
			'"Drip" email campaign'
	    ]
	    $( ".conversion input" ).autocomplete({
	      source: conversion_tags
	    });

	    var retention_tags = [
			'Packaging',
			'Email follow-up',
			'Coupons',
			'Subscription',
			'Easy re-order',
			'Birthday gifts',
			'New product notices',
			'Re-targeting online ads',
			'Cross-promotion / nurture campaigns',
			'Perk milestones for subscription anniversaries'
	    ]
	    $( ".retention input" ).autocomplete({
	      source: retention_tags
	    });

	    var referral_tags = [
			'Packaging',
			'Social sharing incentive',
			'Shareable coupons',
			'Referral incentive',
			'Testimonial / Reviews',
			'User generated content'
	    ]
	    $( ".referral input" ).autocomplete({
	      source: referral_tags
	    });
 	


	});


}

function init_platforms(){


		
		$('.platform_row img').click(function(){
			$(this).addClass('platform_row_img_active')
			$(this).siblings().removeClass('platform_row_img_active')

			$(this).parent().find('.img_input').val($(this).index())
		})

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
			} else {
				var nearest_input = $(this).parent().find('.hidden_input');
			}

			if ($(this).hasClass('hover_box_selected')){	
				nearest_input.val(text)
			} else {
				nearest_input.val("")
			}


		})


}
	



function init_competitors(){


    var options = {

	  url: "/industries",

	  getValue: "industries",

	  list: {	
	    match: {
	      enabled: true
	    }
	  },

	  theme: "square"
	};

	$("#industry").easyAutocomplete(options);
}


function init_company_view(){

	var pathname = window.location.pathname;

	$('.dyn_link').each(function(){
		var id = $(this).attr('id')
		var url = pathname + "?page=" + id
		$(this).attr('href', url)
	})

}





function hover_box(){

	$(".in_box").click(function(event){
		event.stopPropagation()
		if (!$(this).parent().hasClass('hover_box_selected')) {
			$(this).parent().addClass('hover_box_selected')
		}
		input_clicked = true
		return input_clicked
	})

	$('.hover_box').click(function(){
		var input_clicked = false

		var in_box = $(this).find("input")

		//toggle selected
		if($(this).hasClass('hb_many')){
			if(!in_box.hasClass('in_box')){
				$(this).toggleClass('hover_box_selected')
			} else {				
				$(this).toggleClass('hover_box_selected')
				if ($(this).hasClass('hover_box_selected')){
					$(this).find(".in_box").focus()
				} else {	
					$(this).find(".in_box").val("")
				}
			}
		} else {
			$(this).toggleClass('hover_box_selected')
			$(this).siblings().removeClass('hover_box_selected')
			$(this).parent().siblings().children().removeClass('hover_box_selected')
		}


		//populate database val
		var test = $(this).find("h6")
		var text = test[0]['textContent']

		if ($(this).hasClass('hb_many')){
			var nearest_input = $(this).find('.hidden_input');
		} else if ($(this).hasClass('multi_row')){
			var nearest_input = $(this).parentsUntil('.grandparent').find('.hidden_input')
		} else {
			var nearest_input = $(this).parent().find('.hidden_input');
		}

		if ($(this).hasClass('hover_box_selected')){	
			nearest_input.val(text)
		} else {
			nearest_input.val("")
		}
	})
}


function load_company(){
	var perc_format = $('.perc_format')
	var in_box = $('.in_box')

	$(in_box).each(function(){
		var this_hb = $(this).parent()
		if ($(this).val() == ""){
			this_hb.removeClass('hover_box_selected')
		}
	})
}


function load_audience(){
	let param = new URLSearchParams(window.location.search)
	let persona_id = param.get('persona_id')

	var options = {

	  url: "/areas",

	  getValue: "area",

	  list: {	
	    match: {
	      enabled: true
	    }
	  },

	  theme: "square"
	};

	$("#location").easyAutocomplete(options);

	if (persona_id == null){
		$('.persona_intro').text("Think of a GREAT customer. Use them as a model for this first persona.")

		$('.lastly').click(function(){
			$('.lastlyFade').fadeIn()
		})

	} else {

		$(".persona_intro").text("Awesome! Now, think of another excellent customer that's different from the other(s) you've added.")

	} 

	if ($('.product_container').length == 1){

		$("#remove").addClass('invisible')

	} else if ($('.product_container').length > 1){

		$("#remove").removeClass('invisible')
		var removeURL = "/remove/" + persona_id
		$("#remove").attr('href', removeURL)

	}

	$('.product_container:nth-of-type(1)').addClass('product_container_active')




}

function load_past_inputs(){
	var url_path = window.location.pathname;
	var product_2_path = "/competitors/company/audience/product/product_2"

	let init_params = new URLSearchParams(window.location.search)

	var args = {}

	if (init_params.has('persona_id')){
		args = {page: url_path,
				persona_id: init_params.get('persona_id')}
	} else {
		args = {page: url_path}
	}


	$(".onward .continue").attr('value', 'SAVE AND CONTINUE')

	if (url_path !== "/home" && url_path !== "/" && url_path !== "/new" && url_path !== "/admin" && url_path !== "/admin/branch" && url_path !== "/class" && url_path !== "/splash") {

		$.get('/load_past_inputs', args, function(data){
			if (data !== 'nah, not this time' && data !== 'nah') {

				var data = JSON.parse(data)
				console.log(data)
				//if audience


				if (url_path == "/creative") {
					console.log(data)
				}

				if (url_path == "/history/platforms") {
					for (var i = 0; i < data.length; i++){
						Object.keys(data[i]).forEach(function(key){
							const value = data[i][key]
							$('select[name=' + key + ']').val(value)
							$('input[name=' +  key + ']').val(data[0][key])
							$('textarea[name=' + key + ']').val(data[0][key])

							$('.hover_box').each(function(){

								var hb_many = $(this).hasClass('hb_many')
								var closest_val = $(this).closest('.hidden_input').val()
								var single = $(this).hasClass('multi_row') == false && $(this).hasClass('hb_many') == false

								var many_check = hb_many && closest_val !== ""
								var single_check = single && $(this).siblings('.hidden_input').val() !== ""

								var multi_input_select = $(this).parentsUntil('.grandparent').find('.hidden_input').val()
								var multi_row_check = $(this).hasClass('multi_row') && multi_input_select !== ""

								var contains_val = $(this).closest("h6:contains('" + closest_val + "')")


								if (many_check){

									if ($(this).children('.hidden_input').val() !== ""){
										$(this).addClass('hover_box_selected')
									}

								} else if (single_check){

									var single_select =  $(this).siblings('.hidden_input').val()
									var add_select = $(this).children("h6:contains('" + single_select +"')").closest('.hover_box')
									add_select.addClass("hover_box_selected")
									
								} else if (multi_row_check) {

									$(this).parentsUntil('.grandparent').find("h6:contains('" + multi_input_select + "')").closest('.hover_box').addClass('hover_box_selected')
								
								}
							})
						})
					}
				}


				load_sales_cycle(data, init_sales_cycle)

				//if not sales cycle
				if (data.length > 0){
					Object.keys(data[0]).forEach(function(key) {

						var value = data[0][key]
						let param = new URLSearchParams(window.location.search)
						//Does sent exist?
						

						if (param.has('persona_id')){

							let persona_id = param.get('persona_id')
							var audience_filter = data.filter(function(item){
							    return item.audience_id == persona_id;         
							});
							$("#" + persona_id).parent().addClass("product_container_active")
							$(".dyn_link").not("#" + persona_id).parent().removeClass('product_container_active')
							data = audience_filter

						}

						$('select[name=' + key + ']').val(value)
						$('input[name=' +  key + ']').val(data[0][key])
						$('textarea[name=' + key + ']').val(data[0][key])

						$('.hover_box').each(function(){

							var hb_many = $(this).hasClass('hb_many')
							var closest_val = $(this).closest('.hidden_input').val()
							var single = $(this).hasClass('multi_row') == false && $(this).hasClass('hb_many') == false

							var many_check = hb_many && closest_val !== ""
							var single_check = single && $(this).siblings('.hidden_input').val() !== ""

							var multi_input_select = $(this).parentsUntil('.grandparent').find('.hidden_input').val()
							var multi_row_check = $(this).hasClass('multi_row') && multi_input_select !== ""

							var contains_val = $(this).closest("h6:contains('" + closest_val + "')")


							if (many_check){

								if ($(this).children('.hidden_input').val() !== ""){
									$(this).addClass('hover_box_selected')
								}

							} else if (single_check){

								var single_select =  $(this).siblings('.hidden_input').val()
								var add_select = $(this).children("h6:contains('" + single_select +"')").closest('.hover_box')
								add_select.addClass("hover_box_selected")
								
							} else if (multi_row_check) {

								$(this).parentsUntil('.grandparent').find("h6:contains('" + multi_input_select + "')").closest('.hover_box').addClass('hover_box_selected')
							
							}
						})
					})
				}
				load_company()
			}
		})
	}
}




function init_sub_menu(){

	var submenu_count = $('.step').length
	
	var width = (1/submenu_count*100)-1

	$('.step').css('width', width+"%")
}



function init_radio(){
	$( ".radio_container" ).each(function( i ) {

	  	var quantity = $(this).children('.connector').length
	  	var connect_width = (1/quantity*100)-1

	  	$(this).children('.connector').css('width', connect_width + "%")
	  	$(this).siblings('label').css('width',connect_width + "%")
	});
}

function init_creative(){
	$('.delete_asset.x').click(function(){
		$(this).parent().parent().addClass('hidden')
		$(this).parent().parent().siblings().removeClass("hidden")
	})

	$('.confirmed').click(function(){
		var path = $(this).parent().siblings().find('img').attr('src')
		args = {file_path: path}
		$(this).parentsUntil('.files_row').remove()
		$.get('/delete_asset', args, function(data){
		})
	})
	$('.delete_asset.unconfirmed').click(function(){
		$(this).parent().siblings().removeClass('hidden')
		$(this).parent().addClass('hidden')
	})
}

function isURL(str) {
  var pattern = new RegExp('^((ft|htt)ps?:\\/\\/)?'+ // protocol
  '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name and extension
  '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
  '(\\:\\d+)?'+ // port
  '(\\/[-a-z\\d%@_.~+&:]*)*'+ // path
  '(\\?[;&a-z\\d%@_.,~+&:=-]*)?'+ // query string
  '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
  return pattern.test(str);
}


$(document).ready(function(){

	

	$('.ignore_default input').keydown(function(event){
		var keycode = (event.keyCode ? event.keyCode : event.which);

	    if(keycode == '13'){
	        event.preventDefault()
	    }
	})

	load_past_inputs()
	init_sub_menu()

	$('.reveal_button').click(function(){
		$('.reveal').fadeIn('slow')
		$(this).addClass("hidden")
	})

	var url_path = window.location.pathname;
	if (url_path == "/competitors/company/audience"){
		load_audience()
	} 

	hover_box()
	init_creative()

	$(".website").blur(function(){
		var x = isURL($(this).val())
		if (x == false){
			$(this).siblings('.isValid').text("Invalid website")
		} else {
			$(this).siblings('.isValid').text(' ')
		}
		
	})

	var perc = []
	$(".percent").keyup(function(){
		$('.perc').empty()

		var sum = 0;
		$(".percent").each(function(){
		    sum += +$(this).val();
		});

		$(".perc").text(sum);

		if (parseInt($('.perc').text()) == 100) {
			$('.container.counter').addClass('green')
			$('.container.counter').removeClass('red')
		} else if (parseInt($('.perc').text()) > 100) {
			$('.container.counter').addClass('red')
			$('.container.counter').removeClass('green')
		} else {
			$('.container.counter').removeClass('red')
			$('.container.counter').removeClass('green')
		}
	})

	setTimeout(function() { 
        $('.need_help').fadeIn()
	  	$(".xx").click(function(){
	  		$(this).parent().remove()
	  	})
    }, 100000);

	$(function () {
	  $('[data-toggle="tooltip"]').tooltip()
	})


})





