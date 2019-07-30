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

const InputMethods = class {
	populate_inputs = (data, key) => {
		$(`select[name=${key}]`).val(data[0][key]).digits()
		$(`input[name=${key}]`).val(data[0][key]).digits()
		$(`textarea[name=${key}]`).val(data[0][key]).digits()
	} //end populate_inputs

	populate_percent_tiles = () => {
		$('.in_box').each(function(){
			if ($(this).val() != "") {
				const target = $(this).parentsUntil('.hover_box').parent()
				target.not(target.children()).addClass('hover_box_selected')
			}
		})
	} // end populate_percent_tiles

	populate_tiles = () => {
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

	product_title = (data) => {
		const product_name = data[0]['name']
		$('#product_name_target').text(product_name)
	}

	load_sales_cycle = (data) => {
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

function isJson(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

const handle_past_inputs = class {

	constructor(data, url_path, debug) {
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



const account_reps_handler = (data) => {
	data = JSON.parse(data)
	console.log(data)
	// Object.keys(data).forEach(function(key){
	// 	let rep = rep_name(data[key].name)
	// 	$('#current_reps').append(rep)
	// })
}



const account_availability_handler = (data) => {
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


const product_list_handler = (data) => {
	var data = JSON.parse(data)

	for (var i=0;i<data.data;i++){
		let current_name = data[i]['name']
		let product_name = product_container(data[i]['name'])
		$('.product_prev_container').append(product_name)
	}

	$('.product_container:nth-of-type(1)').addClass('product_container_active')
	$('#product-name').text(data[0]['name'])

	$('#p_id').val(data[0]['p_id'])

	localStorage.setItem('data', JSON.stringify(data));
}


const container_handler = (data, title) => {
	data = JSON.parse(data)

	Object.keys(data).forEach(function(key){
		let id = data[key]['id']
		let name = data[key]['name']
		
		let item;
		if (name != null && name != "") {
			item = container_item(name, id, title)
		} else {
			item = container_item('still working...', id, title)
		}
		$("#append_container").append(item)
	})

	const params = new URLSearchParams(window.location.search)
	let id = params.get('view_id')
	$("#" + id).addClass('past_container_active')
}


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

	// 	$("#body-1").append(product_cell('input', ))
	// 	$("#body-2").append('Category')
	// 	$("#body-3").append('COGS')
	// 	$("#body-4").append('Sales Price')
	// 	$("#body-5").append('Price Model')
	// 	$("#body-6").append('Qty Sold Last 12 Mos.')
	// 	$("#body-7").append('Estimated Unique Buyers')

	}
}

const branch_data_handler = data => {
	data = JSON.parse(data)
	const map = new FormMap(data.selling_to, data.biz_model)
	map.build_form()
}

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








