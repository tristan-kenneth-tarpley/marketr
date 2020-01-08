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

        this.css = styles()
    }

    recommendation(rec, index){
        const el = new Rec_shell
        el.setAttribute('rec_id', rec.rec_id)
        el.setAttribute('index', index)
        el.setAttribute('customer_id', this.customer_id)
        el.setAttribute('title', rec.title)
        el.setAttribute('body', rec.body)

        
        return el
    }

    render(){
        this.shadow.innerHTML = ""
        let el = document.createElement('div')

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
            .then(res=>{
                /*html */
                el.innerHTML = `${this.css}`

                for (let i in res) el.appendChild(this.recommendation(res[i], i))
            })
            .then(this.shadow.appendChild(el))
    }

    connectedCallback(){
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('customer-recommendations', Recommendations))