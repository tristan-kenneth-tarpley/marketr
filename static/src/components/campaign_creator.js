import {google} from '/static/src/components/UI_elements.js'
const styles = () => {
    return html(
      'style',
      null,
      `
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css')
        .accordion-toggle {
            display: block;
          }
          
        .accordion-content {
            display: none;
        }
        
        .accordion-content.acc-active {
            display: block;
        }
        textarea.form-control {
            padding: 3%;
        }
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
                <p>Give us a few (2-5) keyword or keyword phrases separated by a comma to get started.</p>
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
                        <a style="color:#62cde0;" href="#content-${keywords[i].group.replace(/ /g, '_')}" class="accordion-toggle">${keywords[i].group}</a>
                        <button id="${keywords[i].group.replace(/ /g, '_')}" class="btn btn-outline btn-outline-primary remove">remove</button>
                    </p>
                    <div class="accordion-content" id="content-${keywords[i].group.replace(/ /g, '_')}">
                        <table id="${keywords[i].group.replace(/ /g, '_')}-table" style="text-align:center;" class="table table-striped">
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
                                <tr id="${keywords[i].keywords[x].keyword.replace(/ /g, '_')}" style="text-align:center;">
                                    <td><input type="checkbox" data-ad_group="${keywords[i].group.replace(/ /g, '_')}" class="include form-control" value="${keywords[i].keywords[x].keyword.replace(/ /g, '_')}"></td>
                                    <td>${keywords[i].keywords[x].keyword}</td>
                                    <td>${keywords[i].keywords[x].advertisers}</td>
                                    <td>${keywords[i].keywords[x].costperday}</td>       
                                    <td>${keywords[i].keywords[x].broad_cpc}</td>
                                    <td><input type="checkbox" class="broad form-control"></td>
                                    <td>${keywords[i].keywords[x].phrase_cpc}</td>
                                    <td><input type="checkbox" class="phrase form-control"></td>
                                    <td>${keywords[i].keywords[x].exact_cpc}</td>
                                    <td><input type="checkbox" class="exact form-control"></td>
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
            <button id="format" class="btn btn-primary format">Continue</button>
        </div>
    </div>
    `.trim()
}

const formatting_template = recs => {
    let printed = []
    const _print = (group, _printed=printed) => {
        let returned = !_printed.includes(group) ? `ad group: ${group}` : ``
        _printed.push(group)
        return returned
    }
    /*html */
    return `
    <div class="row">
        <div class="col-lg-6 col-12">
    ${Object.keys(recs).map(rec=>{
        /*html*/
        let returned = `
            <p><strong>${_print(recs[rec].ad_group)}</strong></p>
            
                <div class="inset">
                ${recs[rec].meta.match_types.map(met=>{ 
                    let _returned = ""
                    switch(met){
                        case 'broad':
                            _returned += "<p>+" + recs[rec].meta.keyword.replace(/ /g, ' +') + "</p>"
                        break
                        case 'exact':
                            _returned += "<p>[" + recs[rec].meta.keyword + ']</p>'
                        break
                        case 'phrase':
                            _returned += '<p>"' + recs[rec].meta.keyword + '"</p>'
                        break
                        default:
                            _returned += '<p>' + recs[rec].meta.keyword + '</p>'
                        break
                    }
                    return _returned
                }).join('')}
                </div>

            `
        return returned
    }).join('')}
        </div>
        <div class="col-lg-6 col-12">
            <p><strong>Ad possibilities</strong></p>
    ${Object.keys(recs).map(rec=>{
        /*html*/
        return `
            <div class="inset">
                ${recs[rec].meta.ads.map(ad=>{
                    return `
                    <div class="google_ad_preview_container">
                        <h5 class="small_txt">${ad.headline}</h5>
                        <p class="small_txt website"><span>ad</span> www.example.com</p>
                        <p class="small_txt">${ad.body}</p>
                    </div>
                    `.trim()
                }).join('')}
            </div>`
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
            recs: [],
            accepted_recs: []
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
                const new_state = this.state.recs.filter(rec => rec.group != id.replace(/_/g, ' '));
                this.state.recs = [...new_state]
                this.edit_res(this.state.recs)
            })
        })
        el.querySelectorAll('.include').forEach(el_=>{
            el_.addEventListener('change', e=>{
                const keyword = e.currentTarget.value.replace(/_/g, ' ')
                const table = el.querySelector(`#${e.currentTarget.dataset.ad_group}-table`)
                const tr = table.querySelector(`#${e.currentTarget.value}`)
                const phrase = tr.querySelector(`.phrase`)
                const broad = tr.querySelector(`.broad`)
                const exact = tr.querySelector(`.exact`)
                if (e.target.checked) {
                    const ad_group = e.currentTarget.dataset.ad_group.replace(/_/g, ' ')
                    const packet = {
                        ad_group,
                        meta: {
                            keyword, match_types: [],
                            ads: (this.state.recs.filter(rec=>rec.group == ad_group))[0].ads
                        }
                    }
                    console.log(packet)
                    let mt = packet.meta.match_types

                    const add_mt = (e, type, iterable=mt) => {
                        if(e.target.checked){
                            if (!iterable.includes(type)){
                                iterable.push(type)
                            }
                        } else {
                            for(let i = 0; i < iterable.length; i++){ 
                                if (iterable[i] === type) {
                                    iterable.splice(i, 1); 
                                }
                            }
                        }
                    }

                    phrase.addEventListener('click', e=>add_mt(e, 'phrase'))
                    broad.addEventListener('click', e=>add_mt(e, 'broad'))
                    exact.addEventListener('click', e=>add_mt(e, 'exact'))

                    this.state.accepted_recs.push(packet)
                } else {
                    const removed = this.state.accepted_recs.filter(_keyword => _keyword.keyword != keyword)
                    this.state.accepted_recs = [...removed]
                }
            })
        })
        el.querySelector('#format').addEventListener('click', e=>{
            this.formatting()
        })


        this.shadow.appendChild(this.css);
        this.shadow.appendChild(el)
    }

    formatting(){
        this.shadow.innerHTML = ""
        const template = formatting_template(this.state.accepted_recs)
        const el = document.createElement('div')
        el.innerHTML = template
        this.shadow.appendChild(this.css);
        this.shadow.appendChild(el)  
    }

    inspect(index){
        const dataset = this.filter_dataset(index)
        const el = this.platform_chart(dataset)
        this.mix_container.style.display = 'none'
        document.querySelector('.inspect_container').style.display = 'block'
        document.querySelector('.inspect_container').innerHTML = el
        document.querySelector('#nav_up').addEventListener('click', e=>this.home(this.metric))

        const others = document.querySelectorAll('.sum_list')

        others.forEach(el => {
            el.addEventListener('click', e=>{
                const platform = e.currentTarget.textContent
                let index = this.campaign_data.findIndex(ind => ind.platform == platform)
                this.inspect(index)
            })
        });
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