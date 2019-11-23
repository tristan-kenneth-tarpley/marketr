const styles = () => {
    return html(
      'style',
      null,
      `
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
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
                    <option>Company brand</option>
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
                <select class="form-control">
                    <option>awareness</option>
                    <option>evaluation</option>
                    <option>conversion</option>
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

    const new_el = await get_personas()
    async function get_products(id=customer_id){
        const products = await fetch(`/api/products?customer_id=${id}`)
        const products_json = await products.json()
        return products_json
    }

    let personas = await get_personas()
    let products = await get_products()

    for (let i in personas){
        let child = `<option>${personas[i].persona_name}</option>`
        el.querySelector('#audiences').insertAdjacentHTML('beforeend', child)
    }
    for (let i in products){
        let child = `<option>${products[i].product_name}</option>`
        el.querySelector('#products').insertAdjacentHTML('beforeend', child)
    }

    return el
}


const prep_second = keywords => {
    console.log(keywords)
    return `
        <div class="row">
            <h1>testing</h1>
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
            'keywords': [],
            'audiences': [],
            'products': []
        }

        this.css = styles()
    }

    select_keywords(keywords){
        this.shadow.innerHTML = ""
        const template = prep_second(keywords)
        const el = document.createElement('div')
        el.innerHTML = template

        this.shadow.appendChild(this.css);
        this.shadow.appendChild(el)
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
                this.select_keywords(data)
            })
            .catch((err)=>console.log(err))
    }

    connectedCallback() {

        prep_first(this.customer_id)
            .then(el=>{
                el.querySelector("#get_ad_groups").addEventListener('click', e=>{
                    e.currentTarget.innerHTML = `<i class="fa fa-spinner fa-spin"></i>`
                    const keywords = el.querySelector("#keywords").value.split(", ")
                    this.handle_first(keywords)
                })
                this.shadow.appendChild(this.css);
                this.shadow.appendChild(el);
            })
    }
}
  
window.customElements.define('campaign-creator', CampaignCreator);