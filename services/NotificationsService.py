from app import app
from flask import url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from services.UserService import UserService, encrypt_password
import data.db as db
from httplib2 import Http
import json

class GoogleChatService:
    def __init__(self):
        pass

    def send(self, url, msg):
        message_headers = { 'Content-Type': 'application/json; charset=UTF-8'}
        http_obj = Http()
        http_obj.request(
            uri=url,
            method='POST',
            headers=message_headers,
            body=json.dumps(msg),
        )

    def rec_accepted(self, rec_id=None, user=None, email=None, company=None):
        url = 'https://chat.googleapis.com/v1/spaces/AAAApItvQ6A/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Wg61u0WhI6AY40Z9F4RwUVfmGP6nxtXTbhFECcvFVlE%3D'
        msg = {
            'text': f'Recommendation {rec_id} accepted\nCompany: {company}\nEmail: {email}\nUser id: {user}'
        }
        self.send(url, msg)

    def rec_dismissed(self, rec_id=None, user=None, email=None, company=None):
        url = 'https://chat.googleapis.com/v1/spaces/AAAApItvQ6A/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Wg61u0WhI6AY40Z9F4RwUVfmGP6nxtXTbhFECcvFVlE%3D'
        msg = {
            'text': f'Recommendation {rec_id} dismissed\nCompany: {company}\nEmail: {email}\nUser id: {user}'
        }
        self.send(url, msg)

    def error(self, e_type, user):
        url = 'https://chat.googleapis.com/v1/spaces/AAAAKn8VwAs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=hdngqlJ25rMELyt67mftmaKlw62QVRcCN-oxyNP6khA%3D'
        msg = {
            'text': f'Error with {e_type}\nUser: {user}'
        }
        self.send(url, msg)

    def manual_rewards(self, msg_txt, customer_id, email):
        url = "https://chat.googleapis.com/v1/spaces/AAAA4S0c7y8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=T0M1Cg56rlUj1dTNT4FsYs-dMpqm_C7O6SgYc0Tl9fU%3D"
        msg = {
            'text': f'{msg_txt}\nCustomer id: {str(customer_id)}\nEmail: {email}'
        }
        self.send(url, msg)

    def audit_request(self, url, email):
        webhook_url = "https://chat.googleapis.com/v1/spaces/AAAAGDGzT7Q/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=4tzuGln9HBgiS_AWn7ze7D-W6yOTTIWLjbiTVY_81bw%3D"
        msg = {
            'text': f'Audit request for {url}\n{email}'
        }
        self.send(webhook_url, msg)

    def chat(self, email=None, admin_added=False, msg=None):
        url = "https://chat.googleapis.com/v1/spaces/AAAAJlefMSU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=jb61xPyoYwkE9S5gsf-XeUrDZlFcu_cgEzWBK_oLtxA%3D"
        append = 'Manager needs to be assigned!' if not admin_added else ''
        bot_message = {
            'text' : f'New message from {email}:\n{msg}\n\n{append}'
        }
        self.send(url, bot_message)

    def onboarding_started(self, email=None):
        webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAAgnkbcqY/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=2FTH-q3zQEZLOmGtOtJCjNytqCeR3GJRPTBJTFxkqw8%3D'
        bot_message = {
            'text' : f'New onboarding started: {email}'
        }
        self.send(webhook_url, bot_message)


    def onboarding_complete(self, email=None):
        url = 'https://chat.googleapis.com/v1/spaces/AAAAp2FwCqg/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=I8CJEvVv2s_xPq5fWEWwe7oT3ghaiGvTaPUed3_cXVE%3D'
        msg = {
            'text': f'Onboarding completed for: {email}'
        }
        self.send(url, msg)

    def new_customer(self, email=None, customer_type=None):
        plan_table = {
			# live mode
			'plan_FfI9OI02wob7Wl': 'ab_binary',
			'plan_FxJImVg8UME2BU':'ad_binary',
			'plan_FfIAIrHBJ78YpY': 'almost_free_binary',
			'plan_FxJJZ1sUDZ0550': 'ad_premium',
            'plan_GDRUIQvA5OEUgK': 'ad_binary',
            'plan_GiHRR96eXXfxQM': 'analytics',
			# test mode
			'plan_Fed1YzQtnto2mT': 'ab_binary',
			'plan_FecAlOmYSmeDK3': 'ad_binary',
			'plan_FeZoBcEgfD35he': 'almost_free_binary'
		}

        webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAACXzT6xU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=pw7QTFKYMb-8vx-z68Bq-R-IBv-hEfL6m1yhMyxyDEo%3D'
        bot_message = {
            'text' : f'New {plan_table[customer_type]} customer: {email}'
        }
        self.send(webhook_url, bot_message)


class NotificationsService:
    def __init__(self, customer_id, prev_log_in=None):
        self.customer_id = customer_id
        self.prev_log_in = prev_log_in

    def get(self) -> dict:
        query = f"""exec fetch_notifications @customer_id = {self.customer_id}"""
        data, cursor = db.execute(query, True, ())
        data = cursor.fetchall()
        columns = [
            'message_string',
            'task_title',
            'insight_body',
            'message_from'
        ]
        return_data = UserService.parseCursor(data, columns)
        return return_data

    def ChatNotification(self, to):
        mailman = EmailService(to=to)
        subject = "You have a new message in Market(r)!"
        message = "Login here to view the message: https://marketr.life/home?view=messages"

        mailman.send(
            subject=subject,
            message=message
        )

    def Insight(self, insight):
        query = "SELECT email FROM customer_basic WHERE id = ?"
        data, cursor = db.execute(query, True, (self.customer_id,))
        data = cursor.fetchone()
        mailman = EmailService(to=data[0])
        subject = "You have a new insight in Market(r)!"
        message = "Login here to view the message: https://marketr.life/home?view=campaigns"

        mailman.send(
            subject=subject,
            message=message
        )
    
    def onboarding_started(self):
        tristan = EmailService(to='tristan@marketr.life')
        tyler = EmailService(to='tyler@marketr.life')
        subject = "Someone started their intake!"
        message = f"customer_id = {self.customer_id}"
        tristan.send(
            subject=subject,
            message=message
        )
        tyler.send(
            subject=subject,
            message=message
        )

    def checkout(self, plan_id):
        lut = {
            # live mode
            'plan_FfI9OI02wob7Wl': 'ab testing',
            'plan_FfI9ZGhlsAkGii':'paid ads',
            'plan_FfIAIrHBJ78YpY': 'almost free',
            # test mode
            'plan_Fed1YzQtnto2mT': 'ab testing',
            'plan_FecAlOmYSmeDK3': 'paid ads',
            'plan_FeZoBcEgfD35he': 'almost free'
        }

        tristan = EmailService(to='tristan@marketr.life')
        tyler = EmailService(to='tyler@marketr.life')
        subject = f"Market(r): New {lut[plan_id]} customer"
        message = f"customer_id = {self.customer_id}"
        tristan.send(
            subject=subject,
            message=message
        )
        tyler.send(
            subject=subject,
            message=message
        )



    def TaskNotification(self, to):
        mailman = EmailService(to=to)
        subject = "You have a new assignment in Market(r)."
        message = "Login here to view the message: https://marketr.life/home?view=messages"

        mailman.send(
            subject=subject,
            message=message
        )


class EmailService:
	def __init__(self, to: str=None):
		app.config.from_pyfile('config.cfg')
		self.mail = Mail(app)
		self.s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
		self.sender = 'no-reply@marketr.life'
		self.to = to

	def send(self, subject=None, message=None):
		msg = Message(subject, sender=self.sender, recipients=[self.to])
		msg.body = message
		self.mail.send(msg)

	def send_email_reset(self, supplied_email):
		query = "SELECT * FROM dbo.customer_basic WHERE email = ?"
		tup = (supplied_email,)
		data, cursor = db.execute(query, True, tup)

		data = data.fetchone()
		cursor.close()

		token = self.s.dumps(supplied_email, salt="password-reset")
		msg = Message('Reset Password', sender=self.sender, recipients=[supplied_email])
		link = url_for('update_password', token=token, _external=True)
		msg.body = "Your password reset link is: %s" % (link,)
		self.mail.send(msg)

	def update_password(self, supplied_password, token=None):
		email = self.s.loads(token, salt='password-reset', max_age=3600)
		password = encrypt_password(supplied_password)

		tup = (password, email)
		query = "UPDATE dbo.customer_basic SET password = ? WHERE email = ?"

		db.execute(query, False, tup, commit=True)