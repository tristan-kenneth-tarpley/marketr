export const shadow_events = markup => {
    const el = document.createElement('div')
    el.innerHTML = markup

    el.querySelectorAll('.nav-link.tab-link').forEach(tab=>{
        tab.addEventListener('click', e=> {
            const $this = e.currentTarget
            const id = $this.id
            const target = $this.dataset.target
            
            el.querySelectorAll('.nav-link.tab-link').forEach(dirty_code=>{
                if (dirty_code.dataset.group == $this.dataset.group) {
                    dirty_code.id != id
                    ? dirty_code.classList.remove('active')
                    : dirty_code.classList.add('active')
                }
            })

            el.querySelectorAll(".tab-pane").forEach( pane=> {
                if (pane.dataset.group == $this.dataset.group) {
                    if (pane.id == target){
                        pane.classList.add('show')
                        pane.classList.add('active')
                    } else {
                        pane.classList.remove('show')
                        pane.classList.remove('active')
                    }
                }
            })
        })
    })
    return el
}

export const tabs = (labels, content, uid) => {
    /*html*/
    const El = `
    <ul class="nav nav-tabs" id="${uid}myTab" role="tablist">
        ${labels.map((label, index) => {
            /*html*/
            return `
            <li class="nav-item">
                <a class="tab-link nav-link ${index == 0 ? 'active' : ''}" id="${label + uid}-tab" data-target="${label + uid}" data-group="${uid}">${label}</a>
            </li>
            `.trim()
        }).join("")}
    </ul>
    <br>
    <div class="tab-content" id="myTabContent${uid}">
        ${labels.map((label, index) => {
            /*html*/
            return `
            <div data-group="${uid}" class="tab-pane ${index == 0 ? 'show active' : ''}" id="${label + uid}">
                ${content[index]}
            </div>
            `.trim()
        }).join("")}
    </div>
    `.trim()

    return El
}



const dots_loader = () => {
    return `
        <div style="text-align:center;margin: 0 auto;" class="col">
            <div style="margin: 0 auto;" class="loading_dots">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `.trim()
}