import {tabs, shadow_events, dots_loader} from '/static/src/components/UI_elements.js'

const styles = () => {
  /*html*/
  return `
  <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('/static/assets/icons/all.min.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');

        .btn {
            font-size: .7em;
            margin: 0;
            border-left: 3px solid transparent !important;
            border-right: 3px solid transparent !important;
            border-top: 3px solid transparent !important; 
        }
        #options_container p {
            margin: 0;
        }
        #options_container ul {
            z-index: 1 !important;
            position: relative;
            top: 0;
            left: -30;
            background-color: white;
            list-style: none;
            width: 200%;
            box-shadow: var(--card-box-shadow);
            padding: 10%;
            border-radius: 6px;
            border: 1px solid rgba(0,0,0,.2);
            max-height: 25em;
            overflow-y: auto;
        }
        #options_container ul li {
            margin: 4% 0;
            padding: 2% 4%;
            border-radius: 6px;
            transition-duration: .3s;
            border: 1px solid transparent;
            cursor: pointer;
        }
        #options_container ul li:hover {
            background-color: var(--panel-bg);
            border: 1px solid rgba(0,0,0,.1);
        }
  </style>
  `.trim()
}

export default class Filter extends HTMLElement {
    static get observedAttributes() {
        return ['customer_id'];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.state = {
            data: null,
            toggled: false
        }


        this.css = styles()
    }

    view_controller(el){
        let selector = el.querySelector('#widget__selector')
        if (selector.dataset.show == 'false') selector.style.display = 'none'
        else selector.style.display = 'block'

        el.querySelector('#toggle').addEventListener('click', e=>{
            selector.dataset.show = selector.dataset.show == 'false' ? 'true' : 'false'
            this.state.toggled = this.state.toggled ? false : true
            this.render()
        })

        return el
        
    }

    render(){
        this.shadow.innerHTML = ""

        const init = async () => {
            let closed = `<i class="far fa-caret-square-right"></i>`,
            open = `<i class="far fa-caret-square-down"></i>`,
            active_icon = this.state.toggled ? open : closed

            const el = document.createElement('div')
            /*html*/
            el.innerHTML = `
                ${this.css}
                <div id="options_container">
                    <button id="toggle" class="btn btn-outline btn-outline-secondary">${this.active_sub_view} ${active_icon}</button>

                    <ul id="widget__selector" data-show="${this.state.toggled ? 'true' : 'false'}">
                        ${
                            this.sub_list.map(li => {
                                return `<li><p>${li.key}</p></li>`
                            }).join("")
                        }
                    </ul>
                </div>
            `
            return el
        }

        init()
            .then( el=> this.view_controller(el) )
            .then( el=> this.shadow.appendChild(el) )


        
    }

    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.sub_list = JSON.parse(this.getAttribute('sub_list'))
        this.active_sub_view = this.getAttribute('active_sub_view')
        this.active_view = this.getAttribute('active_view')

        console.log(this.active_sub_view)

        console.log(this.sub_list)
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('filter-by', Filter))
