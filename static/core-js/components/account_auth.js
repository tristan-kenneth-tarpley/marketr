class campaign_auth extends HTMLElement {
    constructor() {
        super();
        this.root = this.attachShadow({ mode: 'open' });
    }
    set platform(name) {
        /*html*/
        this.root.innerHTML = `
            <h1>${name}</h1>
        `
    }
}

  
function getDefaultTemplate(
    name,
    oldnum = 1,
    newnum = 1,
    target = 1,
    color = '#880011'
) {
    const width = (newnum / target) * 100 + '%';
    return el(
        'div',
        { className: 'box' },
        el(
        'div',
        { className: 'left' },
        el('h2', null, name),
        el(
            'div',
            { className: 'bar' },
            el('div', {
            className: 'fill',
            style: `background-color:${color};width:${width}`
            })
        )
        ),
        el(
        'div',
        { className: 'mini-stats' },
        el('div', null, newnum),
        el('div', null, `Was ${oldnum}`)
        )
    );
}
  
  function getDefaultStyle() {
    return el(
      'style',
      null,
      `
        div {
          font-family: Helvetica, sans-serif;
        }
        h2 {
          margin: 0;
        }
        .left {
          flex: 1;
        }
        .mini-stats {
          flex-grow: 1;
          text-align: center;
        }
        .mini-stats > div {
          font-size: 0.7em;
        }
        .mini-stats > *:first-child {
          font-size: 1.2em;
        }
        div.box {
          display: flex;
          background-color: #F5F5F5;
          padding: 10px;
        }
        div.bar {
          height: 7px;
          width: 200px;
          background: #C0C0C0;
        }
        div.bar .fill {
          height: 100%;
        }
      `.trim()
    );
  }
  
class SocialStats extends HTMLElement {
    static get observedAttributes() {
        return ['oldnum', 'newnum', 'colour', 'target', 'name'];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
    }
    connectedCallback() {
        this.css = getDefaultStyle();
        this.template = getDefaultTemplate(
        ...['name', 'oldnum', 'newnum', 'target', 'colour'].map(name => {
            return this.getAttribute(name);
        })
        );
        this.shadow.appendChild(this.css);
        this.shadow.appendChild(this.template);
    }
}
  
window.customElements.define('social-stats', SocialStats);
customElements.define('campaign-auth', campaign_auth);
const el = document.createElement('campaign-auth');
el.platform = 'test';
document.querySelector('#root').appendChild(el);