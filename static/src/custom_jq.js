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