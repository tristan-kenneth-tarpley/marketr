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



function init_products(){
	function load_product_list(){
		$.get("/load_product_list",function(results){
			var results = JSON.parse(results)
			console.log(results)

			for (var i=0;i<results.length;i++){
				var current_name = results[i]['name']


				$('.product_prev_container').append("<div class='col-lg-3 col-md-3 col-sm-3 product_container'><p>" + results[i]['name'] + "</p></div>")

			}

			$('.product_container:nth-of-type(1)').addClass('product_container_active')
			$('#product-name').text(results[0]['name'])

			$('#p_id').val(results[0]['p_id'])

			localStorage.setItem('results', JSON.stringify(results));
			
		})
	}


	load_product_list()

	var it = 0 

	$('.p_form_submit').click(function(){
		$('textarea').val("")
		$('.hover_box').removeClass('hover_box_selected')
		$('input:checked').prop('checked', false)


		var results = localStorage.getItem('results');
		results = JSON.parse(results)

		var complexity = $('input[name=complexity]:checked').val()
		var price = $('input[name=price]:checked').val()
		var product_or_service = $('input[name=product_or_service]:checked').val()
		var frequency_of_use = $('input[name=frequency_of_use]:checked').val()
		var frequency_of_purchase = $('input[name=frequency_of_purchase]:checked').val()
		var value_prop = $('input[name=value_prop]').val()
		var warranties_or_guarantee = $('input[name=warranties_or_guarantee]').val()
		var warranties_or_guarantee_freeform = $('textarea[name=warranties_or_guarantee_freeform]').val()
		var num_skus = $('input[name=num_skus]:checked').val()
		var level_of_customization = $('input[name=level_of_customization]:checked').val()

		var length = results.length
		console.log(length)

		it++

		if (it < length){
			console.log(it)

			$('#product-name').text(results[it]['name'])
			var p_value = $("#p_id").val()

			$.post("/product_submit", { complexity: complexity, price: price, product_or_service: product_or_service, frequency_of_use: frequency_of_use, frequency_of_purchase: frequency_of_purchase, value_prop: value_prop, warranties_or_guarantee: warranties_or_guarantee, warranties_or_guarantee_freeform: warranties_or_guarantee_freeform, num_skus: num_skus, level_of_customization: level_of_customization, p_id: p_value } )

			
			$('.product_container').not('.product_container:nth-of-type(' + (it+1) + ')').removeClass('product_container_active')
			$('.product_container:nth-of-type(' + (it+1) + ')').addClass('product_container_active')


			var p_id = results[it]['p_id']
			$('#p_id').val(p_id)
			console.log(p_id)
		} else {
			$('.card-body').addClass("hidden")
			$('#setup').removeClass('hidden')
		}

		if(it == length) {
			$('.p_form_submit').addClass('hidden')
			$('.final').removeClass('hidden')
			$('.product_prev_container').addClass("hidden")
			$('.hide_on_end').addClass('hidden')
		}


	  $("html, body").animate({ scrollTop: 0 }, "slow");
	})
}



function init_sales_cycle(){
	$('.stage_container input').not('.first').addClass('hide')

	$('.stage_container input').keydown(function(event){


	    var keycode = (event.keyCode ? event.keyCode : event.which);

	    if(keycode == '13'){
	        event.preventDefault()

		    if($(document.activeElement).is(':last-child')){

	    		if($(document.activeElement).val() == ''){

		    		alert('You have to enter a value');

		    	} else {
		    		if($(document.activeElement).hasClass('last')){
			    		
						$('<span class="x">X</span>').insertAfter(document.activeElement)
						$(document.activeElement).blur()

			    	} else if ($(document.activeElement).parent().siblings().find('input:first-child').hasClass('hide')) {

						$('<span class="x">X</span>').insertAfter(document.activeElement)
		    			$(document.activeElement).parent().siblings().find('input:first-child').removeClass('hide')
		    			$(document.activeElement).parent().siblings().find('input:first-child').focus()

			    	}

		    	}

		    } else {
		    	
		    	if($(document.activeElement).val() == ''){
		    		alert('You have to enter a value');
		    	} else if ($(document.activeElement).next().hasClass('hide')) {

		    		$(document.activeElement).next().removeClass('hide')

		    		if (!$(document.activeElement).hasClass('first')){

						$('<span class="x">X</span>').insertAfter(document.activeElement)

		    		} else {
		    			$('<span class="x hide">X</span>').insertAfter(document.activeElement)
		    		}
		    		$(document.activeElement).nextAll().eq(1).focus()
					

		    	}

		    }
		} else if (keycode == '8' || keycode == '46'){
			
			if ($(document.activeElement).val() == '' && !$(document.activeElement).hasClass("first") && ($(document.activeElement).next().hasClass('hide') || $(document.activeElement).is(':last-child')) && !$(document.activeElement).is(':first-child')){

				event.preventDefault()
				$(document.activeElement).addClass('hide')
				$(document.activeElement).prevAll().eq(1).focus()
				$(document.activeElement).next().remove()

			}

		}


		$('.x').click(function() {
			
	
			$(this).prev().val('')


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
			'Free Trial',
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
	$.get('/load_history',function(data){

		var results = JSON.parse(data)
		// localStorage.setItem('results', JSON.stringify(results));

		console.log(results)

		for (var i = 0; i<results['data'][0].length; i++){
			if(results['data'][0][i] == "yes"){
				console.log(results['columns'][i] + ": " + results['data'][0][i])
				$('.platforms_container').append("<div class='platform_row'><div class='col-lg-2'><h6>" + results['columns'][i] + "</h6><input style='display:none' type='text' value='" + results['columns'][i] + "' name='platform_" + i + "'></div><div class='col-lg-4 col-md-4'><h6>Still using?</h6><div class='hover_box col-lg-5 col-md-5'><br><h6>yes</h6><br></div>&nbsp;<div class='hover_box col-lg-5 col-md-5'><br><h6>no</h6><br></div><input class='hidden_input hidden' type='text' name='still_using_" + i + "'></div><div class='col-lg-6 col-md-6'><h6>How are the results?</h6><img src='/static/assets/img/frown.png' class='col-lg-3'><img src='/static/assets/img/neutral.png' class='col-lg-3'><img src='/static/assets/img/smile.png' class='col-lg-3'><img src='/static/assets/img/grin.png' class='col-lg-3'><input type='text' style='display:none;' class='img_input' name='results_" + i + "'></div></div><hr>")
			}
		}

		
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

	})



	// var results = localStorage.getItem('results');
	// results = JSON.parse(results)

}
	



function init_competitors(){


	var industries = [
		"Select Industry",
		"Accountants",
		"Advertising/Public Relations",
		"Aerospace, Defense Contractors",
		"Agribusiness",
		"Agricultural Services & Products",
		"Agriculture",
		"Air Transport",
		"Air Transport Unions",
		"Airlines",
		"Alcoholic Beverages",
		"Alternative Energy Production & Services",
		"Architectural Services",
		"Attorneys/Law Firms",
		"Auto Dealers",
		"Auto Dealers, Japanese",
		"Auto Manufacturers",
		"Automotive",
		"Banking, Mortgage",
		"Banks, Commercial",
		"Banks, Savings & Loans",
		"Bars & Restaurants",
		"Beer, Wine & Liquor",
		"Books, Magazines & Newspapers",
		"Broadcasters, Radio/TV",
		"Builders/General Contractors",
		"Builders/Residential",
		"Building Materials & Equipment",
		"Building Trade Unions ",
		"Business Associations",
		"Business Services",
		"Cable & Satellite TV Production & Distribution",
		"Candidate Committees ",
		"Candidate Committees, Democratic",
		"Candidate Committees, Republican",
		"Car Dealers",
		"Car Dealers, Imports",
		"Car Manufacturers",
		"Casinos / Gambling",
		"Cattle Ranchers/Livestock",
		"Chemical & Related Manufacturing",
		"Chiropractors",
		"Civil Servants/Public Officials",
		"Clergy & Religious Organizations ",
		"Clothing Manufacturing",
		"Coal Mining",
		"Colleges, Universities & Schools",
		"Commercial Banks",
		"Commercial TV & Radio Stations",
		"Communications/Electronics",
		"Computer Software",
		"Conservative/Republican",
		"Construction",
		"Construction Services",
		"Construction Unions",
		"Credit Unions",
		"Crop Production & Basic Processing",
		"Cruise Lines",
		"Cruise Ships & Lines",
		"Dairy",
		"Defense",
		"Defense Aerospace",
		"Defense Electronics",
		"Defense/Foreign Policy Advocates",
		"Democratic Candidate Committees ",
		"Democratic Leadership PACs",
		"Democratic/Liberal ",
		"Dentists",
		"Doctors & Other Health Professionals",
		"Drug Manufacturers",
		"Education ",
		"Electric Utilities",
		"Electronics Manufacturing & Equipment",
		"Electronics, Defense Contractors",
		"Energy & Natural Resources",
		"Entertainment Industry",
		"Environment ",
		"Farm Bureaus",
		"Farming",
		"Finance / Credit Companies",
		"Finance, Insurance & Real Estate",
		"Food & Beverage",
		"Food Processing & Sales",
		"Food Products Manufacturing",
		"Food Stores",
		"For-profit Education",
		"For-profit Prisons",
		"Foreign & Defense Policy ",
		"Forestry & Forest Products",
		"Foundations, Philanthropists & Non-Profits",
		"Funeral Services",
		"Gambling & Casinos",
		"Gambling, Indian Casinos",
		"Garbage Collection/Waste Management",
		"Gas & Oil",
		"Gay & Lesbian Rights & Issues",
		"General Contractors",
		"Government Employee Unions",
		"Government Employees",
		"Gun Control ",
		"Gun Rights ",
		"Health",
		"Health Professionals",
		"Health Services/HMOs",
		"Hedge Funds",
		"HMOs & Health Care Services",
		"Home Builders",
		"Hospitals & Nursing Homes",
		"Hotels, Motels & Tourism",
		"Human Rights ",
		"Ideological/Single-Issue",
		"Indian Gaming",
		"Industrial Unions ",
		"Insurance",
		"Internet",
		"Israel Policy",
		"Labor",
		"Lawyers & Lobbyists",
		"Lawyers / Law Firms",
		"Leadership PACs ",
		"Liberal/Democratic",
		"Liquor, Wine & Beer",
		"Livestock",
		"Lobbyists",
		"Lodging / Tourism",
		"Logging, Timber & Paper Mills",
		"Manufacturing, Misc",
		"Marine Transport",
		"Meat processing & products",
		"Medical Supplies",
		"Mining",
		"Misc Business",
		"Misc Finance",
		"Misc Manufacturing & Distributing ",
		"Misc Unions ",
		"Miscellaneous Defense",
		"Miscellaneous Services",
		"Mortgage Bankers & Brokers",
		"Motion Picture Production & Distribution",
		"Music Production",
		"Natural Gas Pipelines",
		"Newspaper, Magazine & Book Publishing",
		"Non-profits, Foundations & Philanthropists",
		"Nurses",
		"Nursing Homes/Hospitals",
		"Nutritional & Dietary Supplements",
		"Oil & Gas",
		"Other",
		"Payday Lenders",
		"Pharmaceutical Manufacturing",
		"Pharmaceuticals / Health Products",
		"Phone Companies",
		"Physicians & Other Health Professionals",
		"Postal Unions",
		"Poultry & Eggs",
		"Power Utilities",
		"Printing & Publishing",
		"Private Equity & Investment Firms",
		"Pro-Israel ",
		"Professional Sports, Sports Arenas & Related Equipment & Services",
		"Progressive/Democratic",
		"Public Employees",
		"Public Sector Unions ",
		"Publishing & Printing",
		"Radio/TV Stations",
		"Railroads",
		"Real Estate",
		"Record Companies/Singers",
		"Recorded Music & Music Production",
		"Recreation / Live Entertainment",
		"Religious Organizations/Clergy",
		"Republican Candidate Committees ",
		"Republican Leadership PACs",
		"Republican/Conservative ",
		"Residential Construction",
		"Restaurants & Drinking Establishments",
		"Retail Sales",
		"Retired ",
		"Savings & Loans",
		"Schools/Education",
		"Sea Transport",
		"Securities & Investment",
		"Special Trade Contractors",
		"Sports, Professional",
		"Steel Production ",
		"Stock Brokers/Investment Industry",
		"Student Loan Companies",
		"Sugar Cane & Sugar Beets",
		"Teachers Unions",
		"Teachers/Education",
		"Telecom Services & Equipment",
		"Telephone Utilities",
		"Textiles ",
		"Timber, Logging & Paper Mills",
		"Tobacco",
		"Transportation",
		"Transportation Unions ",
		"Trash Collection/Waste Management",
		"Trucking",
		"TV / Movies / Music",
		"TV Production",
		"Unions",
		"Unions, Airline",
		"Unions, Building Trades",
		"Unions, Industrial",
		"Unions, Misc",
		"Unions, Public Sector",
		"Unions, Teacher",
		"Unions, Transportation",
		"Universities, Colleges & Schools",
		"Vegetables & Fruits",
		"Venture Capital",
		"Waste Management",
		"Wine, Beer & Liquor",
		"Women's Issues"
	]

	for (var t=0;t<industries.length;t++){
		$('#industry').append("<option>" + industries[t] + "</option>")
	}

}


function init_company_view(){

	var pathname = window.location.pathname;

	$('.dyn_link').each(function(){
		var id = $(this).attr('id')
		var url = pathname + "?page=" + id
		$(this).attr('href', url)
	})

}










$(document).ready(function(){

	$("br").remove()



	var url_path = window.location.pathname;

	$.get('/load_past_inputs', {page: url_path}, function(data){

		var data = JSON.parse(data)
		//console.log(data)

		//sales cycle page
		//console.log(data)
		//console.log(Object.keys(data).length)

		function load_sales_cycle(){

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
				//$("." + value).children().find('input').val()  //css('border', '3px solid yellow')
			}



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
				
		}

		load_sales_cycle()



		//if not sales cycle
		if (data.length > 0){
			Object.keys(data[0]).forEach(function(key) {

				var value = data[0][key]


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
	})






	$('.reveal_button').click(function(){
		$('.reveal').fadeIn('slow')
		$(this).addClass("hidden")
	})



	var submenu_count = $('.step').length
	
	var width = (1/submenu_count*100)-1

	$('.step').css('width', width+"%")

	$( ".radio_container" ).each(function( i ) {

	  	var quantity = $(this).children('.connector').length
	  	var connect_width = (1/quantity*100)-1

	  	$(this).children('.connector').css('width', connect_width + "%")
	  	$(this).siblings('label').css('width',connect_width + "%")
	});





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



})

























