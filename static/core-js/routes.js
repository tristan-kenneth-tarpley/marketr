const get_past_inputs = (args, url_path, debug) => {
	$.get('/load_past_inputs', args, function(data){
		const inputHandler = new handle_past_inputs(data, url_path, debug)
		if (inputHandler.data != "nah, not this time"){
			inputHandler.compile()
		}
	})
}

const get_admin_availability = () => {
	$.get('/admin_availability',function(data){
		admin_availability_handler(data)	
	})
}


const get_account_reps = id => {
	$.get(`/account_reps/${id}`, (data)=>{
		account_reps_handler(data)
	})
} 


const get_account_availability = email => {
	$.get('/availability', {email: email}, function(data){
		let available = get_account_availability_handler(data)
		if (available == false) {
			$('.submit_button').attr('disabled', true)
		} else {
			$('.submit_button').attr('disabled', false)
		}
	})
} 

const get_container = title => {
	$.get('/container', {page: title}, function(data){
		$("#load_hide").remove()
		container_handler(data, title)
	})
}

const get_branch_data = () => {
	$.get('/branch_data', function(data){
		branch_data_handler(data)
	})
}

const get_platforms = () => {
	$.get('/get_platforms', function(data){
		$("#load_hide").remove()
		platforms_handler(JSON.parse(data))
	})
}
