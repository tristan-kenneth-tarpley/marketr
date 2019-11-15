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
	            spend: 2,
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

        this.ctx = document.querySelector('#portfolio_mix')
        this.mix_container = document.querySelector('.portfolio_container')
        this.home()
    }

    home(){
        const inspector = document.querySelector('.inspect_container')
        inspector.style.display = 'none'

        this.mix_container.style.display = 'block'
        let labels = []
        for (let index in this.campaign_data){labels.push(this.campaign_data[index].platform)}
        let values = []
        for (let index in this.campaign_data){values.push(this.campaign_data[index].spend)}

        const data = {
            labels: labels,
            datasets: [{
                label: "Ad Spend (usd)",
                backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
                data: values,
                responsive:true
            }]
        }
        const options = {
            title: {
                display: true,
                text: 'Advertising spend (usd)'
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
                            return `<li><button class="sum_list btn btn-outline btn-outline-primary">${others[key]}</button></li>`
                        }).join("")}
                    </ul>
          
                </div>
            </div>
            <div class="card">
                <h5>${dataset.platform}</h5>
                <p>Cost per lead: ${dataset.cpl}</p>
                <p>Total spent: ${dataset.spend}</p>
                <p>Clicks: ${dataset.clicks}</p>
                <p>Click through rate: ${dataset.ctr}</p>
                <p>Revenue per click: ${dataset.rpc}</p>
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
        document.querySelector('#nav_up').addEventListener('click', e=>this.home())

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