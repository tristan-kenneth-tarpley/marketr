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
        let labels = this.state.data ? this.state.data.map(i => i.range) : [0]
        let dataset = this.state.data ? this.state.data.map(i => parseInt(i.visits_per_thousand.toFixed())) : [0]
    
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
        const trendline = new Chart(ctx, {
            type: 'line',
            data: data,
            options: options
        });
    }

    render(init=true){
        this.shadow.innerHTML = ""
        const el = document.createElement('div')
        if (init == false && (this.state.data[0].range != "0000-00-00")) {
            /*html */
            el.innerHTML = `
                ${this.css}
                <div class="row">
                    <div class="col" id="chart_container">
                        <canvas id="trendline"></canvas>
                    </div>
                </div>
            `
            this.shadow.appendChild(el);
            this.init_chart(el.querySelector('#trendline'))
        } else if (init == true) {
            el.innerHTML = `
                ${this.css}
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
                </div>
            `
            this.shadow.appendChild(el);
        } else if (this.state.data[0].range == "0000-00-00") {
            el.innerHTML = `<div class="row"></div>`
        }
    }

    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.company_name = this.getAttribute('company_name')
        this.render()

        setTimeout(()=>{
            fetch('/api/portfolio/trend_line', {
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
                .then((data) => {
                    this.state.data = data
                    this.render(false)
                })
                .catch((err)=>console.log(err))
        }, 100)

    }
}
  
document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-trendline', PortfolioTrendline))