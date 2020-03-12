export default class cta {
    constructor(){
        this.input = document.querySelector('#quantity')
        this.quantity = this.input ? this.input.value : 1
        this.cost = 85
        document.querySelector('#cost') ? document.querySelector('#cost').textContent = this.cost * this.quantity : console.log('not active')
        this.button = document.querySelector('#cta')

        var future = new Date();
        future.setDate(future.getDate() + 30);

     }
    init(){
        try {
            this.input.addEventListener('keyup', e=> {
                this.quantity = this.input.value
                let price = this.cost * this.quantity
                document.querySelector('#cost').textContent = price
                this.button.setAttribute('href', `/checkout/single_campaign?quantity=${this.quantity}`)
            })
            
        } catch (error) {
            console.log(error)
        }
    }
}