import data.db as db
import json

class RecommendationService(object):
    def __init__(self, customer_id=None, admin_id=None): 
        self.customer_id = customer_id
        self.admin_id = admin_id

    def struct(self, row):
        returned = {
            'rec_id': row[0],
            'customer_id': row[1],
            'admin_assigned': row[2],
            'title': row[3],
            'body': row[4],
            'accepted': row[5],
            'dismissed': row[6],
            'label': row[7]
        }
        return returned
    
    def get_one(self, rec_id=None):
        rec, cursor = db.execute("SELECT * FROM recommendations WHERE rec_id = ?", True, (rec_id))
        rec = cursor.fetchone()
        returned = self.struct(rec)
        return returned

    def get_historical(self):
        print(self.customer_id)
        recs, cursor = db.execute("select * from historical_recommendations(?)", True, (self.customer_id,))
        recs = cursor.fetchall()
        rec_list = {
            'approved': list(),
            'dismissed': list()
        }

        for rec in recs:
            rec_id = rec[0]
            title = rec[3]
            body = rec[4]
            accepted = rec[5]
            dismissed = rec[6]

            if accepted:
                rec_list['approved'].append({
                    "rec_id": rec_id,
                    "title": title,
                    "body": body
                })
            elif dismissed:
                rec_list['dismissed'].append({
                    "rec_id": rec_id,
                    "title": title,
                    "body": body
                })
    
        return json.dumps(rec_list)

    def get_all(self):
        recs, cursor = db.execute("SELECT * FROM recommendations WHERE customer_id = ?", True, (self.customer_id,))
        recs = cursor.fetchall()
        rec_list = list()
        for rec in recs:
            rec_list.append(self.struct(rec))

        return json.dumps(rec_list)

    def get_all_outstanding(self):
        recs, cursor = db.execute("SELECT * FROM outstanding_recs(?)", True, (self.customer_id,))
        recs = cursor.fetchall()
        rec_list = list()
        for rec in recs:
            rec_list.append(self.struct(rec))

        return json.dumps(rec_list)

    def new(self, title=None, body=None, label=None, notification_obj=None):
        notification_obj.send(subject="Market(r) just sent you a recommendation", message="Login to your dashboard to see it: https://marketr.life/home")
        db.execute(
            "exec new_rec @customer_id=?, @admin_assigned=?, @title=?, @body=?, @label=?",
            False,
            (self.customer_id, self.admin_id, title, body, label),
            commit=True
        )



class Recommendation(RecommendationService):
    def __init__(self, customer_id=None, rec_id=None, admin_id=None):
        super().__init__(customer_id=customer_id, admin_id=admin_id)
        self.rec_id = rec_id
        self.customer_id = customer_id
        self.meta = self.get_one(rec_id=rec_id)

    def modify(self, title=None, body=None, label=None):
        if title:
            attr = title
        elif body:
            attr = body
        elif label:
            attr = label

        query = f"UPDATE recommendations SET {attr} = ? WHERE rec_id = ?"
        db.execute(query, False, (self.rec_id,), commit=True)

    def accept(self):
        query = "UPDATE recommendations SET accepted = 1 WHERE rec_id = ?"
        db.execute(query, False, (self.rec_id,), commit=True)

    def dismiss(self):
        query = "UPDATE recommendations SET dismissed = 1 WHERE rec_id = ?"
        db.execute(query, False, (self.rec_id,), commit=True)

    def delete(self):
        query = "DELETE FROM recommendations WHERE rec_id = ? and customer_id = ?"
        db.execute(query, False, (self.rec_id, self.customer_id), commit=True)