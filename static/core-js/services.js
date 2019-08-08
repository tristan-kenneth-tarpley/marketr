
const MessagingService = class {
    constructor(url_path) {
        this.url_path = url_path
        this.customer_id = this.url_path.substring(11)
    }

    post_message(params) {
        $.post('/api/send_message', params)
    }

    update_messages (msg) {
        let chat = chat_box(msg, this.get_time(), this.get_date())
        $('.chat').prepend(chat)
        $('#msg').val("")
    }

    get_time () {
        let d = new Date()
        return d.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
    }
    get_date () {
        let d = new Date()
        return d.toDateString().substring(4)
    }

    send(msg) {
        this.success = false
        if (msg != "" && msg != null) {
            const params = {
                "msg": msg,
                "customer_id": this.customer_id
            }
            
            const controller = new Promise(
                (resolve, reject)=>{
                    this.post_message(params)
                    this.message_success = true
                    resolve(params.msg)
                }
            )

            controller
                .then(result => {
                    if (this.message_success == true) {
                        return result
                    }
                })
                .then(result => {
                    this.update_messages(result)
                })
        }
    }
} 



const TaskService = class {
    constructor (url_path) {
        this.url_path = url_path
        this.customer_id = this.url_path.substring(11)
    }

    post_task (args) {
        $.post("/api/add_task", args)
    }

    update_tasks(task){
        const taskEl = taskView(task)
        $('#task_body').prepend(taskEl)
        $('.todo').scrollTop($(".todo")[0].scrollHeight);
    }

    complete(task){
        const args = {
            task: task,
            customer_id: this.customer_id
        }
        $.post("/api/complete_task", args)
    }

    remove(task){
        const args = {
            task: task,
            customer_id: this.customer_id
        }
        $.post("/api/remove_task", args)
    }

    add () {
        let task = $("#task").val()
        if (task != "" && task != ""){
            const args = {
                customer_id: this.customer_id,
                task: $("#task_input").val()
            }

            const controller = new Promise(
                (resolve, reject) => {
                    this.post_task(args)
                    resolve(args.task)
                }
            )

            controller
                .then(task => {
                    this.update_tasks(task)
                })

        }

        
    }
}