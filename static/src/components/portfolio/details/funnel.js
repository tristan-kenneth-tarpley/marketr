const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');
  
        label.small_txt {
            font-size: 80%;
        }

    </style>
    `.trim()
  }
  
  export default class Funnel extends HTMLElement {
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

        const el = `
        <div class="row">
            <div class="col-12">
                ${column_packets.map(packet=>{
            
                    return `
                    <div class="separator"></div>
                    <h5 class="small_txt">${packet.category}</h5>
                    <div class="row">
                        ${packet.columns.map((column, index)=>{
                
                            return `                                  
                                <div class="col-lg-6">
                                    <span class="small_txt">${column.label}</span>
                                    <h5 class="blue_label">${column.metric}</h5>
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
  
    render(init=true){
        this.shadow.innerHTML = ""
        const el = document.createElement('div')
        fetch('/api/portfolio_metrics', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                customer_id: this.customer_id,
                company_name: this.customer_id == 200 ? "o3" : this.company_name
            })
        })
            .then((res) => res.json())
            .then(res=>this.state.data = res)
            .then(()=>{ 
                el.innerHTML = `
                ${this.css}
                ${this.summary()}
            `
            })
        this.shadow.appendChild(el)
    }
  
    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.company_name = this.getAttribute('company_Name')
        this.render()
    }
  }
  
  document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-funnel', Funnel))