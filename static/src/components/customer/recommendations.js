import Rec_shell from '/static/src/components/customer/rec_shell.js'

const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');
        .rec-container {
            padding: 1%;
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
        this.customer_id = this.getAttribute('customer-id')
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

    remove(target){
        const refresh = async () => this.state.data = this.state.data.filter(rec => rec.rec_id != target.getAttribute('rec_id') );
        refresh()
            .then(this.render(true))
    }

    apply(target){
        this.remove(target)
        fetch('/api/recommendation/approve', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                customer_id: this.customer_id,
                rec_id: target.getAttribute('rec_id')
            })
        })
            .then(res=>res.json())
            .then( res=> console.log(res) )

    }

    dismiss(target){
        this.remove(target)
        fetch('/api/recommendation/dismiss', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                customer_id: this.customer_id,
                rec_id: target.getAttribute('rec_id')
            })
        })
            .then(res=>res.json())
            .then( res=> console.log(res) )
    }

    recommendation(rec, index){
        const el = new Rec_shell
        el.setAttribute('rec_id', rec.rec_id)
        el.setAttribute('index', index)
        el.setAttribute('customer_id', this.customer_id)
        el.setAttribute('title', rec.title)
        el.setAttribute('body', rec.body)

        this.observer.observe(el, {
            attributes: true
        });
        
        return el
    }

    render(state = false){
        this.shadow.innerHTML = ""
        let el = document.createElement('div')

        const append = res => {
            el.innerHTML = `${this.css}`
            if (this.state.data.length == 0) {
                el.innerHTML += `<p>You don't currently have any recommendations. We'll email you when you get one!</p>`
            } else for (let i in res) el.appendChild(this.recommendation(res[i], i))
        }

        if (state == false) {
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
                .then( res=> this.state.data = res )
                .then(res=>append(res))
                .then(this.shadow.appendChild(el))
        } else {
            append(this.state.data)
            this.shadow.appendChild(el)
        }
    }

    connectedCallback(){
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('customer-recommendations', Recommendations))