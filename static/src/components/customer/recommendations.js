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

    render(){
        this.shadow.innerHTML = ""
        const el = document.createElement('div')
        /*html */
        el.innerHTML = `
            ${this.css}
            <p>Hello world</p>
        `
        this.shadow.appendChild(el);
    }

    connectedCallback(){
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('customer-recommendations', Recommendations))