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

        this.css = styles()
    }

    form(){
        const el = `
        <form method="POST" id="new_rec">
            <label for="rec_title">Recommendation title</label>
            <input name="rec_title" type="text" class="form-control" placeholder="Recommendation title">
            
            <label for="rec_body">Recommendation</label>
            <textarea type="text" name="rec_body" class="form-control" placeholder="Recommendation body"></textarea>
            
            <input type="submit" class="btn btn-primary">
        </form>
        `.trim()
        return el
    }

    new_insight(form){
        const title = form.get('rec_title')
        const body = form.get('rec_body')
        if (!title) return false
        if (!body) return false

        fetch('/api/recommendations', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                admin_id: this.admin_id,
                customer_id: this.customer_id,
                title,
                body
            })
        })
            .then((res) => res.json())
            .then(res=>console.log(res))
    }

    handlers(el){
        const form = el.querySelector('#new_rec')
        // form.onsubmit = this.new_insight(
        //     el.querySelector('input[name=rec_title]').value,
        //     el.querySelector('input[name=rec_body]').value
        // )
        form.onsubmit = ev =>{
            ev.preventDefault()
            this.new_insight(new FormData(form))
        }
        return el
    }

    render(){
        this.shadow.innerHTML = ""
        const el = document.createElement('div')
        /*html */
        el.innerHTML = `
            ${this.css}
            <h5>Recommendations</h5>
            <div class="row">
                <div class="col-lg-6 col-sm-12">
                    ${this.form()}
                </div>
                <div class="col-lg-6 col-12">
                    <p>The past recs will go here</p>
                </div>
            </div>
            
        `

        this.shadow.appendChild(this.handlers(el));
    }

    connectedCallback(){
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('admin-recommendations', AdminRecs))