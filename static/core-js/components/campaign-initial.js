const styles = () => {
    return html(
      'style',
      null,
      `
        @import url('/static/assets/css/styles.css');
        @import url('/static/assets/css/bootstrap.min.css');
      `
    );
  }

export class CampaignInitial extends HTMLElement {
    static get observedAttributes() {
        return null;//['oldnum', 'newnum', 'colour', 'target', 'name'];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
    }

    init_eventListeners(root){
        root.querySelector('.campaign_controller').addEventListener('click', e=>{
            e.currentTarget.parentNode.parentNode.remove()        
            root.dispatchEvent(query_change);
        })
        root.querySelector('#new_campaign').addEventListener('click', e=>{
            setQueryString('campaign_view', 'new')
        })
        root.querySelector('#existing').addEventListener('click', e=>{
            setQueryString('campaign_view', 'existing')
        })

    }

    connectedCallback() {
        this.css = styles();
        /*html */
        this.template = `
        <div class="row">
            <div class="col">
                <a class="campaign_controller" id="new_campaign" href="#">
                    <div class="hover_box">
                        <div class="center_it" style="margin: auto;padding: 5% 2%;">
                            <thead><strong>Create new campaign</strong></thead>
                        </div>
                    </div>
                </a>
            </div>
            <div class="col">
                <a class="campaign_controller" id="existing" href="#">
                    <div class="hover_box">
                        <div class="center_it" style="margin: auto;padding: 5%;">
                            <thead><strong>Analyze existing campaigns</strong></thead>
                        </div>
                    </div>
                </a>
            </div>
        </div> 
        `
        const el = document.createElement('div')
        el.innerHTML = this.template
        this.shadow.appendChild(this.css);
        this.shadow.appendChild(el);
        this.init_eventListeners(this.shadow)
    }
}
  
window.customElements.define('campaign-initial', CampaignInitial);