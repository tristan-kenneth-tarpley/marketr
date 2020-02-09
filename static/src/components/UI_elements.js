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

export const tabs = (labels, content, uid, vertical=false) => {
    /*html*/
    const El = `
    ${vertical
        ? `<div class="row"><div class="col-lg-3 col-sm-12">`
        : ''
    }
    <ul class="nav ${vertical ? 'vertical' : ''} nav-tabs" id="${uid}myTab" role="tablist">
        ${labels.map((label, index) => {
            /*html*/
            return `
            <li class="nav-item">
                <a class="tab-link nav-link ${index == 0 ? 'active' : ''}" id="${label + uid}-tab" data-target="${label + uid}" data-group="${uid}">${label}</a>
            </li>
            `.trim()
        }).join("")}
    </ul>

    ${vertical
        ? `</div><div class="col">`
        : '<br>'
    }
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

    ${vertical
        ? `</div></div>`
        : '<br>'
    }
    `.trim()

    return El
}



export const dots_loader = () => {
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

export const google = (headline, website, description) => {
    return (
        `<div style="text-align:left;" class="google_ad_preview_container">
            <h5 style="font-size: 110%;">${headline}</h5>
            <p class="website"><span>Ad</span> ${website}</p>
            <p>${description}</p>
        </div>`
    )
}

export const facebook = (headline, img, copy) => {
    return (
        `
        <img class="fb_graphics" style="width:20%;" src="${img}">
        <p style="font-size: 80%;">${copy}</p>
        `
    )
}


`
<!-- Full Height Modal Right -->
<div class="modal fade right" id="fullHeightModalRight" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"
  aria-hidden="true">

  <!-- Add class .modal-full-height and then add class .modal-right (or other classes from list above) to set a position to the modal -->
  <div class="modal-dialog modal-full-height modal-right" role="document">


    <div class="modal-content">
      <div class="modal-header">
        <h4 class="modal-title w-100" id="myModalLabel">Modal title</h4>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        ...
      </div>
      <div class="modal-footer justify-content-center">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>
<!-- Full Height Modal Right -->
`