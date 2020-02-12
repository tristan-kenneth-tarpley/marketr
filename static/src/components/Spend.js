import {right_modal, inline_article} from '/static/src/components/UI_elements.js'
const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');
   
        #allocation_canvas {
            width: 100%;
            height: 100%;
        }
    </style>
    `.trim()
}

export default class AdSpend extends HTMLElement {
    static get observedAttributes() {
        return ['type', 'stage', 'revenue', 'brand_strength', 'growth_needs', 'competitiveness', 'selling_to', 'biz_model', 'active_plan'];
    }

    constructor(){
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.state = {
            data: null,
            real: null
        }

        this.css = styles()
        this.perc_or_usd = 'perc'
    }


    toggle_button(target){
        target.classList.remove('hidden')
        const $this = target
        $this.innerHTML = `<i class="fa fa-spinner fa-spin"></i>`
        setTimeout((target=$this) => {
            target.innerHTML = `recalculate`
            target.classList.add('hidden')
        }, 3000);
    }

    considerations(){

        const considerations_meta = {
            "brand<br>strength": {
                id: "brand_strength",
                hover: `<p>Brand strength is a relative measure of your brand in the marketplace you're targeting.</p>
                <p>Low | less than 5% market share</p>
                <p>Medium | 5% - 15% market share</p>
                <p>High |  more than 15% market share</p>`

            },
            "growth<br>needs": {
                id: "growth_needs",
                hover: `<p>Growth needs ties into how quickly you need (or want) to grow in the marketplace as it compares to competitors and your current position in the marketplace. </p>
                <p>Low |  No need to rapidly acquire new clients.  May be still building product, not ready to scale, and/or holding your market position.</p>
                <p>Medium | Definitely need or want some new clients, but okay to pace with the competition. </p>  
                <p>High |  Need rapid growth at all costs.</p>`

            },
            "market<br>competitiveness": {
                id: "competitiveness",
                hover: `<p>Competitiveness specifies how crowded and intense the competition is within your specific market and niche.  </p>
                <p>Low |  Only a couple players and/or low intensity competition.  Lots of green-field available to expand into.</p>
                <p>Medium | A few established competitors and or new entrants, but more than enough market available.</p>
                <p>High |  Competition is intense.  Established players and/or many new entrants.</p>`

            }
    }

        const shell = (value, title) => {
            return (
            /*html*/
                `
                <div class='col-lg-3 col-md-3 col-sm-12 center_it'>   
                    <div id="six" data-uid="${title}" class="modal-controller button"><p>${title}</p></div>
                    ${modal(title, considerations_meta[title].hover, title)}
                    <select class="form-control considerations" id="${considerations_meta[title].id}" class="considerations_select form-control">
                        <option value="high" ${value == 'high' ? "selected" : ""}>high</option>
                        <option value="medium" ${value == 'medium' ? "selected" : ""}>medium</option>
                        <option value="low" ${value == 'low' ? "selected" : ""}>low</option>
                    </select>
                </div>
                `.trim()
            )
        }
        /*html*/
        return (
            `<div class="row">
            <div class="col-md-3">
                <p class="small_txt">Describe your company market state by selecting Low, Medium, or High for the following:</p>
            </div>

            ${shell(this.brand_strength, "brand<br>strength")}
            ${shell(this.growth_needs, "growth<br>needs")}
            ${shell(this.competitiveness, "market<br>competitiveness")}
            <div class="col"></div>
            <div class="col center_it">
                <button id="recalc_considerations" class="hidden btn btn-outline btn-outline-primary">Recalculate</button>
            </div>
            <div class="col"></div>
        </div>`
        )
    }

    update_cta(total, el){
        el.querySelectorAll('.campaign_cta').forEach(el=>el.setAttribute('href', `/pricing?quantity=${total}`))
        el.querySelectorAll('.num_campaigns').forEach(el=>el.textContent = total)
    }

    update_breakdown(_el){
        
        const target = _el.querySelector('#stage_breakdown')

        const display = value => this.perc_or_usd == 'usd' ? `$${value}` : `${value}%`
        const budget_ = this.data.budget
        this.update_cta(this.data.allocation[0].num_campaigns, _el)
        const data = this.data

        let counter = 0
        
        /*html*/
        const el = `
            <p>Here are the campaigns that we recommend:</p>
            ${this.data.allocation.map((set, index)=>{
                const display_num = this.perc_or_usd == 'perc' ?
                                        percent(set.spend_percent * 100) :
                                        currency_rounded(set.spend)
                /*html */
                return `
                    <p>${display_num}
                       
                            | ${set.bucket}

                            ${ set.bucket == 'seo'
                                ? `<a target="__blank" href="https://marketr.life/blog/the-total-guide-to-investing-in-search-engine-optimization">learn more</a>`
                                : ''
                            }
            
                    </p>
                    <div class="row inset">
                        <div class="col small_txt allocation_tactics awareness_tactics">
                            
                            <ul class="campaign_list">
                                ${set['campaigns'].map((i, _index)=>{
                                    counter++
                                    /*html*/
                                    return `${inline_article(i)
                                                ? `
                                                <li class="campaign_type">
                                                    ${modal_trigger(i, `${counter}: ${i} <span style="color:#62cde0;">></span>`)}
                                                    ${right_modal('', inline_article(i), i)}
                                                </li>
                                                `
                                                : `<li>${counter}: ${i}</li>`
                                            }`
                                }).join("")}
                            </ul>
                        </div>
                    </div>
                `.trim()
            }).join("")}
        `.trim()
        target.innerHTML = el
    }

    mount_chart(target){
        const ctx = target
        
        let data = []
        let labels = []
        for (let i of this.data.allocation) {
            this.perc_or_usd == 'perc'
                ? data.push(remove_commas(i.spend_percent * 100))
                : data.push(remove_commas(i.spend))
            labels.push(i.bucket)
        }

        const chart_data = {
            labels,
            datasets: [{
                label: "Ad Spend (USD)",
                backgroundColor: ["#01d4b4", "#ff9c00","#62cde0","#699fa1","#a5d6d9"],
                data,
                responsive:true
            }]
        }
        const options = {
            legend: {
               display: false
            },
            tooltips: {
               enabled: true
            },
            title: {
                display: true,
            },
            plugins: {
                datalabels:
                {
                    display: true,
                    formatter: (value, context)=> {
                        let label = context.chart.data.labels[context.dataIndex]
                        return label
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

        new Chart(ctx, {type: 'pie', data: chart_data, options});
    }

    shell(){
        const modal_markup = `<p>We provide a recommended budget based on the following factors:</p>
        <ul class='no-dec'>
            <li>Stage of your company</li>
            <li>Annual Revenues</li>
            <li>Business model</li>
        </ul>
        
        <p>Additional factors that you may want to adjust your spend targets (either up or down) include:</p>
        <ul class='no-dec'>
            <li>Competitiveness of your product/service niche.</li>
            <li>Industry-specific adjustments i.e. financial or real-estate services may require a higher spend rate for effective results.</li>
            <li>Location.</li>
            <li>Average Customer Life Time Value.  A higher CLTV means more competitors fighting and driving up the cost to reach and acquire new customers.</li>
        </ul>`
        const uid = "how_calculated"
        /*html*/
        return (
            
            `<div class="row ${this.active_plan ? '' : 'hidden'}">
                <div class="center_it col">
                    <button class="budget_type actual_budget_view allocation_toggle btn ${
                        this.state.real == true
                        ? 'btn btn-secondary'
                        : 'allocation_toggle-inactive'}">real budget</button>
                    <button class="budget_type rec_budget_view allocation_toggle btn ${
                        this.state.real == false
                        ? 'btn btn-secondary'
                        : 'allocation_toggle-inactive'}">recommended</button>
                </div>
            </div>
            <div class="row row_cancel">
                <div class="col-md-2 col-12"></div>
                <div class="${this.state.real && this.active_plan ? 'col-md-8 col-12' : 'col-md-4 col-12'}">
                    <p><strong>
                        ${this.state.real
                            ? `Ad spend budget:`
                            : `Recommended budget:`}
                    </strong></p>
                    <div style="padding-top:7%;" class="card center_it negative_card">
                        <h5>
                            <strong>${currency_rounded(parseFloat(this.viewed_budget))}</strong> /month
                            ${this.state.real && this.active_plan && this.demo != 'True' ? `<a href="/home/settings" class="small_txt">[edit]</a>`:''}
                        </h5>
                        ${this.actual_budget == null ?
                        /*html*/
                        `<div id="six" data-uid="${uid}" class="modal-controller button"><p>How is this calculated?</p></div>
                        ${modal("How is this calculated", modal_markup, uid)}
                        `
                        : 
                        /*html*/
                        `<p class="small_txt">Recommend: ${currency_rounded(this.data.recommended_budget)}/month</p>`}
                    </div>
                </div>
                <div class="col-md-4 col-12 ${this.state.real && this.active_plan ? ' hidden' : ''}">
                    <p class="small_txt">View recommendations with new budget:</p>
                    <div class="form-group">
                        <input type="number" value="${number(parseFloat(this.viewed_budget))}" id="typical" class="form-control">
                        <div class="form-control-border"></div>
                    </div>
                    <p class="small_txt"><em>Changing this will affect the marketing spend mix below</em></p>
                </div>

                <div class="col-md-2 col-12 ${this.state.real && this.active_plan ? 'hidden' : ''}">
                    <button id="recalc" class="hidden btn btn-outline btn-outline-primary">Recalculate</button>
                </div>
           
            </div>

            <div class="row">
                <div class="col-lg-3 col-md-3 col-sm-12">
                    <canvas width="100%" height="100%" id="allocation_canvas"></canvas>
                </div>
                <div class="col-lg-5 col-md-5 col-sm-12">
                    <br>
                    <div style="margin:0 auto;text-align:center;">
                        <button class="spend_num_type view_perc allocation_toggle btn ${
                            this.perc_or_usd == 'perc'
                            ? 'btn btn-secondary'
                            : 'allocation_toggle-inactive'}">%</button>
                        <button class="spend_num_type view_usd allocation_toggle btn ${
                            this.perc_or_usd == 'usd' 
                            ? 'btn btn-secondary'
                            : 'allocation_toggle-inactive'}">$</button>
                    </div>
                    <div id="stage_breakdown" class="inset">
                    </div>
                </div>
                <div class="col-lg-4 col-md-4 col-sm-12">        
                    <div class="next_steps">
                        <h6>Next steps</h6>
                        <div class="top">
                            <h5>Do it yourself</h5>
                            <p>Go forth and conquer.  Keep us posted on your successes!</p>

                            <h5 class="center_it">or</h5>

                            <h5>We can help</h5>
                            <p>Market(r) will create, manage, and optimize your campaign(s) overtime for a flat-monthly fee.</p>

                        </div>
                        <div class="bottom">
                            <div class="center_it">
                                <a class="btn btn-secondary" href="/pricing">view plans</a><br>
                                <a href="/schedule">want to chat first?</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            `
        )
    }

    compile(){

        this.budget_variance = (this.spend_rate - this.data.recommended_budget) / this.spend_rate * 100
        if (this.active_plan) {
            if (this.state.real) this.viewed_budget = this.spend_rate
            else if (this.custom_budget) this.viewed_budget = this.custom_budget
            else this.viewed_budget = this.data.recommended_budget
        } else {
            if (this.custom_budget) this.viewed_budget = this.custom_budget 
            else this.viewed_budget = this.data.recommended_budget
        }
        
        const first = async () => {
            this.shadow.innerHTML = ""
    
            const _el = document.createElement('div')
            _el.innerHTML = `
                ${this.css}
                ${this.considerations()}
                <div class="separator"></div>
                ${this.shell()}
            `
            return _el
        }

        const second = async (_el) => {

            this.num_campaigns = this.data.allocation.map(item => item.num_campaigns).reduce((prev, next) => prev + next); 
            
            this.update_breakdown(_el)
            _el.querySelector("#recalc").addEventListener("click", e=>{
                const value = _el.querySelector("#typical").value
                if (!isNaN(value)) {
                    this.toggle_button(_el.querySelector("#recalc"))
                    this.custom_budget = parseFloat(value)
                    this.render()
                }
            })
            _el.querySelector("#typical").addEventListener("keyup", e=>_el.querySelector("#recalc").classList.remove('hidden'))

            _el.querySelectorAll(".considerations").forEach(c=>{
                c.addEventListener('change', e=>{
                    _el.querySelector("#recalc_considerations").classList.remove("hidden")
                    let value = e.currentTarget.value
                    switch (e.currentTarget.id) {
                        case 'growth_needs':
                            this.growth_needs = value
                            break
                        case 'competitiveness':
                            this.competitiveness = value
                            break
                        case 'brand_strength':
                            this.brand_strength = value
                            break
                    }
                    _el.querySelector("#recalc_considerations").onclick = e => {
                        this.toggle_button(e.currentTarget)
                        this.render()
                    }
                })
            })
            _el.querySelectorAll('.allocation_toggle').forEach(btn=>{
                btn.addEventListener('click', e => {
                    const classList = e.currentTarget.classList
                    
                    if (classList.contains('spend_num_type')) {
                        classList.contains('view_perc')
                            ? this.perc_or_usd = 'perc'
                            : this.perc_or_usd = 'usd'
                        this.render()
                    } else if (classList.contains('budget_type')) {
                        (async () => {
                            this.toggle_button(e.currentTarget)
                            if (classList.contains('actual_budget_view')) {
                                setQueryString('real', 'true')
                                this.actual_budget = null
                            }
                            else {
                                setQueryString('real', 'false')
                            }
                        })().then(()=>this.render())
                    }
                })
            })

            setTimeout(()=>{
                this.mount_chart(_el.querySelector('#allocation_canvas'))
            }, 100)
            
            return _el
        }

        first()
            .then(_el => second(_el))
            .then(_el => this.shadow.appendChild(_el))
            .then(()=>{
                modal_handlers(this.shadow)
            })
    }

    detectReal(){
        const status = eval(params().get('real'))
        
        if (this.active_plan) {
            if (status == null || status == true ) return true
            else if (status == false) return false

        } else return false
    
    }

    render(){
        this.state.real = this.detectReal()

        let budget = null;
        if (this.active_plan) {
            if (this.state.real) budget = this.spend_rate ? this.spend_rate : 0
            else if (this.state.real == false && this.custom_budget) budget = this.custom_budget
            else budget = null
        } else { 
            if (this.custom_budget) budget = this.custom_budget 
            else budget = null
        }

        const body = JSON.stringify({
            customer_id: this.customer_id,
            type: this.type,
            stage: this.stage,
            revenue: this.revenue,
            brand_strength: (this.brand_strength != null) ? this.brand_strength : 'medium',
            growth_needs: (this.growth_needs != null) ? this.growth_needs : 'medium',
            competitiveness: (this.competitiveness != null) ? this.competitiveness : 'medium',
            selling_to: this.selling_to,
            biz_model: this.biz_model,
            viewed_budget: budget
        })
     
        fetch('/api/spend_allocation', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body
        })
            .then((res) => res.json())
            .then((data) => this.data = data )
            .then(()=> this.compile() )
            .catch((err)=>console.log(err))
    }

    connectedCallback(){
        this.customer_id = this.getAttribute('customer_id')
        this.type = this.getAttribute('type')
        this.stage = this.getAttribute('stage')
        this.revenue = parseInt(this.getAttribute('revenue').replace(/\,/g, ''))
        this.brand_strength = this.getAttribute('brand_strength')
        this.growth_needs = this.getAttribute('growth_needs')
        this.competitiveness = this.getAttribute('competitiveness')
        this.selling_to = this.getAttribute('selling_to')
        this.biz_model = this.getAttribute('biz_model')
        this.demo = this.getAttribute('demo')
        this.active_plan = this.getAttribute('active_plan') == 'None'
                            ? false
                            : true

        this.spend_rate = this.getAttribute('spend_rate') != null && this.getAttribute('spend_rate') != 'None'
                            ? this.getAttribute('spend_rate')
                            : 0


        this.state.real = false

        this.render()

    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('ad-spend', AdSpend))