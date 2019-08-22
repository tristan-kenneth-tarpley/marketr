const perc_container = `
			<div style="text-align: center;" class="container counter">
	        	<span style="font-size:120%" class="perc"></span>%
	    	</div>
	    	`

const rep_name = (copy) => {
	return `<li style="color:var(--body-copy);">${copy}</li>`
}

const product_container = (copy) => {
	return `<div class='col-lg-3 col-md-3 col-sm-3 product_container'><p>${copy}</p></div>`
}

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

const product_cell = (type, name) => {
	switch (type) {
		case 'input':
			return input
			break
		case 'dropdown':
			break
	}
}


const platform_row = (name, index) => {
	const el = `<div class="row platform_row">
					<div class='col-lg-2 col-sm-12 col-12'>
						<h5 style="text-align:center;" class="title"><span class="platform_img">${name}</span></h5>
						<input style="display:none;" type='text' value='${name}' name='platform[${index}]'>
					</div>
					<div style="text-align:center;" class='col-lg-4 col-md-4 col-sm-6 col-6'>
						<h6>Still using?</h6><br>
						<div class="container row col-12">
							<div class='hover_box col-lg-5 col-md-5'>
								<h6>yes</h6>
							</div>
							&nbsp;
							<div class='hover_box col-lg-5 col-md-5'>
								<h6>no</h6>
							</div>
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


const chat_box = (copy, time, date) => {
	
	const el = `
				<div class="message_container">
					<div class="chat_label">
						<p><strong>${date} ${time}</strong></p>
					</div>
					<div class="chat_box chat-user">
						${copy}
					</div>
				</div>
				`
	return el
}


const taskView = title => {
	const el = `
			<tr class="editable_task">
				<td>
					<div class="form-check">
						<label class="form-check-label">
							<input class="form-check-input" type="checkbox">
							<span class="form-check-sign"></span>
						</label>
					</div>
				</td>
				<td class="text-left task_title">
					<p id="task_title">${title}</p>
				</td>
				<td class="td-actions text-right">
					<button type="button" rel="tooltip" title="" class="btn btn-danger btn-round btn-icon btn-icon-mini btn-neutral" data-original-title="Remove">
						<i class="now-ui-icons ui-1_simple-remove"></i>
					</button>
				</td>
			</tr>`
	return el
}

const notificationEl = (type, copy, admin) => {
	let link;
	if (admin == false){
		switch(type){
			case 'message':
				link = "/home?view=messages"
				break
			case 'task':
				link = "/home?view=campaigns"
				break
			case 'insight':
				link = "/home?view=campaigns#insights"
				break
		}
	} else {
		link = "#"
	}
	const el = `<a href="${link}" class="notification dropdown-item text-warning">New ${type}: ${copy}</a>`
	return el
}