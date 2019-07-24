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