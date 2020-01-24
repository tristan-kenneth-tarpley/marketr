const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');

        .dark_blue {
            color: var(--darker-blue);
            font-weight: bold;
        }
 
    </style>
    `.trim()
}

export default class Insights extends HTMLElement {
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

    shell(){
        return `
            ${this.state.data.map(ins=>{
                /*html*/
                return `
                ${this.css}
                <p class='dark_blue small_txt'>${ins.time}</p>
                <p>${ins.body}</p>
                `
            }).join("")}

            <div class='separator'></p>
            <p class="x_small_txt">Are these insights helpful?  Send us a message via Chat to ask any follow-up questions or provide feedback for improvement.</p>
            <p>Thanks! ~ Tristan | Founder </p>
        `.trim()
    }

    render(init=true){
        this.shadow.innerHTML = ""
        const el = document.createElement('div')
        fetch('/api/insights', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                customer_id: this.customer_id
            })
        })
        .then(res=>res.json())
        .then(res=>this.state.data = res)
        .then(()=>{
            el.innerHTML = this.shell()
        })
        .then(()=>this.shadow.appendChild(el))
    }

    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-insights', Insights))

