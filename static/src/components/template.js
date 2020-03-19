import {tabs, shadow_events, dots_loader} from '/static/src/components/UI_elements.js'

const styles = () => {
  /*html*/
  return `
  <style>
      @import url('/static/assets/css/app.css');


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

  render(init=true){
      this.shadow.innerHTML = ""
      const el = document.createElement('div')
      el.innerHTML = `
        ${this.css}
        <p>Test test</p>
    `
      this.shadow.appendChild(el)
  }

  connectedCallback() {
      this.customer_id = this.getAttribute('customer_id')
      this.render()
  }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-budet', Budget))
