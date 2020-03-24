import Tactics from './tactics.js';
import Portfolio from './campaigns.js';
import cta from './campaign_cta.js';
import {Achievements, Store, Rewards} from './gamify.js'
import {IntakeProgressMeter, CoreViewModels, AuditRequest, PriceViewModel, AuditViewModel, WalletViewModel} from './ViewModels.js'
import {PaymentsService} from './services.js'
import {isNumber, validateEmail} from './convenience/helpers.js'
import InitFuncs from './future_refactor/InitFuncs.js'
import {select_controller} from '/static/src/components/UI_elements.js'


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

const Controller = class {
	constructor(debug, url_path, params, helpTimer) {
		this.debug = debug
		this.url_path = url_path
		this.params = params
		this.noValLoad = ['/home',
							'/',
							'/new',
							'/admin',
							'/admin/branch',
							'class',
							'splash']
		this.intake = [
						'/begin',
						'/competitors',
						'/competitors/company',
						'/competitors/company/audience',
						'/competitors/company/audience/product',
						'/competitors/company/audience/product/product_2',
						'/competitors/company/audience/product/product_2/salescycle',
						'/goals',
						'/history',
						'/history/platforms',
						'/history/platforms/past',
						'/create',
						]
		this.helpTimer = helpTimer
	}

 	PageMap (route) {
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
			"/demo": "demo",
			"/home": "home",
			"/customers": "customers",
			"/admin": "admin",
			"/personnel": "personnel",
			"/new": "new",
			"/create": "create",
			"/payments": "payments",
			"/pricing": "pricing",
			'/': 'index',
			'/home/settings': 'settings'
		}

		function hasNumber(myString) {
			return /\d/.test(myString);
		}
		if (route.substring(0, 10) == "/customers" && hasNumber(route)){
			
			if (route.substring(27) == '/ad_audit' && hasNumber(route)) {
				return 'audit'
			} else {
				return 'customers'
			}
		}
		else {
			return map[route]
		}
	}

	run() {
		select_controller()
		if (this.intake.includes(this.url_path)){
			const run_page = (resolve, reject) => {
				const init = new InitFuncs()
				const progress = new IntakeProgressMeter()
				switch (this.PageMap(this.url_path)) {
					case 'audience':
						init.container('audience')
						break
					case 'begin':
						progress.fill(1)
						break
					case 'competitors':
						progress.fill(2)
						break
					case 'company':
						progress.fill(3)
						setTimeout(() => {
							init.company()
						}, 1000)
						break
					case 'salescycle':
						init.salescycle()
						break
					case 'product':
						init.products()
						break
					case 'product_2':
						init.container('product_2')
						break
					case 'platforms':
						init.platforms()
						break		
				}
				resolve(init)	
			}

			const set_page = () => new Promise((resolve, reject) => {
				return run_page(resolve)
			})

			set_page()
				.then(resolve => {
					setTimeout(()=> {
						resolve.allIntake(this.params, this.url_path, this.noValLoad, this.debug, this.helpTimer)
					}, 1000)		
				})

		} else {
			const init = new InitFuncs()
			const view_model = new CoreViewModels(this.url_path)
			const game = new Achievements()
			const rewards = new Rewards()
			const store = new Store(rewards)
			
			if (this.url_path.slice(1,9) == 'checkout') {
				let payments = new PaymentsService()
				payments.process()
			}

			switch(this.url_path){
				case '/home':
				case '/home/achievements':
				case '/home/settings':
					game.lets_play()
					game.poll()
					store.init()
					break
			}
						
			switch(this.PageMap(this.url_path)) {
				case 'admin':
					init.company_view()
					break
				case 'new':
					init.create_account()
					break
				case 'personnel':
					init.personnel()	
					break
				case 'customers':
					view_model.tasks()
					view_model.messages()
					view_model.dashboard()
					view_model.dashboard()
					view_model.sync_data()
					view_model.set_real_customer()
					
					break
				case 'audit':
					view_model.tasks()
					view_model.messages()
					view_model.dashboard()
					
					const audit = new AuditViewModel()
					break
				case 'pricing':
				case 'index':
				case 'settings':
					const _cta = new cta()
					_cta.init()
					const pricing = new PriceViewModel()
					pricing.init()
					const audit_request = new AuditRequest()
					audit_request.ready()
					break
				case 'demo':
				case 'home':
					// const tactics = new Tactics(this.params)

					view_model.dashboard()
					view_model.messages()
					view_model.tabs()
					view_model.tasks()

					$(function () {
						$('[data-toggle="popover"]').popover()
					})
					break
			}
		}
	}
}



$(window).on("load", function() {
	$("#loading").fadeOut("fast");
	setTimeout(function(){
		$('#content-ready').css('visibility', 'visible')
	}, 300)
});


const callback = function(){
	const config = {
		debug: false,
		helpTimer: 400000
	}
	const VC = new Controller(
		config.debug,
		window.location.pathname,
		new URLSearchParams(window.location.search),
		config.helpTimer
	);
	VC.run()
};
  


if (
	document.readyState === "complete" ||
	(document.readyState !== "loading" && !document.documentElement.doScroll)
) {
	callback();
} else {
	document.addEventListener("DOMContentLoaded", callback);
}






