import Rec_shell from '/static/src/components/customer/rec_shell.js'
import {dots_loader} from '/static/src/components/UI_elements.js'

const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');

        .rec-container {
            padding: .75em 1.5em;
            border-bottom: 1px solid #f2f2ff;
            background:#fff;
            border-radius: 20px;
            box-shadow: var(--sharper-neu);  
            margin: .6em;          
        }
        .rec {
            border-left: 4px solid gray;
            margin-bottom: 2%;
            padding: 5% 2% 0 5%;
        }
        .dismiss {
            position: relative;
            right: 15%;
            top: 10%;
        }
        .rec-title {
            line-height: .5em;
        }
        .rec-apply {
            font-size: 75%;
            /*float: right;*/
        }
        .read-more {
            margin: auto;
        }
    </style>
    `.trim()
}

export default class Recommendations extends HTMLElement {
    static get observedAttributes() {
        return ['customer-id'];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.state = {
            data: null
        }
        this.observer = new MutationObserver(mutations=>{
            mutations.forEach(mutation => {
                if (mutation.type == "attributes") {
                    if (mutation.attributeName == 'applied') this.apply(mutation.target)
                    else if (mutation.attributeName == 'dismissed') this.dismiss(mutation.target)
                }
            });
        });

        this.css = styles()
    }

    remove_from_view(target){
        const refresh = async () => this.state.data = this.state.data.filter(rec => rec.rec_id != target.getAttribute('rec_id') );
        refresh()
            .then(this.render(true))
    }

    broadcast(){
        if (document.querySelector('rec-history')){
            document.querySelector('rec-history').setAttribute('re_render', 'true')
        }
    }

    apply(target){
        this.broadcast()
        this.remove_from_view(target)
        fetch('/api/recommendation/approve', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                customer_id: this.customer_id,
                title: target.getAttribute('title').replace(/\\/g, ''),
                rec_id: target.getAttribute('rec_id'),
                analytics: this.analytics,
                price: eval(target.getAttribute('price'))
            })
        })
            .then(res=>res.json())
            .then( res=> console.log(res) )

    }

    dismiss(target){
        this.broadcast()
        this.remove_from_view(target)
        fetch('/api/recommendation/dismiss', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                customer_id: this.customer_id,
                rec_id: target.getAttribute('rec_id'),
                analytics: this.analytics
            })
        })
            .then(res=>res.json())
            .then( res=> console.log(res) )
    }

    recommendation(rec, index){
        const el = new Rec_shell
        
        el.setAttribute('price', rec.price_tag)
        el.setAttribute('rec_id', rec.rec_id)
        el.setAttribute('index', index)
        el.setAttribute('customer_id', this.customer_id)
        el.setAttribute('title', rec.title)
        el.setAttribute('body', rec.body)
        el.setAttribute('demo', this.demo)

        this.observer.observe(el, {
            attributes: true
        });
        
        return el
    }

    render(state = false){
        this.shadow.innerHTML = `<div id="rec-container"></div>`
        let el = document.createElement('div')

        const append = res => {
            el.innerHTML = `
                ${this.css}
                <div class="home_row row">
                </div>    
            `
            if (this.state.data.length == 0) {
                el.innerHTML += `
                <p class="small_txt">Every week, you will receive tailored, actionable recommendations from our internal engines and stellar team.</p>
                <p class="small_txt">You can implement these recommendations with only 1 click. Until then, explore your dashboard and we'll email you when you receive your recommendations.</p>`
            } else for (let i in res) {
                let col = document.createElement('div')
                col.classList = ["rec-container col-lg-5 col-md-5 col-sm-12 col-12"]
                col.appendChild(this.recommendation(res[i], i))
                el.querySelector(".home_row").appendChild(col)
            }
        }

        const append_to_shadow = el => this.shadow.querySelector("#rec-container").appendChild(el)
        const init_state = async () => {
            if (state == false) {
                if (this.fetch) {
                    fetch('/api/outstanding_recs', {
                        method: 'POST',
                        headers : new Headers({
                            "content-type": "application/json"
                        }),
                        body:  JSON.stringify({
                            customer_id: this.customer_id,
                            admin_id: this.admin_id
                        })
                    })
                        .then(res=>res.json())
                        .then(res=> this.state.data = res)
                } else this.state.data = this.recs_json ? this.recs_json : []
            }
        }

        init_state().then(()=>{
            append(this.state.data)
            append_to_shadow(el)
        })

    }

    connectedCallback(){
        this.demo = this.getAttribute('demo')
        this.customer_id = this.getAttribute('customer-id')
        this.recs_json = eval(this.getAttribute('recs_json'))
        this.fetch = eval(this.getAttribute('fetch'))
        this.analytics = eval(this.getAttribute('analytics')) == 1 ? true : false
        
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('customer-recommendations', Recommendations))