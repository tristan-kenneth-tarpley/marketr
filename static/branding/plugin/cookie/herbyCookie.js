/*
* herbyCookie jQuery plugin v1.3.2
*
* An easy jQuery plugin asking at user for cookie consent.
*
* Copyright (c) 2015 Paolo Basso
* https://github.com/paolobasso99/herbyCookie
* Licensed under the MIT license
* If you use hebyCookie you agree with our Terms of Service (https://github.com/paolobasso99/herbyCookie/blob/master/TermsOfService.md).
*/
(function ( $ ) {
 
    $.fn.herbyCookie = function( options ) {
 
        // Options
        var settings = $.extend({
            style: "dark",
            btnText: "Got it!",
            policyText: "Privacy policy",
            text: "We use cookies to ensure you get the best experience on our website, if you continue to browse you'll be acconsent with our",
            scroll: false,
            expireDays: 30,
            link: "/policy.html"
        }, options );
        
        // Html
        var herbyHtml = "<div class='herbyCookieConsent herbyIn'><p>"+settings.text+" "+"<a alt='"+settings.policyText+"' href='"+settings.link+"' target='_blank'>"+settings.policyText+"</a>.</p><a alt='"+settings.btnText+"' class='herbyBtn'>"+settings.btnText+"</a></div>";
        
        // Set localStorage
        var herbyName = "herbyCookie"+"_"+window.location.hostname;
        var herbyStorage = JSON.parse(localStorage.getItem(herbyName));
        var herbyActualDate = Math.floor((new Date()).getTime() / 1000);
        
        // Open functions
        if(herbyStorage == null || herbyStorage.consens != true || herbyStorage.expireTime < herbyActualDate){
            $("body").append(herbyHtml);
        }
        
        
        // Close functions
        $(".herbyBtn").click(closeHerby);
        if(settings.scroll == true) {
            $(window).scroll(closeHerby);
        }
        
        function closeHerby() {
            // Set localStorage
            var herbyExpireDate = (herbyActualDate+(settings.expireDays*86400));
            var herbyJson = {consens : true, expireTime : herbyExpireDate};
            localStorage.setItem(herbyName, JSON.stringify(herbyJson));
            
            // Remove the Obj
            $(".herbyCookieConsent").removeClass("herbyIn").addClass("herbyOut");
            setTimeout(
                function() {
                    $(".herbyCookieConsent").remove();
                },
            1001);
        }
        
        if(typeof settings.scroll != "boolean") {
            console.error('hebyCookie: Invalid "scroll" option. Use a boolean value.');
        }
        if(isNaN(settings.expireDays)) {
            console.error('hebyCookie: Invalid "expireDays" option. Use a number.');
        }
        
    };
    
}(jQuery));
