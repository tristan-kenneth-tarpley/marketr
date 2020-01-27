import {google} from '/static/src/components/UI_elements.js'
const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');

        .blue_label {
            color: var(--darker-blue);
            font-weight: bold;
        }
    </style>
    `.trim()
}

export default class AccountCreative extends HTMLElement {
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

    display_shell(name, type, perc_of_budget, index, creative){
        return `
            <div class="row">
                <div class="col-3">
                    <p class="small_txt">${name} (${type})</p>
                </div>
                <div class="col-3">
                    <p class="small_txt">${perc_of_budget}</p>
                </div>
                <div class="col-3">
                    <p class="small_txt">${index}</p>
                </div>
                <div class="col-3">
                    ${creative}
                </div>
            </div>
        `.trim()
    }

    core() {
        return `
        <div class="row">
            <div class="col-lg-12">
                <div class="row row_cancel">
                    <div class="col-3">
                        <p style="font-size: 80%;" class="blue_label">Campaign name (type)</p>
                    </div>
                    <div class="col-3">
                        <p style="font-size: 80%;" class="blue_label">% of budget</p>
                    </div>
                    <div class="col-3">
                        <p style="font-size: 80%;" class="blue_label">Market(r) Index</p>
                    </div>
                    <div class="col-3">
                        <p style="font-size: 80%;" class="blue_label">Ad creative</p>
                    </div>
                </div>
            </div>
        </div>
  
        ${this.data.ads.social.map(it=>{
        const creative = `
            <p style="font-size: 80%;">${it.body}</p>
            <img style="width:100%;" src="${it.thumbnail_url}">
        `
            /*html*/
            return `
                ${this.display_shell(it.name, 'Social', percent(it.cost / this.data.total_spent * 100), it.marketr_index.toFixed(2), creative)}
            `
        }).join("")}

        ${this.data.ads.search.map(it=>{
            let url = JSON.parse(it.finalurl)
            const creative = google(it.headline1 + " " + it.headline2, url[0], it.description != 0 ? it.description : '')

            return `
            ${this.display_shell(it.name, 'Social', percent(it.cost / this.data.total_spent * 100), it.marketr_index.toFixed(2), creative)}
            `
        }).join("")}
  
        `.trim()

    }

    null_state(){
        return `
            <p>This is where you'll see the performance of all of the different ads that will be running for your business. Your Market(r) guide will reach out to you for any more info.</p>
            <p>Head over to the chat tab if you have any questions and you'll get a response within an hour!</p>
            <p class="small_txt">~ Tristan Tarpley, Founder of Market(r)</p>
        `
    }

    render(init=true){
        this.shadow.innerHTML = ""
        const el = document.createElement('div')

        /*html*/
        el.innerHTML = `
          ${this.css}
          ${this.data.total_spent > 0
            ? this.core()
            : this.null_state()
            }
        `
        this.shadow.appendChild(el)
    }

    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.data = JSON.parse(this.getAttribute('data'))
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('account-creative', AccountCreative))

