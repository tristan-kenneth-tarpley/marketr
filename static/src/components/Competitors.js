import {tabs, shadow_events} from '/static/src/components/UI_elements.js'
import Listener from '/static/src/components/intel/listener.js'
import {iterate_text, modal, modal_trigger, modal_handlers, currency,currency_rounded,number,number_rounded,number_no_commas,percent,remove_commas,remove_commas_2} from '/static/src/convenience/helpers.js'
const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/app.css');
        th p {
            font-size: .5em;
        }
        /*mobile typography*/
        @media only screen 
        and (min-width: 200px) 
        and (max-width: 700px)
        and (-webkit-min-device-pixel-ratio: 2) {
            td {
                padding: 0;
            }
        }

        .nav-tabs li {
            width: 100%;
        }
        .nav-tabs {
            padding: 0;
        }
        tr {
            width: 25%;
        }
        .ad_container {
            margin-top: 2%;
        }
        .spend {
            font-weight: bold;
            color: var(--primary);
        }

        .comp-badge {
            max-width: 150px;
        }

        .comp-badge.indirect {
            background-color: var(--darker-blue);
        }

        .nav-tabs {
            margin-bottom: 5%;
        }

        .traffic_meters {
            height: 10px;
        }
        .traffic_meters div {
            display: inline;
        }
        .organic_meter {
            background-color: #9CE4F1;
        }
        .paid_meter {
            background-color: var(--primary);
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

    listener(keywords){
        const el = new Listener()
        el.setAttribute('keywords', JSON.stringify(keywords))
        el.setAttribute('customer_id', this.customer_id)

        return el
    }

    shell(){

        const overview = (name, site, type) => {
            
            return /*html*/ `
            <div class="row">
                <div class="col-12">
                    <div class="row">
                        <div class="col-md-2 col-sm-12"></div>
                        <div class="col-lg-6">
                            <p>${name}</p>
                            <a class="small_txt" target="__blank" href="https://${site}">website</a>
                            <p class="small_txt comp-badge ${type}">${type}</p>
                        </div>
                        <div class='col-lg-4'></div>
                    </div>
                </div>
            </div>
            `.trim()

        }

        const traffic = (name, spend, traffic, organic, paid) => {
            /*html*/
            return `   
            <tr>
                <td>${name}</td>
                <td class="spend">${spend}</td>
                <td>${traffic}</td>
                <td data-paid="${paid}" data-organic="${organic}" class="traffic_meters_container">
                    <div class="traffic_meters paid_meter"></div>
                    <div class="traffic_meters organic_meter"></div>
                </td>
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

            let labels = []
            let content = []
            for (let i of comps) {
                labels.push(i.comp_name) 
                content.push (
                    `<div class="row">
                    ${i.google_ads.map(ad=>{
                        return `
                            <div class="col-md-6 col-sm-12">
                                ${google(ad.title, ad.url, ad.body)}
                            </div>
                        `.trim()
                    }).join("")}
                    </div>
                    `
                )
            } 
            /*html*/
            return `
            <p>Google Ads</p>
            <div class="row">
                ${tabs(labels, content, 'google')}
            </div>
            `
        }

        const display_ads = comps => {
            let labels = []
            let content = []
            for (let i of comps) {
                labels.push(i.comp_name) 
                content.push (
                    `<div class="row">
                        ${ i.display_ads.length > 0 
                            ? i.display_ads.map(ad=>{
                                return `
                                    <div class="col-md-6 col-sm-12">
                                        <img onerror="this.style.display='none'" src="${ad}">
                                    </div>
                                `.trim()
                            }).join("")
                            : `<p>Hmm...It looks like ${i.comp_name} hasn't ran any display ads.</p>`
                        }
                    </div>`.trim()
                )
            } 
                /*html*/
            return `
            <p>Display ads</p>
            <div class="row">
                ${tabs(labels, content, 'display')}
            </div>
            `
        }

        const base = this.state.data
        
        /*html*/
        return `
            <div class="row">
                <div class="col-lg-3 col-sm-12">
                    ${base.map(comp=>{
                        return overview(comp.comp_name, comp.site, comp.type)
                    }).join("")}
                </div>
                <div class="col-lg-9 col-sm-12">
                    <div id="listener" class="row">
                    </div>
                </div>
            </div>
            <div class="separator"></div>

            <div class="row">
                <div class="col-md-1"></div>
                <div class="col">
                    <table style="width: 100%;overflow: auto;" class="table table-responsive table-borderless">
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
                <div class="col-md-1 ad_container"></div>
            </div>

            <div class="separator"></div>

            ${google_ads(base)}

            <!--<div class="separator"></div>

            ${display_ads(base)}-->
            
        `.trim()
    }

    render(state=false){



        const loading = `
        <div class="center_it" id="stall"><span></span></div>

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
        
        const compile = async () => {
            this.shadow.innerHTML = ""
            /*html*/
            const markup = `
                ${this.css}
                ${state == false
                    ? loading
                    : this.shell()
                }
            `
            const el = shadow_events(markup)

            return el
        }

        compile().then(el=>{
            el.querySelectorAll('.traffic_meters').forEach(meter=>{
                const organic = remove_commas_2(meter.parentNode.dataset.organic)
                const paid = remove_commas_2(meter.parentNode.dataset.paid)

                const total = organic + paid

                if (meter.classList.contains('paid_meter')){
                    meter.style.width = `${paid/total*100}%`
                } else if (meter.classList.contains('organic_meter')){
                    meter.style.width = `${organic/total*100}%`
                }
            })

            return el
        }).then(el=>this.shadow.appendChild(el))
        .then(()=>{
            let it;
            if(this.state.data == null){
                const lines = [
                    '...Analyzing top keywords of your competitors...',
                    "...Scanning the web for related conversations...",
                    "...o_O  these look interesting...",
                    "...Check them out and get engaged!"
                ]
                it = iterate_text(lines, this.shadow.querySelector('#stall'))
            } else {
                clearInterval(it)
            }
   
        })
        
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
                        this.render(true)
                    })
                    .then(()=>{
                        let keywords = []
                        for (let i of this.state.data) {
                            keywords = [...keywords.flat(), {
                                'comp_name': i.comp_name,
                                'keywords': i.core.keywords.flat()
                            }]
                        }

                        return keywords
                    })
                    .then(keywords=>{
                        this.shadow.querySelector('#listener').appendChild(this.listener(keywords))
                    })
                    .catch(e=>{
                        console.log(e)
                    })
            : this.render(true)
        
    }
}
  
document.addEventListener( 'DOMContentLoaded', customElements.define('competitive-intelligence', CompetitiveIntelligence))