export class Achievements {
    constructor(){
    }

    claim(target){
        const id = target.getAttribute('id').split('_')
        const amount = parseInt(id[0])
        const achievement_id = parseInt(id[1])

        fetch('/api/claim', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                amount: amount,
                achievement_id: achievement_id
            })
        })
            .then((res) => res.json())
            .then((data) => {
                target.parentNode.innerHTML = "<p class='small_txt'>claimed</p>"

                const amount = document.querySelectorAll(".total_credits")
                const total = data['amount']
                amount.forEach(el=>{
                    el.textContent = total.toString().replace(/\,/g, '')
                })

                setTimeout(()=>{
                    this.render_unclaimed()
                }, 1000)
            })
            .catch((err)=>console.log(err))
    }

    lets_play(){
        const claim = document.querySelectorAll('.claim_credits')
        claim.forEach(el=>{
            el.addEventListener('click', e=>{
                const $this = e.currentTarget
                $this.style.background = '#fff'
                $this.innerHTML = `<div class="loading_dots">
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                    </div>`
                this.claim($this)
            })
        })
    }

    notification(title, body){
        /* html */
        const el = `
            <div class="toast__container">
                <div class="toast__cell">
                    <div class="toast toast--green">
                    <div class="toast__icon">
                        <svg version="1.1" class="toast__svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">
                            <g><g><path d="M504.502,75.496c-9.997-9.998-26.205-9.998-36.204,0L161.594,382.203L43.702,264.311c-9.997-9.998-26.205-9.997-36.204,0    c-9.998,9.997-9.998,26.205,0,36.203l135.994,135.992c9.994,9.997,26.214,9.99,36.204,0L504.502,111.7    C514.5,101.703,514.499,85.494,504.502,75.496z"></path>
                            </g></g>
                        </svg>
                    </div>
                    <div class="toast__content">
                        <p class="toast__type">Achievement Unlocked: ${title.replace("`", "'")}</p>
                        <p class="toast__message">${body.replace("`", "'")}</p>
                    </div>
                    <div class="toast__close">
                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 15.642 15.642" xmlns:xlink="http://www.w3.org/1999/xlink" enable-background="new 0 0 15.642 15.642">
                            <path fill-rule="evenodd" d="M8.882,7.821l6.541-6.541c0.293-0.293,0.293-0.768,0-1.061  c-0.293-0.293-0.768-0.293-1.061,0L7.821,6.76L1.28,0.22c-0.293-0.293-0.768-0.293-1.061,0c-0.293,0.293-0.293,0.768,0,1.061  l6.541,6.541L0.22,14.362c-0.293,0.293-0.293,0.768,0,1.061c0.147,0.146,0.338,0.22,0.53,0.22s0.384-0.073,0.53-0.22l6.541-6.541  l6.541,6.541c0.147,0.146,0.338,0.22,0.53,0.22c0.192,0,0.384-0.073,0.53-0.22c0.293-0.293,0.293-0.768,0-1.061L8.882,7.821z"></path>
                        </svg>
                    </div>
                </div>
            </div>
        `
        return el
    }

    render_notifications(res){
        const body = document.querySelector('body')
        let notifications = document.createElement("div")
        notifications.classList.add('push_to_front')
        if (res.length > 1){
            /* html */
            notifications.innerHTML += `
                <br><button id="clear_notifications">x clear all notifications</button><br>
            `
        }
        for (let ach in res){
            if (res[ach]['title'] != ""){
                let notification = this.notification(res[ach]['title'], res[ach]['body'])
                notifications.innerHTML += '<br>' + notification
            }
        }
        body.prepend(notifications)
        const close = document.querySelectorAll('.toast__close')
        close.forEach(e=>{
            if (e != null){
                e.addEventListener('click', e=>{
                    e.preventDefault();
                    let $this = e.currentTarget
                    let parent = $this.parentNode
                    parent.parentNode.removeChild(parent)
                })
            }
        })

        const clear = document.querySelector('#clear_notifications')
        if (clear != null) {
            clear.addEventListener('click', e=>{
                const $this = e.currentTarget 
                const notifications = document.querySelector('.push_to_front')
                $this.parentNode.parentNode.removeChild(notifications)
            })
        }
    }

    render_unclaimed(){
        const unclaimed = document.querySelectorAll('.claim_credits').length
        const ach_note = document.querySelector('.ach_note')
        if (unclaimed > 0){
            ach_note.textContent = unclaimed
            ach_note.style.display = 'inline-block'
        } else {
            ach_note.style.display = 'none'
        }
    }

    poll(){
        this.render_unclaimed()
        fetch('/api/poll_for_state')
            .then(res=>res.json())
            .then(res=>{
                this.render_notifications(res)
            })
            .catch(e=>{
                console.log(e)
            })
    }
}









export class Store {
    constructor(rewards_obj){
        this.rewards = rewards_obj
    }

    init(){
        const buy_button = document.querySelectorAll('.pack_purchase')
        buy_button.forEach(el=>{
            el.addEventListener('click', e=>{
                const id = e.currentTarget.getAttribute('id')
                this.buy(id, e.currentTarget)
            })
        })
    }

    coin_celebration(amount){
        /* html*/
        const splash_markup = `
            <div id="splash_cont" class="hide">
                    <svg height="400" width="400" xmlns="http://www.w3.org/2000/svg">
                        <circle class="circle" cx="200" cy="200" r="195">
                    </svg>
                <img id="ruby" src="https://i.ibb.co/xf9sYXm/marketr-credit-logo.png" alt="" />
            </div>
        `
        document.querySelector('.store_container').insertAdjacentHTML("afterbegin", splash_markup)
        var splash = el("#splash_cont").addClass("animate").rmClass("hide");

        splash.rmClass("animate").addClass("hide");
        setTimeout(function(){
            this.update_amount(amount)
            splash.rmClass("hide").addClass("animate");
        }, 50);

        setTimeout(()=>{
            document.querySelector('#splash_cont').remove()
        }, 3000)
    }

    update_amount(amount){
        const credits = document.querySelectorAll('.total_credits')
        credits.forEach(el=>el.textContent = amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","))
    }

    notify_after_buy(data, amount, target){

        let copy;
        switch(data['type']){
            case 'tactics_rewards':
                /*html*/
                copy = `<h5>${data['title']}</h5> <p>You won more tactics...Nice! Your tactic has been added to your <a href="/home?view=campaigns">library.</a></p>`
                break
            case 'credit_reward':
                let current = parseInt(document.querySelector('.total_credits').textContent.replace(/\,/g, ''))
                this.coin_celebration(data['parameter'] + current)

                setTimeout(()=>{
                    document.querySelector('.total_credits').classList.add('pulse')
                }, 3000)
                setTimeout(()=>{
                    document.querySelector('.total_credits').classList.remove('pulse')
                }, 4000)

                /*html*/
                copy = `<h5>${data['title']}</h5> </h5><p>Don't spend it all in one place! Your credits have been added to your account. Refresh the page if you don't see them right away.</p>`
                break
            case 'manual_reward':
                /*html*/
                copy = `<h5>${data['title']}</h5><p>Nice! Check your <a href="/home?view=campaigns">messages</a> tab for your next instructions!</p>`
                break
        }

        target.parentNode.insertAdjacentHTML("afterbegin", copy)
        target.textContent = "Buy another!"
    }

    buy(id, target){
        const current_amount = parseInt(document.querySelector('.total_credits').textContent.replace(/\,/g, ''))
        
        let max;
        switch (id){
            case 'helper':
                max = 200
                break
            case 'booster':
                max = 4000
                break
            case 'rocket':
                max = 40000
                break
        }
        if (current_amount >= max){
            confirm(`Are you sure you want to buy the ${id} pack for ${max} credits?`)
            this.update_amount(current_amount-max)
            this.rewards.excite()

            fetch('/api/drop', {
                method: 'POST',
                headers : new Headers({
                    "content-type": "application/json"
                }),
                body:  JSON.stringify({
                    type: id
                })
            })
                .then((res) => res.json())
                .then((data) => {
                    this.rewards.reveal()
                    console.log(data)
                    this.notify_after_buy(data, (current_amount-max), target)
                    this.rewards.get()
                })
                .catch((err)=>console.log(err))

        } else {
            target.innerHTML = "You don't have enough credits to buy this pack."
        }
    }
}












export class Rewards {
    constructor(){
        this.container = document.querySelector('.rewards_container')
    }
    reveal(){
        document.querySelector(".material_load").remove()
        document.querySelector('.store_container').style.display = 'block'
    }
    excite(){
        document.querySelector('.store_container').style.display = 'none'
        document.querySelector('.excite_container').innerHTML = `
        <div class="material_load">
            <div class="dot"></div>
            <div class="outline"><span></span></div>
        </div>`
    }

    refresh(res){
        let rewards = "";
        for (let reward in res){
            /*html*/
            rewards += `
            <div style="padding:1%;margin-bottom: 1%;" class="card negative_card">
                <p class="small_txt"><strong>${res[reward]['date']}</strong></p>
                <p>${res[reward]['achievement']}</p>
            </div>
            `
        }
        this.container.innerHTML = rewards
    }
    get(){
        fetch('/api/rewards')
            .then(res=>res.json())
            .then(res=>{
                this.refresh(res)
            })
            .catch(e=>{
                console.log(e)
            })
    }
}