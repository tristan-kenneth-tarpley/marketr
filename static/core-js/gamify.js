const Achievements = class {
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
                console.log(data)
                target.parentNode.innerHTML = "<p class='small_txt'>claimed</p>"

                const amount = document.querySelectorAll(".total_credits")
                amount.forEach(el=>{
                    el.textContent = data.amount.replace(/\,/g, '')
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
    constructor(rewards_obj){
        this.rewards = rewards_obj
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

    coin_celebration(){
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
                this.coin_celebration()
                this.update_amount(amount)

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
                    this.notify_after_buy(data, (current_amount-max), target)
                    this.rewards.get()
                })
                .catch((err)=>console.log(err))

        } else {
            target.innerHTML = "You don't have enough credits to buy this pack."
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












const Rewards = class {
    constructor(){
        this.container = document.querySelector('.rewards_container')
    }
    reveal(){
        document.querySelector("#possibilities_canv").remove()
        document.querySelector('.store_container').style.display = 'block'
    }
    excite(){
        document.querySelector('.store_container').style.display = 'none'
        const words = [
              "influencer shout out",
              "Credits (125 gp)",
              "New ad creative",
              "Tactic",
              "New ad test",
              "1% Discount on monthly bill (one-time)",
              "Credits (2,500)",
              "Web page audit",
              "Competitive data enhancement",
              "Add competitor",
              "Article (2000 words)",
              "Negative keyword research",
              "Ad spend boost (+$25)",
              "Tactic steps guide",
              "5% Discount on monthly bill (one-time)",
              "Influencer (2,500+ followers) mention",
              "Influencer (10,000+ followers) mention",
              "Pricing analysis",
              "Lead gen tool",
              "A/B test executed",
              "5% Discount on all services (3 months)",
              "Real-time monitoring competitor site (each)",
              "Customer feedback tracking",
              "Unlock Insights",
              "New Insight",
              "Tactics x3",
              "30 min consultation call"
        ];
            document.querySelector('.excite_container').innerHTML += `<canvas id="possibilities_canv"></canvas>`
            var canvas = document.getElementById("possibilities_canv");
            var ctx = canvas.getContext("2d");
            // Utilities
            function randomColor() {
              return '#' + Math.random().toString(16).slice(2, 8);
            }
            
            function randomWord() {
            var word = words[Math.floor(Math.random() * words.length)];
            return word;
          }
            
            function randomInt(min, max) {
              return Math.floor(Math.random() * (max - min + 1)) + min;
            }
            //Make the canvas occupy the full page
            var W = window.innerWidth,
              H = window.innerHeight;
            canvas.width = W;
            canvas.height = H;
            var particles = [];
            var mouse = {};
            //Lets create some particles now
            var particle_count = 100;
            for (var i = 0; i < particle_count; i++) {
              particles.push(new particle());
            }
            canvas.addEventListener('mousedown', track_mouse, false);
            canvas.addEventListener('touch', track_mouse, false);
          
            function track_mouse(e) {
              mouse.x = e.pageX;
              mouse.y = e.pageY;
          
              for (var i = 0; i < particle_count; i++) {
                particles.push(new particle());
              }
            }
          
            function particle() {
              //speed, life, location, life, colors
              //speed range = -2.5 to 2.5
              this.speed = {
                x: -2.5 + Math.random() * 5,
                y: -2.5 + Math.random() * 5
              };
              //location = center of the screen
              if (mouse.x && mouse.y) {
                this.location = {
                  x: mouse.x,
                  y: mouse.y
                };
              } else {
                this.location = {
                  x: W / 2,
                  y: H / 2
                };
              }
              this.color = randomColor()
          
              this.font = {
                size: randomInt(3, 15)
              }
              
              this.word = randomWord()
            }
          
            function draw() {
              ctx.globalCompositeOperation = "source-over";
              //Painting the canvas black
              ctx.fillStyle = "black";
              ctx.fillRect(0, 0, W, H);
              ctx.globalCompositeOperation = "lighter";
              for (var i = 0; i < particles.length; i++) {
                var p = particles[i];
                ctx.beginPath();
                ctx.font = p.font.size + "vh Luckiest Guy";
                ctx.textAlign = "center";
                ctx.transition = "all 2s ease";
                ctx.fillStyle = p.color;
                ctx.fillText(p.word, p.location.x, p.location.y);
                ctx.fill();
                ctx.stroke();
          
                //lets move the particles
                p.location.x += p.speed.x;
                p.location.y += p.speed.y;
                
                p.speed.x += randomInt(-0.01, 0.01);
                p.speed.y += randomInt(-0.01, 0.01);
                
                // Make 'em big and small
                // Warning: Causes extreme lag
                //p.font.size += randomInt(-0.1, 0.1)
              }
            }
            setInterval(draw, 10);
        
          
          

    }

    refresh(res){
        console.log(res)
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