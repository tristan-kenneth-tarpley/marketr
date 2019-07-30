function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

$.fn.digits = function(){ 
    return this.each(function(){ 
    	const id = $(this).attr('id')
    	const not_included = ['zip']
    	if (!not_included.includes(id)) {
       		$(this).val( $(this).val().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,") );
    	} 
    })
}

const print = copy => console.log(copy)

const smilesMapper = (name) => {
	let path = "/static/assets/img/"
	let map = {
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
	let url = path + map[name]
	return url
}

const PageMap = (route) => {
	const map = {
		"/begin": "begin",
		"/competitors": "competitors",
		"/competitors/company": "company",
		"/competitors/company/audience": "audience",
		"/competitors/company/audience/product": "product",
		"/competitors/company/audience/product/product_2": "product_2",
		"/competitors/company/audience/product/product_2/salescycle": "salescycle",
		"/goals": "goals",
		"/history": "history",
		"/history/platforms": "platforms",
		"/history/platforms/past": "past",
		// done with intake routes
		"/home": "home",
		"/customers": "customers",
		"/admin": "admin",
		"/personnel": "personnel",
		"/new": "new",
		"/create": "create"
	}

	function hasNumber(myString) {
		return /\d/.test(myString);
	}
	
	if (route.substring(0, 10) == "/customers" && hasNumber(route)){
		return 'customers'
	} else {
		return map[route]
	}
}