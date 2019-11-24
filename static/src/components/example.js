const template = (
    name,
    oldnum = 1,
    newnum = 1,
    target = 1,
    color = '#880011'
) => {
    const width = (newnum / target) * 100 + '%';
    return (
        `
        ${name}
        ${oldnum}
        ${width}
        `.trim()
    );
}
  
  const styles = () => {
    return html(
      'style',
      null,
      `
        @import url('/static/assets/css/styles.css');
        div {
          font-family: Helvetica, sans-serif;
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
      `
    );
  }
  

export class SocialStats extends HTMLElement {
    static get observedAttributes() {
        return ['oldnum', 'newnum', 'colour', 'target', 'name'];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
    }
    connectedCallback() {
        this.css = styles();
        this.template = template(
            ...['name', 'oldnum', 'newnum', 'target', 'colour'].map(name => {
                return this.getAttribute(name);
            })
        );
        const el = document.createElement('div')
        el.innerHTML = this.template
        this.shadow.appendChild(this.css);
        this.shadow.appendChild(el);
    }
}
  
window.customElements.define('social-stats', SocialStats);