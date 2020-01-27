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
  
  export default class Active extends HTMLElement {
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
          <p>Campaign history</p>
          <table class="table table-striped table-responsive">
            <thead>
                <th>Campaign Type</th>
                <th>% of marketing investment</th>
                <th>Market(r) Index</th>
            </thead>
            <tbody>
                ${this.data.campaign.social.map(it=>{
                    return `
                    <tr>
                        <td>Social Media PPC</td>
                        <td>${it.cost / this.data.total_spent}</td>
                        <td>${it.index}</td>
                    </tr>
                    `
                }).join("")}

                ${this.data.campaign.search.map(it=>{
                    return 'hi'
                }).join("")}
                
            </tbody>
          </table>
      `
        this.shadow.appendChild(el)
    }
  
    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.data = JSON.parse(this.getAttribute('data'))
        this.render()
    }
  }
  
  document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-active', Active))