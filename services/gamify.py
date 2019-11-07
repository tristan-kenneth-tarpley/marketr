import data.db as db

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
        db.execute(query, False, tup, commit=False)

    def state(self):
        return self.evaluate()

class Credits:
    def __init__(self, customer_id=None):
        self.customer_id = customer_id

    def update(self, amount):
        query = "EXEC update_credits @customer_id = ?, @amount = ?"
        data, cursor = db.execute(query, True, (self.customer_id, amount), commit=True)
        data = cursor.fetchone()
        return data[0]