const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');
        th {
            font-size: 90%;
        }
        tr {
            width: 25%;
        }
        .ad_container {
            margin-top: 2%;
        }
 
    </style>
    `.trim()
}

export default class CompetitiveIntelligence extends HTMLElement {
    static get observedAttributes() {
        return ['customer-id'];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.state = {
            data: null
        }

        this.css = styles()
    }

    shell(){

        const overview = (name, site, type) => {
            
            return /*html*/ `
            <div class="row">
                <div class="col-lg-3">
                    <h5>${name}</h5>
                </div>
                <div class="col-lg-3">
                    <a target="__blank" href="https://${site}">website</a>
                </div>
                <div class="col-lg-3">
                    <p class="comp-badge">${type}</p>
                </div>
            </div>
            `.trim()

        }

        const traffic = (name, spend, traffic, organic, paid) => {
            /*html*/
            return `   
            <tr>
                <td><h5>${name}</h5></td>
                <td>${spend}</td>
                <td>${traffic}</td>
            </tr>
            `.trim()
        }

        const google_ads = comps => {
            const google = (headline, website, description) => {
                return (
                    `<div class="google_ad_preview_container">
                        <h5 style="font-size: 110%;">${headline}</h5>
                        <p class="website"><span>Ad</span> ${website}</p>
                        <p>${description}</p>
                    </div>`
                )
            }
            /*html*/
            return `
            <p>Google Ads</p>
            <div class="row">
                ${comps.map(comp=>{
                    return comp.google_ads.map(ad=>{
                        return `
                            <div class="col-md-6 col-sm-12">
                                ${google(ad.title, ad.url, ad.body)}
                            </div>
                        `
                    }).join("")
                }).join("")}
            </div>
            `
        }

        const display_ads = comps => {
                /*html*/
            return `
            <p>Display ads</p>
            <div class="row">
                ${comps.map(comp=>{
                    return comp.display_ads.map(ad=>{
                        return `
                            <div class="col-md-6 col-sm-12">
                                <img onerror="this.style.display='none'" src="${ad}">
                            </div>
                        `
                    }).join("")
                }).join("")}
            </div>
            `
        }

        const base = this.state.data
        /*html*/
        return `
            ${base.map(comp=>{
                return overview(comp.comp_name, comp.site, comp.type)
            }).join("")}

            <div class="separator"></div>

            <div class="row">
                <div class="col-md-2"></div>
                <div class="col">
                    <table style="width: 100%;" class="table table-responsive table-borderless">
                        <thead>
                            <th></th>
                            <th><p>Est. Google Ad Spend per month</p></th>
                            <th><p>Web traffic</p></th>
                            <th><p>Paid vs. Organic search</p></th>
                        </thead>
                        <tbody>
                            ${base.map(comp=>{
                                return traffic(
                                    comp.comp_name, currency_rounded(comp.core.ppc_budget), 
                                    number_no_commas(comp.core.total_traffic), number_no_commas(comp.core.seo_clicks), 
                                    number_no_commas(comp.core.ppc_clicks) 
                                )
                            }).join("")}
                        </tbody>
                    </table>
                </div>
                <div class="col-md-2 ad_container"></div>
            </div>

            <div class="separator"></div>

            ${google_ads(base)}

            <div class="separator"></div>

            ${display_ads(base)}
            
        `.trim()
    }

    render(state=false){

        const loading = `
        <div class="row">  
            <div style="text-align:center;margin: 0 auto;" class="col">
                <div style="margin: 0 auto;" class="loading_dots">
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>`
        
        const compile = () => {
            this.shadow.innerHTML = ""
            const el = document.createElement('div')
            /*html*/
            el.innerHTML = `
                ${this.css}
                ${state == false
                    ? loading
                    : this.shell()
                }
            `
            this.shadow.appendChild(el)
        }

        compile()
    }

    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.render()

        const body = JSON.stringify({
            customer_id: this.customer_id
        })
        
        this.state.data == null
            ?  fetch('/api/competitive_intel', {
                method: 'POST',
                headers : new Headers({
                    "content-type": "application/json"
                }),
                body
            })
                    .then(res=>res.json())
                    .then(res=>{
                        this.state.data = res
                        console.log(res)
                        this.render(true)
                    })
                    .catch(e=>{
                        console.log(e)
                    })
            : this.render(true)
        
    }
}
  
document.addEventListener( 'DOMContentLoaded', customElements.define('competitive-intelligence', CompetitiveIntelligence))