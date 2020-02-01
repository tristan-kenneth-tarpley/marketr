import {google, facebook} from '/static/src/components/UI_elements.js'
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
        th {
            font-size: 90%;
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
        /*html*/
        return `
            <tr>
                <td><p class="small_txt">${name}</p></td>
                <td><p class="small_txt">${type}</p></td>
                <td><p class="small_txt">${index}</p></td>
                <td><p class="small_txt">${perc_of_budget}</p></td>
                <td><p class="small_txt">${creative}</p></td>
            </tr>
        `.trim()
    }

    ad_shell(ad, index, perc_budget, spend){
        return `
        <div class="row">
            <div class="col-lg-6">
                ${ad}
            </div>
            <div class="col-lg-6">
                <div class="row">
                    <div class="col">
                        <span class="small_txt">Market(r) Index</span>
                        <h5 class="blue_label">${index}</h5>
                    </div>
                </div>

                <div class="row">
                    <div class="col">
                        <span class="small_txt">Percent of ad budget</span>
                        <h5 class="blue_label">${perc_budget}</h5>
                    </div>
                </div>

                <div class="row">
                    <div class="col">
                        <span class="small_txt">Amount spent</span>
                        <h5 class="blue_label">${spend}</h5>
                    </div>
                </div>

            </div>
        </div>
        `
    }

    core() {
        /*html*/
        return `
        <div class="row">
            <div class="col">
                <table id="creative_table" class="table table-reponsive">
                    <thead>
                        <th>Campaign name</th>
                        <th>Campaign type</th>
                        <th>Market(r) Index</th>
                        <th>Percent of budget</th>
                        <th>View ad</th>
                    </thead>
                    <tbody>
                        ${this.data.ads.social.map((it, index)=>{
                            const creative_body = this.ad_shell(
                                facebook('', it.thumbnail_url, it.body),
                                it.marketr_index.toFixed(2),
                                percent(it.cost / this.data.total_spent * 100),
                                currency(it.cost)
                            )
                            const uid = `social-${index}`
                            const creative = modal(it.name, creative_body, `social-${index}`) + modal_trigger(uid, 'view ad')
                            
                                /*html*/
                                return `
                                    ${this.display_shell(it.name, 'Social', percent(it.cost / this.data.total_spent * 100), it.marketr_index.toFixed(2), creative)}
                                `
                            }).join("")}
                    
                            ${this.data.ads.search.map((it, index)=>{
                                if (it.headline1 != 0) {
                                    let url = JSON.parse(it.finalurl)
                                    const creative_body = this.ad_shell(
                                        google(it.headline1 + " " + it.headline2, url[0], it.description != 0 ? it.description : ''),
                                        it.marketr_index.toFixed(2),
                                        percent(it.cost / this.data.total_spent * 100),
                                        currency(it.cost)
                                    )
                                    
                                    const uid = `search-${index}`
                                    const creative = modal(it.name, creative_body, uid) + modal_trigger(uid, 'view ad')
                                    return `
                                        ${this.display_shell(it.name, 'Search', percent(it.cost / this.data.total_spent * 100), it.marketr_index.toFixed(2), creative)}
                                    `
                                }
                            }).join("")}
                    </tbody>
                </table>
            </div>
        </div>
  
  
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
        const first = async () => {
            this.shadow.innerHTML = ""
            const el = document.createElement('div')
            return el
        }

        first().then(el=>{
            /*html*/
            el.innerHTML = `
            ${this.css}
            ${this.data.total_spent > 0
                ? this.core()
                : this.null_state()
                }
            `
            return el
        }).then(el=>{
            new DataTable(el.querySelector("#creative_table"))
            return el
        }).then(el=>{
            this.shadow.appendChild(el)
            
        }).then(()=>modal_handlers(this.shadow))
    }

    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.data = JSON.parse(this.getAttribute('data'))
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('account-creative', AccountCreative))

