import {urlify, iterate_text, modal, modal_trigger, modal_handlers, currency,currency_rounded,number,number_rounded,number_no_commas,percent,remove_commas,remove_commas_2} from '/static/src/convenience/helpers.js'

const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/app.css');
        .rec-container {
            padding: 1%;
        }
        .rec {
            margin-bottom: 2%;
            padding: 5% 2% 0 5%;
        }
        .dismiss {
        }
        .rec-title {
            margin-bottom: 0;
            padding-bottom: 0;
        }
        .rec-apply {
            font-size: 75%;
            /*float: right;*/
        }
        #toolbar {
            width: 100%;
            text-align:left;
        }
        #toolbar span {
            margin-right: 5%;
        }
        .read-more {
            margin: auto;
        }
        html, body {
            min-height: 100%;
            height: 100%;
            background-image: url(http://theartmad.com/wp-content/uploads/Dark-Grey-Texture-Wallpaper-5.jpg);
            background-size: cover;
            background-position: top center;
            font-family: helvetica neue, helvetica, arial, sans-serif;
            font-weight: 200;
            }
            html.modal-active, body.modal-active {
            overflow: hidden;
            }

            #modal-container {
            position: fixed;
            display: table;
            height: 100%;
            width: 100%;
            top: 0;
            left: 0;
            transform: scale(0);
            z-index: 1;
            }
            #modal-container.one {
            transform: scaleY(0.01) scaleX(0);
            animation: unfoldIn 1s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.one .modal-background .modal {
            transform: scale(0);
            animation: zoomIn 0.5s 0.8s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.one.out {
            transform: scale(1);
            animation: unfoldOut 1s 0.3s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.one.out .modal-background .modal {
            animation: zoomOut 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.two {
            transform: scale(1);
            }
            #modal-container.two .modal-background {
            background: rgba(0, 0, 0, 0);
            animation: fadeIn 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.two .modal-background .modal {
            opacity: 0;
            animation: scaleUp 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.two + .content {
            animation: scaleBack 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.two.out {
            animation: quickScaleDown 0s .5s linear forwards;
            }
            #modal-container.two.out .modal-background {
            animation: fadeOut 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.two.out .modal-background .modal {
            animation: scaleDown 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.two.out + .content {
            animation: scaleForward 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.three {
            z-index: 0;
            transform: scale(1);
            }
            #modal-container.three .modal-background {
            background: rgba(0, 0, 0, 0.6);
            }
            #modal-container.three .modal-background .modal {
            animation: moveUp 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.three + .content {
            z-index: 1;
            animation: slideUpLarge 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.three.out .modal-background .modal {
            animation: moveDown 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.three.out + .content {
            animation: slideDownLarge 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.four {
            z-index: 0;
            transform: scale(1);
            }
            #modal-container.four .modal-background {
            background: rgba(0, 0, 0, 0.7);
            }
            #modal-container.four .modal-background .modal {
            animation: blowUpModal 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.four + .content {
            z-index: 1;
            animation: blowUpContent 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.four.out .modal-background .modal {
            animation: blowUpModalTwo 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.four.out + .content {
            animation: blowUpContentTwo 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.five {
            transform: scale(1);
            }
            #modal-container.five .modal-background {
            background: rgba(0, 0, 0, 0);
            animation: fadeIn 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.five .modal-background .modal {
            transform: translateX(-1500px);
            animation: roadRunnerIn 0.3s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.five.out {
            animation: quickScaleDown 0s .5s linear forwards;
            }
            #modal-container.five.out .modal-background {
            animation: fadeOut 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.five.out .modal-background .modal {
            animation: roadRunnerOut 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.six {
            transform: scale(1);
            }
            #modal-container.six .modal-background {
            background: rgba(0, 0, 0, 0);
            animation: fadeIn 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.six .modal-background .modal {
            background-color: transparent;
            animation: modalFadeIn 0.5s 0.8s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.six .modal-background .modal h2, #modal-container.six .modal-background .modal p {
            opacity: 0;
            position: relative;
            animation: modalContentFadeIn 0.5s 1s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.six .modal-background .modal .modal-svg rect {
            animation: sketchIn 0.5s 0.3s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.six.out {
            animation: quickScaleDown 0s .5s linear forwards;
            }
            #modal-container.six.out .modal-background {
            animation: fadeOut 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.six.out .modal-background .modal {
            animation: modalFadeOut 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.six.out .modal-background .modal h2, #modal-container.six.out .modal-background .modal p {
            animation: modalContentFadeOut 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.six.out .modal-background .modal .modal-svg rect {
            animation: sketchOut 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.seven {
            transform: scale(1);
            }
            #modal-container.seven .modal-background {
            background: rgba(0, 0, 0, 0);
            animation: fadeIn 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.seven .modal-background .modal {
            height: 75px;
            width: 75px;
            border-radius: 75px;
            overflow: hidden;
            animation: bondJamesBond 1.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.seven .modal-background .modal h2, #modal-container.seven .modal-background .modal p {
            opacity: 0;
            position: relative;
            animation: modalContentFadeIn .5s 1.4s linear forwards;
            }
            #modal-container.seven.out {
            animation: slowFade .5s 1.5s linear forwards;
            }
            #modal-container.seven.out .modal-background {
            background-color: rgba(0, 0, 0, 0.7);
            animation: fadeToRed 2s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.seven.out .modal-background .modal {
            border-radius: 3px;
            height: 162px;
            width: 227px;
            animation: killShot 1s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container.seven.out .modal-background .modal h2, #modal-container.seven.out .modal-background .modal p {
            animation: modalContentFadeOut 0.5s 0.5 cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
            }
            #modal-container .modal-background {
            display: table-cell;
            background: rgba(0, 0, 0, 0.8);
            text-align: center;
            vertical-align: middle;
            }
            #modal-container .modal-background .modal {
            background: white;
            padding: 50px;
            display: inline-block;
            border-radius: 3px;
            font-weight: 300;
            position: relative;
            }
            #modal-container .modal-background .modal h2 {
            font-size: 25px;
            line-height: 25px;
            margin-bottom: 15px;
            }
            #modal-container .modal-background .modal p {
            font-size: 18px;
            line-height: 22px;
            }
            #modal-container .modal-background .modal .modal-svg {
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: 100%;
            border-radius: 3px;
            }
            #modal-container .modal-background .modal .modal-svg rect {
            stroke: #fff;
            stroke-width: 2px;
            stroke-dasharray: 778;
            stroke-dashoffset: 778;
            }

            .content {
            min-height: 100%;
            height: 100%;
            background: white;
            position: relative;
            z-index: 0;
            }
            .content h1 {
            padding: 75px 0 30px 0;
            text-align: center;
            font-size: 30px;
            line-height: 30px;
            }
            .content .buttons {
            max-width: 800px;
            margin: 0 auto;
            padding: 0;
            text-align: center;
            }
            .content .buttons .button {
            display: inline-block;
            text-align: center;
            padding: 10px 15px;
            margin: 10px;
            background: red;
            font-size: 18px;
            background-color: #efefef;
            border-radius: 3px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            cursor: pointer;
            }
            .button {
                color: var(--secondary);
                cursor: pointer;
                padding: 11px 5px;
            }
            .button:hover {
                text-decoration: underline;
            }
            .content .buttons .button:hover {
            color: white;
            background: #009bd5;
            }

            @keyframes unfoldIn {
            0% {
                transform: scaleY(0.005) scaleX(0);
            }
            50% {
                transform: scaleY(0.005) scaleX(1);
            }
            100% {
                transform: scaleY(1) scaleX(1);
            }
            }
            @keyframes unfoldOut {
            0% {
                transform: scaleY(1) scaleX(1);
            }
            50% {
                transform: scaleY(0.005) scaleX(1);
            }
            100% {
                transform: scaleY(0.005) scaleX(0);
            }
            }
            @keyframes zoomIn {
            0% {
                transform: scale(0);
            }
            100% {
                transform: scale(1);
            }
            }
            @keyframes zoomOut {
            0% {
                transform: scale(1);
            }
            100% {
                transform: scale(0);
            }
            }
            @keyframes fadeIn {
            0% {
                background: rgba(0, 0, 0, 0);
            }
            100% {
                background: rgba(0, 0, 0, 0.7);
            }
            }
            @keyframes fadeOut {
            0% {
                background: rgba(0, 0, 0, 0.7);
            }
            100% {
                background: rgba(0, 0, 0, 0);
            }
            }
            @keyframes scaleUp {
            0% {
                transform: scale(0.8) translateY(1000px);
                opacity: 0;
            }
            100% {
                transform: scale(1) translateY(0px);
                opacity: 1;
            }
            }
            @keyframes scaleDown {
            0% {
                transform: scale(1) translateY(0px);
                opacity: 1;
            }
            100% {
                transform: scale(0.8) translateY(1000px);
                opacity: 0;
            }
            }
            @keyframes scaleBack {
            0% {
                transform: scale(1);
            }
            100% {
                transform: scale(0.85);
            }
            }
            @keyframes scaleForward {
            0% {
                transform: scale(0.85);
            }
            100% {
                transform: scale(1);
            }
            }
            @keyframes quickScaleDown {
            0% {
                transform: scale(1);
            }
            99.9% {
                transform: scale(1);
            }
            100% {
                transform: scale(0);
            }
            }
            @keyframes slideUpLarge {
            0% {
                transform: translateY(0%);
            }
            100% {
                transform: translateY(-100%);
            }
            }
            @keyframes slideDownLarge {
            0% {
                transform: translateY(-100%);
            }
            100% {
                transform: translateY(0%);
            }
            }
            @keyframes moveUp {
            0% {
                transform: translateY(150px);
            }
            100% {
                transform: translateY(0);
            }
            }
            @keyframes moveDown {
            0% {
                transform: translateY(0px);
            }
            100% {
                transform: translateY(150px);
            }
            }
            @keyframes blowUpContent {
            0% {
                transform: scale(1);
                opacity: 1;
            }
            99.9% {
                transform: scale(2);
                opacity: 0;
            }
            100% {
                transform: scale(0);
            }
            }
            @keyframes blowUpContentTwo {
            0% {
                transform: scale(2);
                opacity: 0;
            }
            100% {
                transform: scale(1);
                opacity: 1;
            }
            }
            @keyframes blowUpModal {
            0% {
                transform: scale(0);
            }
            100% {
                transform: scale(1);
            }
            }
            @keyframes blowUpModalTwo {
            0% {
                transform: scale(1);
                opacity: 1;
            }
            100% {
                transform: scale(0);
                opacity: 0;
            }
            }
            @keyframes roadRunnerIn {
            0% {
                transform: translateX(-1500px) skewX(30deg) scaleX(1.3);
            }
            70% {
                transform: translateX(30px) skewX(0deg) scaleX(0.9);
            }
            100% {
                transform: translateX(0px) skewX(0deg) scaleX(1);
            }
            }
            @keyframes roadRunnerOut {
            0% {
                transform: translateX(0px) skewX(0deg) scaleX(1);
            }
            30% {
                transform: translateX(-30px) skewX(-5deg) scaleX(0.9);
            }
            100% {
                transform: translateX(1500px) skewX(30deg) scaleX(1.3);
            }
            }
            @keyframes sketchIn {
            0% {
                stroke-dashoffset: 778;
            }
            100% {
                stroke-dashoffset: 0;
            }
            }
            @keyframes sketchOut {
            0% {
                stroke-dashoffset: 0;
            }
            100% {
                stroke-dashoffset: 778;
            }
            }
            @keyframes modalFadeIn {
            0% {
                background-color: transparent;
            }
            100% {
                background-color: white;
            }
            }
            @keyframes modalFadeOut {
            0% {
                background-color: white;
            }
            100% {
                background-color: transparent;
            }
            }
            @keyframes modalContentFadeIn {
            0% {
                opacity: 0;
                top: -20px;
            }
            100% {
                opacity: 1;
                top: 0;
            }
            }
            @keyframes modalContentFadeOut {
            0% {
                opacity: 1;
                top: 0px;
            }
            100% {
                opacity: 0;
                top: -20px;
            }
            }
            @keyframes bondJamesBond {
            0% {
                transform: translateX(1000px);
            }
            80% {
                transform: translateX(0px);
                border-radius: 75px;
                height: 75px;
                width: 75px;
            }
            90% {
                border-radius: 3px;
                height: 182px;
                width: 247px;
            }
            100% {
                border-radius: 3px;
                height: 162px;
                width: 227px;
            }
            }
            @keyframes killShot {
            0% {
                transform: translateY(0) rotate(0deg);
                opacity: 1;
            }
            100% {
                transform: translateY(300px) rotate(45deg);
                opacity: 0;
            }
            }
            @keyframes fadeToRed {
            0% {
                box-shadow: inset 0 0 0 rgba(201, 24, 24, 0.8);
            }
            100% {
                box-shadow: inset 0 2000px 0 rgba(201, 24, 24, 0.8);
            }
            }
            @keyframes slowFade {
            0% {
                opacity: 1;
            }
            99.9% {
                opacity: 0;
                transform: scale(1);
            }
            100% {
                transform: scale(0);
            }
            }

    </style>
    `.trim()
}

export default class Rec_shell extends HTMLElement {
    static get observedAttributes() {
        return ['rec-id', 'customer-id', 'admin-assigned', 'title', 'body'];
    }

    constructor(){
        super();
        this.shadow = this.attachShadow({ mode: 'open' });

        this.state = {
            data: null
        }
        this.css = styles()

    }

    modal(title, body, id){
        /*html*/
        const shell = `
        <div id="modal-container">
            <div class="modal-background">
                <div class="safe modal">
                    <h5 class="widget__title">${title}</h5>
                    <p>${body}</p>
                    <p>Rec id: ${id}</p>
                </div>
            </div>
        </div>
        `.trim()

        return shell
    }

    modal_handlers(){
        
    const modal_container = this.shadow.querySelectorAll("#modal-container")
    const body = document.querySelector('body')
    const parent = this.shadow
    
    parent.querySelectorAll('.button').forEach(el => {
        el.addEventListener('click', e=>{
                let buttonId = e.currentTarget.getAttribute('id')
            
                modal_container.forEach(el=>{
                    if (el.dataset.uid == e.currentTarget.dataset.uid) {
                        el.removeAttribute('class')
                        el.classList.add(buttonId)
                        body.classList.add('modal-active')
                    }
                })
        })
    }); 
    parent.querySelectorAll('.safe').forEach(el=>{
        const text = el.querySelector('p')
        text.innerHTML = urlify(text.textContent)
        el.addEventListener('click', e=>{
            e.stopPropagation()
        })
    })
    modal_container.forEach(el=>{
        el.addEventListener('click', e=>{
            if (el.dataset.uid == e.currentTarget.dataset.uid) {
                const _this = e.currentTarget
                _this.classList.add('out')
                body.classList.remove('modal-active')
            }
        })
    })
    }


    toolbar(){
        const el = document.createElement('div')
        /*html*/
        el.innerHTML = `
            <span>id: ${this.rec_id}</span>
            ${this.accepted == true 
                ? `<span class="small_txt text-success">accepted</span>`
                : ''
            }

            ${this.dismissed == true 
                ? `<span class="small_txt text-danger">dismissed</span>`
                : ''
            }
            <span class="x dismiss">delete</span>
        `.trim()

        return el
    }

    render(){
        this.shadow.innerHTML = ''
        const colors = ['#62cde0','#ca7d66','#01d4b4','#ff9c00', '#62cde0','#ca7d66','#01d4b4','#ff9c00', '#62cde0','#ca7d66','#01d4b4','#ff9c00', '#62cde0','#ca7d66','#01d4b4','#ff9c00']
        /*html*/
        const shell = async () => {
            return `
            ${this.css}
            ${this.modal(this.title, this.body, this.rec_id)}
            <div class="rec-container">
                <div class="rec">
                    <div id="six" class="button">
                        <h5 class="widget__title rec-title">
                            <strong>${this.price != null ? `$${this.price}:`: ``}</strong> ${this.title}
                        </h5>
                    </div>
                    <div id="toolbar"></div>
                </div>
            </div>
            `.trim()
        }

        const init = () => {
            this.modal_handlers()

            this.shadow.querySelector(".x").addEventListener('click', e=>{
                this.style.display = 'none';
                this.setAttribute('deleted', 'true')
            })
        }

        shell()
            .then(html => {
                let el = document.createElement('div')
                el.innerHTML = html
                return el
            })
            .then(el => {el.querySelector("#toolbar").appendChild(this.toolbar()); return el})
            .then(el=> this.shadow.appendChild(el))
            .then(() => init())
    }

    connectedCallback(){
        this.rec_id = this.getAttribute('rec_id')
        this.customer_id = this.getAttribute('customer-id')
        this.customer_id = this.getAttribute('admin-assigned')
        this.title = this.getAttribute('title')
        this.body = this.getAttribute('body')
        this.price = eval(this.getAttribute('price'))

        const accepted = this.getAttribute('accepted')
        this.accepted = accepted != null && parseInt(accepted) == 1
                            ? true
                            : false

        const dismissed = this.getAttribute('dismissed')
        this.dismissed = dismissed != null && parseInt(dismissed) == 1
                            ? true
                            : false
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('admin-recommendation-shell', Rec_shell))