import {tabs, shadow_events, dots_loader} from '/static/src/components/UI_elements.js'
import {iterate_text, modal, modal_trigger, modal_handlers, currency,currency_rounded,number,number_rounded,number_no_commas,percent,remove_commas,remove_commas_2} from '/static/src/convenience/helpers.js'
const styles = () => {
    /*html*/
    return `
    <style>
    @import url('/static/assets/css/dist/styles.min.css');
    :host {
        display:flex;
        flex-direction: column;
        justify-content:center;
        height: 100%;
    }
    #listening i {
        font-size: 1.3em;
    }
    #listening th {
        font-size: 1em;
    }
    #listening tr {
        height: 2em;
    }
    #listening td {
        height: 3em;
        vertical-align:middle;
    }
    #listening p {
        line-height: .8rem;
        margin: 0 !important;
    }
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
        <h1 class="widget__title">Web listener</h1>
        <p>Our engines took the competitors you gave us, found 20 more companies like them, figured out the common topics, and then found 100 relevant conversations around the web.</p>
        <p>How to use this info?</p>
        <ul class="inset">
            <li>Read what people are saying about your competitors</li>
            <li>Find users at the point that they're looking to buy something in your field</li>
            <li>Chime in when people are asking for recommendations</li>
            <li>Let potential customers cry on your shoulder when your competitor hurts them!</li>
            <li>Not seeing enough relevant posts? Try <a href="/competitors?splash=False">changing your competitors</a>.</li>
        </ul>
        <table class="table table-borderless table-striped" id="listening">
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Date</th>
                    <th>Link</th>
                </tr>
            </thead>
            <tbody>
                ${this.state.data.map(res=>{
                    let d = new Date(res.created_at * 1000).toLocaleDateString("en-US")
                    /*html*/
                    return `
                    <tr>
                        <td><p>${res.title}</p></td>
                        <td><p>${d}</p></td>
                        <td><a target="__blank" href="${res.url}"><i class="fas fa-sign-out-alt"></i></a></td>
                    </tr>
                    `
                }).join("")}
            </tbody>
        </table>


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