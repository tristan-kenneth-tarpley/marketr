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
        <div class="center_it">
            <img class="fb_graphics" style="width:30%;" src="${img}">
        </div>
        <div style="width:70%;margin: 0 auto;">
            <p style="font-size: 80%;">${copy}</p>
        </div>
        `
    )
}

export const right_modal = (title, body, uid) => {
    /*html*/
    return (
        `
    <div data-uid="${uid}" id="modal-container">
        <div class="modal-background">
            <div class="_right safe modal">
                <h2>${title}</h2>
                <p>${body}</p>
            </div>
        </div>
    </div>`
    )
}

export const inline_article = (type) => {
    const article = (title, description, why, example) => {
        /*html*/
        return (
            `<h5 class="widget__title"><strong>Campaign:</strong>  ${title}</h5>
            <p><strong>Description:</strong> ${description}</p>
            <br>
            <p><strong>Why is this important?:</strong> ${why}</p>
            <br>
            <p><strong>Example campaign setup:</strong></p>
            <p class="inset">${example}</p>
            `
        )
    }

    const map = {
        'Activity-based': article(
            'Activity-based',
            'Activity-based campaigns will be targeting the users who are searching to DO something.  They may be searching using phrases like:  How do I... Where can I find... How should I... When can I...',
            `The user clearly has a need, and if your product or service can help solve that need, then you can best serve them by making your ad accessible to them. 
            `,
            `Keywords:  How do I slice a banana, How can I slice a banana, How should I slice a banana.<br>   
            Headline 1:  How To Slice Bananas?<br>
            Headline 2:  Look Like A Pro W/ BanaSlice!<br>
            Headline 3:  Order Today To Get Before Xmas<br>
            Display URL:  BanaSlice.com/how-to-slice/bananas<br>
            Description 1:  Stop Worrying About How You Can Slice Bananas.  BanaSlice Makes It Easy!<br>
            Description 2:  Easy Setup, Easy Clean Up.  Become The Envy Of Your Guests With This High Quality Slicer!
            `
        ),
        'Product / service': article(
            'Product / service',
            'Campaigns that focus on what services your business offers or what products you sell. These campaigns will target consumers who tend to use specific, long-tail keyword phrases into search bars.',
            'People who use specific, long-tail keywords know exactly what type of product or service they’re looking for, which means they have an intent to purchase or learn more about the product or services.',
            `Keywords:  Organic carpet cleaning services, Green carpet cleaning company, Eco-friendly carpet cleaning services.<br> 
            Headline 1:  Organic Carpet Cleaning Services<br> 
            Headline 2:  Gentle on Carpets and on Mother Nature<br> 
            Headline 3:  No Harmful Cleaning Agents Used<br> 
            Display URL:  carpetcleaningexperts.com/organic-carpet-cleaning<br> 
            Description 1: Chemical cleaning agents are not only harsh on the environment, they can harm your pet and kids.<br> 
            Description 2:  100% Organic Carpet Cleaning Services. Environmental-friendly and safe. Perfect for delicate carpets.<br> 
            `
        ),
        'Your brand(s)': article(
            'Your brand(s)',
            'You want these ads shown to anyone who is specifically typing your brand(s) into the search bar.  Create separate groups for your general brand and various product / service brands or trademarks.',
            'These are highly-interested searchers who are already looking for you.  Make sure your brand is front and center and they’re not distracted with competitor ads or related offerings.  It’s usually fairly low-cost to rank for your own brand, but it’s absolutely worth it, even if you’re the top organic search result.',
            `Keywords:  BanaSlice<br>
            Headline 1:  BanaSlice Slices Like a Pro<br>
            Headline 2:  Any Banana Anytime<br>
            Headline 3:  Order Today To Get Before Xmas<br>
            Display URL:  BanaSlice.com/slice/bananas<br>
            Description 1:  Stop Worrying About How You Can Slice Bananas.  BanaSlice Makes It Easy!<br>
            Description 2:  Easy Setup, Easy Clean Up.  Become The Envy Of Your Guests With This High Quality Slicer!
            `
        ),
        'Direct competitor brand(s)': article(
            'Direct competitor brand(s)',
            'You want these ads shown to people who are searching for solutions that you solve, but may only be familiar with your competitor brands.  Create separate groups for various competitors.  Tip:  Do NOT include the brand name in your headline or ad copy, using brand names you do not own can get your ad to be disapproved.',
            `These are highly-interested searchers who are already looking for the solution you solve for.  This helps the customer by making sure they’re aware of your competitive (and hopefully better fit) offering that they otherwise may not be aware of.  You will usually pay a premium for these ads, however if done right and paired with relevant landing pages, they can be very successful in attracting people who are interested in your solutions.`,
            `Keywords:  Banana Dicer 3000, 
            Headline 1:  BanaSlice Slices Like a Pro
            Headline 2:  Any Banana Anytime
            Headline 3:  Half The Price
            Display URL:  BanaSlice.com/slice/bananas
            Description 1:  Voted “Best Value Banana Slicer”. BanaSlice Makes It Easy!
            Description 2:  Slice Better Bananas For Half The Price Of The Competition.
            `
        ),
        'Retargeting': article(
            'Retargeting',
            'These campaigns target users who have performed specific actions in the past that expressed interest for the product or service. This could be anything from visiting the company’s website, to liking and following their social media pages.',
            'These users have already expressed interest in the product or service before. By showing up on their search results, it encourages name retention and gives users more chances to purchase your product or service.',
            `Audience: Users who have visited the website, watched our videos or liked/followed your social media accounts.<br>
            Headline 1:  Veteran Criminal Defense Lawyers<br>
            Headline 2:  30+ Years of Not Guilty Verdicts<br>
            Headline 3:  Consultation is 100% Free<br>
            Display URL:  veteranlawyers.com/criminal_defense<br>
            Description 1: Successful track record of “Not Guilty” and “Dismissed” Cases.<br>
            Description 2:  Call us today for your free consultation
            `
        ),
        'LinkedIn role-focused': article(
            'LinkedIn role-focused',
            'Linkedin campaigns that target people that fit a certain profile of your target audience. These can be based on particular industry, job title, and geography.  Mainly used for business-to-business (B2B). This strategy is used to sell products to professionals or businesses in relevant fields.',
            'Linkedin is where many business professionals go for work-related updates, news, and connections.  Having your ads presented while these highly targeted individuals are in that mindset can prove to be very powerful for businesses.',
            `Audience: copy-writers, sales leaders, sales managers, marketing managers
            Description: An email is never just an email - many companies get rejected because of typographical errors and grammar slips. Write professional and concise pieces for web content, email campaigns and other correspondence with our easy-to-use word processing and editing software. Order yours today.
            `
        ),
        'LinkedIn retargeting display': article(
            'LinkedIn retargeting display',
            `Linkedin display ads that target people who expressed interest in the company before - for example, people who already visited your company website. As opposed to text campaigns, display campaigns make use of graphics and banners to provide visually enticing advertising.`,
            `With the number of users Linkedin has, it’s not impossible to find previous website visitors on the platform. And since most advertisers target platforms like Facebook for their retargeting campaign, Linkedin’s retargeting campaign sphere isn’t as competitive. Display ads are used instead of pure text ads because they are more eye-catching.`,
            `Audience: Previous site visitors<br>
            Description: Still using ordinary soap and shampoo for your fur babies? Switch to our gentle formula design specially for your pets! (SInce this is a display ad, keep it short and sweet)
            `
        ),
        'Facebook demographic targeting': article(
            'Facebook demographic targeting',
            `Facebook has a targeting feature that allows you to narrow down your audience by several factors including location, age, job title, hobbies and more.`,
            `Ads without demographic targeting may get you a lot of impressions, but it won’t deliver conversions. Campaigns may end up being too expensive since people outside your target market will click on your ads. By applying demographic targeting, you ensure that only people who need the product or service you’re offering will see the ad.`,
            `Keywords: early kids reading program, advanced reading program for kids<br>
            Audience: Mothers of young children, Preschool teachers<br>
            Description: Do you know that almost half of kids struggle when learning to read! There’s no shame in finding new and advanced ways to make reading easier and more fun for kids! We use the latest teaching strategies coupled with a fun, interactive environment to motivate kids and help them enjoy reading!<br>
            Headline: Help your kids learn how to read today!<br>
            Landing page: <a href="http://www.advancedkidsreading.com/kids-reading-program" target="__blank">http://www.advancedkidsreading.com/kids-reading-program</a>
            `
        ),
        'Facebook retargeting display': article(
            'Facebook retargeting display',
            `Facebook campaigns that target users who expressed interest in the product or service in the past either by visiting the website or the company’s Facebook page. Your ads will only appear for audiences who meet this criteria.`,
            `Almost everyone has a Facebook account, so it’s easy to find prior website visitors on the platform. The goal of these ads is to encourage brand retention in hopes that the consumer is now ready to purchase.`,
            `Keywords: convenient banana slicer, automated banana slicer<br>
            Audience: Previous website visitors or FB page visitors.<br>
            Description: People love bananas, but slicing them? Not so much. But with our revolutionary banana slicer, you get clean, even slices with just one pull of the lever. And best of all, no sticky banana residue on your knives!<br>
            Headline: Banana slicing made easy!<br>
            Landing page: BanaSlice.com/
            `
        ),
        'Primary issue(s) + solution content': article(
            'Primary issue(s) + solution content',
            `This type of campaign focuses on a specific target market concern and creates content that offers a solution to this concern or problem.`,
            `Presenting solutions to your consumers’ concerns will help elevate your business and brand you as a subject matter expert. It’s also easier to market your product or service as the solution to the problem this way.`,
            `Keywords:  lock repair 24/7, locksmith available 24/7, on-call locksmith<br>
            Description: An article that helps solve people’s problem with getting locked out of their homes or vehicles outside a regular locksmith’s office hours. The article’s goal is to inform consumers that some locksmiths are on-call and work around the clock<br>
            Meta Title: Solve Your Lock Woes With 24/7 On-Call Locksmith Service<br>
            Meta Description: Find yourself locked out of the house in the wee hours of the morning? Our professional locksmiths are always available 24 hours a day, even on weekends and holidays.
            `
        ),
        'Lead nurturing drip': article(
            `Lead nurturing drip`,
            `This campaign’s goal is to maintain interest from users who have chosen to sign up for promotional emails or rss feeds.`,
            `Consumers who willingly sign up for promotional emails are interested in the product or service, but there’s a blocker. It’s important to maintain a good relationship with these leads as they will most likely purchase once that blocker is removed.`,
            `Sample blocker: Rates too high<br>
            Email Campaign: 30% off on programming summer camps<br>
            Sample Email Content: Summer is almost upon us! Here at KidsCode, we know that programming is one of the fastest growing hobbies among kids and teens. This is why we’re offering 30% off on all our summer camp programs for kids and teens! Just present the code SUMMEROFF30 upon enrolment. Jumpstarting your little one’s interest in coding has never been easier!
            `
        ),
        'Display Retargeting': article(
            'Display Retargeting',
            `These are banner campaigns that make use of lively and colorful graphics as opposed to simple text. These banners show up on ad spaces on websites. This campaign will only target people who have visited the company’s website previously. The company’s ads will show up when searchers visit similar or relevant websites.`,
            `One main reason why some users never come back to a website is simply because they forgot which website they found a particular product/service on. Display advertising on search networks gives companies an opportunity to pique the interest of a user when they visit similar websites.`,
            `Keywords: Banana slicer, revolutionary banana slicer<br>
            Headline 1:  SampleCompany Banana Slicers<br>
            Headline 2:  Various Sizes and Colors<br>
            Headline 3:  Check Our Gallery of Over 50 Designs<br>
            Display URL:  bananaslice.com<br>
            Description: Usually comes with a banner or image
            `
        )
    }
    return map[type] == undefined ? false : map[type]
}

