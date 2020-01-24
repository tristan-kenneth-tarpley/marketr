const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');

        .blue_label {
            font-weight: bold;
            color: var(--darker-blue);
        }
    </style>
    `.trim()
}

export default class Budget extends HTMLElement {
    static get observedAttributes() {
        return ['customer_id'];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.state = {
            data: null
        }

        this.css = styles()
    }

    shell() {
        /*html*/
        return `
        ${this.css}
        <div class="row row_cancel">
            <div class="col-4">
                <p class='small_txt'>Funds remaining<br><a href="/home/settings">[add more]</a>:</p>
            </div>
            <div class="col-4">
                <p class="small_txt">Amount spent (last 7 days):</p>
            </div>
            <div class="col-4">
                <p class="small_txt">Target weekly spend<br><a href="/home/settings">[change]</a>:</p>
            </div>
        </div>

        <div class="row">
            <div class="col-4">
                <h5 class='blue_label'>${currency(parseFloat(this.funds_remaining))}</h5>
            </div>
            <div class="col-4">
                <h5 class="blue_label">${currency_rounded(parseFloat(this.state.data.spend))}</h5>
            </div>
            <div class="col-4">
                <h5 class="blue_label">${currency_rounded(this.spend_rate * 12 / 52)}</h5>
            </div>
        </div>
        `.trim()
    }

    render(init=true){
        this.shadow.innerHTML = ""
        const el = document.createElement('div')
        
        fetch('/api/spend/last_7', {
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
            .then(res=>this.state.data = res)
            .then(()=>{
                el.innerHTML = this.shell()
            })
            .then(()=>{
                this.shadow.appendChild(el)
            })
    }

    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.spend_rate = this.getAttribute('spend_rate')
        this.funds_remaining = this.getAttribute('funds_remaining')
        this.company_name = this.getAttribute('company_name')
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-budget', Budget))

