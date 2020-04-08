import {tabs, shadow_events, dots_loader} from '/static/src/components/UI_elements.js'

const styles = () => {
  /*html*/
  return `
  <style>
    @import url('/static/assets/css/bootstrap.min.css');
    @import url('/static/assets/css/styles.css');
    @import url('/static/assets/icons/all.min.css');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');
    #resource_links li {
        margin: 2em 0;
        list-style-type: none;
    }
    #resource_links li,
    #resource_links li a {
        color: #fff !important;
        font-weight: 500;
    }
    #resource_links a {
        text-decoration: underline;
    }
    #resources_response #back_button {
        position: relative;
        left: -2em;
    }
    #resources_response p {
        font-size: 1.7em;
        font-weight: 600;
        line-height: 1.3em;
    }
    .white-color {
        color: #F5F5F5 !important;
    }
    h3.white-color {
        margin: 0 0 20px;
        padding: 0 0 20px;
        position: relative;
        font-weight: 600;
    }
    @-webkit-keyframes click-wave {
    0% {
        height: 40px;
        width: 40px;
        opacity: 0.35;
        position: relative;
    }
    100% {
        height: 200px;
        width: 200px;
        margin-left: -80px;
        margin-top: -80px;
        opacity: 0;
    }
    }
    @-moz-keyframes click-wave {
    0% {
        height: 40px;
        width: 40px;
        opacity: 0.35;
        position: relative;
    }
    100% {
        height: 200px;
        width: 200px;
        margin-left: -80px;
        margin-top: -80px;
        opacity: 0;
    }
    }
    @keyframes click-wave {
    0% {
        height: 40px;
        width: 40px;
        opacity: 0.35;
        position: relative;
    }
    100% {
        height: 200px;
        width: 200px;
        margin-left: -80px;
        margin-top: -80px;
        opacity: 0;
    }
    }
    .option-input {
        -webkit-appearance: none;
        -moz-appearance: none;
        -ms-appearance: none;
        -o-appearance: none;
        appearance: none;
        position: relative;
        top: 13.3333333333px;
        right: 0;
        bottom: 0;
        left: 0;
        height: 40px;
        width: 40px;
        -webkit-transition: all 0.15s ease-out 0s;
        -moz-transition: all 0.15s ease-out 0s;
        transition: all 0.15s ease-out 0s;
        background: #cbd1d8 !important;
        border: none;
        color: #fff !important;
        cursor: pointer;
        display: inline-block;
        margin-right: 0.5rem;
        outline: none;
        position: relative;
        z-index: 1000;
        border: 2px solid white;
    }
    .option-input:hover {
        background: #9faab7 !important;
    }
    .option-input:checked {
        background: #40e0d0 !important;
    }
    .option-input:checked::before {
        height: 40px;
        width: 40px;
        position: absolute;
        content: "\\2716";
        display: inline-block;
        font-size: 26.6666666667px;
        text-align: center;
        line-height: 40px;
    }
    .option-input:checked::after {
        -webkit-animation: click-wave 0.65s;
        -moz-animation: click-wave 0.65s;
        animation: click-wave 0.65s;
        background: #40e0d0 !important;
        content: '';
        display: block;
        position: relative;
        z-index: 100;
    }
    .option-input.radio {
        border-radius: 50%;
    }
    .option-input.radio::after {
        border-radius: 50%;
    }

    .form__container {
        display: flex;
        flex-direction: column;
        color: #fff !important;
        text-align: center;
        align-items: flex-start;
    }
    .form__container label {
        display: block;
        line-height: 40px;
        cursor: pointer;
        text-align:left;
        font-size: 1.4em;
        font-weight: 600;
    }
    .btn-neutral {
        color: white !important;
    }
    .btn-neutral:hover {
        color: var(--secondary) !important;
    }

  </style>
  `.trim()
}

export default class Quiz extends HTMLElement {
    static get observedAttributes() {
        return ['customer_id'];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.state = {
            data: null,
            checked: false
        }

        this.css = styles()
    }

    ResourcesResponse() {
        const table = this.ResourcesTable()[this.biggest_need]
        /*html*/
        this.right_response = `
        <section id="resources_right">
            <p>${table.sales_copy}</p>
            <div class="hb-form">
                <form>
                    <div class="input-group">
                        <a style="border: 3px solid transparent;" class="btn btn-primary" href="/new">Let's try it out <i class="fad fa-external-link"></i></a>&nbsp;
                        <a class="btn btn-neutral" href="#about">I want to learn more about Market(r) <i class="fad fa-chevron-down"></i></a> 
                    </div>
                    <span class="help-text">You won't be charged a dime for 6 months...</span>
                </form>
            </div>
        </section>`
        /*html*/
        return (`
            <section id="resources_response">
                <button id="back_button" class="btn btn-neutral">
                    <i class="fas fa-backward"></i>
                    select different
                </button>
                <p class="white-color">${table.answer}</p>
                <p class="white-color">${table.articles.length > 1 ? `Here are some resources you might find helpful:` : ``}</p>
                <ul id="resource_links">
                    ${table.articles.map(article=>{
                        /*html*/
                        return (`
                            <li><i class="fas fa-external-link-square-alt"></i> <a target="__blank" href="${article.link}">${article.title}</a></li>
                        `)
                    }).join("")}
                </ul>
            </section>
        `)
    }

    ResourcesTable() {
        const struct = (answer, sales_copy, articles, other_platforms) => {
            return {
                answer,
                sales_copy,
                articles,
                other_platforms
            }
        }
        /*html*/
        const cta_line = `
            <p>We're inspired to see so many businesses helping one another out.  We want to help too - to that end, we're offering our Analytics package <strong>FREE</strong> for 6 months.</p> 
            <p>You'll get:</p>
            <ul id="features_list">
                <li> <i class="fas fa-check"></i> Weekly 1-click recommendations on how to not only survive right now, but continue to grow your business.</li>
                <li> <i class="fas fa-check"></i> Profit Potential Per $100 Spent: See how much you're getting out of every ad, ad group, campaign, and channel at a glance</li>
                <li> <i class="fas fa-check"></i> Use our listener tool to see what the market is saying about your competition, industry, and your brand.</li>
                <li><i class="fas fa-check"></i> Market(r) learns exactly how much you should spend and where to spend it.</li>
            </ul>`

        return {
            cut: struct(
                "Don't cut your spend! Effective marketing leads to revenue. Now is not the time to cut off revenue. Instead, figure out a way to make it more effective.",
                `<p>With that said, 40% of all ad spend is typically wasted. During COVID-19, this is a bad time to be throwing away almost half of your budget!</p> ${cta_line}`,
                [
                    {
                        link: 'https://www.forbes.com/sites/bradadgate/2019/09/05/when-a-recession-comes-dont-stop-advertising/#557695944608',
                        title: "Forbes: When a Recession Comes, Don't Stop Advertising"
                    },
                    {
                        link: 'https://www.seerinteractive.com/blog/recession-marketing-the-scalpel-vs-the-sledgehammer/',
                        title: "Seer Interactive: Marketing in a Recession: Budget Cuts - The Scalpel vs. the Sledgehammer"
                    },
                    {
                        link: 'https://hbr.org/2009/04/how-to-market-in-a-downturn-2',
                        title: "Harvard Business Review: How to Market in a Downturn"
                    },
                ],
                []
            ),
            waste: struct(
                `<p class="white-color">Historically, 40% of all ad spend is completely wasted. (according to the Interactive Advertising Bureau). There are two types of industries right now amidst the COVID-19 crisis: Those whose ad costs are rising and those whose are falling. Both, however, present opportunities!</p>`,
                `${cta_line}`,
                [
                    {
                        link: 'https://www.seerinteractive.com/blog/we-analyzed-201k-youtube-channels-and-found-3802-kids-channels-to-negate/',
                        title: "Seer Interactive: We Analyzed 201k YouTube Channels and Founded 3,802 Kids Channels to Negate"
                    },
                    {
                        link: 'https://hbr.org/2009/04/how-to-market-in-a-downturn-2',
                        title: 'Harvard Business Review: How to Market in a Downturn'
                    },
                    {
                        link: 'https://hbr.org/2002/04/look-before-you-lay-off',
                        title: 'Harvard Business Review: Look Before You Lay Off'
                    }
                ],
                []
            ),
            opportunities: struct(
                `There are a lot of opportunities right now! Now is the time for marketing that reads the room, finds how they can be truly useful to their target market, and then genuinely help them.`,
                `${cta_line}`,
                [
                    {
                        link: 'https://www.redfin.com/blog/virtual-home-tours-increase-amid-coronavirus/',
                        title: "Video Home Tour Requests Soar Nearly 500% in One Week"
                    },
                    {
                        link: 'https://blog.wunderstock.com/sba-disaster-loans/',
                        title: "Example: Video Home Tour Requests Soar Nearly 500% in One Week"
                    },
                    {
                        link: 'https://blog.wunderstock.com/sba-disaster-loans/',
                        title: "Example: Video Home Tour Requests Soar Nearly 500% in One Week"
                    }
                ],
                []
            )
        }
    }

    ViewController(el){
        const quiz = el.querySelectorAll('input[name="quiz__answers"]')
        if (quiz){
            quiz.forEach(ans=>{
                ans.addEventListener('change', e=>{
                    this.biggest_need = e.currentTarget.dataset.value
                    this.state.checked = true
                    setTimeout(()=>{
                        this.render()
                        document.querySelector("#replace_right").innerHTML = this.right_response
                    }, 500)
                })
            })
        }

        const back_button = el.querySelector("#back_button")
        if (back_button) {
            back_button.addEventListener('click', e=>{
                this.state.checked = false
                this.render()
            })
        }
        return el
    }

    Form(){
        /*html*/
        return(`
        <h3 style="font-size:35px;" class="white-color">Where do you need the most marketing help during COVID-19?</h3>
        <p class="white-color">Select one from the list:</p>
        <div class="form__container">
            <label>
                <input data-value="cut" type="radio" class="option-input radio" name="quiz__answers" />
                Should I cut my marketing spend? 
            </label>
            <label>
                <input data-value="waste" type="radio" class="option-input radio" name="quiz__answers" />
                Am I wasting my marketing spend?
            </label>
            <label>
                <input data-value="opportunities" type="radio" class="option-input radio" name="quiz__answers" />
                I don't even know where to start...
            </label>
        </div>
        `)
    }

    render(init=true){
        this.shadow.innerHTML = ""
        const el = document.createElement('div')
        /*html*/
        el.innerHTML = `
        ${this.css}
        ${
        !this.state.checked
            ? this.Form()
            : this.ResourcesResponse()
        }
    `
        this.shadow.appendChild(this.ViewController(el))
    }

    connectedCallback() {
        this.customer_id = this.getAttribute('customer_id')
        this.render()
    }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('covid-quiz', Quiz))
