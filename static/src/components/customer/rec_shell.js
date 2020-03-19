import {iterate_text, modal, modal_trigger, modal_handlers, currency,currency_rounded,number,number_rounded,number_no_commas,percent,remove_commas,remove_commas_2} from '/static/src/convenience/helpers.js'

const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/app.css');
        
        .rec-container {
            padding: 4%;
            border-bottom: 1px solid #f2f2ff;
        }
        .rec {
            margin-bottom: 2%;
            padding: 5% 0 0;
            overflow-x: hidden;
        }
        .dismiss {
            position: relative;
            top: 0;
            margin: 0px 1px 15px !important;
            font-weight: 400;
            text-transform: lowercase;
            font-weight: 
        }
        .rec-title {
            position: relative;
            top: 0;
            left: 0;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        .rec-apply {
            font-size: 75%;
            padding: 5px 10px;
            /*float: right;*/
            font-weight: 300;
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
        const x = this.shadow.querySelectorAll(".x")
        if (this.demo != 'True') {
            x.forEach(el=>{
                el.addEventListener('click', e=>{
                    this.style.display = 'none';
                    this.setAttribute('dismissed', 'true')
                })
            })

            const apply = this.shadow.querySelectorAll('.rec-apply')
            
            apply.forEach(el=>{
                el.addEventListener('click', e=>{
                    e.currentTarget.textContent = 'Done!'
                    setTimeout(()=>{
                        this.style.display = 'none'
                        this.setAttribute('applied', 'true')
                    }, 1000)
                })
            })
        }
        
    }

    render(){
        this.shadow.innerHTML = ''
        const colors = ['#62cde0','#ca7d66','#01d4b4','#ff9c00', '#62cde0','#ca7d66','#01d4b4','#ff9c00', '#62cde0','#ca7d66','#01d4b4','#ff9c00', '#62cde0','#ca7d66','#01d4b4','#ff9c00']
        /*html*/
        const shell = async () => {
            return `
            ${this.css}
            ${modal(this.title, this.body, this.title)}
            <div class="rec-container">
                <div class="rec">
                    <div class="row">
                        <div class="col-lg-8 col-md-8 col-sm-12">
                            <p class="squashed rec-title small_txt">${this.title}</p>
                            <div data-uid="${this.title}" id="six" class="small_txt button">read more <i class="fas fa-caret-right"></i></div>
                        </div>
                        <div style="text-align:right;margin: auto;" class="col-lg-4 col-md-4 col-sm-12">
                            <button class="small_txt rec-apply btn btn-secondary">do it</button>
                            <br>
                            <button style="padding: 0;" class="btn btn-neutral dismiss">dismiss</button>
                        </div>
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
        this.customer_id = this.getAttribute('customer-id')
        this.title = this.getAttribute('title')
        this.body = this.getAttribute('body')
        this.index = parseInt(this.getAttribute('index')) % 4
        this.demo = this.getAttribute('demo')

        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('recommendation-shell', Rec_shell))