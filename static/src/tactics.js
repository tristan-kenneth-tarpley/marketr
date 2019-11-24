import {TacticService} from './services.js'

export default class Tactics {
    constructor(params){
        this.mount = document.querySelector('#tactics_mount')
        this.loading = document.querySelector('.tactics_loading')

        const render = document.querySelectorAll('.render_tactics')
        if (params.has('view') && params.get('view') == 'campaigns') {
            this.render()
        } else {
            render.forEach(el=>{
                el.addEventListener('click', e=>{
                    if (this.mount.innerHTML == ""){
                        this.render()
                    }
                })
            })
        }
    }

    render(){
        fetch('/api/tactic_of_day')
        .then(res=>res.text())
        .then(res=>{
            this.loading.style.display = 'none'
            this.mount.innerHTML = res
            const tactics = new TacticService()
            
            $("#add_tactic").click(e=>{
                const target = e.currentTarget
                const title = $(target).siblings('#tactic_title').text()
                tactics.add_tactic(target.value, title)
            })
        })
        .catch(e=>{
            console.log(e)
        })
    }
}