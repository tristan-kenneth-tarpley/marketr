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
        .shadow_insights {
            max-height: 500px;
            overflow-y: scroll;
        }
    
        .shadow_insights p {
            white-space: pre-wrap;
        }
        ._insight_row {
            padding: 4%;
            border-top: 1px solid rgba(0,0,0,.1);
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
        <div class="shadow_insights">
                ${this.state.data.map((ins, index)=>{
  

                    /*html*/
                    return `
                    ${this.css}
                    <div class="_insight_row">
                        <h1 class="widget__title">${index + 1}) From ${ins.admin}</h1>
                        <h3 class='widget__title small dark_blue small_txt'>Written on ${ins.time}</h3>
                        <p class="truncate">${ins.body}</p>
                    </div>
                    `
                }).join("")}
                <hr>
                ${this.state.data.length == 0
                    ? `
                    <p>Every week your Market(r) guide will send you detailed analysis on your portfolio performance. These insights are archived here!</p>
                    <p>Head over to the chat tab if you have any questions and you'll get a response within an hour!</p>`
                    :  `    
                    <p class="x_small_txt">Are these insights helpful?  Send us a message via Chat to ask any follow-up questions or provide feedback for improvement.</p>
                    <p>Thanks! ~ Tristan | Founder </p>`
                }
        </div>
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

