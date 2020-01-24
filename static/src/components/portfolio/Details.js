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

    render(init=true){
        this.shadow.innerHTML = ""
        const el = document.createElement('div')
        el.innerHTML = `<p>I am the details</p>`
        this.shadow.appendChild(el)
    }

    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-details', PortfolioDetails))


