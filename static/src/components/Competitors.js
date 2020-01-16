const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');

 
    </style>
    `.trim()
}

export default class CompetitiveIntelligence extends HTMLElement {
    static get observedAttributes() {
        return ['customer-id', 'start_date'];
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

        const google = (headline, website, description) => {
            return (
                `<div class="google_ad_preview_container">
                    <h5 style="font-size: 110%;">${headline}</h5>
                    <p class="website"><span>Ad</span> ${website}</p>
                    <p>${description}</p>
                </div>`
            )
        }
        const template = (name, site, type, ad) => {
            return (
                /*html*/
                `
                <div class="row">
                    <div class="col-lg-4 col-sm-12">
                        <h5>${name}</h5>
                        <a href="https://${site}" target="__blank">${site}</a>
                    </div>
                    <div class="col-lg-2 col-sm-12">
                        <p class="comp-badge">${type}</p>
                        <p>Competitor type</p>
                    </div>
                </div>

                <div class="row comp_metrics">
                    <div style="text-align:center;" class="col-lg-3 col-sm-12">
                        <div class="comp_box comp_box-metrics">
                            <p>Adwords Budget<br>
                            <strong>${currency_rounded(ad.budget)}/month</strong></p>
                        </div>
                        <div class="comp_box comp_box-metrics">
                            <p><strong>${number_no_commas(ad.clicks)}</strong><br>clicks in past 30 days</p>
                        </div>
                    </div>
                    <div class="col-lg-1"></div>
                    <div class="col-lg-8 col-sm-12 comp_box">
                        <h5>Recent Ads</h5>
                        ${google(ad.ads[0].title, ad.ads[0].url, ad.ads[0].body)}
                        ${google(ad.ads[1].title, ad.ads[1].url, ad.ads[1].body)}
                    </div>
                </div>
                `
            )
        }

        const base = this.state.data
        /*html*/
        return `
            ${template(base.comp_1_name, base.comp_1_website, base.comp_1_type, base.competitor_intro_1)}
            <div class="separator"></div>
            ${template(base.comp_2_name, base.comp_2_website, base.comp_2_type, base.competitor_intro_2)}
        `.trim()

        return (
            /*html*/
            ` 

            
            <!--<div class="row">
                <div class=“col-lg-5 col-sm-12”>
                    <img src=“/static/assets/img/competitors.jpg”>
                </div>
                <div class=“col-lg-1”></div>
                <div class=“col-lg-6”>
                    <h5>Hey, what’s your competition doing over there?..</h5>
                    <p>Give us some info on your competitors and we’ll pull some strings and collect valuable intelligence on things like:</p>
                    <ul>
                        <li>Estimated monthly spend</li>
                        <li>Monthly clicks</li>
                        <li>Recent Ads</li>
                    </ul>
                    <a href=“/competitors” class=“btn btn-secondary”>Complete now</a>
                </div>
            </div>-->
        `.trim()
        )
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
        this.render()
        this.state.data == null
            ?  fetch('/api/competitive_intel')
                    .then(res=>res.json())
                    .then(res=>{
                        this.state.data = res
                        this.render(true)
                    })
                    .catch(e=>{
                        console.log(e)
                    })
            : this.render(true)
        
    }
}
  
document.addEventListener( 'DOMContentLoaded', customElements.define('competitive-intelligence', CompetitiveIntelligence))