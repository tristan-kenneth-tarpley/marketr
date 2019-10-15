const IntakeProgressMeter = class {
    constructor() {
        $('.progress_meter-container').css('display', 'block')
    }
    fill(step){
        const target = `.progress_meter div:nth-of-type(${step})`
        $(target).css('background-color', '#62cde0')
        $(target).addClass('slide_in')

        $(".indicator").text(`step ${step}/3`)
    }
}

const CoreViewModels = class {

	constructor(url_path) {
        this.url_path = url_path
        if (this.url_path.slice(1,10) == 'customers') {
            this.admin = true
        } else {
            this.admin = false
        }
    }

    left_nav_update(e) {
        let target = $(e.currentTarget)
        let id = target.attr('id')
        let nav_target,
            param_val;
        switch (id) {
            case "profile-tab":
                nav_target = $("#profile-nav")
                param_val = "profile"
                break
            case "campaigns-tab":
                nav_target = $("#campaigns-nav")
                param_val = "campaigns"
                break
            case "messages-tab":
                nav_target = $("#messages-nav")
                param_val = "messages"
                break
        }
        let new_url = updateURLParameter(this.url_path, 'view', param_val)
        history.pushState(null, null, new_url)
        
        nav_target.removeClass('hidden')
        $(".sidebar-wrapper div").not(nav_target).addClass('hidden')
    }

    tabs() {

        let url_string = window.location.href,
            url = new URL(url_string),
            view = url.searchParams.get("view");
         
        let tab_target;
        switch(view) {
            case 'profile':
                tab_target = "#profile"
                break
            case null:
            case 'campaigns':
                tab_target = "#campaigns"
                break
            case 'messages':
                tab_target = "#messages"
                break
        }

        $(tab_target).addClass('active')

        $(".tab-link").click(e=>{
            this.left_nav_update(e)
        }) 
        $(".tab-pane").not(tab_target).removeClass('active')
        $(`.nav-tabs`).find(`a[href='${tab_target}']`).addClass('active')
        $(".nav-tabs").find(`a`).not(`a[href='${tab_target}']`).removeClass('active') 
    }


    dashboard() {

        $('.truncate').each(function(){
            var full_text = $(this).text()
            // $(this).after("<p class='full_text'>" + full_text + "</p>")
            if ($(this).text().length > 49){
                var truncated_text = $(this).text()
                    .trim()    // remove leading and trailing spaces
                    .substring(0, 50)    // get first 600 characters
                    .split(" ") // separate characters into an array of words
                    .slice(0, -1)    // remove the last full or partial word
                    .join(" ") + "..."; // combine into a single string and append "..."
                $(this).html("<span class='daText'>" + truncated_text + "</span> <span class='showAll'>Show more</span>")
                $('.showAll').click(function(){
                    $(this).toggleClass('clicked')
                    if ($(this).hasClass('clicked')){
                        $(this).siblings('.daText').html(full_text)
                        $(this).html("<span class='showAll'>See less</span>")
                    } else {
                        $(this).siblings('.daText').html(truncated_text)
                        $(this).html("<span class='showAll'>Show more</span>")
                    }
                })
            }
        })
        
        
        $('.results_img').each(function(){
            var val = parseInt($(this).text())
            if (val == 2){
                $(this).html('<img class="smilesHome" src="/static/assets/img/frown.png">')
            } else if (val == 3){
                $(this).html('<img class="smilesHome" src="/static/assets/img/neutral.png">')
            } else if (val == 4){
                $(this).html('<img class="smilesHome" src="/static/assets/img/smile.png">')
            } else if (val == 5){
                $(this).html('<img class="smilesHome" src="/static/assets/img/grin.png">')
            }
        })
        
        $(".platform_img").each(function(){
            var platform = $(this).text().replace(/^\s+/g, '').replace(/\s+$/g, '');
            var img = smilesMapper(platform)
            $(this).html(`<img class="smilesHome" src='${img}'>`)
        })
        
        $('.meter').each(function(){
            var perc = parseInt($(this).text().replace('%',''))
            $(this).addClass('special')
            $(this).find('.perc_width').css('width', perc+"%")
        })
        
        $('.sub_nav a').click(function(){
            $(document).unbind("scroll")
            $(this).addClass('targeted')
            $('.sub_nav a').not(this).removeClass('targeted')
            setTimeout(function(){ 
                $(document).bind('scroll',function(e){
                    assign_hash()
                });
            }, 1000);
        })

        const assign_hash = () => {
            $('.target').each((index, element)=> {
                if (
                   $(element).offset().top < window.pageYOffset + 10
                && $(element).offset().top + $(element).height() > window.pageYOffset + 10
                && $(element).attr('id') != "" 
                ) {
                    window.location.hash = $(element).attr('id');
                }
            });
        }

        const change_nav_active = () => {
            const hash = window.location.hash.substring(1)
            let target = `a.${hash}`
            $('a').not(target).removeClass('targeted')
            $(target).addClass("targeted")
        }

        $(document).on('scroll', e => {
            assign_hash()
        });
        
        $(window).on('hashchange', () => {
            change_nav_active()
        });
        
        $(window).on('load', e => {
            const show_nav = target => {
                $(`#${target}`).addClass('active')
                $(`#${target}-tab`).addClass('active')
                $(`#${target}-tab`).addClass('show')
                $(`#${target}-nav`).removeClass('hidden')
            }
            
            const urlParams = new URLSearchParams(window.location.search);
            let view = urlParams.get('view') != null ? urlParams.get('view') : 'campaigns'
            $(".sidebar-wrapper div").addClass('hidden')
            show_nav(view)
        })
    }

    score() {
        const score = new ScoreService(this.url_path, this.admin)
        score.get()
    }

    notifications() {
        const notifications = new NotificationsService(this.url_path, this.admin)
        notifications.get()

        $("#notification_list").click(()=>{
            if ($(".notification_count").text() != "") {
                $(".notification_count").remove()
            }
        })
    }
    

	tasks() {
        $("#add_task").click(() => {
            const tasks = new TaskService(this.url_path)
            tasks.add()
        })
        $(".task_complete").change(event=>{
            const $this = $(event.currentTarget)
            if($this.prop('checked')) {
                const tasks = new TaskService(this.url_path)
                let val = $this.parent().parent().parent().next().html().trim() //.replace(/^\s+/g, '').replace(/\s+$/g, '');;
                val = val.slice(19,(val.length-4))
                tasks.complete(val)
            }
        })
        $("#remove_task").click((event)=>{
            const tasks = new TaskService(this.url_path)
            const $this = $(event.currentTarget)
            const val = $this.parent().prev().text().replace(/^\s+/g, '').replace(/\s+$/g, '');

            console.log(val)
            tasks.remove(val)
            $this.parent().parent().remove()
        })
    }

    messages() {
        const send_message = () => {
            const messagingService = new MessagingService(this.url_path)
            const msg = $("#msg").val()
            messagingService.send(msg)  
        }

        $("#send_msg").click(() => {
            send_message()
        })

        $('#msg').keydown(event=>{
            let keycode = (event.keyCode ? event.keyCode : event.which);
            if(keycode == '13' && $("#msg").is(":focus")){
                send_message()
            }
        })
    }
}





const PriceViewModel = class {
    constructor(){
        $('input').on('change, keyup', e => {
            let currentInput = $(e.currentTarget).val();
            let fixedInput = currentInput.replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",")
            $(e.currentTarget).val(fixedInput);
        });
    }
    num_commas (num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); 
    }
    calc_fee (base_fee, spend, perc_of_spend) {
        return (base_fee + (spend * perc_of_spend)).toFixed(2)
    } 
    marketr_model(spend){
        let fee;
        if (spend < 250){ return 1 }
        else if (spend >= 250 && spend < 5000){ fee = 395 }
        else if (spend >= 5000){ fee = 1495 }
        return fee
    }
    marketr_test_model(tests){
        let cost_per_test = 195
        if (tests == 1) { return 1 }
        else if (tests >= 1) { return cost_per_test * tests }
    }

    competitors(spend, competitor){
        const wordstream = spend => {
            const base_fee = 1000
            let perc_of_spend;
            if (spend < 5000){ return false }
            else if (spend >= 5000 && spend < 10000){ perc_of_spend = .10 }
            else if (spend >= 10000 && spend < 25000){ perc_of_spend = .09 }
            else if (spend >= 25000 && spend < 50000){ perc_of_spend = .08 }
            else if (spend >= 50000){ perc_of_spend = .07 }
            return this.calc_fee(base_fee, spend, perc_of_spend)
        }
        const avg_agency = spend => {
            let base_fee;
            let perc_of_spend = .20;
            if (spend < 5000){ base_fee = 1000 }
            else if (spend >= 5000 && spend < 10000){ base_fee = 2000 }
            else if (spend >= 10000 && spend < 25000){ base_fee = 3000 }
            else if (spend >= 25000 && spend < 50000){ base_fee = 5000 }
            else if (spend >= 50000){ base_fee = 10000 }
            return this.calc_fee(base_fee, spend, perc_of_spend)
        }
        const adroll = spend => {
            let perc_of_spend = .20;
            let base_fee = 0;
            return this.calc_fee(base_fee, spend, perc_of_spend)
        }

        const call_table = {
            'wordstream': wordstream,
            'avg_agency': avg_agency,
            'adroll': adroll
        }
        return call_table[competitor](spend)
    }
    init(){
        const add_revert_handler = (target, secondary) => {
            $(target).blur(() => {
                if ($(target).val() == ""){
                    $(target).val(0)
                    $(secondary).text(0)
                }
            })
        }
        const populate_ad_fields = () =>{
            const spend = parseInt($("#ad_spend").val().replace(/,/g, '')),
                  competitor_name = $("#competitor_name").val(),
                  marketr_spend = this.marketr_model(spend),
                  comp_spend = this.competitors(spend, competitor_name),
                  savings = (comp_spend*12-marketr_spend*12).toFixed(2)
            
            if (!Number.isNaN(spend)) {
                if (spend <= 500){
                    $("#ad_checkout_link").attr('href', '/checkout/almost_free')
                } else if (spend > 500 && spend < 5000) {
                    $("#ad_checkout_link").attr('href', '/checkout/paid_ads')
                } else if (spend > 5000) {
                    $("#ad_checkout_link").attr('href', '/checkout/paid_ads_premium')
                }
                let comp_output = comp_spend != false ? `$${this.num_commas(comp_spend)}/month` : "Doesn't reach minimum spend"
                let savings_output = comp_output == "Doesn't reach minimum spend" ? 'N/A' : `$${savings}/year`
                $(".ads_marketr_cost").text(this.num_commas(marketr_spend))
                $("#ads_comp_est").text(this.num_commas(comp_output))                
                $("#ad_savings").text(this.num_commas(savings_output))
            }
        }

        const populate_test_fields = () => {
            const tests = parseInt($("#test_count").val().replace(/,/g, '')),
                  marketr_cost = this.marketr_test_model(tests)
            if (tests <= 1) {
                $("#testing_checkout_link").attr('href', '/checkout/almost_free')
            } else {
                $("#testing_checkout_link").attr('href', '/checkout/ab_testing')
            }
            
            if (!Number.isNaN(tests)) {
                $(".testing_marketr_cost").text(this.num_commas(marketr_cost))
                $("#testing_savings").text(this.num_commas("$" + ((3000 - marketr_cost)) * 12))
            }
        }

        $("#ad_spend").keyup( ()=> populate_ad_fields() )
        $("#competitor_name").change( ()=> populate_ad_fields() )
        add_revert_handler("#ad_spend", "#ads_marketr_cost")
        add_revert_handler("#test_count", "#testing_marketr_cost")

        $("#test_count").keyup( ()=> populate_test_fields() )
  
        // $("#competitor_name")
        // $("#ad_spend")
        // $("#test_count")
        // $("#ads_marketr_cost")
        // $("#testing_marketr_cost")
        // $("#ads_comp_est")
        // $("#testing_comp_est")
        // $("#ad_savings")
        // $("#testing_savings")
    }
}

class AuditViewModel {
    constructor() {
        this.audit_service = new AdAuditService()
        this.level = 0
        $("#end_audit").click(()=>{
            this.audit_service.kill()
        })
        $('.affirmative').click(()=>{
            this.level++
            this.audit_service.answer(true, this.level)
        })
        $('.negative').click(()=>{
            this.level++
            this.audit_service.answer(false, this.level)
        })
        $(".admin_feedback").click(e=>{
            let $this = e.currentTarget
            $($this).siblings().toggleClass('hidden')
            window.scrollTo(0,document.body.scrollHeight);
        })
    }
}


const WalletViewModel = class {
    constructor(){
    }
    
    disable(type){
        document.querySelector('.spend_submit').disabled = true;
        let copy;
        switch (type) {
            case 'almost_free':
                copy = "Your plan only allows for up to $500/month in ad spend. To spend more, <a href='/checkout/paid_ads'>upgrade your plan</a>"
                break
            case 'mid':
                copy = "Your plan only allows for up to $5,000/month in ad spend. To spend more, <a href='/checkout/paid_ads_premium'>upgrade your plan</a>"
                break
        }
        $("#plan_info").html(copy)
    }
    enable() {
        document.querySelector('.spend_submit').disabled = false;
        $("#plan_info").html('')
    }

    suggest_downgrade(){
        let copy = `
        If you want to spend less than $500/month with us, we will only charge you $1/month. If you want to proceed, <a href="/checkout/almost_free">downgrade your account</a>.
        `
        $("#plan_info").html(copy)
    }

    add_validation(){
        $(".almost_free_val").keyup(e=>{
            let $this = parseInt($(".almost_free_val").val())
            if ($this > 250) {
                this.disable('almost_free')
            } else {
                this.enable()
            }
        })

        $(".ad_mid_val").keyup(e=>{

            let $this = parseInt($(".ad_mid_val").val())
            if ($this > 4999) {
                this.disable('mid')
            } else if ($this < 250) {
                setTimeout(e=>{
                    this.suggest_downgrade()
                },1000)
            }
            else {
                this.enable()
            }
        })
    }
}