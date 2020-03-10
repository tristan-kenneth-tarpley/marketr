const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('/static/assets/icons/all.min.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');
        .signature {
            font-style: italic;
        }
        .dark_blue {
            color: var(--darker-blue);
            font-weight: bold;
        }
        .shadow_insights {
            max-height: 500px;
            overflow-y: auto;
            overflow-x: hidden;
        }
    
        .shadow_insights p {
            white-space: pre-wrap;
        }
        ._insight_row {
            padding: 4%;
            border-top: 1px solid rgba(0,0,0,.1);
        }
        .clipped_txt {
            white-space: normal !important;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            margin: 0;
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
        /*html*/
        return `
        ${this.css}
        <div class="shadow_insights">
                ${this.state.data.map((ins, index)=>{
                    let title = `From ${ins.admin} on ${ins.time}`
                    let uid = `${ins.time}_${index}`
                    let body = urlify(ins.body)

                    /*html*/
                    return `
                    ${modal(title, body, uid)}
                    <div class="rec-container">
                        <div class="rec">
                            <div class="row">
                                <div class="col">
                                    <p style="text-decoration:underline;" class="squashed rec-title small_txt">${title}</p>
                                    <p class="small_txt clipped_txt">${body}</p>
                                    <div style="padding: 0;" data-uid="${uid}" id="six" class="small_txt button">read more <i class="fas fa-caret-right"></i></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <hr>
                    `
                }).join("")}

                ${this.state.data.length == 0
                    ? `
                    <p>Every week your Market(r) guide will send you detailed analysis on your portfolio performance. These insights are archived here!</p>
                    <p>Head over to the chat tab if you have any questions and you'll get a response within an hour!</p>`
                    :  `    
                    <p class="signature x_small_txt">Are these insights helpful?  Send us a message via Chat to ask any follow-up questions or provide feedback for improvement.</p>
                    <p class="signature x_small_txt">Thanks! ~ Tristan | Founder </p>`
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
        .then(()=>this.shadow.appendChild(modal_handlers(el)))
    }

    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-insights', Insights))

