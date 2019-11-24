export default class CampaignViewModel {
    constructor(){
        this.params = params()
        
        document.querySelectorAll('.campaign_controller').forEach(el=>{
            el.addEventListener('click', e=>{
                this.hide_root()
            })
        })
        document.querySelector('#new_campaign').addEventListener('click', e=>{
            setQueryString('campaign_view', 'new')
            this.show_new()
        })
        document.querySelector('#existing').addEventListener('click', e=>{
            setQueryString('campaign_view', 'existing')
            this.show_existing()
        })
    }

    show_new(){
        $(".views").not('#new').addClass('hidden')
        $("#new").removeClass('hidden')
    }

    show_existing(){
        $(".views").not('#existing_view').addClass('hidden')
        $("#existing_view").removeClass('hidden')
    }

    hide_root(){
        document.querySelector("#root").classList.add('hidden')
    }

    run(){
        if (this.params.has('campaign_view')){
            this.hide_root()
            switch(this.params.get('campaign_view')){
                case 'new':
                    this.show_new()
                    break
                case 'existing':
                    this.show_existing()
                    break
            }
        }
    }
}