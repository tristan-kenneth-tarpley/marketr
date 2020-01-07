const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');
        .rec-container {
            padding: 1%;
        }
        .rec {
            border-left: 4px solid gray;
            margin-bottom: 2%;
            padding: 5% 2% 0 5%;
        }
        .dismiss {
            position: relative;
            right: 15%;
            top: 10%;
        }
        .rec-title {
            line-height: .5em;
        }
        .rec-apply {
            font-size: 75%;
            /*float: right;*/
        }
        .read-more {
            margin: auto;
        }
    </style>
    `.trim()
}

export default class Rec_shell extends HTMLElement {
    static get observedAttributes() {
        return ['rec-id', 'customer-id', 'title', 'body', 'index'];
    }

    constructor(){
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.rec_id = this.getAttribute('rec-id')
        this.customer_id = this.getAttribute('customer-id')
        this.title = this.getAttribute('title')
        this.body = this.getAttribute('body')
        this.index = this.getAttribute('index')
        console.log(this.index)
        this.state = {
            data: null
        }


        this.css = styles()

    }

    render(){
        this.shadow.innerHTML = ''
        const colors = ['#62cde0','#ca7d66','#01d4b4','#ff9c00', '#62cde0','#ca7d66','#01d4b4','#ff9c00', '#62cde0','#ca7d66','#01d4b4','#ff9c00', '#62cde0','#ca7d66','#01d4b4','#ff9c00']
        console.log(this.title)
        const shell = `
        ${this.css}

        <!-- Modal -->
        <div class="modal fade" id="${this.index}_modal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">${this.title}</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    ${this.body}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                </div>
                </div>
            </div>
        </div>

        <div class="rec-container">
            <div style="border-left: 4px solid ${colors[this.index]}" class="rec">
                <h5 class="rec-title">${this.title}</h5>
                <span class="x dismiss">X</span> 
                <div class="row">
                    <div class="col-6">
                        <button
                            class="read-more btn btn-neutral"
                            data-toggle="modal"
                            data-target="#${this.index}_modal">
                        Read more</button>
                    </div>
                    <div class="col-6"><button class="rec-apply btn btn-secondary">Apply</button></div>
                </div>
            </div>
        </div>
        `.trim()
   
        let el = document.createElement('div')
        el.innerHTML = shell
        this.shadow.appendChild(el)
    }

    connectedCallback(){
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('recommendation-shell', Rec_shell))