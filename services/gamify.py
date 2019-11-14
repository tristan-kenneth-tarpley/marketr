import data.db as db
from random import choices
from services.NotificationsService import GoogleChatService
from services.SharedService import MessagingService
import json

class Achievements:
    def __init__(self, customer_id=None):
        self.customer_id = customer_id

    def history(self):
        query = "select * from achievement_state(?)"
        data, cursor = db.execute(query, True, (self.customer_id,))
        data = cursor.fetchone()
        return eval(data[0])['state']

    def evaluate(self):
        history = self.history()
        state = []
        for achievement in history:
            value = 'value'
            check = eval(achievement['test'])
            if check:
                state.append(achievement)

        return state

    def save(self, achievement_id = None, frequency = None):
        query = "exec save_achievement @customer_id = ?, @achievement_id = ?, @frequency = ?"
        tup = (self.customer_id, achievement_id, frequency)
        db.execute(query, False, tup, commit=True)

    def acknowledge(self, achievement_id = None):

        query = "UPDATE achievement_log SET claimed = 1 WHERE achievement_id = ? and customer_id = ?"
        db.execute(query, False, (achievement_id, self.customer_id), commit=True)

    def state(self):
        returned = self.evaluate()
        for achievement in returned:
            self.save(achievement_id = achievement['id'], frequency=achievement['frequency'])
        return returned

class Credits:
    def __init__(self, customer_id=None):
        self.customer_id = customer_id

    def get(self):
        query = "SELECT credits FROM customer_basic WHERE id = ?"
        data, cursor = db.execute(query, True, (self.customer_id,))
        data = cursor.fetchone()
        returned = data[0] if data[0] else 0
        return data[0]

    def update(self, amount):
        current = self.get()
        current_amt = current if current else 0
        new = current_amt + amount
        query = """
                UPDATE customer_basic SET credits = ? WHERE id = ?;commit;
                """
        db.execute(query, True, (new, self.customer_id), commit=True)
        return new


class Rewards:
    def __init__(self, customer_id = None):
        self.customer_id = customer_id
        self.rewards = [{
                'title': 'Credits (+225)',
                'parameter': 225,
                'executable': self.credit_reward,
                'type': 'credit_reward',
                'weights': {
                    'free': {
                        'helper': 47.50,
                        'booster': 0.00,
                        'rocket': 0.00
                    },
                    'ad_management': {
                        'helper': 47.50,
                        'booster': 0.00,
                        'rocket': 0.00
                    }
                }
            }, {
                'title': '1 New Tactic',
                'parameter': 1,
                'executable': self.tactics_rewards,
                'type': 'tactics_rewards',
                'weights': {
                    'free': {
                        'helper': 47.5,
                        'booster': 0.00,
                        'rocket': 0.00
                    },
                    'ad_management': {
                        'helper': 47.50,
                        'booster': 0.00,
                        'rocket': 0.00
                    }
                }
            }, {
                'title': 'Credits (2,500)',
                'parameter': 2500,
                'executable': self.credit_reward,
                'type': 'credit_reward',
                'weights': {
                    'free': {
                        'helper': 0.95,
                        'booster': 19.00,
                        'rocket': 0.00
                    },
                    'ad_management': {
                        'helper': 0.79,
                        'booster': 15.83,
                        'rocket': 0.00
                    }
                }
            }, {
                'title': 'Web page audit',
                'parameter': "Congrats on the web page audit!  What web page would you like us to audit?",
                'executable': self.manual_reward,
                'type': 'manual_reward',
                'weights': {
                    'free': {
                        'helper': 0.95,
                        'booster': 19.00,
                        'rocket': 0.00
                    },
                    'ad_management': {
                        'helper': 0.79,
                        'booster': 15.83,
                        'rocket': 0.00
                    }
                }
            }, {
                'title': 'Article (2000 words)',
                'executable': self.manual_reward,
                'type': 'manual_reward',
                'parameter': "Articles are amazing for keeping content fresh. Do you have a specific topic you'd like us to write about?",
                'weights': {
                    'free': {
                        'helper': 0.95,
                        'booster': 19.00,
                        'rocket': 0.00
                    },
                    'ad_management': {
                        'helper': 0.79,
                        'booster': 15.83,
                        'rocket': 0.00
                    }
                }
            }, {
                'title': 'Influencer (2,500+ followers) mention',
                "parameter": "Let's get that word out!  Is there a particular product or service that you would like to be highlighted?  Or just general company brand reference?",
                'executable': self.manual_reward,
                'type': 'manual_reward',
                'weights': {
                    'free': {
                        'helper': 0.00,
                        'booster': 0.00,
                        'rocket': 0.00
                    },
                    'ad_management': {
                        'helper': 0.79,
                        'booster': 15.83,
                        'rocket': 0.00
                    }
                }
            }, {
                'title': 'Influencer (10,000+ followers) mention',
                "parameter": "Let's get that word out!  Is there a particular product or service that you would like to be highlighted?  Or just general company brand reference?",
                'executable': self.manual_reward,
                'type': 'manual_reward',
                'weights': {
                    'free': {
                        'helper': 0.00,
                        'booster': 0.00,
                        'rocket': 0.00
                    },
                    'ad_management': {
                        'helper': 0.13,
                        'booster': 2.50,
                        'rocket': 50.00
                    }
                }
            }, {
                'title': 'Pricing analysis',
                "parameter": "Pricing is critical.  So many factors to consider - let us help you!  Would you like us to get started now?",
                'executable': self.manual_reward,
                'type': 'manual_reward',
                'weights': {
                    'free': {
                        'helper': 0.25,
                        'booster': 5.00,
                        'rocket': 100.00
                    },
                    'ad_management': {
                        'helper': 0.13,
                        'booster': 2.50,
                        'rocket': 50.000
                    }
                }
            }, {
                'title': 'Tactics x3',
                'executable': self.tactics_rewards,
                'type': 'tactics_rewards',
                'parameter': 3,
                'weights': {
                    'free': {
                        'helper': 0.95,
                        'booster': 19.00,
                        'rocket': 0.00
                    },
                    'ad_management': {
                        'helper': 0.79,
                        'booster': 15.83,
                        'rocket': 0.00
                    }
                }
            }, {
                'title': '30 min consultation call',
                "parameter": "You won a 30 min consultation call with one of our leading marketing experts!  Look for an email invite to choose a time slot.  Looking forward to talking with you :)",
                'executable': self.manual_reward,
                'type': 'manual_reward',
                'weights': {
                    'free': {
                        'helper': 0.95,
                        'booster': 19.00,
                        'rocket': 0.00
                    },
                    'ad_management': {
                        'helper': 0.79,
                        'booster': 15.83,
                        'rocket': 0.00
                    }
                }
            } 
        ]

        query = "SELECT current_plan FROM customer_basic WHERE id = ?"
        data, cursor = db.execute(query, True, (customer_id,))
        data = cursor.fetchone()
        if data[0] and int(data[0]) == 1:
            self.plan = True
        else:
            self.plan = False

    def update_balance(self, balance):
        credits_service = Credits(customer_id=self.customer_id)
        current = credits_service.get()
        new = current - balance
        query = "UPDATE customer_basic SET credits = ? WHERE id = ?"
        db.execute(query, False, (new, self.customer_id), commit=True)

    def add_to_balance(self, amount):
        credits_service = Credits(customer_id=self.customer_id)
        current = credits_service.get()
        new = current + amount
        query = "UPDATE customer_basic SET credits = ? WHERE id = ?"
        db.execute(query, False, (new, self.customer_id), commit=True)


    def drop(self, drop_type):
        drops = []
        weights = []
        plan_index = 'free' if not self.plan else 'ad_management'

        if drop_type == 'helper':
            max_amt = 200
        elif drop_type == 'booster':
            max_amt = 2000
        elif drop_type == 'rocket':
            max_amt = 40000

        self.update_balance(max_amt)
        
        for drop in self.rewards:
            drops.append(self.rewards.index(drop))
            weights.append(
                drop['weights'][plan_index][drop_type]
            )

        random_index = choices(drops, weights)[0]
        pack = self.rewards[random_index]
        reward = pack['executable'](pack['parameter'])
        return_reward = {
            'title': pack['title'],
            'type': pack['type'],
            'parameter': pack.get('parameter'),
            'reward': reward
        }

        QUERY = """INSERT INTO rewards_log (customer_id, reward_title, added)
                values(?, ?, GETDATE())"""

        db.execute(QUERY, False, (self.customer_id, pack['title']), commit=True)
        
        return return_reward

    def credit_reward(self, amount):
        self.update_balance(amount)

        return None

    def tactics_rewards(self, amount):
        query = """
            SET NOCOUNT ON
            exec get_tactics @customer_id = ?;
        """
        data, cursor = db.execute(query, True, (self.customer_id,), commit=True)

        data = cursor.fetchone()
        tactic = {
            'title': data[0] if data else None,
            'description': data[1] if data else None,
            'id': data[2] if data else None
        }
        cursor.close()

        update_query = "insert into tactics_log (customer_id, tactic_id) values (?,?)"
        db.execute(update_query, False, (self.customer_id, tactic['id']), commit=True)

        return tactic



    def manual_reward(self, message):
        google = GoogleChatService()
        google.manual_rewards(message)

        messaging = MessagingService(self.customer_id, admin_id=6, user='admin')
        messaging.post_message(message)

        return None
