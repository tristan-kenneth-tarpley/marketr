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