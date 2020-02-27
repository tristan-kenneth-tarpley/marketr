import json
import data.db as db

class Wallet:
    def __init__(self, customer_id):
        self.customer_id = customer_id

    def update_balance(self, amount):
        query = "EXEC update_ledger @customer_id = ?, @amount = ?"
        db.execute(query, False, (self.customer_id, amount), commit=True)

    def meta(self):
        query = "SELECT * FROM wallet_meta(?) order by date_added desc"
        data, cursor = db.execute(query, True, (self.customer_id,))
        data = cursor.fetchall()

        funds_remaining = data[0][0]
        returned = {
            'funds_remaining': funds_remaining,
            'transactions': list()
        }
        
        for row in data:
            returned['transactions'].append({
                'date_added': row[1],
                'amount': row[2],
                'transaction_id': row[3]
            })

        return json.dumps(returned)