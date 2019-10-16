from app import app
from flask import url_for
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from services.UserService import UserService, encrypt_password
import data.db as db

class TacticsService:
    def __init__(self, customer_id):
        self.customer_id = customer_id

    def get(self):
        query = """ exec get_tactics @customer_id = ? """
        data, cursor = db.execute(query, True, (self.customer_id,))
        data = cursor.fetchall()
        columns = [
            'title',
            'description',
            'tactic_id'
        ]
        returned = UserService.parseCursor(data, columns)
        return returned