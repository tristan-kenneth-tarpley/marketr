import {tabs, shadow_events, dots_loader} from '/static/src/components/UI_elements.js'

const styles = () => {
  /*html*/
  return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('/static/assets/icons/all.min.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');


    </style>
  `.trim()
}

export default class Budget extends HTMLElement {
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

    ViewController(el){
        return el
    }

    render(init=true){
        this.shadow.innerHTML = ""
        const el = document.createElement('div')
        el.innerHTML = `
        ${this.css}
        <p>Test test</p>
    `
        this.shadow.appendChild(this.ViewController(el))
    }

    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-budet', Budget))
