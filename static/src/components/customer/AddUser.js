import {tabs, shadow_events, dots_loader} from '/static/src/components/UI_elements.js'
import {modal, modal_trigger, modal_handlers, validateEmail} from '/static/src/convenience/helpers.js'

const styles = () => {
  /*html*/
  return `
  <style>
    @import url('/static/assets/css/dist/styles.min.css');
    #six p {
        font-weight: 400;
        text-decoration: none;
        color: var(--secondary) !important;
    }
    #user_list p {
        margin: 0;
    }
    #user_list ul {
        z-index: 1 !important;
        position: relative;
        top: 0;
        left: -30;
        background-color: white;
        list-style: none;
        width: 100%;
        padding: 2%;
        border-radius: 6px;
    }
    #user_list ul li {
        margin: 1% 0;
        padding: 2% 4%;
        border-radius: 6px;
        transition-duration: .3s;
        border: 1px solid transparent;
        cursor: pointer;
    }
    #user_list ul li:hover {
        background-color: var(--panel-bg);
        border: 1px solid rgba(0,0,0,.1);
    }
  </style>
  `.trim()
}

export default class AddUser extends HTMLElement {
    static get observedAttributes() {
        return ['customer_id'];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.state = {
            data: null,
            all_uses: null
        }

        this.css = styles()
    }

    error(type){
        switch(type) {
            case 'email':
                alert('Invalid email. Please try again.')
                break
            case 'empty_fields':
                alert('Please fill out all fields')
                break
        }
    }

    post(data){
        alert(`${data.get('first_name')} ${data.get('last_name')} successfully added!`)
        fetch('/users/add_secondary', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({
                first_name: data.get('first_name'),
                last_name: data.get('last_name'),
                email: data.get('email'),
                password: data.get('password')
            })
        })
    }

    remove_user(email){
        alert(`${email} removed`)
        fetch('/users/remove_secondary', {
            method: 'POST',
            headers : new Headers({
                "content-type": "application/json"
            }),
            body:  JSON.stringify({email})
        })
        this.render()
    }

    view_controller(el){
        const form = el.querySelector('#add_user')

        el.querySelectorAll('.remove_user').forEach(usr=>{
            usr.addEventListener('click', e=>{
                this.remove_user(e.currentTarget.dataset.email)
            })
        })

        form.onsubmit = ev => {
            ev.preventDefault()
            let data = new FormData(form)
            if (data.get('first_name') && data.get('last_name')) {
                if (validateEmail(data.get('email'))) this.post(data)
                else {
                    this.error('email')
                    return false
                }
            }
            else {
                this.error('empty_fields')
                return false
            }

            form.reset()

        }

        return el
    }

    form(){
        /*html*/
        return (`
            <form method="POST" id="add_user" name="add_user">
                <div class="row">
                    <div class="col-lg-6 col-md-6 col-sm-6 col-6">
                        <div class="input-group">
                            <label>First name</label>
                            <input class="form-control" type="text" name="first_name">
                            <span class="form-control-border"></span>
                        </div>
                    </div>
                    <div class="col-lg-6 col-md-6 col-sm-6 col-6">
                        <div class="input-group">
                            <label>Last name</label>
                            <input class="form-control" type="text" name="last_name">
                            <span class="form-control-border"></span>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <div class="input-group">
                            <label>email</label>
                            <input class="form-control" type="text" name="email">
                            <span class="form-control-border"></span>
                        </div>
                    </div>
                </div>
                
                <div class="input-group">
                    <input type="submit" class="btn btn-secondary" value="add user">
                </div>
            </form>
            <div id="user_list">
                <ul id="">
                    ${this.state.all_users.map((usr, index)=>{
                        /*html*/
                        return `<li>
                                    <div class="row row_cancel">
                                        <div class="col-lg-6 col-md-6 col-sm-6 col-6">
                                            <p>${usr.first_name} ${usr.last_name}</p>
                                            <p class="x_small_txt">${usr.email}</p>
                                        </div>
                                         <div class="col-lg-6 col-md-6 col-sm-6 col-6"> 
                                            ${index > 0 && usr.email != this.email
                                                ?`             
                                                <button class="x_small_txt remove_user btn btn-danger" data-email="${usr.email}">
                                                    remove user
                                                </button>`
                                                : ''
                                            }      
                                        </div>
                                    </div>
                                </li>`
                    }).join("")}
                </ul>
            </div>
        `)
    }

    render(init=true){
        
        fetch('/api/get_all_account_users', {
            method: 'GET',
            headers : new Headers({
                "content-type": "application/json"
            })
        })
        .then(res=>res.json())
        .then(res=> this.state.all_users = res)
        .then(()=>{
            this.shadow.innerHTML = ""
            const el = document.createElement('div')
            el.innerHTML = `
                ${this.css}
                ${modal_trigger('add_user', 'Add user', false)}
                ${modal('Add a user to your account', this.form(), 'add_user')}
            `

            return el
        })
        .then(el=>{
            this.shadow.appendChild(modal_handlers(this.view_controller(el)))
        })
    }

    connectedCallback() {
        this.email = this.getAttribute('email')
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('add-user', AddUser))
