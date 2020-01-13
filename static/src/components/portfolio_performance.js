import PortfolioTrendline from '/static/src/components/portfolio_trendline.js'

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

    summary(){
        const handle = (key, value) => {
            const data = this.state.data
            let returned;
            if (data == null){
                returned = "..."
            } else {
                let _value = data[key][value]
                switch (value) {
                    case 'engagement':
                        returned = percent(_value)
                        break
                    case 'impressions':
                        returned = number_no_commas(_value)
                        break
                    case 'ctr':
                        returned = percent(_value)
                        break
                    case 'cpc':
                        returned = currency(_value)
                        break
                    case 'cta':
                        returned = number_no_commas(_value)
                        break
                    case 'site_visits':
                        returned = number_no_commas(_value)
                        break
                    case 'end':
                    case 'start': 
                        returned = _value
                        break
                    case 'cost':
                        returned = currency(data.cost)
                        break
                    
                }
            }
            return `<span class="metric_display">${returned}</span>`
        }

        const column_packets = [
            {
                'category': 'Awareness',
                'columns': [
                    {
                        'metric': handle('awareness', 'engagement'),
                        'label': 'Engagement'
                    },
                    {
                        'metric': handle('awareness', 'impressions'),
                        'label': 'Impressions'
                    },
                ]
            },
            {
                'category': 'Evaluation',
                'columns': [
                    {
                        'metric': handle('evaluation', 'ctr'),
                        'label': 'Click-through rate'
                    },
                    {
                        'metric': handle('evaluation', 'cpc'),
                        'label': 'Cost per click'
                    },
                ]
            },
            {
                'category': 'Conversion',
                'columns': [
                    {
                        'metric': handle('conversion', 'cta'),
                        'label': 'Conversions'
                    },
                    {
                        'metric': handle('conversion', 'site_visits'),
                        'label': 'Site visits'
                    },
                ]
            }
        ]
        /*html */
        const el = `
        <div class="row">
            <div class="col">
                <h5 class="small_txt">For the week of ${handle('range', 'start')} through ${handle('range', 'end')}</h5>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-6 col-sm-12">
                <div class="inset" style="text-align:left;">
                    <p class="metric_labels">Funds remaining: <a class="small_txt" href="/home/settings">[Add funds]</a></p>
                    <h5 class="metric_display">$${this.funds_remaining}</h5>
                    
                    <br><br>
                    <p class="metric_labels">Amount spent:</p>
                    <h5 class="metric_display">${handle('cost', 'cost')}</h5>

                    <p class="metric_labels">Targeted spend per week: <a class="small_txt" href="/home/settings">[Modify]</a></p>
                    <h5 class="metric_display">${this.spend_rate != null ? currency(this.spend_rate*12/52) : currency(0)}</h5>
                </div>
            </div>
            <div class="col-lg-6 col-sm-12">
                ${column_packets.map(packet=>{
                    /*html */
                    return `
                    <div class="separator"></div>
                    <h5 class="small_txt">${packet.category}</h5>
                    <div class="row">
                        ${packet.columns.map((column, index)=>{
                            /*html */
                            return `                                  
                                <div class="col-lg-6">
                                    <span class="small_txt">${column.label}</span>
                                    <h5>${column.metric}</h5>
                                </div>
                            `
                        }).join("")}
                    </div>
                    `
                }).join("")}
            </div>
        </div>
        `.trim()

        return el
    }

    summary_handlers(el){
        el.querySelectorAll('.allocation_toggle').forEach(ele=>{
            ele.addEventListener('click', e=>{
                el.querySelector('.allocation_toggle:not(.allocation_toggle-inactive)').classList.remove('btn-secondary')
                el.querySelector('.allocation_toggle:not(.allocation_toggle-inactive)').classList.add('allocation_toggle-inactive')
                e.currentTarget.classList.remove('allocation_toggle-inactive')
                e.currentTarget.classList.add('btn-secondary')
            })
        })

        const container = el.querySelector("#container")
        container.innerHTML = this.summary()
        el.querySelector("#details").addEventListener('click', e=>{
            container.innerHTML = this.summary()
        })
        el.querySelector("#insights").addEventListener('click', e=>{
            container.innerHTML = ""
            this.insights(container)
        })

        el.querySelector("#select_range").addEventListener('change', e=>this.connectedCallback(e.currentTarget.value))

        return el
    }

    insights(target){
        let returned = `<p>Insights the week of ${this.state.data.range.start}</p>`
        fetch('/api/insights', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                start_date: this.state.data.range.start,
                end_date: this.state.data.range.end,
                customer_id: this.customer_id
            })
        })
            .then((res) => res.json())
            .then((data) => {
                returned += data.length > 0 
                    ? `${data.map((insight, index)=>{
                        return `<div style="text-align:left; class="insight_container">
                            <label>Insight #${index + 1} of ${data.length}</label>
                            <label class="small_txt">${insight.time}</label>
                            <p class="inset insight_body">${insight.body}</p>
                        </div>`}).join("")}`
                    : '<p>No insights were received this week</p>'
            })
            .then(()=>target.innerHTML = returned)
            .catch((err)=>console.log(err))
    }

    trendline(){
        const el = new PortfolioTrendline()
        el.setAttribute('customer_id', this.customer_id)
        el.setAttribute('company_name', this.company_name)
        return el
    }

    render(init=true){
        this.shadow.innerHTML = ""
        const el = document.createElement('div')
        /*html */
        el.innerHTML = `
            ${this.css}
            <div class="row">
                <div id="trendline" class="col">
                </div>
            </div>
            <div style="text-align:center;">
                <input id="select_range" value="${this.state.data == null ? now() : this.state.data.range.start}" type="date">
            <div>
            <div style="text-align:center;">
                <button id="details" class="allocation_toggle btn btn-secondary">Details</button>
                <button disabled="true" id="insights" class="btn allocation_toggle allocation_toggle-inactive">Insights</button>
                <div id="container"></div>
            </div>
        `
        el.querySelector('#trendline').appendChild(this.trendline())
        this.shadow.appendChild(this.summary_handlers(el));
    }

    connectedCallback(start=now()) {
        this.customer_id = this.getAttribute('customer-id')
        this.facebook_id = this.getAttribute('facebook_id') != null ? true : false
        this.google_id = this.getAttribute('google_id') != null ? true : false
        this.company_name = this.getAttribute('company-name')
        this.spend_rate = this.getAttribute('spend_rate')
        this.funds_remaining = this.getAttribute('funds_remaining')
        this.insights_json = eval(this.getAttribute('insights'))
        console.log(this.customer_id == 200 ? "o3" : this.company_name)
        this.render()
        setTimeout(()=>{
            this.start_date = start
            fetch('/api/portfolio_metrics', {
                method: 'POST',
                headers : new Headers({
                    "content-type": "application/json"
                }),
                body:  JSON.stringify({
                    start_date: this.start_date,
                    customer_id: this.customer_id,
                    company_name: this.customer_id == 200 ? "o3" : this.company_name,
                    google: this.google_id,
                    facebook: this.facebook_id
                })
            })
                .then((res) => res.json())
                .then((data) => {
                    console.log(data)
                    this.state.data = data
                    this.render(false)
                })
                .then(()=> this.shadow.querySelector('#insights').disabled = false)
                .catch((err)=>console.log(err))
        }, 100)

    }
}
  
document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-performance', PortfolioPerformance))