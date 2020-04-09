import {tabs, shadow_events, dots_loader} from '/static/src/components/UI_elements.js'

const styles = () => {
  /*html*/
  return `
  <style>
      @@import url('/static/assets/css/dist/styles.min.css');
  </style>
  `.trim()
}

export default class MetaManager extends HTMLElement {
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

  claim(data){
        const body = JSON.stringify({
            customer_id: this.customer_id,
            campaign_id: data.campaign_id,
            type: data.type,
            campaign_name: data.campaign_name
        })
        fetch('/api/claim_campaign', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body
        })
  }

  data_handler(el){
    el.querySelectorAll('.claimed').forEach(_el => {
        _el.addEventListener( 'change', e=> {
            if(e.currentTarget.checked) {
                this.claim(e.currentTarget.dataset)
            } else {
                console.log(false)
            }
        });
    });

    return el
  }

  datatable(){
    const el = document.createElement('div')
    /*html*/
    el.innerHTML = `
    <table id="campaign_table" class="table-responsive table">
        <thead>
            <th>type</th>
            <th>state</th>
            <th>campaign_name</th>
            <th>claimed?</th>
        </thead>
        ${this.state.data.map(camp=>{
            console.log(camp.claimed)
            let {type, state, campaign_name, campaign_id, claimed} = camp
            /*html*/
            return `
            <tr>
                <td><p>${type}</p></td>
                <td><p>${state}</p></td>
                <td><p>${campaign_name}</p></td>
                <td><input data-campaign_name="${campaign_name}" data-campaign_id="${campaign_id}" data-type="${type}" class="claimed form-control" type="checkbox" ${claimed ? 'checked' : ''}></td>
            </tr>
            `
        }).join("")}
    </table>
    `

    new DataTable(el.querySelector("#campaign_table"));
    return this.data_handler(el)
  }

  render(init=true){
    this.shadow.innerHTML = ""
    const el = document.createElement('div')

    el.innerHTML = `
        ${this.css}
    `

    if (init) {
        fetch('/api/campaigns', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                customer_id: this.customer_id,
                company_name: this.company_name,
                facebook: this.facebook,
                google: this.google
            })
        })
        .then(res=> res.json())
        .then(res=>{
            this.state.data = res
            el.appendChild(this.datatable())
        })
    } else {

    }
    this.shadow.appendChild(el)
  }

  connectedCallback() {
      this.customer_id = this.getAttribute('customer-id')
      this.company_name = this.getAttribute('company_name')
      this.google = this.getAttribute('google') ? true : false
      this.facebook = this.getAttribute('facebook') ? true : false
        
      this.render()
  }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('campaign-meta-manager', MetaManager))
