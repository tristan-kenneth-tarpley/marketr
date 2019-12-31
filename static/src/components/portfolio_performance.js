const styles = () => {
    return html(
      'style',
      null,
      `
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css')

      `
    );
}

export default class PortfolioPerformance extends HTMLElement {
    static get observedAttributes() {
        return ['customer-id', 'company-name', 'facebook_id', 'google_id', 'spend_rate', 'funds_remaining'];
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
 
        // console.log(this.company_name)
        this.state = {
            data: null
        }

        this.css = styles()
    }

    summary(){
        const data = this.state.data
        const handle = (key, value) => data == null ? '...' : data[key][value]

        /* html */
        const el = `
        <div class="row">
            <div class="col">
                <h5 class="small_txt center_it">Awareness</h5>
                <div class="negative_card">
                    <div class="col-lg-6">
                        <h5>${number(handle('awareness', 'engagement'))}</h5>
                    </div>
                    <div class="col-lg-6">
                        <p class="small_txt">Engagement</p>
                    </div>
                    <div class="col-lg-6">
                        <h5>${handle('awareness', 'impressions')}</h5>
                    </div>
                    <div class="col-lg-6">
                        <p class="small_txt">Impressions</p>
                    </div>
                </div>
            </div>
            <div class="col">
                <h5 class="small_txt center_it">Evaluation</h5>
                <div class="negative_card">
                    <div class="col-lg-6">
                        <h5>${handle('evaluation', 'ctr')}</h5>
                    </div>
                    <div class="col-lg-6">
                        <p class="small_txt">CTR</p>
                    </div>
                    <div class="col-lg-6">
                        <h5>${handle('evaluation', 'cpc')}</h5>
                    </div>
                    <div class="col-lg-6">
                        <p class="small_txt">Cost per click</p>
                    </div>
                </div>
            </div>
            <div class="col">
                <h5 class="small_txt center_it">Conversion</h5>
                <div class="negative_card">
                    <div class="col-lg-6">
                        <h5>${handle('conversion', 'cta')}</h5>
                    </div>
                    <div class="col-lg-6">
                        <p class="small_txt">Conversions</p>
                    </div>
                    <div class="col-lg-6">
                        <h5>${handle('conversion', 'site_visits')}</h5>
                    </div>
                    <div class="col-lg-6">
                        <p class="small_txt">Site visits</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <h5 class="small_txt">Funds remaining: $${this.funds_remaining}</h5>
            </div>
            <div class="col">
                <h5 class="small_txt">Spend per month: $${this.spend_rate}</h5>
            </div>
            <div class="col">
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
            container.innerHTML = this.insights()
        })

        return el
    }

    insights(){
        const el = `
            <p>these are the insights</p>
        `.trim()
        return el
    }

    render(){
        this.shadow.innerHTML = ""
        const el = document.createElement('div')
        el.innerHTML = `
            <div style="text-align:center;">
                <button id="details" class="allocation_toggle btn btn-secondary">Details</button>
                <button id="insights" class="btn allocation_toggle allocation_toggle-inactive">Insights</button>
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
                    // this.state.recs = [...data]
                    // this.edit_res(this.state.recs)
                })
                .catch((err)=>console.log(err))
        }, 1000)

    }
}
  
document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-performance', PortfolioPerformance))