import {tabs, shadow_events, dots_loader} from '/static/src/components/UI_elements.js'

const _score_color = (val) => {
  let _class;
  if (val <= 4) _class = '_red'
  else if (val > 4 && val <= 7) _class = '_yellow'
  else if (val > 7) _class = '_green'

  return _class
}
const _score = (val) => {
  let _class = _score_color(val)
  return `<h1 class="${_class} widget__value">${number(val)}</h1>`
}

const styles = (attrs) => {
  let {max_height} = attrs
  /*html*/
  return `
  <style>
      @import url('/static/assets/css/bootstrap.min.css');
      @import url('/static/assets/css/styles.css');
      @import url('/static/assets/icons/all.min.css');
      @import url("https://cdn.jsdelivr.net/npm/vanilla-datatables@v1.6.16/dist/vanilla-dataTables.min.css");
      @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');

      .opp_container {
          max-height: ${max_height}px;
          overflow-y: scroll;
          overflow-x: hidden;
      }
      .opp_row {
        border-bottom: 1px solid #eee !important;
        margin-bottom: 4%;
        display: flex;
        align-items: center;
        padding: 1% 5%;
      }
      table .widget__title {
        margin-bottom: 0 !important;
        font-size: .7em;
      }
      
      td {
        vertical-align: middle !important;
      }
      td span {
        font-size: 8pt;
      }
  </style>
  `.trim()
}

export default class Opportunities extends HTMLElement {
  static get observedAttributes() {
      return ['json'];
  }
  constructor() {
      super();
      this.shadow = this.attachShadow({ mode: 'open' });
      this.state = {
          data: null
      }
  }

  collapsed_view() {
    return `
    <div class="row">
      <div class="col-lg-6 col-md-6 col-sm-6">
        <h1 class="widget__title small">Topic</h1>
      </div>
      <div style="text-align:right;" class="col-lg-6 col-md-6 col-sm-6 ">
        <h1 style="justify-content: flex-end;" class="widget__title small">Opportunity score</h1>
      </div>
    </div>

    <div class="opp_container">
      ${this.state.data.aggregate.map(top =>{
        let {opp_score, cleaned_keywords} = top
        let returned = ''

        if (opp_score > 0) returned += this.row(cleaned_keywords, opp_score)
        else returned += ''

        return returned
      }).join("")}
    </div>`
  }

  expanded_view(){
    let data = this.state.data.raw
    const header = (title) => `<h1 class="widget__title">${title}</h1>`
    const value = (val) => `${val}`
    const num_value = (val, options) => {
      if (val) {
        let defaults = {
          percent: false,
          rounded: false,
          currency: false,
          color: false
        }

        options = Object.assign({}, defaults, options);

        const display = num => {
          let returned;
          if (options.rounded) returned = number_rounded(num)
          else returned = number(num)

          if (options.color) returned = `<span style="font-size:inherit;" class="${_score_color(returned)}">${returned}</span>`

          return returned
        }
        
        return `${options.currency ? "$" : ""}${val ? display(val) : 0}${options.percent ? "%" : ""}`
      }
      else return 'n/a'
    }

    let headings = [
      'opp. score',
      'keyword',
      'quality score',
      'quality score opportunity score',
      'impression share',
      'impression share opportunity score',
      'top impression share',
      'top impression share opportunity score',
      'lost top impression share',
      'lost impression share opportunity score',
      'profit potential per $100 spent',
      'contrained health score',
      'impressions',
      'clicks',
      'ctr',
      'cpc',
      'cost',
    ]

    let d_rows = data.map(row=>{
      return [
        num_value(row.opp_score > 0 ? row.opp_score : null, {color: true}),
        value(row.keyword),
        num_value(row.qualityscore),
        num_value(row.qs_opp_score),
        num_value(row.searchimprshare * 100, {percent: true}),
        num_value(row.is_opp_score),
        num_value(row.searchtopis * 100, {percent: true}),
        num_value(row.top_is_opp_score),
        num_value(row.searchlosttopisrank * 100, {percent: true}),
        num_value(row.lost_is_opp_score),
        num_value(row.pp100, {currency: true}),
        num_value(row.contrained_mi),
        num_value(row.impressions, {rounded: true}),
        num_value(row.clicks, {rounded: true}),
        num_value(row.ctr * 100, {percent: true}),
        num_value(row.cpc, {currency: true}),
        num_value(row.cost, {currency: true}),
      ]
    })

    const options = {
      searchable: false,
      perPage: 5,
      perPageSelect: false,
      sortable: true,
      data: {
        "headings": headings,
        "data": d_rows
      }
    }

    return options
  }

  row(keyword, score) {
    /*html*/
    return `
      <div class="opp_row row">
        <div class="col-lg-6 col-md-6 col-sm-6">
          <span>${keyword}</span>
        </div>
        <div style="text-align:right;" class="col-lg-6 col-md-6 col-sm-6">
          ${_score(score)}
        </div>
      </div>
    `
  }

  render(init=true){
      this.shadow.innerHTML = ""
      const el = document.createElement('div')
      /*html*/
      el.innerHTML = `
        ${this.css}
        ${!this.state.expanded ? this.collapsed_view() : `<table class="table-responsive" id="expanded_table"></table>`}
      `

      this.shadow.appendChild(el)

      if (this.state.expanded) {
        new DataTable(this.shadow.querySelector("#expanded_table"), this.expanded_view());
      }
  }

  connectedCallback() {
      this.state.data = JSON.parse(this.getAttribute('json'))
      this.max_height = this.getAttribute('max-height')
      this.state.expanded = eval(this.getAttribute('expanded'))

      this.css = styles({
        max_height: this.max_height
      })

      this.render()
  }
}

document.addEventListener( 'DOMContentLoaded', customElements.define('opportunities-agg', Opportunities))
