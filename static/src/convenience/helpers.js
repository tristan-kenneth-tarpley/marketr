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


const isNumber = input => typeof input == 'number'


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



function html(elemName, props, ...children) {
    const elem = document.createElement(elemName);
    if (props) {
        Object.assign(elem, props);
    }
    if (children) {
        children.forEach(child => {
        if (typeof child === 'object') {
            elem.appendChild(child);
        } else {
            elem.appendChild(document.createTextNode(child));
        }
        });
    }
    return elem;
}

const setQueryString = (name, value) => {
	const params = new URLSearchParams(location.search);
	params.set(name, value);
	window.history.replaceState({}, "", decodeURIComponent(`${location.pathname}?${params}`));
}

const params = () => new URLSearchParams(location.search);

// Create a new event
const query_change = new CustomEvent('query_change');

const currency = num => `$${num.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`
const currency_rounded = num => `$${num.toFixed().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`
const number = num => num.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",")
const number_no_commas = num => num.toFixed().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
const percent = num => `${num.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",")}%`
const remove_commas = num => num.toFixed(2).replace(/\,/g, '')
const remove_commas_2 = num => parseFloat(num.replace(/\,/g,''))

const now = () => {
    let date = new Date();
    let dateString = new Date(date.getTime() - (date.getTimezoneOffset() * 60000 ))
                        .toISOString()
                        .split("T")[0];
    return dateString
} 