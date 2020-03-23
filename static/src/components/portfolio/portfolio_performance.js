import PortfolioTrendline from '/static/src/components/portfolio/portfolio_trendline.js'
import PortfolioDetails from '/static/src/components/portfolio/Details.js'
import Insights from '/static/src/components/portfolio/Insights.js'
import Creative from '/static/src/components/portfolio/Creative.js'
import {google, facebook} from '/static/src/components/UI_elements.js'
import Recommendations from '/static/src/components/customer/recommendations.js'
import Opportunities from '/static/src/components/portfolio/Opportunities.js'
import Filter from '/static/src/components/portfolio/filter_by.js'
import { dots_loader, custom_select_body } from '/static/src/components/UI_elements.js'
import {remove_duplicates, iterate_text, modal, modal_trigger, modal_handlers, currency,currency_rounded,number,number_rounded,number_no_commas,percent,remove_commas,remove_commas_2} from '/static/src/convenience/helpers.js'
import NanocalRanger from 'https://unpkg.com/nanocal-ranger'

const title = (text, small=false) => `<h1 class="widget__title ${small ? `small` : ''}">${text}</h1>`
const value = (text, small=false) => `<h1 class="${small ? 'small_txt' : '' } widget__value">${text}</h1>`
export const marketr_score = (value, sub=false, huge=false) => {
    let _class;
    let returned
       
    try {
        if (value <= 1) _class = '_red'
        else if (value > 1 && value <= 2) _class = '_yellow'
        else if (value > 2) _class = '_green'

        return `<h1 class="${_class} ${huge ? 'oversized_text' : ''} widget__value">${number(value)} ${sub ? `<p style="font-size:40%;">health score</p>` : ''}</h1>`
        
    } catch (error) {
        return `<h1 class="${huge ? 'oversized_text' : ''} widget__value">n/a ${sub ? `<p style="font-size:40%;">health score</p>` : ''}</h1>`
    }
}

const styles = () => {
    /*html*/
    return `
    <style>
        @import url('/static/assets/css/bootstrap.min.css');
        @import url('/static/assets/css/styles.css');
        @import url('/static/assets/icons/all.min.css');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');
        .center__widget {
            display: flex;
            align-self:center;
            flex-direction: column;
        }
        .comparison_row h1 {
            margin-bottom: 0;
        }
        #info_bar {
            position: absolute;
            right: 1%;
            top: -75px;
            width: 35%;
        }
        #info_bar p {
            display: flex;
            justify-content: flex-end;
            font-size: .7em;
            line-height: 1.5em;
            margin: 0;
            white-space: nowrap;
        }
        #info_bar i {
            display: flex;
            justify-content: center;
            align-content: center;
            font-size: 1.3em;
            /*box-shadow: var(--silicon-raised);
            width: 30px;
            height: 34px;
            background-color: var(--panel-bg);
            border-radius: 100px;*/
        }
        #select_date_range {
            border-left: 3px solid transparent !important;
            border-right: 3px solid transparent !important;
            border-top: 3px solid transparent !important; 
        }
        #select_date_range:hover {
            box-shadow: none;
            border-radius: 6px;
        }
        #select_date_range span {
            color: inherit;
            font-size: inherit;
            padding: 2%;
        }
        #select_date_range span:hover {
            background-color: rgba(0,0,0,.1);
        }
        #comparison_table td {
            /*border-bottom: 1px solid #f2f2ff;*/
            padding: 2%;
        }
        .custom_modal .button {
            display: flex;
            flex-grow: 1;
            padding: 0;
            margin: 0;
            flex-direction: column;
        }
        #select_date_range {
            font-size: .7em;
            margin: 0;
        }
        .custom_modal p {
            display: none;
        }
        .custom_modal h1.small {
            color: var(--nav-color);
        }
        .metric_display {
            color: var(--primary);
            font-weight: bold;
            font-size: 120%;
        }

        #profit_chart_container {
            width: 100% !important;
            max-height: 380px !important; 
        }

        #profit_chart {
            width: 100% !important;
        }
        #insights {
            max-height: 500px;
        }

        .metric_labels {
            font-weight: 300;
            font-size: 95%;
        }
        #select_container .widget__title {
            margin-bottom: 3%;
        }
        #view_selector {
            padding: 0 4%;
        }
        #view_selector button {
            font-size: .7em;
            margin: 0;
            width: 100%;
        }
        #view_selector div:nth-child(1) button {
            border-left: 2px solid var(--primary) !important;
            border-right: 1px solid var(--primary) !important;
            border-radius: 0.1875rem 0 0 0.1875rem !important;
        }
        #view_selector div:nth-child(4) button {
            border-left: 1px solid var(--primary) !important;
            border-right: 2px solid var(--primary) !important;
            border-radius: 0 0.1875rem 0.1875rem 0 !important;
        }
        #view_selector div {
            padding: 0;
            margin: 0;
        }
        #view_selector div button.btn-secondary {
            padding: 10px 22px !important;
        }
        #view_selector div button {
            border-radius: 0;
            border-top: 2px solid var(--primary);
            border-right: 1px solid var(--primary);
            border-left: 1px solid var(--primary);
            border-bottom: 2px solid var(--primary);
        }
        #select_range {
            border-top: none;
            border-left: none;
            border-right: none;
            border-bottom: 2px solid rgba(0,0,0,.1);
        }
        @media only screen and (max-width: 700px) {
            #select_range {
                position: static;
                width: 100%;
            }
        }

        .blue-card {
            background-color: var(--panel-bg);
            box-shadow: var(--silicon-raised);
            text-align:center;
        }

        .stats {
            align-items: center;
            padding: 13px 0 11px;
            border-bottom: 1px solid #f2f2ff;
        }

        .stats {
            list-style-type: none;
            margin: 0;
            padding: 0;
            list-style: none;
        }
        .stat {
            display: flex;
            align-items: center;
            padding: 13px 0 11px;
            border-bottom: 1px solid #f2f2ff;
        }
        .stat-wrapper {
            padding: 0 30px;
            position: relative;
            list-style-type: none;
            width: 100%;
        }
        .stat span {
            vertical-align: baseline;
            margin-bottom: 0;
        }
        .stat h1 {
            color: var(--darker-blue);
            font-weight: 600;
            font-size: 25px;
            margin-right: 20px;
            flex-shrink: 0;
            margin-bottom: 0;
        }
        .stat h3 {
            font-size: 18px;
            font-weight: 600;
            margin-left: auto;
            margin-bottom: 0;
        }
        .secondary_value {
            color: var(--secondary);
            font-size: 18px;
            font-weight: 600;
            margin-left: auto;
            margin-bottom: 0;
        }


    </style>

    `.trim()
}

export default class PortfolioPerformance extends HTMLElement {
    static get observedAttributes() {
        return [
            'start_date_1', 'end_date_1', 'start_date_2', 'end_date_2',
            'customer-id', 'company-name', 'facebook_id', 'google_id', 'spend_rate', 'funds_remaining', 'insights'
        ];
    }
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.state = {
            data: null,
            date_range: 30,
            active_view: 0,
            active_data: {
                profitability: {
                    
                }
            },
            opp_expanded: false,
            null_data: false
        }

        this.static_copy = {
            score: `<p>An overall health metric of your portfolio. It’s a metric without limit.</p>
            <p>And much like a stock price, ideally increases over time. </p>
            <p>It’s a function of:</p>
            <ul style="text-align:left;">
                <li>Customer lifetime value</li>
                <li>Lead close rates</li>
                <li>Click through rates</li>
                <li>Cost per impression</li>
                <li>Impression share ranking</li>
                <li>Marketing portfolio strength</li>
            </ul>
            
            <p>This value is calculated and compared at the lowest levels of your marketing tactics and rolled up to the Account Portfolio level.</p>
            `
        }

             
        this.filter_observer = new MutationObserver(mutations=>{
            mutations.forEach(mutation => {
                if (mutation.type == "attributes") {
                    if (mutation.attributeName == 'active_sub_view') {
                        this.reset_sub_view(this.shadow.querySelector('filter-by').getAttribute('active_sub_view'))
                    }
                }
            });
        });

        this.css = styles()
    }

    abort(){
        this.state = {
            data: null,
            date_range: 30,
            active_view: 0,
            active_data: {
                profitability: {
                    
                }
            }
        }
        this.render()
    }

    profit_chart(target){
        var chart = target.getContext('2d')

        target.innerHTML = ""

        let {dates, pp100, cpm} = this.state.active_data.profitability
   
        const data = {
            labels: dates,
            datasets: [
                {
                    label: "Profit potential per $100 spent",
                    fill: false,
                    borderColor: "#09A1BC",
                    backgroundColor: "rgba(98, 205, 224, 0.8)",
                    borderWidth: 5,
                    pointRadius: 0,
                    pointBackgroundColor: "rgb(154, 238, 252)",
                    pointBorderColor: "rgba(98, 205, 224, 0.9)",
                    data: pp100,
                    pointHoverBorderWidth: 2,
                    pointHoverRadius: 7,
                    drawBorder: true
                },
                // {
                //     label: "Cost per thousand impressions",
                //     fill: false,
                //     borderColor: "#ca7d66",
                //     backgroundColor: "rgba(202, 125, 100, 0.8)",
                //     borderWidth: 5,
                //     pointRadius: 0,
                //     pointBackgroundColor: "rgb(224, 167, 148)",
                //     pointBorderColor: "rgba(202, 125, 100, 0.8)",
                //     data: cpm,
                //     pointHoverBorderWidth: 2,
                //     pointHoverRadius: 7,
                //     drawBorder: true
                // }
            ]
        };
        let font_color = `#b8b8d9`
        const options = {
            maintainAspectRatio: false,
            legend: {
                display: false,
                labels: {
                    fontColor: font_color
                }
            },
            scales: {
                xAxes: [{ 
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                      fontColor: font_color
                    },
                }],
                yAxes: [{
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                      fontColor: font_color
                    },
                }],
            },
            plugins: {
                datalabels:{
                    display: false
                }
            },
            elements: {
                line: {
                    tension: 0
                }
            },
            responsive: true
        };
        new Chart(chart, {
            type: 'line',
            data: data,
            options: options
        });
    }

    reset_charts(el){
        setTimeout(()=>{
            this.profit_chart(el.querySelector("#profit_chart"))
        }, 800)
    }


    data_controller(){
        let { active_view, data } = this.state
        let dates = [],
            pp100 = [],
            cpm = [],
            sub_filters = [],
            campaigns = [],
            adsets = []
    
        const sub_filter_struct = (sub) => {
            return {
                key: sub.key,
                campaign_name: sub.campaign_name,
                adset_name: sub.adset_name,
                marketr_index: sub.marketr_index
            }
        }
        const append_data = (iterable, value) => [...iterable, value]
        const group = i => {
            dates = append_data(dates, i.date_start)
            pp100 = append_data(pp100, i.pp100)
            cpm = append_data(cpm, i.cpm)
        }

        switch(active_view) {
            // portfolio
            case 0:
                for (let i of data.aggregate.raw) group(i)
                this.state.breakdown = data.buckets
                this.state.active_data.profitability = {dates, pp100, cpm, marketr_index: this.state.data.aggregate.index}
                break
            // platforms
            case 1:
                const campaign_struct = (camp) => {
                    return {
                        campaign_name: camp.campaign_name,
                        pp100: camp.pp100,
                        cpm: camp.cpm,
                        date_start: camp.date_start,
                        marketr_index:camp.marketr_index,
                        action: camp.action,
                        conversions: camp.conversions,
                        cost: camp.cost,
                        cost_comp: camp.cost_comp,
                        pp100_comp: camp.pp100_comp,
                        index_comp: camp.index_comp,
                        cost_comp: camp.cost_comp,
                        cpl_comp: camp.cpl_comp,
                        perc_change: camp.perc_change
                    }
                } 
                let ranged_campaigns = []
                const group_ranged_campaigns = camp => {
                    ranged_campaigns = [...ranged_campaigns, campaign_struct(camp)]

                    if (!sub_filters.includes(camp.campaign_name)) sub_filters.push(sub_filter_struct({
                        key: camp.campaign_name,
                        marketr_index: camp.marketr_index
                    }))
                }
                const group_campaigns = camp => {
                    campaigns = [...campaigns, campaign_struct(camp)]
                }

                if (data.ranged_campaigns.search) {
                    data.ranged_campaigns.search.map(camp=> group_ranged_campaigns(camp) )
                }
                if (data.ranged_campaigns.social) {
                    data.ranged_campaigns.social.map(camp=> group_ranged_campaigns(camp) )
                }
                if (data.campaigns.search) {
                    data.campaigns.search.map(camp=> group_campaigns(camp) )
                }
                if (data.campaigns.social) {
                    data.campaigns.social.map(camp=> group_campaigns(camp) )
                }

                this.sub_filters = sub_filters
                let _ranged_campaigns = ranged_campaigns.filter(x=>x.campaign_name == this.state.active_sub_view)
                let _campaigns = campaigns.filter(x=>x.campaign_name == this.state.active_sub_view)
                this.state.breakdown = remove_duplicates(_campaigns, 'campaign_name')

                this.state.active_data.profitability = {
                    dates: _ranged_campaigns.map(_camp=>_camp.date_start),
                    pp100: _ranged_campaigns.map(_camp=>_camp.pp100),
                    cpm: _ranged_campaigns.map(_camp=>_camp.cpm),
                    marketr_index: _ranged_campaigns.map(_camp=>_camp.marketr_index)[_ranged_campaigns.map(_camp=>_camp.marketr_index).length - 1],
                    action: _ranged_campaigns.map(i=>i.action)[ranged_campaigns.map(i=>i.action).length - 1],
                    cost: _ranged_campaigns.map(i=>i.cost).reduce((a, b) => a + b, 0)
                }
                // for (let i of data.buckets) group_buckets(i)
                // this.sub_filters = sub_filters
                // let _buckets = buckets.filter(x=>{
                //     return x.type == this.state.active_sub_view
                // })
                
                // this.state.breakdown = data.campaigns
                // this.state.active_data.profitability = {
                //     dates: _buckets.map(i => i.dates).flat(),
                //     pp100: _buckets.map(i=>i.pp100).flat(),
                //     cpm: _buckets.map(i=>i.cpm).flat(),
                //     marketr_index: _buckets[0] ? _buckets[0]['marketr_index'] : 0,
                //     cost: _buckets.map(i=>i.cost).reduce((a, b) => a + b, 0)
                // }
                break
            // campaigns
            case 2:
                // anchor
                const group_struct = (group) => {
                    return {
                        campaign_name: group.campaign_name,
                        adset_name: group.adset_name,
                        pp100: group.pp100,
                        cpm: group.cpm,
                        date_start: group.date_start,
                        marketr_index:group.marketr_index,
                        action: group.action,
                        conversions: group.conversions,
                        cost: group.cost,
                        cost_comp: group.cost_comp,
                        pp100_comp: group.pp100_comp,
                        index_comp: group.index_comp,
                        cost_comp: group.cost_comp,
                        cpl_comp: group.cpl_comp,
                        perc_change: group.perc_change
                    }
                } 
                let ranged_adsets = []
                const group_ranged_adsets = group => {
                    ranged_adsets = [...ranged_adsets, group_struct(group)]
                    if (!sub_filters.includes(group.adset_name)) sub_filters.push(sub_filter_struct({
                        key: group.adset_name,
                        campaign_name: group.campaign_name,
                        marketr_index: group.marketr_index
                    }))
                }
                const group_adsets = group => {
                    adsets = [...adsets, group_struct(group)]
                }

                if (data.ranged_ad_groups.search) {
                    data.ranged_ad_groups.search.map(ad_groups=> group_ranged_adsets(ad_groups) )
                }
                if (data.ranged_ad_groups.social) {
                    data.ranged_ad_groups.social.map(ad_groups=> group_ranged_adsets(ad_groups) )
                }
                if (data.ad_groups.search) {
                    data.ad_groups.search.map(ad_groups=> group_adsets(ad_groups) )
                }
                if (data.ad_groups.social) {
                    data.ad_groups.social.map(ad_groups=> group_adsets(ad_groups) )
                }

                this.sub_filters = sub_filters
               
                let _ranged_adsets = ranged_adsets.filter(x=>x.adset_name == this.state.active_sub_view)
                let _adsets = adsets.filter(x=>x.adset_name == this.state.active_sub_view)
                this.state.breakdown = remove_duplicates(_adsets, 'adset_name')

                this.state.active_data.profitability = {
                    dates: _ranged_adsets.map(_camp=>_camp.date_start),
                    pp100: _ranged_adsets.map(_camp=>_camp.pp100),
                    cpm: _ranged_adsets.map(_camp=>_camp.cpm),
                    marketr_index: _ranged_adsets.map(_camp=>_camp.marketr_index)[_ranged_adsets.map(_camp=>_camp.marketr_index).length - 1],
                    action: _ranged_adsets.map(i=>i.action)[_ranged_adsets.map(i=>i.action).length - 1],
                    cost: _ranged_adsets.map(i=>i.cost).reduce((a, b) => a + b, 0)
                }
        
                break
            // ads
            case 3:
                let ads = []
                let ranged_ads = []
                const ads_struct = (i, id, name, creative) => {
                    return {
                        campaign_name: i.campaign_name,
                        adset_name: i.adset_name,
                        id: id,
                        pp100: i.pp100,
                        cpm: i.cpm,
                        marketr_index:i.marketr_index,
                        date_start: i.date_start,
                        action: i.action,
                        cost: i.cost,
                        creative,
                        name,
                        conversions: i.conversions,
                        cost_comp: i.cost_comp,
                        pp100_comp: i.pp100_comp,
                        index_comp: i.index_comp,
                        cost_comp: i.cost_comp,
                        cpl_comp: i.cpl_comp,
                        perc_change: i.perc_change
                    }
                }

                const group_ranged_ads = i => {
                    let id = i.id == undefined ? i['adid'] : i['id']
                    
                    let name = i.ad_name == undefined || 0 ? id : i.ad_name
                    let creative;

                    if (i.id == undefined) {
                        creative = {
                            headline: `${i.headline1} | ${i.headline2}`,
                            description: i.description,
                            url: i.finalurl,
                            imageadurl: i.imageadurl
                        }
                    } else {
                        creative = {
                            thumbnail: i.thumbnail_url,
                            body: i.body
                        }
                    }

                    ranged_ads = [...ranged_ads, ads_struct(i, id, name, creative)]
                    if (!sub_filters.includes(name)) sub_filters.push(sub_filter_struct({
                        key: name,
                        campaign_name: i.campaign_name,
                        adset_name: i.adset_name,
                        marketr_index: i.marketr_index
                    }))
                }
                

                if (data.ranged_ads.search) {
                    data.ranged_ads.search.map(ad=>{
                        group_ranged_ads(ad)
                    })
                }
                if (data.ranged_ads.social) {
                    data.ranged_ads.social.map(ad=>{
                        group_ranged_ads(ad)
                    })
                }




                const group_ads = i => {
                    let id = i.id == undefined ? i['adid'] : i['id']
                        
                    let name = i.ad_name == undefined || 0 ? id : i.ad_name
                    let creative;

                    if (i.id == undefined) {
                        creative = {
                            headline: `${i.headline1} | ${i.headline2}`,
                            description: i.description,
                            url: i.finalurl,
                            imageadurl: i.imageadurl
                        }
                    } else {
                        creative = {
                            thumbnail: i.thumbnail_url,
                            body: i.body
                        }

                    }

                    ads = [...ads, ads_struct(i, id, name, creative)]

                }

                if (data.ads.search) {
                    data.ads.search.map(ad=>{
                        group_ads(ad)
                    })
                }
                if (data.ads.social) {
                    data.ads.social.map(ad=>{
                        group_ads(ad)
                    })
                }

                this.sub_filters = sub_filters
                
                let _copied_ads = ranged_ads.filter(x=>x.name == this.state.active_sub_view)
                let copied_ads;

                if (_copied_ads.length == 0) copied_ads = ranged_ads.filter(x=>x.id == this.state.active_sub_view)
                else copied_ads = _copied_ads

                let _breakdown_ads = ads.filter(x=>x.name == this.state.active_sub_view)
                let breakdown_ads;

                if (_breakdown_ads.length == 0) {
                    try {
                        breakdown_ads = ads.filter(x=>x.id === this.state.active_sub_view)
                    } catch (error) {
                        console.log(error)
                        breakdown_ads = _breakdown_ads
                    }   
                } else {
                    breakdown_ads = _breakdown_ads
                }

                this.state.breakdown = breakdown_ads[0]

                this.state.active_data.profitability = {
                    dates: copied_ads.map(_camp=>_camp.date_start),
                    pp100: copied_ads.map(_camp=>_camp.pp100),
                    cpm: copied_ads.map(_camp=>_camp.cpm),
                    marketr_index: copied_ads.map(_camp=>_camp.marketr_index).reduce((sum, value) => sum + value, 0 / copied_ads.map(_camp=>_camp.marketr_index).length),
                    action: copied_ads.map(i=>i.action)[copied_ads.map(i=>i.action).length - 1],
                    cost: copied_ads.map(i=>i.cost).reduce((a, b) => a + b, 0)
                }
                break
        }
    }

    select_date_range(){
        let back = document.querySelector('#date_popup_back')
        back.style.display = 'flex'
        back.onclick = e => {
            if (e.target.id == 'date_popup_back') e.currentTarget.style.display = 'none'
        }
        
        const ranger = new NanocalRanger({ target: document.getElementById('ranger') })
        ranger.on('selectedRange', ([start, end]) => {
            const close = () => back.style.display = 'none'
            const apply = document.querySelector('#apply_date')
            const cancel = document.querySelector('#cancel_date')

            apply.style.display = 'flex'
            cancel.style.display = 'flex'

            apply.addEventListener('click', e=>{
                this.start_date_1 = `${start.year}-${start.month}-${start.day} 00:00:00 UTC`
                this.end_date_1 = `${end.year}-${end.month}-${end.day} 00:00:00 UTC`
                
                this.render()
                close()
            })
            cancel.addEventListener('click', e=> close() )
        })
    }

    reset_sub_view(value){
        this.sub_edited = true
        const first = async () => this.state.active_sub_view = value
        first().then(()=>this.data_controller()).then(() => {
            setTimeout(()=>{
                this.render(false)
            }, 200)
        })
    }

    view_controller(el, error=false){
        if (!error) {
            el.querySelectorAll('#view_selector button').forEach(el=>{
                el.addEventListener('click', e => {
                    let target = e.currentTarget
                    target.classList.remove('btn-outline')
                    target.classList.remove('btn-outline-secondary')
                    target.classList.add('btn-secondary')

                    this.sub_edited = !this.sub_edited ? false : true
                    const first = async () => {
                        this.state.active_view = parseInt(target.value)
                    } 
                    first().then(()=>this.data_controller()).then(()=>{
                        setTimeout(()=>{
                            this.render(false)
                        }, 600)
                    })
                })
            })
        }

        el.querySelector('#select_date_range').addEventListener('click', e=> this.select_date_range() )


        return el
    }

    mas_campaigns_cta() {
        return `
        <div class="center_it"> 
        <br><br>
            <h1 style="margin-bottom:0;" class="widget__title">Is there a campaign type you want to run, but we don't offer (yet)?</h1>
            <p class="small_txt">Head over to chat and tell your Market(r) guide and we'll add it to our list.</p>
            <a href="${!this.demo ? '/home?view=messages' : '#'}" class="btn btn-outline btn-outline-secondary">Tell us</a>
        </div>
        `
    }

    breakdown_markup(){
        let markup;
        let data = this.state.breakdown
        let {active_view} = this.state
        
        if (!data) this.data_controller()

        const row = (index, description, description_sub, cost) => {
            let third_sub = {
                0: `<p style="font-size:8pt;">total spent</p>`,
                1: `<p style="font-size:8pt;">total spent</p>`,
                2: `<p style="font-size:8pt;">cost per<br>conversion</p>`,
                3: ``
            }
            /*html*/
            return`
                <li class="stat-wrapper">
                    <div class="stat">
                        ${marketr_score(index, true)}
                        <br>
                        <span>${description}<br> <p style="font-size: 8pt;">${description_sub}</p></span>
                        <h3 style="text-align:right;">
                            ${currency(cost)}
                            ${third_sub[active_view]}
                        </h3>
                    </div>
                </li>
            `
        } 

        const meta = (index, perc_change, condensed=false) => {
            let third_sub = {
                0: `<p style="font-size:8pt;">total spent</p>`,
                1: `<p style="font-size:8pt;">total spent</p>`,
                2: `<p style="font-size:8pt;">total spent</p>`,
                3: ``
            }
            let up = `<i class="fas direction_icons good_direction fa-arrow-circle-up"></i>`
            let down = `<i class="fas direction_icons bad_direction fa-arrow-circle-down"></i>`
            /*html*/
            return`
                <div class="center_vertically ${condensed ? 'condensed' : '' }">
                    <div class="center_it">
                        ${title('health score', true)}
                        ${marketr_score(index, false, true)}
                    </div>
                    
                    <div class="center_it stat-trend up green">
                        ${perc_change > 0 ? up : down }
                        <p class="center_it"><span class="${perc_change > 0 ? '_green' : '_red'}">${number_rounded(perc_change * 100)}%</span> in past 7 days</p>
                    </div>
                </div>
                
                
            `
        } 

        
        switch(this.state.active_view) {
            case 0:
                /*html*/
                markup = `
                ${data.map(_row=>{
                    return row(_row.index, _row.type, 'campaign type', _row.cost)
                }).join('')}
                
                `

                if (data.length < 3) markup += this.mas_campaigns_cta()

                break
            case 1:
                
                /*html*/
                markup = `
                ${data.map(_row=>{
                    return meta(_row.marketr_index, _row.perc_change)
                }).join("")}
                `
                
                break
            case 2:
                /*html*/
                markup = `
                ${data.map(_row=>{
                    return meta(_row.marketr_index, _row.perc_change)
                }).join("")}
                `
                break
            case 3:
                let is_search;
                let is_social;

                if (data) {
                    is_search = data.creative.headline == undefined ? false : true;
                    is_social = data.creative.headline == undefined ? true : false;
                }
                markup = meta(data.marketr_index, data.perc_change, true) + `<div class='separator'></div>`

                if (is_search) {
                    if (data.creative.headline != '0 | 0') {
                        markup += google(
                            data.creative.headline,
                            JSON.parse(data.creative.url)[0],
                            data.creative.description
                        )
                    } else {
                        
                        markup += facebook('', data.creative.imageadurl, '')
                    }
                }

                else if (is_social) markup +=  `
                    <div class="center_it">${modal_trigger('view_creative', 'view creative')}</div>
                    ${modal('', facebook('', data.creative.thumbnail, data.creative.body), 'view_creative')}
                `

                break
        }
        return markup
    }

    date_range(){
        /*html*/
        return `
            <button id="select_date_range" class="btn btn-outline btn-outline-secondary">
                <span>${this.start_date_1.slice(0, -13)} <i class="far fa-caret-square-down"></i></span>
                / <span>${this.end_date_1.slice(0, -13)} <i class="far fa-caret-square-down"></i></span>
            </button>
        `
    }

    comparison_markup(){
  
        let breakdown;
        try {
            breakdown = this.state.breakdown[0] == undefined ? this.state.breakdown : this.state.breakdown[0]
        } catch (error) {
            console.log(error)
            this.abort()
        }
        let {cost, cost_comp, pp100, pp100_comp, marketr_index, index_comp, cpl_comp, conversions} = breakdown
        let cpl = conversions > 0 ? cost / conversions : null
        
        const perc_variance = (_value, low_is_good=false) => {
            let value = !isNaN(_value) ? parseFloat(_value) : 'n/a'
            let green = '_green'
            let red = '_red'
            let color;
        
            if (value > 0) {
                if (low_is_good == true) color = red
                else if (low_is_good == false) color = green
            } else if (value < 0) {
                if (low_is_good == false) color = red
                else if (low_is_good == true) color = green
            } else if (value == 0) color = 'rgba(0,0,0,.3)'
            
            if (low_is_good == null) color = 'rgba(0,0,0,.3)'
            return color
        }

        const comparison_row = (_title, _value, perc) => {
            let {__title} = _title,
                {__value, _currency, score} = _value,
                {comp, low_is_good} = perc

            let display_value;
            if (_currency) display_value = value(currency(__value))
            else if (score) display_value = marketr_score(__value)
            else display_value = value(number_rounded(__value))


            /*html*/
            return `
            <div class="">
                <div style="height:25%;" class="comparison_row row">
                    <div class="center__widget col-lg-6 col-md-6 col-sm-6 col-6">
                        <h1 class="widget__title">${__title}</h1>
                    </div>
                    <div style="text-align:right;" class="center__widget col-lg-6 col-md-6 col-sm-6 col-6">
                        ${display_value}
                        <p style="margin-bottom: 0;font-size: 8pt;">
                            <span class="${perc_variance(comp, low_is_good)}">${comp > 1 ? "+" : ""}${number_rounded(comp)}%</span>
                            vs. campaign avg.
                        </p>
                    </div>
                </div>
            </div>
            `
        }

        const el = /*html*/ `
            ${comparison_row(
                {__title: 'health score'},
                {__value: marketr_index ? marketr_index : 0, _currency: false, score: true},
                {comp: index_comp ? index_comp : 0, low_is_good: false}
            )}
            ${comparison_row(
                {__title: 'spend over<br>time period'},
                {__value: cost ? cost : 0, _currency: true, score: false},
                {comp: cost_comp ? cost_comp : 0, low_is_good: null}
            )}
            ${comparison_row(
                {__title: 'conversion cost'},
                {__value: cpl ? cpl : 0, _currency: true, score: false},
                {comp: cpl_comp ? cpl_comp : 0, low_is_good: true}
            )}
            ${comparison_row(
                {__title: 'profit potential per $100 spent'},
                {__value: pp100 ? pp100 : 0, _currency: true, score: false},
                {comp: pp100_comp ? pp100_comp : 0, low_is_good: false}
            )}
            `

        return el
    }

    profit_spread() {
        return `
            <div id="profit_chart_container">
                <canvas style="width: 100%; height: 100%;" id="profit_chart"></canvas>
            </div>
        `
    }

    summary() {
        let company_index = this.state.data.aggregate.index
        let {marketr_index, action, cost} = this.state.active_data.profitability
        let meta_map = {
            0: '',
            1: 'platform',
            2: 'campaign',
            3: 'ad'
        }
        let {active_view} = this.state
        return  `
            <div class="card card-body">
                <div class="row row_cancel">
                    
                    <div style="display: ${active_view != 0 ? 'auto' : 'none'};" class="col-lg-6 col-md-6 col-sm-12">
                        ${title(`${meta_map[active_view]}<br>Health score`)}
                        ${value(number(marketr_index ? marketr_index : 0))}
                    </div>
        
                    <div class="col-lg-6 col-md-6 col-sm-12">
                        ${title('company<br>health score')}
                        ${value(number(company_index ? company_index : 0))}
                    </div>

                </div>
            </div>`
    }

    opps_classList(){
        let opps_classList;

        if (this.analytics) opps_classList = `col-lg-4 col-md-4 col-sm-12`
        if (this.state.opp_expanded) opps_classList = `h--750 col-lg-12 col-md-12 col-sm-12`
        else opps_classList = `col-lg-4 col-md-4 col-sm-12`

        return opps_classList
    }

    opps_title(){
        let closed = `<i class="far fa-caret-square-right"></i>`,
            open = `<i class="far fa-caret-square-down"></i>`,
            expanded = this.state.opp_expanded;

        /*html*/
        return `
        <h1 style="margin-bottom: 1em;" class="widget__title">
            Opportunities
            <button style="padding: 0;margin: 0 0 0 7px;" id="opp_expand" class="btn btn-neutral small_txt">
                Nerd view
                ${expanded ? open : closed}
            </button>
        </h1>
    `
    }

    opps_container(){
        let el = document.createElement('div')

        if (this.state.opp_expanded) this.shadow.querySelector("#opps_container").style.margin = "0 0 2em 0"
        /*html*/
        el.innerHTML = `
            <div class="h--700 mobile--h--700 card card-body" id="topic_opps">
                ${this.opps_title()}
                <div id="append__to"></div>
            </div>
        `

        let opp = this.Opportunities()
        opp.setAttribute('json', JSON.stringify(this.state.data.topics))
        el.querySelector('#append__to').appendChild(opp)

        el.querySelector("#opp_expand").addEventListener('click', e=>{
            this.state.opp_expanded = this.state.opp_expanded ? false : true
            let target = this.shadow.querySelector("#opps_container")
            target.classList.remove(...target.classList)
            target.classList.add(...this.opps_classList().split(" "))
            this.shadow.querySelector('#opps_container').innerHTML = ""
            this.shadow.querySelector('#opps_container').appendChild(this.opps_container())
        })

        return el
    }

    template(){
        let {action} = this.state.active_data.profitability
        let {active_view} = this.state


        let breakdown_title = {
            0: 'active platforms',
            1: 'campaign breakdown',
            2: 'ad group breakdown',
            3: 'ad breakdown'
        }

        let recommendation_map = {
            'middle of the pack': 'middle of the pack',
            'invest more': `You've found a winner! Figure out what's succeeding with this campaign and replicate it. Make use of the intel tab. If you need some inspiration, just reach out to your Market(r) guide in the chat!`,
            'kill it': `They can't all be winners, unfortunately. We recommend cutting bait on this one, analyzing to see what didn't work, and learning for next time.`
        }
        let class_list = `col`
        let column_set = ![0].includes(active_view) ? 'col-lg-6 col-md-6 col-sm-12' : 'col-lg-12 col-md-12 col-sm-12'
        /*html*/
        return `

        <div class="row row_cancel">
            <div style="${this.state.opp_expanded ? 'margin-bottom: 2em;' : ""}" class="${this.opps_classList()}" id="opps_container">
            </div>

            ${this.analytics ? `` : /*html*/ `
                <div id="recommendations" class="col-lg-4 col-md-4 col-sm-12">
                    <div class="h--500 card card-body">
                        <h1 class="widget__title">Recommendations</h1>
                    </div>
                </div>
                
                <div class="col-lg-4 col-md-4 col-sm-12">
                   <!-- <div class="d-none d-md-block d-lg-none divider"></div>-->
                    <div id="insights" class="card card-responsive card-body">
                        ${title('insights')}    
                    </div>
                </div>`
            }
        </div>


        <div class="row row_cancel">
      
            <div class="col-lg-6 col-md-6 col-12">
                ${this.view_by()}
            </div>
            <div class="col-lg-6 col-md-6 col-12">
                <div class="card card-body mobile--h--225 h--300">
                    <div class="row row_cancel">
                        ${
                            this.state.active_view != 0
                            /*html*/
                            ? `
                            <div class="col-lg-6 col-sm-6">
                                ${title('filter by', true)}
                                <div id="sub_target"></div>
          <!--                      <select id="sub_target" class="form-control">
                                    ${ !this.state.null_data
                                        ?
                                            this.sub_filters.map((filter, index)=>{
                                                /*html*/
                                                return (
                                                    `<option value="${filter}" ${filter == this.state.active_sub_view  ? `selected` : '' }>
                                                        ${filter}
                                                    </option>
                                                    `
                                                )
                                            }).join('')
                                        : `<option></option>`
                                }
                                </select> -->
                            </div>`
                            : `<select id="sub_target" style="display:none;" class="form-control"></select>`
                        }
                        <div class="${this.state.active_view != 0 ? "col-lg-6 col-sm-6" : "col-lg-9 col-sm-9"}">
                            ${title(`Select dates`, true)}
                            ${this.date_range()}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row row_cancel">
            <div class="col-lg-8 col-md-8 col-sm-12">
                <div class="row">
                    <div class="${column_set}">
                        <div style="overflow-y:auto;" class="h--500 mobile--h--cancel card card-body">
                            ${title(breakdown_title[active_view])}
                            ${ !this.state.null_data
                                ?
                                    this.breakdown_markup()
                                :
                                    `${this.null_state()}`
                            }
                        </div>
                    </div>
                    ${
                        ![0].includes(active_view)
                            ? `
                            <div class="col-lg-6 col-md-6 col-sm-12">
                                <div style="overflow-y:auto;" class="h--500 mobile--h--600 card card-body">
                                    <!--${title(`Our recommendation: &nbsp;<span class="action">${action ? action : ""}</span>`)}-->
                                    ${ !this.state.null_data
                                        ?
                                            this.comparison_markup()
                                        :
                                            `${this.null_state()}`
                                    }
                                </div>
                            </div>`
                            : ''
                        }
                </div>
            </div>

            <div class="h--500 col-lg-4 col-md-6 col-sm-12">
                <div class="h--500 card card-body">
                    ${title('profit potential per $100 spent')}
                    <br>
                    ${ !this.state.null_data
                        ?
                            this.profit_spread()
                        :
                            `${this.null_state()}`
                    }

                </div>
            </div>
            ${this.analytics ? `

            <div style="${this.state.opp_expanded ? 'margin-bottom: 2em;' : ""}" class="${this.opps_classList()}" id="opps_container"></div>
            
            ` : ''}

        </div>
        `
    }

    shell(){
        /*html*/
        return `
            <div style="padding-left: 0; padding-right: 0;" class="container-fluid">
                <div id="info_bar" class="row row_cancel">
                    ${this.analytics ? ''
                    : /*html*/`

                        <div class="row row_cancel">
                            <div class="align-self-center col-lg-6 col-md-6 col-sm-6 col-6"> 
                                <div class="row row_cancel">
                                    <div class="align-self-center col-lg-6 col-md-6 col-sm-6 col-6">
                                        ${marketr_score(
                                            this.state.data ? this.state.data.aggregate.index : 0
                                        )}
                                    </div>
                                    <div class="align-self-center col-lg-6 col-md-6 col-sm-6 col-6">
                                        <p style="white-space:nowrap;">${this.company_name}'s<br>Health score</p>
                                    </div>
                                </div>
                            </div>
                            <div class="align-self-center col-lg-6 col-md-6 col-sm-6 col-6">
                                <div class="row row_cancel">
                                    <div class="align-self-center col-lg-3 col-md-3 col-sm-3 col-3">
                                        <i class="fas fa-dollar-sign"></i>
                                    </div>
                                    <div class="align-self-center col-lg-9 col-md-9 col-sm-9 col-9">
                                        <p style="margin-bottom: 0;">
                                            <strong>${currency_rounded(this.funds_remaining ? this.funds_remaining : 0)}</strong>&nbsp;
                                            remaining
                                        </p>
                                        <p><strong>${currency_rounded(this.spend_rate ? this.spend_rate : 0)}</strong>/mo budget</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                    `
                    }
                    
                </div>
                
                </div>
            </div>

            <div style="padding-left: 0; padding-right: 0;" class="container-fluid" id="home-row">
            </div>
           
        `
    }

    recs(){
        const recs_ = new Recommendations()
        recs_.setAttribute('customer-id', this.customer_id)
        recs_.setAttribute('demo', this.demo)
        recs_.setAttribute('recs_json', this.recs_json)
        recs_.setAttribute('fetch', false)
        return recs_
    }

    Filter(){

        const filter = new Filter()
        filter.setAttribute('sub_list', JSON.stringify(this.sub_filters))
        filter.setAttribute('active_sub_view', this.state.active_sub_view)
        filter.setAttribute('active_view', this.state.active_view)

        this.filter_observer.observe(filter, {
            attributes: true
        });

        return filter
    }

    insights(){
        const insights = new Insights()
        insights.setAttribute('customer_id', this.customer_id)
        insights.setAttribute('insights_json', this.insights_json)
        insights.setAttribute('fetch', false)
        return insights
    }


    Opportunities(){
        const ops = new Opportunities()
        ops.setAttribute('max-height', '383')
        ops.setAttribute('expanded', this.state.opp_expanded)
        return ops
    }

    null_state(){
        return `<p>no data available</p>`
    }

    error_markup(){
        /*html*/
        const div = `
        <div class="row row_cancel">
            <div class="col-lg-12 col-md-12 col-sm-12">
                <div class="center_it card card-body">
                    <p style="margin: auto;">There's no data for this time period.</p>
                    <p class="small_txt" style="margin: auto;">Either your data hasn't finished syncing yet or your looking at a timeframe where you didn't have any data.</p>
                    ${this.date_range()}
                </div>
            </div>
        </div>
        <div class="row row_cancel">
            <div id="recommendations" class="col-lg-6 col-md-6 col-sm-12">
                <div class="h--500 card card-body">
                    ${title('Recommendations')}  
                </div>
            </div>

            <div class="col-lg-6 col-md-6 col-sm-12">
                <div id="insights" class="card card-responsive card-body">
                    ${title('insights')}    
                </div>
            </div>
        </div>
        `
        return div
    }

    view_by(){
        let btn_length = `col-lg-3 col-md-3 col-sm-3`
        let {active_view} = this.state
        let active_classlist = `btn-secondary`
        let inactive_classlist = `btn-outline btn-outline-secondary`
        /*html*/
        return `
        <div class="h--300 mobile--h--225 card card-body">
            <div class="row row_cancel">
                <div id="select_container" class="col-lg-12">
                    ${title('view by', true)}
                    <div id="view_selector" class="h--300 row row_cancel">
                        <div class="${btn_length}">
                            <button value="0" class="btn ${active_view == 0 ? active_classlist : inactive_classlist}">
                            platforms
                            </button>
                        </div>
                        <div class="${btn_length}">
                            <button value="1" class="btn ${active_view == 1 ? active_classlist : inactive_classlist}">
                            campaigns
                            </button>
                        </div>
                        <div class="${btn_length}">
                            <button value="2" class="btn ${active_view == 2 ? active_classlist : inactive_classlist}">
                            ad groups
                            </button>
                        </div>
                        <div class="${btn_length}">
                            <button value="3" class="btn ${active_view == 3 ? active_classlist : inactive_classlist}">
                            ads
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `
    }

    render(init=true){
        this.shadow.innerHTML = ""

        const recs = this.recs()
        const insights = this.insights()
        const opps = this.Opportunities()

        const append_other = el => {
            if (!this.analytics) {
                el.querySelector("#recommendations div").appendChild(recs)
                el.querySelector('#insights').appendChild(insights)
            }
            
            if (this.state.active_view > 0) el.querySelector('#sub_target').appendChild(this.Filter())
        }

        const compile = async () => {
            let el;
            const markup = `
                ${this.css}
                ${this.shell()}
            `
            el = document.createElement('div')
            el.innerHTML = markup
            if (this.state.active_view > 0 && !this.sub_edited) this.state.active_sub_view = this.sub_filters[0].key
            if (!this.state.null_data) this.data_controller()

            return el
        } 

        const run = () => {
            this.shadow.innerHTML = ""
            compile()
                .then(el=>{
                    el.querySelector('#home-row').innerHTML += this.template()
                    return el
                })
                .then(el=>{
                    if (!this.state.null_data) this.reset_charts(el)
                    el.querySelector('#opps_container').appendChild(this.opps_container())

                    append_other(el)
                    return modal_handlers(el)
                })
                .then( el => this.shadow.appendChild(this.view_controller(el)) )
                .then(() => document.querySelector('#performance_loader').style.display = 'none')
 
        }


        if (init == true) {
            document.querySelector('#performance_loader').style.display = 'block'
            fetch('/api/index/detailed', {
                method: 'POST',
                headers : new Headers({
                    "content-type": "application/json"
                }),
                body:  JSON.stringify({
                    customer_id: this.customer_id,
                    company_name: this.customer_id == 200 ? "o3" : this.company_name,
                    ltv: this.ltv,
                    start_date_1: this.start_date_1,
                    end_date_1: this.end_date_1,
                    facebook: this.facebook_id,
                    google: this.google_id
                })
            })
            .then(res => res.json())
            .then(res => {
                if (res.index) {
                    this.state.null_data = false
                    this.state.data = res.index
                    this.state.data.topics = res.topics ? res.topics : null
                } else this.state.null_data = true

                opps.setAttribute('json', JSON.stringify(res.topics))
                run()
                
            })
            .catch(e=>{
                console.log(e)
                document.querySelector('#performance_loader').style.display = 'none'
                this.shadow.innerHTML = `
                    ${this.css}
                    ${this.error_markup()}
                `
                append_other(this.shadow)
                this.view_controller(this.shadow, true)
            })
        } else run()
    }

    attributeChangedCallback(name, oldValue, newValue){
        switch(name){
            case 'start_date_1':
            case 'end_date_1':
            case 'start_date_2':
            case 'end_date_2':
                console.log(newValue)
                break
        }
    }

    connectedCallback() {
        this.customer_id = this.getAttribute('customer-id')
        this.facebook_id = this.getAttribute('facebook_id') ? true : false
        this.google_id = this.getAttribute('google_id') ? true : false
        this.company_name = this.getAttribute('company-name')
        this.spend_rate = this.getAttribute('spend_rate') != null ? parseFloat(this.getAttribute('spend_rate')) : 0
        this.funds_remaining = this.getAttribute('funds_remaining') != null ? parseFloat(this.getAttribute('funds_remaining')) : 0
        this.insights_json = this.getAttribute('insights')
        this.recs_json = this.getAttribute('recommendations')
        this.ltv = this.getAttribute('ltv')
        this.demo = this.getAttribute('demo')
        this.analytics = this.getAttribute('analytics') ? true : false

        const today = new Date()
        this.start_date_1 = this.getAttribute('start_date_1')
                                ? this.getAttribute('start_date_1')
                                : `${today.getFullYear()}-${today.getMonth()}-${today.getDate()} 00:00:00 UTC`

        this.end_date_1 = this.getAttribute('end_date_1')
                            ? this.getAttribute('end_date_1')
                            : `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()} 00:00:00 UTC`

        this.render()

    }
}
  
document.addEventListener( 'DOMContentLoaded', customElements.define('portfolio-performance', PortfolioPerformance))

