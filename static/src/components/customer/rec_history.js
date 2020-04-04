import {tabs, shadow_events, dots_loader} from '/static/src/components/UI_elements.js'
import {modal, modal_handlers, modal_trigger} from '/static/src/convenience/helpers.js'

const styles = () => {
  /*html*/
  return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('/static/assets/icons/all.min.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');

        .rec-container {
            padding: 4%;
            border-bottom: 1px solid #f2f2ff;
        }
    </style>
  `.trim()
}

export default class RecHistory extends HTMLElement {
    static get observedAttributes() {
        return ['re_render'];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.state = {
            data: null,
            view: 'approved'
        }

        this.css = styles()
    }

    dropdown(){
        return (/*html*/`
            View: <select class="form-control" id="widget__dropdown">
                <option ${this.state.view == 'approved' ? "selected" : ''}>approved</option>
                <option ${this.state.view == 'dismissed' ? "selected" : ''}>dismissed</option>
            </select>
        `)
    }

    ViewController(el){
        el.querySelector('#widget__dropdown').addEventListener('change', e=>{
            this.state.view = e.currentTarget.value
            this.render(false)
        })
        return el
    }

    render(init=true){
        this.shadow.innerHTML = ""

        const compile = () => {
            const {data, view} = this.state
            const first = async () => {
                console.log(data)
                const el = document.createElement('div')
                el.innerHTML = `
                    ${this.css}
                    ${this.dropdown()}
                    <div class="divider"></div>
                    ${data[view].length > 0
                        ?
                            data[view].map((rec, index)=>{
                                return `
                                <div class="rec-container">
                                    <p class="squashed rec-title small_txt">${rec.title}</p>
                                    ${modal_trigger(index, 'read more', false)}
                                    ${modal(rec.title, rec.body, index)}
                                </div>
                                `
                            }).join("")
                        :
                            `<p>You haven't ${view} any recommendations yet</p>`
                    }
                `
                return el
            }
            first().then(el=>{
                console.log(data[view])
                this.shadow.appendChild(modal_handlers(this.ViewController(el)))
            })
        }

        init
        ? 
            fetch('/api/historical_recs', {
                method: 'POST',
                headers : new Headers({
                    "content-type": "application/json"
                }),
                body:  JSON.stringify({
                    customer_id: this.customer_id
                })
            })
                .then(res=>res.json())
                .then(res=> this.state.data = res)
                .then(()=>compile())
        : compile()
        
    }

    attributeChangedCallback(name, oldValue, newValue){
        if (name == 're_render'){
            setTimeout(()=>{
                this.render()
            }, 600)
            
        }
    }

    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.render()
    }
}


document.addEventListener( 'DOMContentLoaded', customElements.define('rec-history', RecHistory))