export default class Competitors {
    constructor(params){
        this.mount = document.querySelector('#mount_competitors')
        this.loading = document.querySelector('.competitor_loading')

        const render = document.querySelectorAll('.render_competitors')
        if (params.has('view') && params.get('view') == 'competitors') {
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
        fetch('/api/competitive_intel')
            .then(res=>res.text())
            .then(res=>{
                this.loading.style.display = 'none'
                this.mount.innerHTML = res
            })
            .catch(e=>{
                console.log(e)
            })
    }
}