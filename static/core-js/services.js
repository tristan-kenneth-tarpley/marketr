const NotificationsService = class {
    constructor(url_path, admin=false) {
        this.url_path = url_path
        this.admin = admin
    }

    update(notifications) {
        let data = JSON.parse(notifications)
        let messages = []
        let tasks_and_insights = []
        Object.keys(data).forEach(key=> {
            let notification;
            let type;
            if (data[key].message_string != null){
                type = 'message'
                notification = data[key].message_string
                messages.push('message')
            } else if (data[key].task_title != null) {
                type = 'task'
                notification = data[key].task_title
                tasks_and_insights.push('task')
            } else if (data[key].insight_body != null) {
                type = 'insight'
                notification = data[key].insight_body
                tasks_and_insights.push('insight')
            }

            const row = notificationEl(type, notification, this.admin)
            $("#notifications").append(row)
        })
        $(".notification_count").text(Object.keys(data).length)
        $(".tab_and_insight_count").text(tasks_and_insights.length)
        $(".message_count").text(messages.length)
    }

    get() {
        if (this.admin == false) {
            $.get('/api/notifications', data=>{
                this.update(data)
            })
        } else {
            $.get(`/api/notifications`, {
                customer_id: this.url_path.slice(11, 14)
            }, data=>{
                this.update(data)
            })
        }
    }
}

const ScoreService = class {
    constructor(url_path, admin=false) {
        this.url_path = url_path
        this.admin = admin
    }

    update(data) {
        let condition_class;
        let condition;
        $("#marketr-score").text(data)
        if (parseInt(data) < 390) {
            condition_class = 'score-very_weak'
            condition = 'very weak'
        } else if (parseInt(data) > 390 && parseInt(data) < 510) {
            condition_class = 'score-weak'
            condition = 'weak'
        } else if (parseInt(data) > 510 && parseInt(data) < 580) {
            condition_class = 'score-moderate'
            condition = 'moderate'
        } else if (parseInt(data) > 580 && parseInt(data) < 680) {
            condition_class = 'score-good'
            condition = 'good'
        } else if (parseInt(data) > 680) {
            condition_class = 'score-excellent'
            condition = 'excellent'
        }

        $(".score_container").addClass(condition_class)
        $("#marketr-score-quality").text(condition)
    }

    get() {
        if (this.admin == false) {
            $.get('/api/marketr_score', data=>{
                this.update(data)
            })
        } else {
            $.get(`/api/marketr_score`, {
                customer_id: this.url_path.slice(11, 14)
            }, data=>{
                this.update(data)
            })
        }
    }
}


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