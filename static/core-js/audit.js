const BarChart = class {
    constructor(selector, labels, data, legend) {
        this.selector = selector
        this.labels = labels
        this.data = data
        this.legend = legend
    }
    render(){
        const EmotionChartCanvas = document.querySelector(`#${this.selector}`)
        let emotional_chart = new Chart(EmotionChartCanvas, {
            type: 'bar',
            data: {
                labels: this.labels,
                datasets: [{
                    label: this.legend,
                    data: this.data,
                    responsive: true,
                    backgroundColor: [
                        'rgba(202, 125, 102, 0.7)',
                        'rgba(98, 205, 224, 0.7)',
                        'rgba(202, 125, 102, 0.5)',
                        'rgba(98, 205, 224, 0.5)',
                        'rgba(202, 125, 102, 0.3)',
                        'rgba(98, 205, 224, 0.3)'
                    ],
                    borderColor: [
                        'rgba(202, 125, 102, 0.9)',
                        'rgba(98, 205, 224, 0.9)',
                        'rgba(202, 125, 102, 0.7)',
                        'rgba(98, 205, 224, 0.7)',
                        'rgba(202, 125, 102, 0.5)',
                        'rgba(98, 205, 224, 0.5)'
                    ],
                    borderWidth: 1
                }]
            },
            options: { 
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }
}   

const CostEstimator = class {
    constructor(avg_cpc){
        const avg = avg_cpc => (avg_cpc.reduce((a,b) => a + b, 0) / avg_cpc.length).toFixed(2)
        this.avg_cpc = avg(avg_cpc)
    }
    activate(){
        document.querySelector('#avg_cpc').textContent = this.avg_cpc
        const target = document.querySelector('#spend_target')
        let estimate = document.querySelector('#click_est')
        target.addEventListener('keyup', e=>{
            estimate.textContent = '0'
            let value = e.currentTarget.value

            const clicks = (value / this.avg_cpc ).toFixed(0)
            estimate.textContent = clicks
        })
    }
}

const secondary_load_time_check = (load_time) => {
    let load_headline = document.querySelector('#load_headline')
    let load_body = document.querySelector('#load_body')
    if (load_time <= 1) {
        load_headline.textContent = "Wow! Much fast. Very wow."
        load_body.textContent = "Your site's load time is best in class. This can help website conversions by more than 123%! Make sure to keep an eye on this and figure out what other meat you can add to your website to further increase it."
    }
    else if (load_time > 1 && load_time <= 3) {
        load_headline.textContent = "Consider me impressed!"
        load_body.textContent = "The recommended site load time is less than 3 seconds... And guess what... You passed! If you wanted to really go Superman mode, try to get it under 1 second for a 21% reduction in bounce rate."
    }
    else if (load_time > 3 && load_time <= 5) {
        load_headline.textContent = "The site better be good given how long you made us wait!"
        load_body.textContent = "You can decrease the number of users that leave immediately by 32% if your site loaded in less than 3 seconds."
    }
    else if (load_time > 5 && load_time <= 6) {
        load_headline.textContent = "The site better be good given how long you made us wait!"
        load_body.textContent = "You can decrease the number of users that leave immediately by 90% if your site loaded in less than 5 seconds."
    }
    else if (load_time > 6 && load_time <= 10) {
        load_headline.textContent = "Ah! The anticipation was KILLING me."
        load_body.textContent = "You can decrease the number of users that leave immediately by 106% if your site loaded in less than 6 seconds."
    }
    else if (load_time > 10) {
        load_headline.textContent = "Hold on, we're still waiting on... Oh wait. It just loaded."
        load_body.textContent = "You can decrease the number of users that leave immediately by 123% if your site loaded in less than 10 seconds."
    }
}


var canvas;
var canvasWidth;
var ctx;

function init() {
    canvas = document.getElementById('emotion_chart');
    if (canvas.getContext) {
        ctx = canvas.getContext("2d");

        window.addEventListener('resize', resizeCanvas, false);
        window.addEventListener('orientationchange', resizeCanvas, false);
        resizeCanvas();
    }
}

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}