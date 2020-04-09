import {tabs, shadow_events, dots_loader} from '/static/src/components/UI_elements.js'
import {remove_duplicates} from '/static/src/convenience/helpers.js'
import {marketr_score} from '/static/src/components/portfolio/portfolio_performance.js'

const styles = () => {
  /*html*/
  return `
  <style>
        @import url('/static/assets/css/dist/styles.min.css');
        .widget__active-row {
            color: var(--primary) !important;
        }
        .widget__align-vertical {
            display: inline-flex;
            flex-direction: column;
            flex-wrap: wrap;
            height: 100%;
            justify-content: center;
            align-self: center;
            justify-content: center;
        }
        .p__cancel_margin p {
            margin-bottom: 0;
        }
        .widget__value {
            display: flex;
        }
        #toggle {
            width: 100%;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
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
        .filter-row {
            margin-bottom: 4%;
            display: flex;
            align-items: center;
            padding: 1% 5%;
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
            toggled: false,
            rows: []
        }


        this.css = styles()
    }

    select(key){
        this.active_sub_view = key
        this.setAttribute('active_sub_view', key)
        this.state.toggled = false
        this.render()
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

        el.querySelectorAll("#widget__selector li").forEach(li => {
            li.addEventListener('click', e => this.select(e.currentTarget.dataset.key) )
        }); 

        return el
        
    }

    row(li){
        const label_table = {
            1: {
                primary: 'Campaign'
            },
            2: {
                primary: 'Ad group',
                secondary: {
                    key: 'campaign_name',
                    title: 'Campaign'
                }
            },
            3: {
                primary: 'Ad id',
                secondary: {
                    key: 'adset_name',
                    title: 'Ad group'
                },
                tertiary: {
                    key: 'campaign_name',
                    title: 'Campaign'
                }
            }
        }
        /*html*/
        return (
            `<li data-key="${li.key}">
                <div class="row row_cancel">
                    <div class="p__cancel_margin col-lg-8 col-md-8 col-sm-8 col-8">
                        <p class="${li.key == this.active_sub_view ? 'widget__active-row' : ''}">
                            <strong>${label_table[this.active_view].primary}</strong>: 
                            ${li.key}
                        </p>
                        ${this.active_view >= 2
                            /*html*/
                            ? `
                            <p class="x_small_txt">
                                <strong>${label_table[this.active_view].secondary.title}</strong>: 
                                ${li[label_table[this.active_view].secondary.key]}
                            </p>`
                            : ``
                        }
                        ${this.active_view == 3
                            /*html*/
                            ? `
                            <p class="x_small_txt">
                                <strong>${label_table[this.active_view].tertiary.title}</strong>: 
                                ${li[label_table[this.active_view].tertiary.key]}
                            </p>`
                            : ``
                        }
                    </div>
                    <div style="text-align:right;" class="widget__align-vertical col-lg-4 col-md-4 col-sm-4 col-4">
                        ${marketr_score(li.marketr_index)}
                    </div>
                </div>
                
            </li>`
        )
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
                                return this.row(li)
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
        this.sub_list = remove_duplicates(JSON.parse(this.getAttribute('sub_list')), 'key')
        this.active_sub_view = this.getAttribute('active_sub_view')
        this.active_view = parseInt(this.getAttribute('active_view'))

        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('filter-by', Filter))
