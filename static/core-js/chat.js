export default class Chat {
    constructor(type, user_email, sig, customer_id, name) {
        this.type = type
        this.user_email = user_email
        this.sig = sig
        this.customer_id = customer_id
        this.name = name
    }
    connect(){
        Talk.ready.then(()=>{
            var me = new Talk.User({
                name: this.name,
                id: this.customer_id,
                email: this.user_email,
                role: this.type
            });
            console.log('called')
            window.talkSession = new Talk.Session({
                appId: "S9ifmqxv",
                me: me,
                signature: this.sig
            });
            let operator_role;
            switch(this.type){
                case 'User':
                    operator_role = 'Admin'
                case 'Admin':
                    operator_role = 'User'
            }
            var operator = new Talk.User({
                id: "6",
                role: operator_role,
                name: "Tristan Tarpley",
                email: "info@marketr.life",
                photoUrl: "https://marketr.life/static/branding/img/tristan.jpg",
                welcomeMessage: "Hi there! How can I help you?"
            }); 
            var conversation = window.talkSession.getOrCreateConversation("item_2493");
            conversation.setParticipant(me);
            conversation.setParticipant(operator);
            var chatbox = window.talkSession.createChatbox(conversation);
            chatbox.mount(document.getElementById("talkjs-container"));
        });
    }
}