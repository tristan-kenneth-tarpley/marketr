import Rec_shell from '/static/src/components/admin/rec_shell.js'
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
            position: absolute;
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
        .new_rec {
            width: 100%;
        }
        #rec_body {
            padding: 4%;
        }
        #past {
            max-height: 500px;
            overflow-y: scroll;
        }
    </style>
    `.trim()
}

export default class AdminRecs extends HTMLElement {
    static get observedAttributes() {
        return ['customer-id', 'admin-id'];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.customer_id = this.getAttribute('customer-id')
        this.admin_id = this.getAttribute('admin-id')
        this.state = {
            data: null
        }
        this.has_price_tag = false

        this.observer = new MutationObserver(mutations=>{
            mutations.forEach(mutation => {
                if (mutation.type == "attributes") {
                    if (mutation.attributeName == 'deleted') this.delete(mutation.target)
                }
            });
        });

        this.css = styles()
    }

    form(){
        /* html */
        const el = `
        <form method="POST" id="new_rec">
            <h5 for="rec_title widget__title">Recommendation title</h5>
            <input name="rec_title" type="text" class="form-control" placeholder="Recommendation title">

            <p style="margin:1em 0 0;" for="price_tag_t_f">
                Is there a price tag?
                <input type="checkbox" name="price_tag_t_f">    
            </p>

            <div class="input-group">
                <div class="input-group-prepend">
                    <span class="input-group-text">$</span>
                </div>
                <input disabled name="price_total" type="number" value="0" class="form-control" placeholder="$0">
            </div>
            
            <h5 for="rec_body widget__title">Recommendation</h5>
            <textarea type="text" id="rec_body" name="rec_body" class="form-control" placeholder="Recommendation body"></textarea>
            
            <input type="submit" class="btn btn-primary">
        </form>
        `.trim()
        return el
    }

    remove_from_view(target){
        const refresh = async () => this.state.data = this.state.data.filter(rec => rec.rec_id != target.getAttribute('rec_id') );
        refresh()
            .then(this.render(true))
    }

    delete(target){
        this.remove_from_view(target)
        fetch('/api/recommendation/delete', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                admin_id: this.admin_id,
                customer_id: this.customer_id,
                rec_id: target.getAttribute('rec_id')
            })
        })
    }

    new_rec(form){
        const title = form.get('rec_title')
        const body = form.get('rec_body')
        const price = this.price_tag ? form.get('price_total') : null
        if (!title || !body) {
            this.has_price_tag = false
            this.shadow.querySelector('input[name="price_tag_t_f"]').checked = false
            this.shadow.querySelector('input[name="price_total"]').disabled = true
            alert("All fields must be filled out")
            return false
        }

        fetch('/api/recommendations', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                admin_id: this.admin_id,
                customer_id: this.customer_id,
                title,
                body,
                outstanding: true,
                price 
            })
        })
            .then((res) => res.json())
            .then(res=> this.state.data = res )
            .then(this.render())
    }

    handlers(el){
        el.querySelector('input[name="price_tag_t_f"]').addEventListener('change', e=>{
            let total = el.querySelector('input[name="price_total"]')
            let disabled = total.disabled == false ? true : false
            total.disabled = disabled
            this.has_price_tag = disabled ? false : true
        })

        el.querySelector('input[name="price_total"]').addEventListener('keyup', e=>{
            this.price_tag = e.currentTarget.value
        })

        const form = el.querySelector('#new_rec')
        form.onsubmit = ev => {
            ev.preventDefault()
            this.new_rec(new FormData(form))
            form.reset()
        }
        return el
    }

    recommendation(rec){
        const el = new Rec_shell

        el.setAttribute('price', rec.price)
        el.setAttribute('rec_id', rec.rec_id)
        el.setAttribute('admin-assigned', this.admin_id)
        el.setAttribute('customer_id', this.customer_id)
        el.setAttribute('title', rec.title)
        el.setAttribute('body', rec.body)
        el.setAttribute('accepted', rec.accepted)
        el.setAttribute('dismissed', rec.dismissed)

        this.observer.observe(el, {
            attributes: true
        });
        
        return el
    }

    render(state = false){

        this.shadow.innerHTML = ""

        const append = (res) => {
            let el = document.createElement('div')
            /*html */
            el.innerHTML = `
                ${this.css}
                <h5 class="widget__title">Recommendations</h5>
                <div class="row">
                    <div class="col-lg-6 col-sm-12">
                        ${this.form()}
                    </div>
                    <div id="past" class="col-lg-6 col-12">
                        
                    </div>
                </div>
            `
            const past = el.querySelector("#past")
            if (this.state.data.length == 0) {
                past.innerHTML += `<p>This user doesn't currently have any recommendations. Make sure to assign some!</p>`
            } else for (let i in res) past.appendChild(this.recommendation(res[i]))
            
            return this.handlers(el)
        }

        if (state == false) {
            fetch('/api/recommendations', {
                method: 'POST',
                headers : new Headers({
                    "content-type": "application/json"
                }),
                body:  JSON.stringify({
                    customer_id: this.customer_id,
                    admin_id: this.admin_id
                })
            })
                .then(res=>res.json())
                .then(res=>this.state.data = res)
                .then(res=> append(res))
                .then(el => this.shadow.appendChild(el))
        } else {
            const el = append(this.state.data)
            this.shadow.appendChild(el)
        }
        
    }

    connectedCallback(){
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('admin-recommendations', AdminRecs))