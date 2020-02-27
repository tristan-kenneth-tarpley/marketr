import {tabs, shadow_events, dots_loader} from '/static/src/components/UI_elements.js'

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

export default class Wallet extends HTMLElement {
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

    error() {
        console.log('error')
    }

    init_submit(target, value) {
        target.addEventListener('click', e=>{
            let _value = value.value
            fetch(`/api/wallet/update`, {
                method: 'POST',
                headers : new Headers({
                    "content-type": "application/json"
                }),
                body: JSON.stringify({customer_id: this.customer_id, amount: _value})
            })
            .then(res => res.json())
            .then(res => {
                res.result == 200 ? location.reload() : this.error()
            })
        })
    }

    transaction(tr){
        let {date_added, amount, transaction_id} = tr
        let state = amount > 0 ? '+' : '-'
        let color = state == '+' ? '_green' : '_red'
        /*html*/
            const el = `
            <tr>
                <td><p>${date_added ? date_added : 'n/a'}</p></td>
                <td><p class="${color}">${state}$${amount}</p></td>
                <td><p>${transaction_id}</p></td>
            </tr>
            `

            return el
    }

    get_past_transactions(target){ 
        const get = async () => {
            const meta = await fetch(`/api/wallet/meta`, {
                method: 'POST',
                headers : new Headers({
                    "content-type": "application/json"
                }),
                body: JSON.stringify({customer_id: this.customer_id})
            })

            const _json = await meta.json()
            this.transactions = await _json

            /*html*/
            return `
            <table class="table table-striped table-borderless table-response">
                <thead>
                    <th>date added</th>
                    <th>amount</th>
                    <th>transaction_id</th>
                </thead>
                <tbody>
                    ${this.transactions.transactions.map(tr=>{
                        return this.transaction(tr)
                    }).join("")}   
                </tbody>
            </table>
            `
        }

        get().then(markup => {
            target.innerHTML += markup
        })
    }

    edit_form(){
        /*html*/
        const el = `
            <div class="row">
                <div class="col-lg-4 col-md-4 col-sm-12">
                    <div class="input-group">
                        <div class="input-group-prepend">
                            <span class="input-group-text">$</span>
                        </div>
                        <input class="form-control" id="amount">
                        <span class="form-control-border"></span>
                    </div>
                    
                    <button id="update_wallet" class="btn btn-primary">Update</button>
                </div>
                <div class="col-lg-8 col-md-8 col-sm-12">  
                    <div id="transactions">
                        <h1 class="widget__title">Past transactions &darr;</h1>
                    </div>
                </div>
            </div>
            
        `

        return el
    }

  render(init=true){
    const first = async () => {
        this.shadow.innerHTML = ""
        const el = document.createElement('div')
        el.innerHTML = `
            ${this.css}
            ${modal_trigger('wallet', 'edit')}
            ${modal('Enter amount to add or remove', this.edit_form(), 'wallet', false)}
        `
        return el
    }

    first().then(el=>{
        this.get_past_transactions(el.querySelector("#transactions"))
        this.init_submit(el.querySelector('#update_wallet'), el.querySelector("#amount"))

        return el
    })
    .then(el=>{
        this.shadow.appendChild(modal_handlers(el))
    })
  }

  connectedCallback() {
      this.customer_id = this.getAttribute('customer_id')
      this.render()
  }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('admin-wallet', Wallet))
