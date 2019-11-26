const styles = () => {
    return html(
      'style',
      null,
      `
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css')
        .accordion-toggle {
            display: block;
          }
          
        .accordion-content {
            display: none;
        }
        
        .accordion-content.acc-active {
            display: block;
        }
      `
    );
}
const home = () => {
    return `
    <div class="row">
        <div class="col">
            <button class="active_metric btn btn-secondary">ctr</button>
        </div>
        <div class="col"><button class="active_metric btn btn-secondary">cpl</button></div>
        <div class="col"><button class="active_metric btn btn-secondary">spend</button></div>
        <div class="col"><button class="active_metric btn btn-secondary">clicks</button></div>
    </div>
    <div class="center_it portfolio_container">
        <p>Click on a platform to view more details</p>
        <canvas id="portfolio_mix"></canvas>
    </div>
    <div class="inspect_container">
    </div>`.trim()
}
    


const inspector = (dataset, others) => {
   return `
    <div class="row row_cancel">
        <div class="col">
            <div class="back">
                <button id="nav_up" class="btn btn-primary">
                    <strong><i class="now-ui-icons arrows-1_minimal-left"></i></strong>&nbsp;
                    Back
                </button>
            </div>
        </div>
        <div class="col">
            <ul class="inline-list">
                ${Object.keys(others).map(key=>{
                    return `<li class="small_txt"><button style="margin:0;" class="sum_list btn btn-neutral">${others[key]}</button></li>`
                }).join("")}
            </ul>
    
        </div>
    </div>
    <h5 class="center_it">${dataset.platform}</h5>
    <div class="row row_cancel">
        <div style="text-align:left;" class="col"></div>
        <div style="text-align:left;" class="col">
            <p>Cost per lead:</p>
        </div>
        <div style="text-align:right;" class="col">
            <p>$${dataset.cpl.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}</p>
        </div>
        <div style="text-align:left;" class="col"></div>
    </div>
    <div class="row row_cancel">
        <div style="text-align:left;" class="col"></div>
        <div style="text-align:left;" class="col">
            <p>Total spent:</p>
        </div>
        <div style="text-align:right;" class="col">
            <p>$${dataset.spend.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}</p>
        </div>
        <div style="text-align:left;" class="col"></div>
    </div>
    <div class="row row_cancel">
        <div style="text-align:left;" class="col"></div>
        <div style="text-align:left;" class="col">
            <p>Clicks:</p>
        </div>
        <div style="text-align:right;" class="col">
            <p>${dataset.clicks.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}</p>
        </div>
        <div style="text-align:left;" class="col"></div>
    </div>
    <div class="row row_cancel">
        <div style="text-align:left;" class="col"></div>
        <div style="text-align:left;" class="col">
            <p>Click through rate:</p>
        </div>
        <div style="text-align:right;" class="col">
            <p>${dataset.ctr.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}</p>
        </div>
        <div style="text-align:left;" class="col"></div>
    </div>
    <div class="row row_cancel">
        <div style="text-align:left;" class="col"></div>
        <div style="text-align:left;" class="col">
            <p>Revenue per click:</p>
        </div>
        <div style="text-align:right;" class="col">
            <p>${dataset.rpc.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}</p>
        </div>
        <div style="text-align:left;" class="col"></div>
    </div>`.trim()
}


export default class CampaignAnalyzer extends HTMLElement {
    static get observedAttributes() {
        return ['customer-id'];
    }
    constructor() {
        super();       
        this.campaign_data = [
            {
                platform: 'facebook',
                cpl: 24,
	            spend: 2050,
	            clicks: 1708,
	            ctr: 3.98,
	            rpc: 'coming soon'
            },
            {
                platform: 'pinterest',
                cpl: 18,
	            spend: 200,
	            clicks: 222,
	            ctr: 2.23,
	            rpc: 'coming soon'
            },
            {
                platform: 'twitter',
                cpl: 25,
	            spend: 590,
	            clicks: 472,
	            ctr: 1.59,
	            rpc: 'coming soon'
            },
            {
                platform: 'google ads',
                cpl: 29,
	            spend: 590,
	            clicks: 406,
	            ctr: 5.59,
	            rpc: 'coming soon'
            }
        ]
        this.shadow = this.attachShadow({ mode: 'open' });
        this.customer_id = this.getAttribute('customer-id')
    
        if (this.mix_container != null){
            this.home(this.metric)
        }

        this.css = styles()
    }    

    home(metric=this.metric){

        const inspector = this.shadow.querySelector('.inspect_container')
        const active_metric = this.shadow.querySelectorAll('.active_metric')
        active_metric.forEach(el=>{
            if (el.textContent == this.metric){
                el.style.opacity = '.5'
            } else {
                el.style.opacity = '1'
            }
            el.addEventListener('click', e=>{
                this.metric = e.currentTarget.textContent
                this.home(e.currentTarget.textContent)
            })
        })
        inspector.style.display = 'none'

        this.mix_container.style.display = 'block'
        let labels = []
        for (let index in this.campaign_data){labels.push(this.campaign_data[index].platform)}

        const values = metric => {
            let values = [];
            for (let index in this.campaign_data){
                values.push(this.campaign_data[index][metric])
            }
            return values
        }
        
        const chart_data = {
            labels: labels,
            datasets: [{
                label: "Ad Spend (USD)",
                backgroundColor: ["#01d4b4", "#ff9c00","#62cde0","#699fa1","#a5d6d9"],
                data: values(metric),
                responsive:true
            }]
        }
        const format_val = value => {
            if (this.metric == 'ctr') return `${value}%`
            else if (this.metric == 'cpc') return `$${value}`
            else if (this.metric == 'spend') return `$${value}`
            else if (this.metric == 'cpl') return `$${value}/lead`
        }
        const options = {
            legend: {
               display: true
            },
            tooltips: {
               enabled: false
            },
            title: {
                display: false,
            },
            plugins: {
                datalabels:{
                    formatter: (value, context)=> {
                        return format_val(value)
                    },
                    labels: {
                        title: {
                            color: 'rgba(255,255,255,.9)',
                            weight: "bold",
                            size: "30px",
                            textAlign: "center"
                        }
                    }
                }
            }
        }
        
        const mix = new Chart(this.ctx, {
            type: 'pie',
            data: chart_data,
            options: options
        });

        this.ctx.addEventListener('click', e=> this.inspect(mix.getElementsAtEvent(e)[0]._index)) 
    }

    platform_chart(dataset){
        let others = [];
        for (let i in this.campaign_data){
            if (this.campaign_data[i].platform != dataset.platform){
                others.push(this.campaign_data[i].platform)
            }
        }
        let platform_icon;
        switch(dataset.platform){
            case 'google ads':
                platform_icon = 'google.com'
                break
            case 'facebook':
                platform_icon = 'facebook.com'
                break
            case 'twitter':
                platform_icon = 'twitter.com'
                break
            case 'pinterest':
                platform_icon = 'pinterest.com'
                break
            case 'linkedin':
                platform_icon = 'linkedin.com'
                break
        }
        const platform_url = `http://logo.clearbit.com/${platform_icon}`
        const el = inspector(dataset, others)
        return el
    }

    filter_dataset(index){
        let dataset = this.campaign_data.filter(platform => platform.platform == this.campaign_data[index].platform)
        return dataset[0]
    }

    inspect(index){
        const dataset = this.filter_dataset(index)
        const el = this.platform_chart(dataset)
        this.mix_container.style.display = 'none'
        this.shadow.querySelector('.inspect_container').style.display = 'block'
        this.shadow.querySelector('.inspect_container').innerHTML = el
        this.shadow.querySelector('#nav_up').addEventListener('click', e=>this.home(this.metric))

        const others = this.shadow.querySelectorAll('.sum_list')

        others.forEach(el => {
            el.addEventListener('click', e=>{
                const platform = e.currentTarget.textContent
                let index = this.campaign_data.findIndex(ind => ind.platform == platform)
                this.inspect(index)
            })
        });
    }


    connectedCallback() {
        async function first(){            
            const el = document.createElement('div')
            el.innerHTML = home()

            return el
        } 
        first()
            .then(el=>{
                this.ctx = el.querySelector('#portfolio_mix')
                this.mix_container = el.querySelector('.portfolio_container')
                this.metric = 'spend'
                this.shadow.appendChild(this.css);
                this.shadow.appendChild(el);       
                return el
            })
            .then(el=>el)
            .then(el=>{
                this.home()
            })
    }
}
  
window.customElements.define('campaign-analyzer', CampaignAnalyzer);