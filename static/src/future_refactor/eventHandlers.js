$(window).on("load", function() {
	$("#loading").fadeOut("fast");
	setTimeout(function(){
		$('#content-ready').css('visibility', 'visible')
	}, 300)
});

$("#xx, #wogf").on("click",function(event){
	 const target = event.target || event.srcElement;
	 switch(target.id)
	 {
	    case "xx":
	     	$(this).parent().remove()
	    case "wogf":
	    	$("#warranties_or_guarantee_freeform").focus()
	    break;
	 }
});

$('#new_email').on("blur", (event) => {
	let email = $("#new_email").val()
	if (validateEmail(email)){
		$("#new_email").removeClass('input-danger')
		document.querySelector('#email_availability').innerHTML = ""
		get_account_availability(email)

	} else {
		$("#new_email").addClass('input-danger')
		document.querySelector("#email_availability").innerHTML = '<p>Email is invalid</p>'
		$('.submit_button').attr('disabled', true)
	}
})

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


