import Funnel from '/static/src/components/portfolio/details/funnel.js'
import Active from '/static/src/components/portfolio/details/active.js'
const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');

 
    </style>
    `.trim()
}

export default class PortfolioDetails extends HTMLElement {
    static get observedAttributes() {
        return ['customer_id'];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.state = {
            data: null
        }

        this.css = styles()
    }

    active(){
        const el = new Active()
        el.setAttribute('customer_id', this.customer_id)
        el.setAttribute('company_name', this.company_name)
        el.setAttribute('data', this.data)
        return el
    }

    funnel(){
        const el = new Funnel()
        el.setAttribute('customer_id', this.customer_id)
        el.setAttribute('company_name', this.company_name)
        return el
    }

    render(init=true){
        this.shadow.innerHTML = ""
        const el = document.createElement('div')

        el.innerHTML = `
            ${this.css}
            <div class="row">
                <div id="funnel" class="col-lg-12 col-md-12">
                </div>
            </div>
        `
        //el.querySelector("#active").appendChild(this.active())
        el.querySelector("#funnel").appendChild(this.funnel())
        this.shadow.appendChild(el)
    }

    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.company_name = this.getAttribute('company_name')
        this.data = JSON.parse(this.getAttribute('data'))
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-details', PortfolioDetails))


