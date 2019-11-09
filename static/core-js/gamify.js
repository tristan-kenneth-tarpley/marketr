const Achievements = class {
    constructor(){

    }

    claim(target){
        const id = target.getAttribute('id').split('_')
        const amount = parseInt(id[0])
        const achievement_id = parseInt(id[1])
        console.log(amount)

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
                console.log(data)
                target.parentNode.innerHTML = "<p class='small_txt'>claimed</p>"

                const amount = document.querySelectorAll(".total_credits")
                amount.forEach(el=>{
                    el.textContent = data.amount
                })
            })
            .catch((err)=>console.log(err))
    }

    lets_play(){
        const claim = document.querySelectorAll('.claim_credits')
        claim.forEach(el=>{
            el.addEventListener('click', e=>{
                const $this = e.currentTarget
                $this.innerHTML = '<div class="quigly"></div>'
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
        if (res.length > 0){
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

    poll(){
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

const Store = class {
    constructor(){

    }

    init(){
        this.modals()
        const buy_button = document.querySelectorAll('.pack_purchase')
        buy_button.forEach(el=>{
            el.addEventListener('click', e=>{
                const id = e.currentTarget.getAttribute('id')
                this.buy(id, e.currentTarget)
            })
        })
    }

    notify_after_buy(data, amount, target){
        console.log(data)
        const credits = document.querySelectorAll('.total_credits')
        credits.forEach(el=>el.textContent = amount)

        let copy;
        switch(data['type']){
            case 'tactics_rewards':
                /*html*/
                copy = `<p>Nice! Your tactic has been added to your <a href="/home?view=campaigns">library.</a></p>`
                break
            case 'credit_reward':
                /*html*/
                copy = `<p>Nice! Your credits have been added to your account. Refresh the page if you don't see them right away.</p>`
                break
            case 'manual_reward':
                /*html*/
                copy = `<p>Nice! Check your <a href="/home?view=campaigns">messages</a> tab for your next instructions!</p>`
                break
        }

        alert(data['title'])
        target.parentNode.innerHTML = copy
    }

    buy(id, target){
        const current_amount = parseInt(document.querySelector('.total_credits').textContent)
        let max;
        switch (id){
            case 'helper':
                max = 200
                break
            case 'booster':
                max = 2000
                break
            case 'rocket':
                max = 40000
                break
        }
        if (current_amount >= max){
            target.innerHTML = '<div class="quigly"></div>'

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
                    this.notify_after_buy(data, (current_amount-max), target)
                    
                })
                .catch((err)=>console.log(err))
        } else {
            alert("You don't have enough credits to purchase this pack.")
        }
    }

    modal_shell(type){
        let title;
        let body;
        
        switch (type){
            case 'helper':
                title = "Helper Pack"
                body = "This guarantees one of the following:"
                break
            case 'booster':
                title = "Booster Pack"
                body = "This guarantees one of the following:"
                break
            case 'rocket':
                title = "Rocket Pack"
                body = "This guarantees one of the following:"
                break
        }
        console.log(`#${type}_modal_header`)
        document.querySelector(`#${type}_modal_header`).textContent = title
        document.querySelector(`#${type}_modal_body`).textContent = body
    }

    modals(){
        const buttons = document.querySelectorAll('.pack_modal')
        buttons.forEach(el=>{
            el.addEventListener('click', e=>{
                const $this = e.currentTarget
                const id = $this.getAttribute('id')
                this.modal_shell(id)
            })
        })
    }
}