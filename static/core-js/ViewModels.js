const CoreViewModels = class {

	constructor(url_path) {
		this.url_path = url_path
    }
    

	tasks() {
        $('.todo').scrollTop($(".todo")[0].scrollHeight);
        $("#add_task").click(() => {
            const tasks = new TaskService(this.url_path)
            tasks.add()
        })
        $(".task_complete").change((event)=>{
            const $this = $(event.currentTarget)
            if($this.prop('checked')) {
                const tasks = new TaskService(this.url_path)
                const val = $this.parent().parent().parent().next().text().replace(/^\s+/g, '').replace(/\s+$/g, '');;
                
                tasks.complete(val)
            }
        })
        $("#remove_task").click((event)=>{
            const tasks = new TaskService(this.url_path)
            const $this = $(event.currentTarget)
            const val = $this.parent().prev().text().replace(/^\s+/g, '').replace(/\s+$/g, '');

            tasks.remove(val)
            $this.parent().parent().remove()
        })
    }

    messages() {
        $('.chat').scrollTop($(".chat")[0].scrollHeight);
        $("#send_msg").click(() => {
            const messagingService = new MessagingService(this.url_path)
            const msg = $("#msg").val()
            messagingService.send(msg)  
        })
    }
}

