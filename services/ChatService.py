import hashlib
import hmac
import data.db as db
import requests
import json

class ChatService:
    def __init__(self, u_type, email, user_id, customer_id=None):
        self.type = u_type
        if u_type == 'User':
            self.email = email
        elif u_type == 'Admin':
            query = """select email, first_name, last_name from customer_basic where id = ?
                        union
                        select email, first_name, last_name from admins where id = ?"""
            db_email, cursor = db.execute(query, True, (customer_id, user_id))
            db_email = cursor.fetchall()
            self.customer_email = db_email[0][0]
            self.customer_name = str(db_email[0][1]) + " " + str(db_email[0][2])
            self.email = db_email[1][0]
            self.admin_name = str(db_email[1][1]) + " " + str(db_email[1][2])

        if customer_id:
            self.customer_id = customer_id

        self.user_id = str(user_id)

    def auth(self):
        user_id = self.user_id if self.type == 'User' else f"admin-{self.user_id}"
        userID = bytes(user_id, 'utf-8')
        secret = bytes('sk_live_as2RRYrVsNz8buYoKNSu8v8v', 'utf-8')
        hash = hmac.new(secret, userID, hashlib.sha256)
        return hash.hexdigest()

    def run(self):
        self.hash = self.auth()

    def send(self, customer_id, message):
        url = f'https://api.talkjs.com/v1/S9ifmqxv/conversations/marketr-{customer_id}/messages'
        data = [{
            'text': message,
            'sender': f'admin-6',
            'type': "UserMessage",
            'custom': { message: message }
        }]
        print(data)

        requests.post(url, data = json.dumps(data))