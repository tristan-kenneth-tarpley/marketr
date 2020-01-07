export default class AdSpend {
    constructor(type, stage, revenue, brand_strength, growth_needs, competitiveness, biz_type, biz_model, ){
        this.type = type
        this.stage = stage
        this.revenue = parseInt(revenue.replace(/\,/g, ''))
        this.brand_strength = brand_strength
        this.growth_needs = growth_needs
        this.competitiveness = competitiveness
        this.biz_type = biz_type
        this.biz_model = biz_model
        this.actual_budget = null
        this.custom = false

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
        // let awareness_val;
        // let evaluation_val;
        // let conversion_val;
        // let stage_budget;
        // let stage;
        
        // switch(this.perc_or_usd){
        //     case 'perc':
        //         stage_budget = key => parseInt(data.stage_meta[key].total)
        //         stage = key => (stage_budget(key) / budget_ * 100).toFixed(0)
        //         awareness_val = key => data.stage_detailed[0][key].spend_per_tactic / stage_budget('awareness') * 100
        //         evaluation_val = key => data.stage_detailed[1][key].spend_per_tactic / stage_budget('evaluation') * 100
        //         conversion_val = key => data.stage_detailed[2][key].spend_per_tactic / stage_budget('conversion') * 100
        //         break
        //     case 'usd':
        //         stage = key => data.stage_meta[key].total
        //         awareness_val = key => data.stage_detailed[0][key].spend_per_tactic
        //         evaluation_val = key => data.stage_detailed[1][key].spend_per_tactic
        //         conversion_val = key => data.stage_detailed[2][key].spend_per_tactic
        //         break
        // }
        
        /*html*/
        const el = `
            ${this.data.allocation.map(set=>{
                const display_num = this.perc_or_usd == 'perc' ?
                                        percent(set.spend_percent) :
                                        currency(set.spend_per_tactic)
                /*html */
                return `
                    <p>${display_num} <span class="allocation_headers">${set.bucket}</span></p>
                    <div class="row inset">
                        <div class="col small_txt allocation_tactics awareness_tactics">
                            <p>${set.tactic}</p>
                        </div>
                    </div>
                `.trim()
            }).join("")}
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
                data.push(remove_commas(this.data.allocation[i]['spend_percent']))
            } else if (this.perc_or_usd == 'usd') {
                data.push(remove_commas(this.data.allocation[i]['spend_per_tactic']))
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
               enabled: false
            },
            title: {
                display: false,
            },
            plugins: {
                datalabels:{
                    formatter: (value, context)=> {
                        return `${this.perc_or_usd == 'usd' ? "$" : ""}${value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}${this.perc_or_usd == 'perc' ? "%" : ""}`
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
            biz_type: this.biz_type,
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
            .then((data) => this.data = data)
            .then(()=>{
                this.mount_chart()
                this.update_breakdown()
                document.querySelector("#recalc").classList.add("hidden")
                document.querySelector("#recalc_considerations").classList.add('hidden')
            })
            .catch((err)=>console.log(err))
    }
}





/*
archive
<p>${display(stage('awareness')).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")} <span class="allocation_headers">awareness</span></p>
            <div class="row inset">
                <div class="col small_txt allocation_tactics awareness_tactics">
                    ${Object.keys(data.allocation).map(index=>{
                        return `
                        <p>
                            <strong>${display((awareness_val(key)).toFixed(0))}</strong>
                            &nbsp;&nbsp;&nbsp;
                            ${data.stage_detailed[0][key].tactic}
                        </p>
                        `
                        }).join("")}
                </div>
            </div>
            <p>${display(stage('evaluation')).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")} <span class="allocation_headers">evaluation</span></p>
            <div class="row inset">
                <div class="col small_txt allocation_tactics evaluation_tactics">
                    ${Object.keys(data.stage_detailed[1]).map(key=>{
                        return `
                        <p>
                            <strong>${display((evaluation_val(key)).toFixed(0))}</strong>
                            &nbsp;&nbsp;&nbsp;
                            ${data.stage_detailed[1][key].tactic}
                        </p>
                        `
                        }).join("")}
                </div>
            </div>
            <p>${display(stage('conversion')).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")} <span class="allocation_headers">conversion</span></p>
            <div class="row inset">
                <div class="col small_txt allocation_tactics awareness_tactics">
                    ${Object.keys(data.stage_detailed[2]).map(key=>{
                        return `
                        <p>
                            <strong>${display((conversion_val(key)).toFixed(0))}</strong>
                            &nbsp;&nbsp;&nbsp;
                            ${data.stage_detailed[2][key].tactic}
                        </p>
                        `
                        }).join("")}
                </div>
            </div>-->


*/