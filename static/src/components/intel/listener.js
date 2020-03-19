import {tabs, shadow_events, dots_loader} from '/static/src/components/UI_elements.js'
import {iterate_text, modal, modal_trigger, modal_handlers, currency,currency_rounded,number,number_rounded,number_no_commas,percent,remove_commas,remove_commas_2} from '/static/src/convenience/helpers.js'
const styles = () => {
    /*html*/
    return `
    <style>
    @import url('/static/assets/css/app.css');
    </style>
    `.trim()
  }
  
  export default class Listener extends HTMLElement {
    static get observedAttributes() {
        return ['keywords', 'customer_id'];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.state = {
            data: null
        }
  
        this.css = styles()
    }

    core(){
        /*html*/
        return `
        <h5 class="small_txt">What people are saying:</h5>
        <div class="row">
            <div class="col">
                <table class="table" id="listening">
                    <thead>
                        <th>Title</th>
                        <th>Link</th>
                    </thead>
                    <tbody>
                        ${this.state.data.map(res=>{
                            /*html*/
                            return `
                            <tr>
                                <td><p>${res.title}</p></td>
                                <td><a target="__blank" href="${res.url}">View</a></td>
                            </tr>
                            `
                        }).join("")}
                    </tbody>
                </table>
            </div>
        </div>
        `
    }

    null(){
        return `
            <div id="stall" style="center_it"><span><span></div>
            ${dots_loader()}
            <div id="table_container" style="display:none;">
                <table id="listening"></table>
            </div>
        `
    }
  
    render(init=true){
        const first = async () => {
            this.shadow.innerHTML = ""
            const el = document.createElement('div')
            el.innerHTML = `
              ${this.css}
              ${
                  this.state.data
                  ? this.core()
                  : this.null()
              }
          `
            return el
        }
        first().then(el=>{
            new DataTable(el.querySelector("#listening"));
            return el
        })
        .then(el=>{
            this.shadow.appendChild(el)
        })
        .then(()=>{
            let it;
            if(this.state.data == null){
                const lines = [
                    '...Analyzing top keywords of your competitors...',
                    "...Scanning the web for related conversations...",
                    "...o_O  these look interesting...",
                    "...Check them out and get engaged!"
                ]
                it = iterate_text(lines, this.shadow.querySelector('#stall'))
            } else {
                clearInterval(it)
            }
   
        })
    }
  
    connectedCallback() {
        this.keywords = this.getAttribute('keywords')
        this.customer_id = this.getAttribute('customer_id')

        const body = JSON.stringify({
            keywords: JSON.parse(this.keywords),
            customer_id: this.customer_id
        })


        this.render()
        fetch('/api/intel/listener', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body
        })
            .then(res=>res.json())
            .then(res=>{
                this.state.data = res
                this.render(true)
            })
            .catch(e=>{
                console.log(e)
            })

    }
  }
  
  document.addEventListener( 'DOMContentLoaded', customElements.define('market-listener', Listener))