const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');
        #trendline {
            width: 100% !important;
            margin: 0 auto;
        }
 
    </style>
    `.trim()
}

export default class PortfolioTrendline extends HTMLElement {
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

    init_chart(target){
        target.innerHTML = ""
        let labels = this.state.data ? this.state.data.map(i => i.date) : [0]
        let dataset = this.state.data ? this.state.data.map(i => i.index) : [0]
    
        const data = {
            labels,
            datasets: [
                {
                    label: "Market(r) Index",
                    fill: false,
                    borderColor: "#62cde0",
                    backgroundColor: "rgba(98, 205, 224, 0.8)",
                    borderWidth: 2,
                    pointRadius: 7,
                    pointBackgroundColor: "rgb(154, 238, 252)",
                    pointBorderColor: "rgba(98, 205, 224, 0.9)",
                    data: dataset,
                    pointHoverBorderWidth: 2,
                    pointHoverRadius: 7
                }
            ]
        };
        const ctx = target.getContext("2d");
        const options = {
            plugins: {
                datalabels:{
                    display: false
                }
            },
            elements: {
                line: {
                    tension: 0
                }
            },
            responsive: true,
            scales: {
                xAxes: [{
                    gridLines: {
                        display:false
                    }
                }],
                yAxes: [{
                    gridLines: {
                        display:false
                    }   
                }]
            }
        };
        new Chart(ctx, {
            type: 'line',
            data: data,
            options: options
        });
    }

    render(){
        this.shadow.innerHTML = ""
        const el = document.createElement('div')
        /*html*/
        el.innerHTML = `
            ${this.css}
            ${this.state.data
                ? `<p class="small_txt">When your campaigns become active, you will begin to see a trendline of your Market(r) Index-- your marketing portfolio health score.</p>
                <p class="small_txt">If you have any questions, head over to the chat tab and your Market(r) guide will reponse within an hour!</p>
                <p class="small_txt">~ Tristan Tarpley, Founder of Market(r)</p>`
                : ''
            }
            <div class="row">
                <div class="col" id="chart_container">
                    <canvas id="trendline"></canvas>
                </div>
            </div>
        `

        fetch('/api/index/trendline', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                company_name: this.customer_id == 200 ? "o3" : this.company_name,
                customer_id: this.customer_id
            })
        })
            .then((res) => res.json())
            .then(data => this.state.data = data)
            .then(() => {
                setTimeout(()=>{
                    this.init_chart(el.querySelector("#trendline"))
                }, 500)
            })
            .then(()=>{
                this.shadow.appendChild(el)
            })
            .catch((err)=>console.log(err))
    }

    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.company_name = this.getAttribute('company_name')
        this.render()

    }
}
  
document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-trendline', PortfolioTrendline))