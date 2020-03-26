import {tabs, shadow_events} from '/static/src/components/UI_elements.js'
import Listener from '/static/src/components/intel/listener.js'
import {iterate_text, modal, modal_trigger, modal_handlers, currency,currency_rounded,number,number_rounded,number_no_commas,percent,remove_commas,remove_commas_2} from '/static/src/convenience/helpers.js'
const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');
        .comp__inner {
            height: 25%;
            flex-direction: column;
            display:flex;
            justify-content:center;
            margin-top: 5em;
        }
        .comp_name {
            background-color: var(--panel-bg);
            padding: 8%;
            border-radius: 6px;
            box-shadow: var(--card-box-shadow);
            margin-top:2em;
        }
        
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

        .nav-tabs {
            padding: 0;
            margin-bottom: 0 !important;
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
            height: 15px;
            border-radius: 5px;
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

                <div class="col-lg-6 col-md-6 col-sm-12">
                    <p class="comp_name" style="margin: 0;"><a target="__blank" href="https://${site}">${name}</a><br>(${type} competitor)</p>
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
        // comp.comp_name, currency_rounded(comp.core.ppc_budget), 
        // number_no_commas(comp.core.total_traffic), number_no_commas(comp.core.seo_clicks), 
        // number_no_commas(comp.core.ppc_clicks)

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
                    `<div class="row row_cancel">
                    ${i.google_ads.length > 0 ? i.google_ads.map(ad=>{
                        
                        return `
                            <div class="col-md-6 col-sm-12">
                                ${google(ad.title, ad.url, ad.body)}
                            </div>
                        `.trim()
                    }).join("") : `<p>Looks like ${i.comp_name} either isn't running any Google ads, or we haven't found them yet.</p>`}
                    </div>
                    `
                )
            } 
            /*html*/
            return `
            <h1 class="widget__title">Top performing search ads</h1>
            <div class="row">
                <div class="col">
                ${tabs(labels, content, 'google')}
                </div>
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
                <div class="col-lg-4 col-md-5 col-sm-12 col-12">
                    <div style="margin-bottom:0;" class="h-100 card card-body">
                        <div id="comp_meta_container">
                            <h1 class="widget__title">Competitive intelligence &nbsp;<a class="small_txt" href="/competitors?home=True">edit</a></h1>
                            
                            <div class="row">
                            ${base.map(comp=>{
                                return overview(comp.comp_name, comp.site, comp.type)
                            }).join("")}
                            </div>

                            <div class="comp__inner">
                                <div class="row">
                                    ${base.map(comp=>{
                                        return (`
                                        <div class="col-lg-6 col-md-6 col-sm-6 col-6">
                                            <h1 class="widget__value">
                                            ${currency_rounded(comp.core.ppc_budget)}<span style="font-size:.5em;">/month</span>
                                            </h1>
                                        </div>
                                        `)
                                    }).join("")}
                                </div>
                                <h1 class="widget__title small center_it">Monthly Search ads budget</h1>
                            </div>

                            <div class="comp__inner">
                                <div class="row">
                                    ${base.map(comp=>{
                                        return (`
                                        <div class="col-lg-6 col-md-6 col-sm-6 col-6">
                                            <h1 class="widget__value">
                                            ${number_rounded(comp.core.total_traffic)}<span style="font-size:.5em;">visits</span>
                                            </h1>
                                        </div>
                                        `)
                                    }).join("")}
                                </div>
                                <h1 class="widget__title small">Web traffic</h1>
                            </div>


                            <div class="comp__inner">
                                <div class="row">
                                    ${base.map(comp=>{
                                        let {ppc_clicks, seo_clicks} = comp.core
                                        let perc_paid = number_rounded(ppc_clicks / (seo_clicks + ppc_clicks) * 100)
                                        let perc_organic = number_rounded(seo_clicks / (seo_clicks + ppc_clicks) * 100)
                                        
                                        return (`
                                        <div data-paid="${ppc_clicks}" data-organic="${seo_clicks}" class="col-lg-6 col-md-6 col-sm-6 col-6">
                                            <p style="margin-bottom: 0;" class="small_txt">paid: ${!isNaN(perc_paid) ? perc_paid : 0}%</p> <div class="traffic_meters paid_meter"></div>
                                            <p style="margin-bottom: 0;" class="small_txt">organic: ${!isNaN(perc_organic) ? perc_organic : 0}%</p> <div class="traffic_meters organic_meter"></div>
                                        </div>
                                        `)
                                    }).join("")}
                                </div>
                                <h1 class="widget__title small">Paid vs. organic search traffic</h1>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-8 col-md-7 col-sm-12">
                    <div style="margin-bottom: 0;" id="listener" class="h-100 card card-body row">
                    </div>
                </div>
            </div>

            <div class="row"> 
                <div class="col">
                    <div class="card card-body">
                        ${google_ads(base)}
                    </div>
                </div>
            </div>
 
            <!-- ${display_ads(base)} -->
            
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