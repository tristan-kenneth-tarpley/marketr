const InitFuncs = class {

	container(title){
		get_container(title)
	}

	allIntake(params, url_path, disallowed_urls, debug, helpTimer){
		// const motivations = [
		// 	"You're doing great! Remember, if you need a break, you can always log out and come back later.",
		// 	"Your progress is saved! If you need to leave, you'll pick up right where you left off.",
		// 	"You're getting so close! Pretty soon, we'll have everything we need to be able to skyrocket your marketing.",
		// 	"",
		// 	"",
		// 	"",
		// 	"",
		// 	"",
		// 	"Did you know: Charles Darwin’s personal pet tortoise didn’t die until 2006.",
		// 	"Did you know: The average person will spend six months of their life waiting for red lights to turn green.",
		// 	"Market(r) uses sophisticated algorithms to grow businesses around the country. All of this is vital information!",
		// 	"Did you know: Marie Curie’s notebooks are still radioactive."
		// ]
		// const line = motivations[Math.floor(Math.random()*motivations.length)];
		// if (line != "" && !params.has('home')){
		// 	$(".motivation_container").fadeIn(()=>{
		// 		$(".motivation_container p").text(line)
		// 	})
		// }


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
			get_past_inputs(args, url_path, debug)
		}

	} // end all

	admin(){
		get_admin_availability()
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
		get_platforms()
	} // end platforms

	products(i){
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





const PageViewController = class {
	constructor(debug, url_path, params, helpTimer) {
		this.debug = debug
		this.url_path = url_path
		this.params = params
		this.noValLoad = ['/home',
							'/',
							'/new',
							'/admin',
							'/admin/branch',
							'class',
							'splash']
		this.intake = [
						'/begin',
						'/competitors',
						'/competitors/company',
						'/competitors/company/audience',
						'/competitors/company/audience/product',
						'/competitors/company/audience/product/product_2',
						'/competitors/company/audience/product/product_2/salescycle',
						'/goals',
						'/history',
						'/history/platforms',
						'/history/platforms/past',
						'/create',
						]
		this.helpTimer = helpTimer
	}

	run() {


		if (this.intake.includes(this.url_path)){

			const run_page = (resolve, reject) => {
				const init = new InitFuncs()
				const progress = new IntakeProgressMeter()
				switch (PageMap(this.url_path)) {
					case 'audience':
						init.container('audience')
						break
					case 'begin':
						progress.fill(1)
						break
					case 'competitors':
						progress.fill(2)
						break
					case 'company':
						progress.fill(3)
						setTimeout(() => {
							init.company()
						}, 1000)
						break
					case 'salescycle':
						init.salescycle()
						break
					case '/create':
						init_creative()
						break
					case 'product':
						init.products()
						break
					case 'product_2':
						init.container('product_2')
						break
					case 'platforms':
						init.platforms()
						break		
				}
				resolve(init)	
			}

			const set_page = () => new Promise((resolve, reject) => {
				return run_page(resolve)
			})

			set_page()
				.then(resolve => {
					setTimeout(()=> {
						resolve.allIntake(this.params, this.url_path, this.noValLoad, this.debug, this.helpTimer)
					}, 1000)		
				})

		} else {
			const init = new InitFuncs()
			const view_model = new CoreViewModels(this.url_path)

			switch(this.url_path.slice(15)) {
				case 'profile':
					view_model.score()
					break
			}

			if (this.url_path.slice(15) == 'profile' || this.url_path.slice(1,5) =='home') {
				view_model.score()
				view_model.notifications()
			}
			
			if (this.url_path.slice(1,9) == 'checkout') {
				let payments = new PaymentsService()
				payments.process()
			}

			if (this.url_path.includes('settings')) {
				let Wallet = new WalletViewModel()
				Wallet.add_validation()
			}
						
			switch(PageMap(this.url_path)) {
				case 'admin':
					init.company_view()
					break
				case 'new':
					init.create_account()
					break
				case 'personnel':
					init.personnel()	
					break
				case 'customers':
					view_model.tasks()
					view_model.messages()
					view_model.dashboard()
					break
				case 'audit':
					view_model.tasks()
					view_model.messages()
					view_model.dashboard()
					const audit = new AuditViewModel()
					break
				case 'pricing':
				case 'index':
				case 'settings':
					const pricing = new PriceViewModel()
					pricing.init()
					break
				case 'home':
					view_model.dashboard()
					view_model.messages()
					view_model.tabs()
					view_model.tasks()
					$(function () {
						$('[data-toggle="popover"]').popover()
					})
					break
			}
		}
	}
}










$(document).ready(() => {
	const params = new URLSearchParams(window.location.search)
	const config = {
		debug: false,
		helpTimer: 400000,
	}
	const VC = new PageViewController(
		config.debug,
		window.location.pathname,
		new URLSearchParams(window.location.search),
		config.helpTimer
	);
	VC.run()
})





