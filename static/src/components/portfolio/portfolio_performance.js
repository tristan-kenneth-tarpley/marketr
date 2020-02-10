import PortfolioTrendline from '/static/src/components/portfolio/portfolio_trendline.js'
import PortfolioDetails from '/static/src/components/portfolio/Details.js'
import Insights from '/static/src/components/portfolio/Insights.js'
import Creative from '/static/src/components/portfolio/Creative.js'
import {google, facebook} from '/static/src/components/UI_elements.js'
import Recommendations from '/static/src/components/customer/recommendations.js'
import { dots_loader } from '/static/src/components/UI_elements.js'


const title = (text, small=false) => `<h1 class="widget__title ${small ? `small` : ''}">${text}</h1>`
const value = text => `<h1 class="widget__value">${text}</h1>`

const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');
        .widget__title {
            color: var(--nav-color);
            font-size: 18px;
            margin-bottom: 5%;
            font-weight: 300;
            text-transform: capitalize;
            overflow: hidden;
            white-space: nowrap;
        }
        .widget__title.small {
            color: #b8b8d9;
            display: flex;
            font-size: 14px;
            font-weight: 500;
            margin-left: 10px;
        }
        .widget__value {
            align-items: baseline;
            color: var(--darker-blue);
            display: inline;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 15px;
            font-feature-settings: "tnum";

        }
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

        .blue-card {
            background-color: var(--panel-bg);
            box-shadow: var(--silicon-raised);
            text-align:center;
        }

        .stats {
            align-items: center;
            padding: 13px 0 11px;
            border-bottom: 1px solid #f2f2ff;
        }

        .stats {
            list-style-type: none;
            margin: 0;
            padding: 0;
            list-style: none;
        }
        .stat {
            display: flex;
            align-items: center;
            padding: 13px 0 11px;
            border-bottom: 1px solid #f2f2ff;
        }
        .stat-wrapper {
            padding: 0 30px;
            position: relative;
            list-style-type: none;
            width: 100%;
        }
        .stat span {
            vertical-align: baseline;
            margin-bottom: 0;
        }
        .stat h2 {
            color: var(--darker-blue);
            font-weight: 600;
            font-size: 25px;
            margin-right: 20px;
            flex-shrink: 0;
            margin-bottom: 0;
        }
        .stat h3 {
            color: var(--secondary);
            font-size: 18px;
            font-weight: 600;
            margin-left: auto;
            margin-bottom: 0;
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
            data: null,
            active_view: 0,
            active_data: {
                profitability: {
                    
                }
            }
        }

        this.css = styles()
    }

    profit_chart(target){
        var chart = target.getContext('2d')

        target.innerHTML = ""

        let {dates, pp1ki, cpm} = this.state.active_data.profitability
   
        const data = {
            labels: dates,
            datasets: [
                {
                    label: "Profit potential",
                    fill: false,
                    borderColor: "#62cde0",
                    backgroundColor: "rgba(98, 205, 224, 0.8)",
                    borderWidth: 2,
                    pointRadius: 7,
                    pointBackgroundColor: "rgb(154, 238, 252)",
                    pointBorderColor: "rgba(98, 205, 224, 0.9)",
                    data: pp1ki,
                    pointHoverBorderWidth: 2,
                    pointHoverRadius: 7,
                    drawBorder: true
                },
                {
                    label: "Cost per thousand impressions",
                    fill: false,
                    borderColor: "#ca7d66",
                    backgroundColor: "rgba(202, 125, 100, 0.8)",
                    borderWidth: 2,
                    pointRadius: 7,
                    pointBackgroundColor: "rgb(224, 167, 148)",
                    pointBorderColor: "rgba(202, 125, 100, 0.8)",
                    data: cpm,
                    pointHoverBorderWidth: 2,
                    pointHoverRadius: 7,
                    drawBorder: true
                }
            ]
        };
        const options = {
            legend: {
                display: true
            },
            plugins: {
                datalabels:{
                    display: false
                }
            },
            elements: {
                line: {
                    tension: 0
                }
            },
            responsive: true,
            scales: {
                xAxes: [{
                    gridLines: {
                        display:false
                    }
                }],
                yAxes: [{
                    gridLines: {
                        display:false
                    }   
                }]
            }
        };
        new Chart(chart, {
            type: 'line',
            data: data,
            options: options
        });
    }

    reset_charts(el){
        setTimeout(()=>{
            this.profit_chart(el.querySelector("#profit_chart"))
        }, 800)
    }


    data_controller(){
        let { active_view, data, active_data } = this.state
        let dates = []
        let pp1ki = []
        let cpm = []
        let buckets = []
        let sub_filters = []
        let campaigns = []
        let ads = []
    
        const append_data = (iterable, value) => [...iterable, value]
        const group = i => {
            dates = append_data(dates, i.date_start)
            pp1ki = append_data(pp1ki, i.pp1ki)
            cpm = append_data(cpm, i.cpm)
        }
        const group_buckets = i => {
            sub_filters.push(i.type)
            buckets = [...buckets, {
                type: i.type,
                dates: i.raw.map(x => x.date_start),
                cpm: i.raw.map(x => x.cpm),
                pp1ki: i.raw.map(x => x.pp1ki),
                marketr_index:i.index,
                action: i.action,
                cost: i.cost
            }]
        }
        const group_campaigns = camp => {
            campaigns = [...campaigns, {
                campaign_name: camp.campaign_name,
                pp1ki: camp.pp1ki,
                cpm: camp.cpm,
                date_start: camp.date_start,
                marketr_index:camp.marketr_index,
                action: camp.action,
                cost: camp.cost
            }]
            if (!sub_filters.includes(camp.campaign_name)) sub_filters.push(camp.campaign_name)

        }
        const group_ads = i => {
            let id = i.id == undefined ? i['adid'] : i['id']
            ads = [...ads, {
                id: id,
                pp1ki: i.pp1ki,
                cpm: i.cpm,
                marketr_index:i.marketr_index,
                date_start: i.date_start,
                action: i.action,
                cost: i.cost
            }]
            if (!sub_filters.includes(id)) sub_filters.push(id)
        }
         //dates = Array.from(new Set([...dates, i.date_start]))
        
        switch(active_view) {
            // portfolio
            case 0:
                for (let i of data.aggregate.raw) group(i)
                this.state.breakdown = data.buckets
                this.state.active_data.profitability = {dates, pp1ki, cpm, marketr_index: this.state.data.aggregate.index}
                break
            // platforms
            case 1:
                for (let i of data.buckets) group_buckets(i)
                this.sub_filters = sub_filters
                let _buckets = buckets.filter(x=>x.type == this.state.active_sub_view)
                this.state.breakdown = data.campaigns
                this.state.active_data.profitability = {
                    dates: _buckets.map(i => i.date_start),
                    pp1ki: _buckets.map(i=>i.pp1ki),
                    cpm: _buckets.map(i=>i.cpm),
                    marketr_index: _buckets[0] ? _buckets[0]['marketr_index'] : 0,
                    action: _buckets.map(i=>i.action)[0],
                    cost: _buckets.map(i=>i.cost).reduce((a, b) => a + b, 0)
                }
                break
            // campaigns
            case 2:
                if (data.campaigns.search) {
                    data.campaigns.search.map(camp=>{
                        group_campaigns(camp)
                    })
                }
                if (data.campaigns.social) {
                    data.campaigns.social.map(camp=>{
                        group_campaigns(camp)
                    })
                }

                this.sub_filters = sub_filters
                let _campaigns = campaigns.filter(x=>x.campaign_name == this.state.active_sub_view)
                let copied_campaigns = _campaigns.filter(x=>x.campaign_name == this.state.active_sub_view)
                this.state.breakdown = data.campaigns
                this.state.active_data.profitability = {
                    dates: copied_campaigns.map(_camp=>_camp.date_start),
                    pp1ki: copied_campaigns.map(_camp=>_camp.pp1ki),
                    cpm: copied_campaigns.map(_camp=>_camp.cpm),
                    marketr_index: copied_campaigns.map(_camp=>_camp.marketr_index)[copied_campaigns.map(_camp=>_camp.marketr_index).length - 1],
                    action: copied_campaigns.map(i=>i.action)[copied_campaigns.map(i=>i.action).length - 1],
                    cost: copied_campaigns.map(i=>i.cost).reduce((a, b) => a + b, 0)
                }
        
                break
            // ads
            case 3:
                if (data.ads.search) {
                    data.ads.search.map(camp=>{
                        group_ads(camp)
                    })
                }
                if (data.ads.social) {
                    data.ads.social.map(camp=>{
                        group_ads(camp)
                    })
                }
                this.sub_filters = sub_filters
                let copied_ads = ads.filter(x=>x.id == this.state.active_sub_view)
                this.state.breakdown = copied_ads[0]
                this.state.active_data.profitability = {
                    dates: copied_ads.map(_camp=>_camp.date_start),
                    pp1ki: copied_ads.map(_camp=>_camp.pp1ki),
                    cpm: copied_ads.map(_camp=>_camp.cpm),
                    marketr_index: copied_ads.map(_camp=>_camp.marketr_index).reduce((sum, value) => sum + value, 0 / copied_ads.map(_camp=>_camp.marketr_index).length),
                    action: copied_ads.map(i=>i.action)[copied_ads.map(i=>i.action).length - 1],
                    cost: copied_ads.map(i=>i.cost).reduce((a, b) => a + b, 0)
                }
                break
        }

    }

    view_controller(el){
        
        el.querySelector('#view_selector').addEventListener('change', e => {

            const first = async () => {
                this.state.active_view = parseInt(e.currentTarget.value)
            } 
            first().then(()=>this.data_controller()).then(()=>{
                this.render(false)
            })

        })

        el.querySelector("#sub_target").addEventListener('change', e=>{
            this.sub_edited = true
            const first = async () => this.state.active_sub_view = e.currentTarget.value
            first().then(()=>this.data_controller()).then(() => {
                this.render(false)
            })

        })

        return el
    }

    breakdown_markup(){
        let markup;
        let data = this.state.breakdown
        let {active_view} = this.state
        /*html*/
        const row = (index, description, description_sub, cost) => {
            return`
                <li class="stat-wrapper">
                    <div class="stat">
                        <h2>${number(index)} <p style="font-size:40%;">(health score)</p></h2>
                        <span>${description} <p style="font-size:40%;">(${description_sub})</p></span>
                        <h3>${currency(cost)} ${active_view == 1 ? `<p style="font-size:40%;">(cost per conversion)</p>` : ''}</h3>
                    </div>
                </li>
            `
        } 
        switch(this.state.active_view) {
            case 0:
                console.log(data)
                /*html*/
                markup = `
                ${data.map(_row=>{
                    return row(_row.index, _row.type, 'campaign type', _row.cost)
                }).join('')}
                `
                break
            case 1:
                let social = remove_duplicates(data.social.reverse(), 'campaign_id')
                let search = remove_duplicates(data.search.reverse(), 'campaign_id')
                console.log(social)
                console.log(search)
                markup = `
                    ${social.map(_row=>{
                        return row(
                            _row.marketr_index,
                            _row.campaign_name,
                            'campaign name',
                            _row.cost/_row.conversions || 0
                        )
                    }).join("")}
                    ${search.map(_row=>{
                        return row(
                            _row.marketr_index,
                            _row.campaign_name,
                            'campaign name',
                            _row.cost/_row.conversions || 0
                        )
                    }).join("")}
                `         
                break
            case 2:
                /*html*/
                markup = `
                <p>test 3</p>
                `
                break
            case 3:
                /*html*/
                markup = `
                <p>test 4</p>
                `
                break
        }
        return markup
    }

    template(){
        let {total_spent} = this.state.data
        let {marketr_index, action, cost} = this.state.active_data.profitability
        let company_index = this.state.data.aggregate.index
        let meta_map = {
            0: '',
            1: 'platform',
            2: 'campaign',
            3: 'ad'
        }
        /*html*/
        return `
            <div class="col-lg-6 col-md-6 col-12">
                <div class="card card-body">
                    <div class="row row_cancel">
                        <div style="display: ${this.state.active_view != 0 ? 'auto' : 'none'};" class="col">
                            ${title(`${meta_map[this.state.active_view]} health score`)}
                            ${value(number(marketr_index ? marketr_index : 0))}
                        </div>
                        <div class="col">
                            ${title('total health score')}
                            ${value(number(company_index ? company_index : 0))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-sm-6 ${this.state.active_view == 0 ? 'col-lg-6 col-md-6' : 'col-lg-5 col-md-5'}">
            <div class="row">
                <div class="col card card-body">
                    ${title('profitability spread')}
                    <br>
                    <div class="row">
                        <div class="col" id="profit_chart_container">
                            <canvas id="profit_chart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                ${
                    this.state.active_view != 0
                        ? `
                        <div class="col">
                    
                            <div class="card card-body">
                                ${title('our recommendation')}
                                ${value(action ? action : "")}
                            </div>
                        </div>`
                        : ''
                    }
            </div>
        </div>
        <div class="col-sm-6 ${this.state.active_view == 0 ? 'col-lg-6 col-md-6' : 'col-lg-7 col-md-7'}">
            <div class="card card-body">
                ${title('Breakdown')}
                ${this.breakdown_markup()}
            </div>
        </div>
        </div>
        <div class="row">
            <div class="col">
                <div id="insights" class="card card-body">
                    ${title('insights')}
                </div>
            </div>
            <div class="col">
                <div id="recommendations" class="card card-body">
                    ${title('recommendations')}
                </div>
            </div>
        </div>
        `
    }

    shell(){


        /*html*/
        return `
            <div class="row">
                <div class="col-lg-2 col-md-2 col-12">
                </div>
                <div class="blue-card card card-body col-lg-8 col-md-8 col-12">
                    <div class="row row_cancel">
                        <div class='col'></div>
                        <div class="col-lg-4 col-md-4 col-12">
                            ${title(`Funds remaining: ${value(currency(this.funds_remaining))}`)}
                        </div>
                        <div class="col-lg-4 col-md-4 col-12">
                            ${title(`spend rate: ${value(`${currency(this.spend_rate)}/month`)}`)}
                        </div>
                        <div class='col'></div>
                    </div>
                </div>
                <div class="col-lg-2 col-md-2 col-12">
                </div>
            </div>
            <div id="home-row" class="row">
                <div class="col-lg-6 col-md-6 col-12">
                    <div class="card card-body">
                        <div class="row">
                            <div class="col">
                                ${title('view by')}
                                <select class="form-control" id="view_selector">
                                    <option value="0" ${this.state.active_view == 0 ? 'selected' : ''}>portfolio</option>
                                    <option value="1" ${this.state.active_view == 1 ? 'selected' : ''}>platforms</option>
                                    <option value="2" ${this.state.active_view == 2 ? 'selected' : ''}>campaigns</option>
                                    <option value="3" ${this.state.active_view == 3 ? 'selected' : ''}>ads</option>
                                </select>
                            </div>
                            <div class="col">
                                ${
                                    this.state.active_view != 0
                                    /*html*/
                                    ? `
                                
                                        ${title('filter by', true)}
                                        <select id="sub_target" class="form-control">
                                            ${this.sub_filters.map((filter, index)=>{
                                                return (
                                                    `<option value="${filter}" ${filter == this.state.active_sub_view  ? `selected` : '' }>
                                                        ${filter}
                                                    </option>
                                                    `
                                                )
                                            }).join('')}
                                        </select>`
                                    : `<select id="sub_target" style="visibility:hidden;" class="form-control"></select>`
                                }
                            </div>
                        </div>
                    </div>
                </div>
           
        `
    }

    recs(){
        const recs_ = new Recommendations()
        recs_.setAttribute('customer-id', this.customer_id)

        return recs_
    }


    insights(){
        const insights = new Insights()
        insights.setAttribute('customer_id', this.customer_id)

        return insights
    }


    render(init=true){
        this.shadow.innerHTML = ""

        const recs = this.recs()
        const insights = this.insights()

        const compile = async () => {

            let el;
      
    
            const markup = `
                ${this.css}
                ${this.shell()}
            `
            el = document.createElement('div')
            el.innerHTML = markup

            if (this.state.active_view > 0 && !this.sub_edited) this.state.active_sub_view = this.sub_filters[0]
            this.data_controller()

            return el
        } 

        const run = () => {
            compile()
                .then(el=>{
                    el.querySelector('#home-row').innerHTML += this.template()
                    return el
                })
                .then(el=>{
                    this.reset_charts(el)
                    el.querySelector("#recommendations").appendChild(recs)
                    el.querySelector('#insights').appendChild(insights)
                    return el
                })
                .then( el => this.shadow.appendChild(this.view_controller(el)) )
        }


        if (init == true) {
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
            .then(res => {
                this.state.data = res
            })
            .then(()=> run())
        } else run()
    }

    connectedCallback(start=now()) {
        this.customer_id = this.getAttribute('customer-id')
        this.facebook_id = this.getAttribute('facebook_id') != null ? true : false
        this.google_id = this.getAttribute('google_id') != null ? true : false
        this.company_name = this.getAttribute('company-name')
        this.spend_rate = this.getAttribute('spend_rate') != null ? parseFloat(this.getAttribute('spend_rate')) : 0
        this.funds_remaining = this.getAttribute('funds_remaining') != null ? parseFloat(this.getAttribute('funds_remaining')) : 0
        this.insights_json = eval(this.getAttribute('insights'))
        this.ltv = this.getAttribute('ltv')
        this.render()

    }
}
  
document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-performance', PortfolioPerformance))

