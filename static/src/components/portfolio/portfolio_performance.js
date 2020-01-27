import PortfolioTrendline from '/static/src/components/portfolio/portfolio_trendline.js'
import PortfolioDetails from '/static/src/components/portfolio/Details.js'
import Insights from '/static/src/components/portfolio/Insights.js'
import Creative from '/static/src/components/portfolio/Creative.js'
import {tabs, shadow_events} from '/static/src/components/UI_elements.js'

const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');

        .metric_display {
            color: var(--primary);
            font-weight: bold;
            font-size: 120%;
        }

        .metric_labels {
            font-weight: 300;
            font-size: 95%;
        }
        #select_range {
            border-top: none;
            border-left: none;
            border-right: none;
            border-bottom: 2px solid rgba(0,0,0,.1);
        }
        @media only screen and (max-width: 700px) {
            #select_range {
                position: static;
                width: 100%;
            }
        }

    </style>
    `.trim()
}

export default class PortfolioPerformance extends HTMLElement {
    static get observedAttributes() {
        return ['customer-id', 'company-name', 'facebook_id', 'google_id', 'spend_rate', 'funds_remaining', 'insights'];
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
        let labels = ['Chart', 'Funnel', 'Ads', 'Insights']
        
        let content = [
            '<div id="trendline"></div>',
            '<div id="details"></div>',
            '<div id="creative"></div>',
            '<div id="insights"></div>'
        ]
        return `
        ${tabs(labels, content, 'perf_tabs')}
        `
    }

    creative(){
        const creative = new Creative()
        creative.setAttribute('customer_id', this.customer_id)

        return creative
    }

    details(){
        const details = new PortfolioDetails()
        details.setAttribute('customer_id', this.customer_id)
        details.setAttribute('company_name', this.company_name)

        return details
    }

    insights(){
        const insights = new Insights()
        insights.setAttribute('customer_id', this.customer_id)

        return insights
    }

    trendline(){
        const trendline = new PortfolioTrendline()
        trendline.setAttribute('customer_id', this.customer_id)
        trendline.setAttribute('company_name', this.company_name)

        return trendline
    }

    render(init=true){

        this.shadow.innerHTML = ""
        /*html */
        const markup = `
            ${this.css}
            ${this.shell()}
        `

        const el = shadow_events(markup)
        el.querySelector('#trendline').appendChild(this.trendline())
        
        fetch('/api/index/detailed', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                customer_id: this.customer_id,
                company_name: this.customer_id == 200 ? "o3" : this.company_name,
                ltv: this.ltv
            })
        })
        .then(res=>res.json())
        .then(res=>{
            let deets = this.details()
            deets.setAttribute('data', JSON.stringify(res))

            let creator = this.creative()
            creator.setAttribute('data', JSON.stringify(res))

            return {creator, deets}
        })
        .then(({creator, deets})=>{
            el.querySelector('#insights').appendChild(this.insights())
            el.querySelector('#details').appendChild(deets)
            el.querySelector('#creative').appendChild(creator)
        })

        this.shadow.appendChild(el)

    }

    connectedCallback(start=now()) {
        this.customer_id = this.getAttribute('customer-id')
        this.facebook_id = this.getAttribute('facebook_id') != null ? true : false
        this.google_id = this.getAttribute('google_id') != null ? true : false
        this.company_name = this.getAttribute('company-name')
        this.spend_rate = this.getAttribute('spend_rate')
        this.funds_remaining = this.getAttribute('funds_remaining') != null ? this.getAttribute('funds_remaining') : 0
        this.insights_json = eval(this.getAttribute('insights'))
        this.ltv = this.getAttribute('ltv')
        this.render()

    }
}
  
document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-performance', PortfolioPerformance))

