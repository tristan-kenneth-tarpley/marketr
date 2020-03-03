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
            margin-bottom: 2%;
            padding: 5% 0 0;
            border-bottom: 1px solid #f2f2ff;
            overflow-x: hidden;
        }
        .dismiss {
            position: relative;
            top: 0;
            margin: 0px 1px 15px !important;
            font-weight: 500;
            text-transform: lowercase;
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
        }
        .read-more {
            margin: auto;
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
                        <div class="col-lg-7 col-md-7 col-sm-12">
                            <p class="rec-title small_txt">${this.title}</p>
                            <div data-uid="${this.title}" id="six" class="small_txt button">[Read more]</div>
                        </div>
                        <div style="text-align:right;" class="col-lg-5 col-md-5 col-sm-12">
                            <button style="padding: 0;" class="btn btn-neutral dismiss">dismiss</button> 
                            <button class="small_txt rec-apply btn btn-outline btn-outline-secondary">Do it</button>
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