import {tabs, shadow_events, dots_loader} from '/static/src/components/UI_elements.js'
const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');
        @import url("https://cdn.jsdelivr.net/npm/vanilla-datatables@v1.6.16/dist/vanilla-dataTables.min.css");
  
    </style>
    `.trim()
  }
  
  export default class Listener extends HTMLElement {
    static get observedAttributes() {
        return ['keywords'];
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
                                <td>${res.title}</td>
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
            ${dots_loader()}
            <table class="hidden" id="listening"></table>
        `
    }
  
    render(init=true){
        const first = async () => {
            this.shadow.innerHTML = ""
            const el = document.createElement('div')
            el.innerHTML = `
              ${this.css}
              <h5 class="small_txt">What people are saying:</h5>
              ${
                  this.state.data
                  ? this.core()
                  : this.null()
              }
          `
            return el
        }
        first().then(el=>{
            console.log(el.querySelector("#listening"))
            new DataTable(el.querySelector("#listening"));
            return el
        })
        .then(el=>{
            this.shadow.appendChild(el)
        })
    }
  
    connectedCallback() {
        this.keywords = JSON.parse(this.getAttribute('keywords'))
        const body = JSON.stringify({ keywords: this.keywords })
        
        this.state.data == null
        ?  fetch('/api/intel/listener', {
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
        : this.render(true)
        this.render()
    }
  }
  
  document.addEventListener( 'DOMContentLoaded', customElements.define('market-listener', Listener))