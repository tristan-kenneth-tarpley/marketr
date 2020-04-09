import {tabs, shadow_events, dots_loader} from '/static/src/components/UI_elements.js'
import {iterate_text, modal, modal_trigger, modal_handlers, currency,currency_rounded,number,number_rounded,number_no_commas,percent,remove_commas,remove_commas_2} from '/static/src/convenience/helpers.js'

const _score_color = (val) => {
  let _class;
  if (val <= 4) _class = '_red'
  else if (val > 4 && val <= 7) _class = '_yellow'
  else if (val > 7) _class = '_green'

  return _class
}
const _score = (val) => {
  let _class = ''//_score_color(val)
  return `<h1 class="${_class} widget__value">${number(val)}</h1>`
}

const styles = (attrs) => {
  let {max_height} = attrs
  /*html*/
  return `
  <style>
      @import url('/static/assets/css/dist/styles.min.css');

      .opp_container {
          max-height: ${max_height}px;
          overflow-y: scroll;
          overflow-x: hidden;
      }
      .opp_row {
        border-bottom: 1px solid rgba(0,0,0,.1) !important;
        display: flex;
        align-items: center;
        padding: 1% 5% 1% 0;
      }
      .opp_row p {
        margin-bottom: 0;
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
      h1.small {
        margin-bottom: 0 !important;
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
    // quality score opp score
    // impression share opp score
    /*html*/
    return `
    <div class="row row_cancel">
      <div class="col-lg-6 col-md-6 col-sm-6 col-6">
        <h1 class="widget__title small">Keyword</h1>
      </div>
      <div style="text-align:right;" class="col-lg-6 col-md-6 col-sm-6 col-6">
        <h1 style="justify-content: flex-end;" class="widget__title small">Total Opportunity score (out of 10)</h1>
      </div>
    </div>

    <div class="opp_container">
      ${this.state.data.raw.map(top =>{
        let returned = ''
        if (top.opp_score > 0) returned += this.row(top)
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

  row(row) {
    // const arr = [
    //   {
    //     title: "quality score",
    //     value: row.qs_opp_score
    //   },
    //   {
    //     title: "Impression share",
    //     value: row.is_opp_score
    //   },
    //   {
    //     title: "Lost impression share",
    //     value: row.low_is_opp_score
    //   },
    //   {
    //     title: "Top impression share",
    //     value: row.top_is_opp_score
    //   },
    //   {
    //     title: "Lost top impression share",
    //     value: row.searchlosttopisrank
    //   }
    // // ]
    
    // let test = Object.keys( arr ).map(function ( value ) { return arr[value]; });
    // console.log(Math.max.apply(null, test))

    const {keyword, opp_score} = row
    /*html*/
    return `
      <div class="opp_row row">
        <div class="col-lg-6 col-md-6 col-sm-6 col-6">
          <p class="small_txt">${keyword}</p>
        </div>
        <div style="text-align:right;" class="col-lg-6 col-md-6 col-sm-6 col-6">
          ${_score(opp_score)}
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
