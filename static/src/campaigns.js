export default class Portfolio {
    constructor(){
        this.campaign_data = [
            {
                platform: 'facebook',
                cpl: 24,
	            spend: 2050,
	            clicks: 2.34,
	            ctr: 2.59,
	            rpc: 'coming soon'
            },
            {
                platform: 'pinterest',
                cpl: 300,
	            spend: 200,
	            clicks: 2.34,
	            ctr: 2.59,
	            rpc: 'coming soon'
            },
            {
                platform: 'twitter',
                cpl: 3500,
	            spend: 590,
	            clicks: 2.34,
	            ctr: 2.59,
	            rpc: 'coming soon'
            },
            {
                platform: 'google ads',
                cpl: 930,
	            spend: 590,
	            clicks: 2.34,
	            ctr: 2.59,
	            rpc: 'coming soon'
            }
        ]

    }

    home(metric=this.metric){
        const inspector = document.querySelector('.inspect_container')
        const active_metric = document.querySelectorAll('.active_metric')
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
        
        const data = {
            labels: labels,
            datasets: [{
                label: "",
                backgroundColor: ["#01d4b4", "#ff9c00","#62cde0","#699fa1","#a5d6d9"],
                data: values(metric),
                responsive:true
            }]
        }
        const options = {
            title: {
                display: true,
                text: ''
            }
        }
        const mix = new Chart(this.ctx, {
            type: 'pie',
            data: data,
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
        /*html*/
        const el = `
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
                </div>
        `
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
        document.querySelector('.inspect_container').style.display = 'block'
        document.querySelector('.inspect_container').innerHTML = el
        document.querySelector('#nav_up').addEventListener('click', e=>this.home(this.metric))

        const others = document.querySelectorAll('.sum_list')

        others.forEach(el => {
            el.addEventListener('click', e=>{
                const platform = e.currentTarget.textContent
                let index = this.campaign_data.findIndex(ind => ind.platform == platform)
                this.inspect(index)
            })
        });
    }
}




