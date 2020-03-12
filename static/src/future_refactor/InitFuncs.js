import {perc_container} from '/static/src/components/UI_elements.js'

const get_account_availability = email => {
	const get_account_availability_handler = (data) => {
		let target = $("#new_email")
		if (data == 'False') {
	
			target.removeClass('input-success')
			target.addClass('input-danger')
	
			return false
	
		} else {
			target.removeClass('input-danger')
			target.addClass('input-success')
	
			return true
		}
	}	


	$.get('/availability', {email: email}, function(data){
		let available = get_account_availability_handler(data)
		if (available == false) {
			$('.submit_button').attr('disabled', true)
			$("#email_availability").html(`<p>An account already exists with the provided email. <a href="/login">Login here.</a></p>`)
		} else {
			$('.submit_button').attr('disabled', false)
		}
	})
} 

const platform_row = (name, index) => {	
	const tile = (title) => {
		return `
		<div class="table-responsive hover_box col-lg-5 col-md-">
			<table class="table">
				<thead>
					<tr>
						<th style="text-align:center;">
							<h6 style="font-size: 70%;" class="x_small_txt">${title}</h6>
						</th>
					</tr>
				</thead>
			</table>
		</div>`
	}
	/*html*/
	const el = `<div class="row platform_row">
					<div class='col-lg-2 col-sm-12 col-12'>
						<h5 style="text-align:center;" class="title"><span class="platform_img">${name}</span></h5>
						<input style="display:none;" type='text' value='${name}' name='platform[${index}]'>
					</div>
					<div style="text-align:center;" class='col-lg-4 col-md-4 col-sm-6 col-6'>
						<h6>Still using?</h6><br>
						<div class="container row col-12">
							${tile('yes')}
							&nbsp;
							${tile('no')}
							<input type="text" name="currently_using[${index}]" class="hidden_input hidden">
						</div>
					</div>
					<div class='col-lg-6 col-md-6 col-6'>
						<h6>How are the results?</h6>
						<br>
						<img src='/static/assets/img/frown.png' class='col-lg-2 col-5'>
						<img src='/static/assets/img/neutral.png' class='col-lg-2 col-5'>
						<img src='/static/assets/img/smile.png' class='col-lg-2 col-5'>
						<img src='/static/assets/img/grin.png' class='col-lg-2 col-5'>
						<input type='text' style='display:none;' class='img_input' name='results[${index}]'>
					</div>
				</div>`
	return el
}


const get_container = title => {
	const container_item = (name, id, page) => {
		let base_url = "/competitors/company/"
		let link;
		if (page == 'audience') {
			link = base_url + `audience?view_id=${id}&splash=False`
		} else if (page == 'product_2') {
			link = base_url + `audience/product/product_2?view_id=${id}&splash=False`
		}
		let el = `
				<a class='col-lg-3 col-md-3 col-sm-6 col-6 past_container' id="${id}" href="${link}">
					${name}
				</a>
				`
		return el
	}

	const container_handler = (data, title) => {
		data = JSON.parse(data)
		console.log(Object.keys(data).length)
	
		if (Object.keys(data).length > 1) {
			Object.keys(data).forEach(function(key){
				let id = data[key]['id']
				let name = data[key]['name']
				
				let item;
				if (name != null && name != "") {
					item = container_item(name, id, title)
				} else {
					item = container_item('Incomplete', id, title)
				}
				$("#append_container").append(item)
			})
		} else {
			$("#append_container").css('display', 'none')
		}
			
	
		const params = new URLSearchParams(window.location.search)
		let id = params.get('view_id')
		$("#" + id).addClass('past_container_active')
	}


	$.get('/container', {page: title}, function(data){
		$("#load_hide").remove()
		container_handler(data, title)
	})
}

const get_account_reps = id => {
	const account_reps_handler = (data) => {
		data = JSON.parse(data)
	}

	$.get(`/account_reps/${id}`, (data)=>{
		account_reps_handler(data)
	})
} 	

const InputMethods = class {
	populate_inputs (data, key) {
		$(`select[name=${key}]`).val(data[0][key]).digits()
		$(`input[name=${key}]`).val(data[0][key]).digits()
		$(`textarea[name=${key}]`).val(data[0][key]).digits()
	} //end populate_inputs

	populate_percent_tiles () {
		$('.in_box').each(function(){
			if ($(this).val() != "") {
				const target = $(this).parentsUntil('.hover_box').parent()
				target.not(target.children()).addClass('hover_box_selected')
			}
		})
	} // end populate_percent_tiles

	populate_tiles () {
		$('.hidden_input').each(function(){
			if ($(this).val() != '') {
				// check if multi or single hover_box
				const value = $(this).val()
				// const parent_hover = $(this).parent().parent().parent().parent().parent().parent().parent()
				let target_val;
				if ($(this).parent().parent().parent().parent().parent().parent().hasClass('hb_many')) {
					target_val = $(this).parent().parent().find(`h6:contains('${value}')`)
				} else {
					target_val = $(this).parent().siblings('.hover_box').children().children().children().find(`h6:contains('${value}')`)
				}
				const target = target_val.parentsUntil('.hover_box').parent()
				target.not(target.children()).addClass('hover_box_selected')
			}
		})
	} //end populate_tiles

	product_title (data)  {
		const product_name = data[0]['name']
		$('#product_name_target').text(product_name)
	}

	load_sales_cycle (data) {
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

		// $('.stages input').not('.stages input').addClass('hide')

		for (var i=0;i<stages.length;i++){
			var length = get_length(stages[i])
			for (var x=0;x<stages[i].length;x++){
				var toShow = $(".stage_container." + stages[i][x]['stage'] + " input").slice(0, length)
				toShow.removeClass('hide')
				if (toShow.val() !== stages[i][x]['tactic']){
					toShow.eq(x).val(stages[i][x]['tactic'])
				}
			} // come back
		}	
	} //end load_sales_cycle
}

const handle_past_inputs = class {

	constructor(data, url_path, debug) {
		function isJson(str) {
			try {
				JSON.parse(str);
			} catch (e) {
				return false;
			}
			return true;
		}

		let jsonTest = isJson(data)
		if (jsonTest == true) {
			let inputs = JSON.parse(data)
			this.data = inputs
			this.url_path = url_path
			this.debug = debug		
		} else {
			this.data = data
		}
	}


	compile(){
		let denied_responses = ['nah, not this time', 'nah']
		if (!denied_responses.includes(this.data)) {
			if (this.debug == true) {
				console.log(this.data)
			}

			let methods = new InputMethods;

			const loop_it = data => {
				Object.keys(data[0]).forEach(function(key) {
					let param = new URLSearchParams(window.location.search)	
					methods.populate_inputs(data, key)
				})
			}
			
			setTimeout(function(){
				methods.populate_tiles()
			}, 300)
			
			switch (this.url_path) {
				case '/competitors/company/audience/product/product_2/salescycle':
					methods.load_sales_cycle(this.data)
					break
				case '/competitors/company':
					loop_it(this.data)
					methods.populate_percent_tiles()
					break
				case '/competitors/company/audience/product/product_2':
					loop_it(this.data)
					methods.product_title(this.data)
					break
				default:
					loop_it(this.data)
			}	
		}
	}
}


const stage_interactions = () => {

	const handle_last_in_left = () => {
		alert('last of left')
	}

	const add_row = (active, last=false) => {
		const path_to_input = active.parent().parent().next().find('input')
		const condition = (active.val() != '')

		if (last == false) {
			if (condition) {
				path_to_input.removeClass('hide')
				path_to_input.focus()	
			}
		} else {
			const path_to_right_stage = active.parent().parent().parent().parent().parent().parent().next().find('tr:first-of-type > td > input')
			if (condition) {
				path_to_right_stage.removeClass("hide")
				path_to_right_stage.focus()
			}
		}
	}

	const remove_row = (active, on_right=false) => {
		const path_to_prev = active.parent().parent().prev().find('input')
		if (on_right == false) {
			active.addClass('hide')
			path_to_prev.focus()	
		} else {
			const path_to_last_stage = active.parent().parent().parent().parent().parent().parent().prev().find('tr:last-of-type > td > input')
			active.addClass('hide')
			path_to_last_stage.focus()
		}
	}

	const handle_enter = (event, active, row, path_to_input, stage_container) => {
        event.preventDefault()

        if (row.is(':not(:last-child)')){
        	add_row(active)
	    } else {
	        if (stage_container.hasClass('left_stage')){
	        	add_row(active, true)
	        } 
	    }
	}

	const handle_backspace = (event, active, row) => {
		const not_first_of_left = (row.is(":not(.left_stage tr:first-of-type)"))
		const not_first_of_right = (row.is(":not(.right_stage tr:first-of-type)"))

		if (active.val() == ''){
			event.preventDefault()
			if (not_first_of_left && not_first_of_right) {
				remove_row(active)
			} else if (!not_first_of_right) {
				remove_row(active, true)
			}
		}
	}

	$('.stage_container input').keydown(function(event){

	    const active = $(document.activeElement)
	    const row = active.parent().parent()
	    const path_to_input = active.parent().parent().next().find('input')
	    const stage_container = active.parent().parent().parent().parent().parent().parent()

	    const keycode = (event.keyCode ? event.keyCode : event.which)

	    switch(keycode) {
	    	case 13:
	    		handle_enter(event, active, row, path_to_input, stage_container)
	    		break
	    	case 8:
	    	case 46:
	    		handle_backspace(event, active, row)
	    		break
	    }
	});

}

export default class InitFuncs {

	container(title){
		get_container(title)
	}

	allIntake(params, url_path, disallowed_urls, debug, helpTimer){
		

		const hover_box = () => {
			$(".in_box").click(function(event){
				event.stopPropagation()
				if (!$(this).parent().parent().parent().parent().parent().parent().hasClass('hover_box_selected')) {
					$(this).parent().parent().parent().parent().parent().parent().addClass('hover_box_selected')
				}
				input_clicked = true
				return input_clicked
			})


			$('.platform_row img').click(function(){				
				let input = $(this).parent().find('.img_input'),
					siblings = $(this).siblings(),
					face = $(this),
					active = 'platform_row_img_active'

				siblings.removeClass(active)
				if (!face.hasClass(active)) {
					input.val($(this).index())
				} else {
					input.val("")
				}
				face.toggleClass(active)
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

		hover_box()

		$('.ignore_btn').click(function(event){
			event.preventDefault()
		})

		$('.ignore_default input').keydown(function(event){
			var keycode = (event.keyCode ? event.keyCode : event.which);

		    if(keycode == '13'){
		        event.preventDefault()
		    }
		})

		$('.reveal_button').click(function(){
			$('.reveal').fadeIn('slow')
			$(this).addClass("hidden")
		})

		setTimeout(function() { 
		    $('.need_help').fadeIn()
		}, helpTimer);

		var args = {}
		if (params.has('view_id')){
			args = {page: url_path,
					view_id: params.get('view_id')}
		} else {
			args = {page: url_path}
		}

		if (!disallowed_urls.includes(url_path)) {

			$.get('/load_past_inputs', args, function(data){
				const inputHandler = new handle_past_inputs(data, url_path, debug)
				if (inputHandler.data != "nah, not this time"){
					inputHandler.compile()
				}
			})

		}

	} // end all

	admin(){
		const get_admin_availability = () => {
			const admin_availability_handler = (data) => {
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
			}
		
			$.get('/admin_availability',function(data){
				admin_availability_handler(data)	
			})
		}
	} // end admin

	company() {

		var perc_format = $('.perc_format')
		var in_box = $('.in_box')

		$(in_box).each(function(){
			var this_hb = $(this).parent()
			if ($(this).val() == ""){
				this_hb.removeClass('hover_box_selected')
			}
		})

		const get_sum = () => {
			let sums = 0
			$(".percent").each(function(){
				let val = parseInt($(this).val())

			    if (!Number.isNaN(val)){
			    	sums += val;	
				}
			});
			return sums
		}

		const sum_and_populate = (sums) => {

			$(".perc").text(sums)

			const percent = parseInt($('.perc').text())
			const selector = $('.container.counter')

			if (percent == 100) {
				selector.removeClass('red')
				selector.addClass('green')
			} else if (percent > 100) {
				selector.addClass('red')
				selector.removeClass('green')
			} else {
				selector.removeClass('red')
				selector.removeClass('green')
			}
		}

		const init_sum = get_sum()
	    let target = $('.percent').parentsUntil('.row').parent()
	    target = target.not(target.children())
	    target.after(perc_container)

	    sum_and_populate(get_sum())

	    $(".percent").keyup(function(){
			sum_and_populate(get_sum())
		})
	} // end company

	company_view() {
		var pathname = window.location.pathname;
		$('.dyn_link').each(function(){
			var id = $(this).attr('id')
			var url = pathname + "?page=" + id
			$(this).attr('href', url)
		})
	}

	create_account() {
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
			get_account_availability()
			var testEmail = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i;
			if (testEmail.test($('#email').val())){
				$('.format').text(' ')
			} else {
				$('.format').text('invalid email format')
			}
		}, 1000));
	} // end create account

	customers(){	

		$('#account_reps').click(function(){
			const id = $(this).attr('id')
			$('#current_reps').empty()
			get_account_reps(id)
		})
	}


	personnel(){
		$('#account_reps').click(function(){
			const id = $(this).attr('id')
			$('#current_reps').empty()
			get_account_reps(id)
		})
	} // end personnel

	platforms(){
		const get_platforms = () => {
			const platforms_handler = data => {
				let x = 0
				for (let i = 0; i < data.length; i++){
					if (data[i] != ""){
						let row = platform_row(data[i], x)
						x++
						$('.platforms_container').append(row)
					}
				}
				let length = $(".platform_row").length
				$('#platform_length').val(length)
			}
		
			$.get('/get_platforms', function(data){
				$("#load_hide").remove()
				platforms_handler(JSON.parse(data))
			})
		}
		get_platforms()
	} // end platforms

	products(i){
		const get_branch_data = () => {
			const FormMap = class {
				constructor(selling_to, biz_model) {
					this.selling_to = selling_to
					this.biz_model = biz_model
				}
			
				build_form() {
					let test;
					switch (this.selling_to) {
						case 'B2C':
							test = 'hi'
							break
						case 'B2B':
							break
						case 'C2C':
							break
						case 'other':
							break
					}
			
					switch (this.biz_model) {
						case 'SaaS':
							break
						case 'Digital Products':
							break
						case 'Tangible Product':
							break
						case 'Professional Services':
							break
						case 'Manual Services':
							break
						case 'Media Provider':
							break
						case 'Commission / Rev Share':
							$("#heading-7").addClass('hidden')
							break
					}
			
			
					$("#heading-1").text('Product name')
		
			
				}
			}	
		
			const branch_data_handler = data => {
				data = JSON.parse(data)
				const map = new FormMap(data.selling_to, data.biz_model)
				map.build_form()
			}
		
			$.get('/branch_data', function(data){
				branch_data_handler(data)
			})
		}

		get_branch_data()

		$("#product_table label").not('th > label').remove()

		$(".edit_product").click(function(e){
			e.preventDefault()

			const handle_click = (e, i) => {
				if ($(this).hasClass("add_product")){
					let clone = $('.data-row').last().clone()
					
					let new_id = `data-row-${i}`
					clone.attr('id', new_id)

					let route = `td > .form-group > ul > li > table`
					let sub_route = ' > tbody > tr'

					const clone_selector = (pos, el='input') => clone.find(route + sub_route + `:nth-of-type(${pos}) > td > ` + el)
					const change_attr = (selector, name) => selector.attr('name', name).attr('id', name)

					let base_id = `product-${i}-`,
						name_id = base_id + "name",
						category_id = base_id + "category",
						cogs_id = base_id + "cogs",
						sales_price_id = base_id + "sales_price",
						price_model_id = base_id + "price_model",
						qty_sold_id = base_id + "qty_sold",
						est_unique_buyers_id = base_id + "est_unique_buyers",
						csrf_id = base_id + "csrf_token"


					clone.find(route).attr('id', `product-${i}`)

					change_attr(clone_selector(1), name_id)
					change_attr(clone_selector(2), category_id)
					change_attr(clone_selector(3), cogs_id)
					change_attr(clone_selector(4), sales_price_id)
					change_attr(clone_selector(5, 'select'), price_model_id)
					change_attr(clone_selector(6), qty_sold_id)
					change_attr(clone_selector(7), est_unique_buyers_id)
					change_attr(clone.find(route).siblings('input'), csrf_id)

					$('.tbody').append("<div class='product_separator separator'></div>")
					$('.tbody').append(clone)

				} else if ($(this).hasClass('remove_product')){
					if (i > 1){
						let last = $('.data-row').last()
						let last_sep = $(".product_separator").last()
						last.remove()
						last_sep.remove()
					}
				}		
			}

			let i = $("#product_table > tbody > .data-row").length
			handle_click(e, i)
		})

	}


	salescycle(){

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

		$('.left_stage').addClass("stages")
		$('.right_stage').addClass('stages')


		const row_select = $(".stages.left_stage tr")
		const right_rows = $(".stages.right_stage input")
		row_select.not(":first-child").find('input').addClass('hide')
		right_rows.addClass("hide")

		// in eventHandlers.js
		stage_interactions()
	} //end salescycle
}
