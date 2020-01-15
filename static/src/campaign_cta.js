export default class cta {
    constructor(){
        this.input = document.querySelector('#quantity')
        this.quantity = this.input.value
        this.cost = 85
        document.querySelector('#cost').textContent = this.cost * this.quantity
        this.button = document.querySelector('#cta')

        var future = new Date();
        future.setDate(future.getDate() + 30);

     }
    init(){
        this.input.addEventListener('keyup', e=>{
            this.quantity = this.input.value
            let price = this.cost * this.quantity
            document.querySelector('#cost').textContent = price
            this.button.setAttribute('href', `/checkout/single_campaign?quantity=${this.quantity}`)
        })
    }
}