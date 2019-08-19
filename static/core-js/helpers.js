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
		"linkedin": "LinkedIn.png",
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
		"/create": "create",
		"/payments": "payments"
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


function updateURLParameter(url, param, paramVal)
{
    var TheAnchor = null;
    var newAdditionalURL = "";
    var tempArray = url.split("?");
    var baseURL = tempArray[0];
    var additionalURL = tempArray[1];
    var temp = "";

    if (additionalURL) 
    {
        var tmpAnchor = additionalURL.split("#");
        var TheParams = tmpAnchor[0];
            TheAnchor = tmpAnchor[1];
        if(TheAnchor)
            additionalURL = TheParams;

        tempArray = additionalURL.split("&");

        for (var i=0; i<tempArray.length; i++)
        {
            if(tempArray[i].split('=')[0] != param)
            {
                newAdditionalURL += temp + tempArray[i];
                temp = "&";
            }
        }        
    }
    else
    {
        var tmpAnchor = baseURL.split("#");
        var TheParams = tmpAnchor[0];
            TheAnchor  = tmpAnchor[1];

        if(TheParams)
            baseURL = TheParams;
    }

    if(TheAnchor)
        paramVal += "#" + TheAnchor;

    var rows_txt = temp + "" + param + "=" + paramVal;
    return baseURL + "?" + newAdditionalURL + rows_txt;
}