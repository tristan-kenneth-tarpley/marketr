import {iterate_text, modal, modal_trigger, modal_handlers, currency,currency_rounded,number,number_rounded,number_no_commas,percent,remove_commas,remove_commas_2} from '/static/src/convenience/helpers.js'

const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('/static/assets/icons/all.min.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');
        .rec__body {
            margin-bottom:2em;
        }
        .toolbar {
            position: absolute;
            height: 2em;
            width: 100%;
            bottom: 0;
            left: 0;
        }
        .toolbar .btn {
            width: 50%;
            position:absolute;
            height:100%;
        }
        .rec-apply {
            font-size: 75%;
            padding: 5px 10px;
            font-weight: 300;
            left:50%;
            margin: 0;
        }
        .dismiss {
            position: relative;
            top: 0;
            margin: 0px 1px 15px !important;
            font-weight: 400;
            text-transform: lowercase;
            left:0;
        }
        .rec {
            margin-bottom: 2%;
            padding: 5% 0 0;
            overflow-x: hidden;
        }
        .rec-title {
            position: relative;
            top: 0;
            left: 0;
            margin-bottom: 0;
            padding-bottom: 0;
            font-weight:bold;
        }
        .rec-body__summary {
            white-space: pre-wrap;
            margin: 0;
        }
        .read-more {
            margin: auto;
            padding: 0;
        }

        


    </style>
    `.trim()
}

export default class Rec_shell extends HTMLElement {
    static get observedAttributes() {
        return ['rec-id', 'customer-id', 'title', 'body', 'index'];
    }

    constructor(){
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        
        this.state = {
            data: null
        }
        this.css = styles()

    }


    RecEvents(){
        const x = this.shadow.querySelectorAll(".dismiss")
        if (this.demo != 'True') {
            x.forEach(el=>{
                el.addEventListener('click', e=>{
                    this.style.display = 'none';
                    this.setAttribute('dismissed', 'true')
                })
            })

            const apply = this.shadow.querySelectorAll('.rec-apply')
            
            const action__apply = e =>{
                e.currentTarget.textContent = 'Done!'
                setTimeout(()=>{
                    this.style.display = 'none'
                    this.setAttribute('applied', 'true')
                }, 1000)
            }
            apply.forEach(el=>{
                el.addEventListener('click', e=>{
                    if (this.price) {
                        let confirmation = prompt(`Confirmation required. You will be charged $${this.price}. Type "confirm" to accept.`)
                        confirmation.toLowerCase() == 'confirm'
                        ? action__apply(e)
                        : alert(`Acceptance cancelled`)
                    }
                    else action__apply(e)
                })
            })
        }
        
    }

    render(){
        this.shadow.innerHTML = ''
        let apply_copy = this.price != null ? `do it for $${this.price}` : `do it`
        /*html*/
        const shell = async () => {
            return `
            ${this.css}
            ${modal(this.title, this.body, this.title)}
                <div class="rec-container">
                    <div class="rec">
                        <div class="rec__body">
                            <p class="squashed rec-title small_txt">${this.title}</p>
                            <p class="small_txt rec-body__summary trunc">${this.body.trunc(50)}</p>
                            <div data-uid="${this.title}" id="six" class="small_txt button">read more <i class="fas fa-caret-right"></i></div>
                        </div>

                        <div class="toolbar">      
                            <button style="padding: 0;" class="btn btn-neutral dismiss">dismiss</button>
                            <button class="small_txt rec-apply btn btn-secondary">${apply_copy}</button>  
                        </div>
                    </div>
                </div>
            `.trim()
        }

        const init = () => {
            this.RecEvents();
            modal_handlers(this.shadow)
        }

        shell()
            .then(html => {
                let el = document.createElement('div')
                el.innerHTML = html
                modal_handlers(this.shadow)
                return el
            })
            .then(el=> {this.shadow.appendChild(el); return el})
            .then(el => init())
    }

    connectedCallback(){
        this.rec_id = parseInt(this.getAttribute('rec-id'))
        this.price = eval(this.getAttribute('price'))

        this.customer_id = this.getAttribute('customer-id')
        this.title = this.getAttribute('title').replace(/\\/g, '')
        this.body = this.getAttribute('body').replace(/\\/g, '')
        this.index = parseInt(this.getAttribute('index')) % 4
        this.demo = this.getAttribute('demo')

        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('recommendation-shell', Rec_shell))