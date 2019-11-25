const styles = () => {
    return html(
      'style',
      null,
      `
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        .accordion-toggle {
            display: block;
          }
          
        .accordion-content {
            display: none;
        }
        
        .accordion-content.acc-active {
            display: block;
        }
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css')
      `
    );
}





async function prep_first(customer_id){
        const first = () => {
        /*html */
        return `
        <div class="row">
            <div class="col-lg-6 col-12">
                <p>Is this campaign for the overall brand or a specific product?</p>
            </div>
            <div class="col-lg-6 col-12">
                <select id="products" class="form-control">
                    <option value="brand">Company brand</option>
                </select>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-6 col-12">
                <p>Which persona is it for?</p>
            </div>
            <div class="col-lg-6 col-12">
                <select id="audiences" class="form-control">
                    
                </select>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-6 col-12">
                <p>What part of the customer journey is it for?</p>
            </div>
            <div class="col-lg-6 col-12">
                <select id="stage" class="form-control">
                    <option value="awareness">awareness</option>
                    <option value="evaluation">evaluation</option>
                    <option value="conversion">conversion</option>
                </select>         
            </div>
        </div>
        <div class="row">
            <div class="col-lg-6 col-12">
                <p>Give us a few (2-5) keyword or keyword phrases separated by a commas to get started.</p>
            </div>
            <div class="col-lg-6 col-12">
                <textarea id="keywords" rows="6" class="form-control"></textarea>
            </div>
        </div>
        <div class="center_it" style="margin: 0 auto">
            <button id="get_ad_groups" class="btn btn-primary">Run</button>
        </div>
        
        `.trim()
    }


    async function get_el(){
        const el = document.createElement('div')
        el.innerHTML = first()
        return el
    }

    let el = await get_el()
    
    async function get_personas(id=customer_id){
        const personas = await fetch(`/api/personas?customer_id=${id}`)
        const personas_json = await personas.json()
        return personas_json
    }

    async function get_products(id=customer_id){
        const products = await fetch(`/api/products?customer_id=${id}`)
        const products_json = await products.json()
        return products_json
    }

    let personas = await get_personas()
    let products = await get_products()

    for (let i in personas){
        let child = `<option value="${personas[i].persona_name}">${personas[i].persona_name}</option>`
        el.querySelector('#audiences').insertAdjacentHTML('beforeend', child)
    }
    for (let i in products){
        let child = `<option value="${products[i].product_name}">${products[i].product_name}</option>`
        el.querySelector('#products').insertAdjacentHTML('beforeend', child)
    }

    return el
}


const prep_second = keywords => {
    return `
    <div class="row">
        <div class="col">
            <h6>Ad groups</h6>
            ${Object.keys(keywords).map((i) => {
                let returned;
                keywords[i].ads != undefined ? returned = `
                <div class="ad-group-group">
                <hr>
                    <p>
                        <a style="color:#62cde0;" href="#content-${keywords[i].group.replace(" ", "_")}" class="accordion-toggle">${keywords[i].group}</a>
                        <button id="${keywords[i].group.replace(" ", "_")}" class="btn btn-outline btn-outline-primary remove">remove</button>
                    </p>
                    <div class="accordion-content" id="content-${keywords[i].group.replace(" ", "_")}">
                        <table style="text-align:center;" class="table table-striped">
                            <thead>
                                <th style="font-size:80%;">Include?</th>
                                <th style="font-size:80%;">Keyword</th>
                                <th style="font-size:80%;">Advertisers</th>
                                <th style="font-size:80%;">Cost Per Day</th>
                                <th style="font-size:80%;">Broad CPC</th>
                                <th style="font-size:80%;">Broad Match</th>
                                <th style="font-size:80%;">Phrase CPC</th>
                                <th style="font-size:80%;">Phrase Match</th>
                                <th style="font-size:80%;">Exact CPC</th>
                                <th style="font-size:80%;">Exact Match</th>
                            </thead>
                            <tbody>
                        ${Object.keys(keywords[i].keywords).map((x) => {
                             return `
                                <tr style="text-align:center;">
                                <td><input type="checkbox" class="form-control"></td>
                                <td>${keywords[i].keywords[x].keyword}</td>
                                <td>${keywords[i].keywords[x].advertisers}</td>
                                <td>${keywords[i].keywords[x].costperday}</td>       
                                <td>${keywords[i].keywords[x].broad_cpc}</td>
                                <td><input type="checkbox" class="form-control"></td>
                                <td>${keywords[i].keywords[x].phrase_cpc}</td>
                                <td><input type="checkbox" class="form-control"></td>
                                <td>${keywords[i].keywords[x].exact_cpc}</td>
                                <td><input type="checkbox" class="form-control"></td>
                                </tr>
                             `.trim()
                        }).join('')}
                            </tbody>
                        </table>
                    </div>
                <br>
                </div>` : returned = ''
                return returned
            }).join('')}
        </div>
    </div>
    `.trim()
}




export default class CampaignCreator extends HTMLElement {
    static get observedAttributes() {
        return ['customer-id'];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.customer_id = this.getAttribute('customer-id')
        this.state = {
            brand_or_product: "",
            persona: "",
            stage: "",
            recs: []
        }

        this.css = styles()
    }


    handle_first(keywords){
        fetch('/api/create_campaign', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                keywords: keywords,
                customer_id: this.customer_id
            })
        })
            .then((res) => res.json())
            .then((data) => {
                this.state.recs = [...data]
                this.edit_res(this.state.recs)
            })
            .catch((err)=>console.log(err))
    }


    edit_res(keywords){
        this.shadow.innerHTML = ""
        const template = prep_second(keywords)
        const el = document.createElement('div')
        el.innerHTML = template
        // Listen for click on the document
        el.addEventListener('click', event => {
            if (!event.target.classList.contains('accordion-toggle')) return;
            var content = el.querySelector(event.target.hash);
            if (!content) return;
            event.preventDefault();
            if (content.classList.contains('acc-active')) {
                content.classList.remove('acc-active');
                return;
            }
            var accordions = el.querySelectorAll('.accordion-content.acc-active');
            for (var i = 0; i < accordions.length; i++) {
                accordions[i].classList.remove('acc-active');
            }
            content.classList.toggle('acc-active');
        })
        el.querySelectorAll(".remove").forEach(el=>{
            el.addEventListener('click', e=>{
                const id = e.currentTarget.getAttribute('id')
                const new_state = this.state.recs.filter(rec => rec.group != id.replace("_", " "));
                this.state.recs = [...new_state]
                this.edit_res(this.state.recs)
            })
        })


        this.shadow.appendChild(this.css);
        this.shadow.appendChild(el)
    }

    connectedCallback() {

        prep_first(this.customer_id)
            .then(el=>{
                el.querySelector("#get_ad_groups").addEventListener('click', e=>{
                    e.currentTarget.innerHTML = `<i class="fa fa-spinner fa-spin"></i>`
                    const keywords = el.querySelector("#keywords").value.split(", ")
                    const products = el.querySelector("#products")
                    this.state.brand_or_product = products.options[products.selectedIndex].value
                    const personas = el.querySelector("#audiences")
                    this.state.persona = personas.options[personas.selectedIndex].value
                    const stage = el.querySelector("#stage")
                    this.state.stage = stage.options[stage.selectedIndex].value
                    this.handle_first(keywords)
                })
                this.shadow.appendChild(this.css);
                this.shadow.appendChild(el);
            })
    }
}
  
window.customElements.define('campaign-creator', CampaignCreator);