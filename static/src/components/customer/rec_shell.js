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
            left: 85%;
            top: 0;
        }
        .rec-title {
            margin-bottom: 0;
            padding-bottom: 0;
            font-size: 97%;
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
                <div style="border-left: 4px solid ${colors[this.index]}" class="rec">
                    <span class="x dismiss">X</span> 
                    <h5 class="rec-title">${this.title}</h5>
                    <div class="row">
                        <div class="col-md-6 col-12">
                            <div data-uid="${this.title}" id="six" class="button">Read more</div>
                        </div>
                        <div class="col-md-6 col-12"><button class="rec-apply btn btn-secondary">Do it</button></div>
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