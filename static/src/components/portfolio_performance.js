const styles = () => {
    return html(
      'style',
      null,
      `
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css')

        .insight_body {
            
        }
      `
    );
}

export default class PortfolioPerformance extends HTMLElement {
    static get observedAttributes() {
        return ['customer-id', 'company-name', 'facebook_id', 'google_id', 'spend_rate', 'funds_remaining', 'insights'];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.customer_id = this.getAttribute('customer-id')
        this.facebook_id = this.getAttribute('facebook_id') != null ? true : false
        this.google_id = this.getAttribute('google_id') != null ? true : false
        this.company_name = 'o3'//this.getAttribute('company-name')
        this.spend_rate = this.getAttribute('spend_rate')
        this.funds_remaining = this.getAttribute('funds_remaining')
        this.insights_json = eval(this.getAttribute('insights'))
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
            return returned
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
            ${column_packets.map(packet=>{
                /*html */
                return `
                <div class="col">
                    <h5 class="small_txt center_it">${packet.category}</h5>
                    <div class="negative_card small_txt">
                        ${packet.columns.map(column=>{
                            /*html */
                            return `                                  
                                <div class="col">
                                    <h5>${column.metric}
                                    <span class="small_txt">${column.label}</span>
                                    </h5>
                                </div>
                            `
                        }).join("")}
                    </div>
                </div>
                `
            }).join("")}
        </div>
        
        <div class="row">
            <div style="text-align:left;" class="col-lg-6 col-12">
                <p><label class="small_txt">Amount spent between ${handle('range', 'start')} and ${handle('range', 'end')}</label>: ${handle('cost', 'cost')}</p>
                <p><label class="small_txt">Funds remaining:</label> $${this.funds_remaining}</p>
                <p><label class="small_txt">Target spend per month:</label> $${this.spend_rate}/month</p>
                <a href="/home/settings">Add funds | Modify spend per week</a>
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

    render(){
        this.shadow.innerHTML = ""
        const el = document.createElement('div')
        el.innerHTML = `
            <div style="text-align:center;">
                <button id="details" class="allocation_toggle btn btn-secondary">Details</button>
                <button disabled="true" id="insights" class="btn allocation_toggle allocation_toggle-inactive">Insights</button>
                <div id="container"></div>
            </div>
        `
        this.shadow.appendChild(this.summary_handlers(el));
        this.shadow.appendChild(this.css);
    }

    connectedCallback() {
        this.render()
        setTimeout(()=>{
            fetch('/api/portfolio_metrics', {
                method: 'POST',
                headers : new Headers({
                    "content-type": "application/json"
                }),
                body:  JSON.stringify({
                    start_date: now(),
                    customer_id: this.customer_id,
                    company_name: this.company_name,
                    google: this.google_id,
                    facebook: this.facebook_id
                })
            })
                .then((res) => res.json())
                .then((data) => {
                    this.state.data = data
                    this.render()
                })
                .then(()=> this.shadow.querySelector('#insights').disabled = false)
                .catch((err)=>console.log(err))
        }, 500)

    }
}
  
document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-performance', PortfolioPerformance))