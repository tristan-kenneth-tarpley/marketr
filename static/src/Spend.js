export default class AdSpend {
    constructor(type, stage, revenue, brand_strength, growth_needs, competitiveness, selling_to, biz_model, active_plan){
        this.type = type
        this.stage = stage
        this.revenue = parseInt(revenue.replace(/\,/g, ''))
        this.brand_strength = brand_strength
        this.growth_needs = growth_needs
        this.competitiveness = competitiveness
        this.selling_to = selling_to
        this.biz_model = biz_model
        this.actual_budget = null
        this.custom = false
        this.active_plan = active_plan

        this.perc_or_usd = 'perc'

        document.querySelectorAll('.allocation_toggle').forEach(el => {
            el.addEventListener('click', e=>{
                e.currentTarget.classList.remove('allocation_toggle-inactive')
                e.currentTarget.classList.add('btn-secondary')
                $(".allocation_toggle").not(e.currentTarget).addClass('allocation_toggle-inactive').removeClass('btn-secondary')
                if (e.currentTarget.classList.contains('view_usd')){
                    this.perc_or_usd = 'usd'
                } else if (e.currentTarget.classList.contains('view_perc')){
                    this.perc_or_usd = 'perc'
                }
                this.update_breakdown()
                this.mount_chart()
            })
        });

        document.querySelector('#typical').addEventListener('keyup', e=>{
            this.change_budget(e.currentTarget)
        })
        document.querySelectorAll('.considerations_select').forEach(el=>{
            el.onchange = e => {
                document.querySelector("#recalc_considerations").classList.remove('hidden')
                this.change_considerations()
            }
        }) 
    }

    sum(arr){
        return arr.reduce((a,b) => a + b, 0)
    }
    prep_values(iterable) {
        let val = [];
        for (let i in iterable) {
            val.push(iterable[i].spend_per_tactic)
        }
        return this.sum(val)
    }

    change_budget(target){
        document.querySelector("#recalc").classList.remove("hidden")
        document.querySelector("#recalc").addEventListener('click', e=>{
            e.stopImmediatePropagation()
            this.custom = true
            this.actual_budget = target.value
            this.get()
            this.toggle_button(e.currentTarget)
        })
        document.querySelectorAll(".viewed_budget").forEach(element => {
            element.textContent = this.actual_budget
        });
    }

    toggle_button(target){
        const $this = target
        $this.innerHTML = `<i class="fa fa-spinner fa-spin"></i>`
        setTimeout((target=$this) => {
            target.innerHTML = `recalculate`
        }, 3000);
    }

    change_considerations(target){
        this.brand_strength = document.querySelector("#brand_strength").value
        this.growth_needs = document.querySelector("#growth_needs").value
        this.competitiveness = document.querySelector("#competitiveness").value

        document.querySelector("#recalc_considerations").classList.remove("hidden")
        document.querySelector("#recalc_considerations").addEventListener('click', e=>{
            this.toggle_button(e.currentTarget)
            this.get()
        })
    }


    metrics_state(data, perc_or_usd){
        const budget = this.actual_budget != undefined ? parseInt(this.actual_budget) : data.budget
        let budget_display = budget => "$" + budget.toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")

        document.querySelectorAll(".rec_budget").forEach(element => {
            element.textContent = budget_display(data.budget)
        });
        document.querySelectorAll(".viewed_budget").forEach(element => {
            element.textContent = budget_display(budget)
        });
        document.querySelector("#typical").value = budget.toFixed(0)
    }

    update_cta(total){
        document.querySelectorAll('.campaign_cta').forEach(el=>el.setAttribute('href', `/pricing?quantity=${total}`))
        document.querySelectorAll('.num_campaigns').forEach(el=>el.textContent = total)
    }

    update_breakdown(){
        this.metrics_state(this.data, this.perc_or_usd)
        const target = document.querySelector('#stage_breakdown')

        const display = value => this.perc_or_usd == 'usd' ? `$${value}` : `${value}%`
        const budget_ = this.data.budget
        this.update_cta(this.data.allocation[0].num_campaigns)
        const data = this.data
        
        /*html*/
        const el = `
            ${this.data.allocation.map(set=>{
                const display_num = this.perc_or_usd == 'perc' ?
                                        percent(set.spend_percent * 100) :
                                        currency_rounded(set.spend)
                /*html */
                return `
                    <p>${display_num} <span class="allocation_headers">${set.bucket}</span></p>
                    <div class="row inset">
                        <div class="col small_txt allocation_tactics awareness_tactics">
                            <ul class="campaign_list">
                                ${set['campaigns'].map(i=>{
                                    return `<li>${i}</li>`
                                }).join("")}
                            </ul>
                        </div>
                    </div>
                `.trim()
            }).join("")}

            <div class="row">
                <div class="col">
                    <h5 class="small_txt"><strong>We recommend:</strong></h5>
                    <p>${this.num_campaigns} campaigns</p>
                    <p>${currency_rounded(this.data.budget)} per month to the advertising platforms</p>
                    
                    ${ this.active_plan == 'None'
                        ? `
                        <a class="btn btn-primary" href="/pricing?quantity=${this.num_campaigns}">Apply recommendations</a>`
                        : ''
                    }
                
                </div>
            </div>
        `.trim()
        target.innerHTML = el
    }

    mount_chart(){
        const ctx = document.querySelector('#allocation_canvas')
        ctx.innerHTML = ''
        this.metrics_state(this.data, this.perc_or_usd)        
        let data = []
        let labels = []
        for (let i in this.data.allocation){
            if (this.perc_or_usd == 'perc'){
                data.push(remove_commas(this.data.allocation[i]['spend_percent'] * 100))
            } else if (this.perc_or_usd == 'usd') {
                data.push(remove_commas(this.data.allocation[i]['spend']))
            }
            
            labels.push(this.data.allocation[i].bucket)
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
               display: true
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
                    display: false
                    // formatter: (value, context)=> {
                    //     return `${this.perc_or_usd == 'usd' ? "$" : ""}${value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}${this.perc_or_usd == 'perc' ? "%" : ""}`
                    // },
                    // labels: {
                    //     title: {
                    //         color: 'rgba(255,255,255,.9)',
                    //         weight: "bold",
                    //         size: "30px",
                    //         textAlign: "center"
                    //     }
                    // }
                }
            }
        }

        const mix = new Chart(ctx, {
            type: 'pie',
            data: chart_data,
            options: options
        });
    }

    get(){
        const body = JSON.stringify({
            type: this.type,
            stage: this.stage,
            revenue: this.revenue,
            brand_strength: (this.brand_strength != null) ? this.brand_strength : 'medium',
            growth_needs: (this.growth_needs != null) ? this.growth_needs : 'medium',
            competitiveness: (this.competitiveness != null) ? this.competitiveness : 'medium',
            selling_to: this.selling_to,
            biz_model: this.biz_model,
            actual_budget: this.actual_budget
        })
        fetch('/api/spend_allocation', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body
        })
            .then((res) => res.json())
            .then((data) => {
                this.data = data
                this.num_campaigns = data.allocation.map(item => item.num_campaigns).reduce((prev, next) => prev + next);
            })
            .then(()=>{
                console.log(this.data)
                this.mount_chart()
                this.update_breakdown()
                document.querySelector("#recalc").classList.add("hidden")
                document.querySelector("#recalc_considerations").classList.add('hidden')
            })
            .catch((err)=>console.log(err))
    }
}