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

    payments(){
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
                    $('.target').each(function(){
                        if (
                           $(this).offset().top < window.pageYOffset + 10
                        && $(this).offset().top + $(this).height() > window.pageYOffset + 10
                        ) {
                            window.location.hash = $(this).attr('id');
                        }
                    });
                });
        
            }, 1000);
        })
        
        $(window).on('hashchange', () => {
            var select = "." + window.location.hash.substring(1)
            var target = "a" + select
            $('a').not(target).removeClass('targeted')
            $(target).addClass("targeted")
        });
        
        $(window).on('load', e => {
            const urlParams = new URLSearchParams(window.location.search);
            const view = urlParams.get('view');
            $(".sidebar-wrapper div").addClass('hidden')
            switch(view) {
                case 'profile':
                case null:
                    $("#profile").addClass('active')
                    $("#profile-tab").addClass('active')
                    $("#profile-tab").addClass('show')
                    $("#profile-nav").removeClass('hidden')
                    break
                case 'campaigns':
                    $("#campaigns").addClass('active')
                    $("#campaigns-tab").addClass('active')
                    $("#campaigns-tab").addClass('show')
                    $("#campaigns-nav").removeClass('hidden')
                    break
                case 'messages':
                    $("#messages").addClass('active')
                    $("#messages-tab").addClass('active')
                    $("#messages-tab").addClass('show')
                    $("#messages-nav").removeClass('hidden')
                    break
            }
            $(document).on('scroll', e => {
                $('.target').each(function() {
                    if (
                       $(this).offset().top < window.pageYOffset + 10
                    && $(this).offset().top + $(this).height() > window.pageYOffset + 10
                    ) {
                        window.location.hash = $(this).attr('id');
                    }
                });
            });
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
        $(".task_complete").change((event)=>{
            const $this = $(event.currentTarget)
            if($this.prop('checked')) {
                const tasks = new TaskService(this.url_path)
                const val = $this.parent().parent().parent().next().text().replace(/^\s+/g, '').replace(/\s+$/g, '');;
                
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

