from flask import render_template, session, url_for, redirect
import data.db as db
import time
import datetime
import zipcodes
import json
from passlib.hash import sha256_crypt
from bleach import clean
from flask_mail import Mail, Message
from services.UserService import UserService, encrypt_password
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from typing import Any, TypeVar, AnyStr, Optional, overload, Union, Tuple, List


class CoreService:
    def __init__(self, customer_id):
        self.customer_id = customer_id

    def populate_null(self):
        return {}

    def customer_core(self):
        query = """SELECT * FROM customer_core(?)"""
        data, cursor = db.execute(query, True, (self.customer_id,))
        data = cursor.fetchone()
        if data != None:
            return data
        else:
            return self.populate_null()

    def get_products(self):
        query = """SELECT * FROM product_list WHERE customer_id = ?"""
        data, cursor = db.execute(query, True, (self.customer_id,))
        data = cursor.fetchall()
        if data != None:
            return data
        else:
            return self.populate_null()
    
    def get_audience(self):
        query = """SELECT * FROM audience WHERE customer_id = ?"""
        data, cursor = db.execute(query, True, (self.customer_id,))
        data = cursor.fetchall()
        if data != None:
            return data
        else:
            return self.populate_null()

    def get_platforms(self):
        query = """SELECT * FROM platforms WHERE customer_id = ?"""
        data, cursor = db.execute(query, True, (self.customer_id,))
        data = cursor.fetchall()
        if data != None:
            return data
        else:
            return self.populate_null()
    
    def get_salescycle(self):
        query = "SELECT * FROM view_sales_cycle(?)"
        data, cursor = db.execute(query, True, (self.customer_id,))
        data = cursor.fetchone()
        if data != None:
            return data
        else:
            return self.populate_null()

    def get_messages(self, user='customer'):
        messaging = MessagingService(self.customer_id, user=user)
        messages = messaging.get_messages()
        if messages != None:
            return messages
        else:
            return self.populate_null()
    
    def get_tasks(self, user='customer'):
        tasks = TaskService(self.customer_id)
        task_list = tasks.get_tasks()
        if task_list != None:
            return task_list
        else:
            return self.populate_null()

    def get_google(self, user='customer'):
        query = """SELECT * FROM customer_ads_display(?)"""
        data, cursor = db.execute(query, True, (self.customer_id))
        data = cursor.fetchall()
        columns = [
            'agg_ctr',
            'agg_cost',
            'best_ctr',
            'worst_ctr',
            'best_headline_1',
            'best_headline_2',
            'best_description',
            'worst_headline_1',
            'worst_headline_2',
            'worst_description'
        ]
        return_data = UserService.parseCursor(data, columns)

        return return_data
    



class MessagingService:
    def __init__(self, customer_id: int, admin_id: int=None, user='customer') -> None:
        self.customer_id = customer_id
        self.admin_id = admin_id
        self.user = user

    def get_messages(self) -> dict:
        print(self.customer_id)
        query = """SELECT * FROM get_messages(?)"""
        result, cursor = db.execute(query, True, (self.customer_id))
        columns = ['message_string', 'admin_id', 'customer_id', 'from', 'timestamp']
        result = cursor.fetchall()
        result = UserService.parseCursor(result, columns)
        return result

    def post_message(self, msg):
        tup = (msg, self.admin_id, self.customer_id, self.user)
        query = """
                INSERT INTO messages
                (message_string, admin_id, customer_id, _from)
                VALUES
                (?, ?, ?, ?)
                """
        db.execute(query, False, tup, commit=True)


class TaskService:
    def __init__(self, customer_id: int = None, admin_id: int = None, user='customer') -> None:
        self.customer_id = customer_id
        self.admin_id = admin_id

    def get_tasks(self) -> dict:
        query = """SELECT * FROM get_tasks(?) ORDER BY created_date DESC"""
        result, cursor = db.execute(query, True, (self.customer_id))
        columns = ['task_title', 'complete_binary']
        result = cursor.fetchall()
        result = UserService.parseCursor(result, columns)
        return result

    def post_task(self, task) -> None:
        tup = (task, self.customer_id, task, 0, self.admin_id, self.customer_id)
        query = """
                IF NOT EXISTS (SELECT task_title FROM to_do WHERE task_title = ? and customer_id = ?)
                    INSERT INTO to_do
                    (task_title, completed_binary, admin_assigned, customer_id)
                    VALUES
                    (?,?,?,?)
                """
        db.execute(query, False, tup, commit=True)

    def complete_task(self, task):
        tup = (task, self.customer_id)
        query = """
                UPDATE to_do SET completed_binary = 1 WHERE task_title = ? and customer_id = ?
                """
        db.execute(query, False, tup, commit=True)

    def remove_task(self, task):
        tup = (task, self.customer_id)
        query = """
                DELETE FROM to_do WHERE task_title = ? and customer_id = ?
                """
        db.execute(query, False, tup, commit=True)


class InsightsService:
    def __init__(self, customer_id: int, admin_id: int = None, user='customer'):
        self.customer_id = customer_id
        self.admin_id = admin_id
        self.user = user

    def fetch(self):
        if self.user == 'customer':
            query = """SELECT body, CONVERT(varchar, time) as time FROM insights WHERE customer_id = ? order by time desc"""
            tup = (self.customer_id,)
        else:
            query = """SELECT body, CONVERT(varchar, time) as time FROM insights WHERE admin_id = ? and customer_id = ? order by time desc"""
            tup = (self.admin_id, self.customer_id)
        data, cursor = db.execute(query, True, tup)
        data = cursor.fetchall()
        columns = ['body', 'time']

        if len(data) > 0:
            return_data = UserService.parseCursor(data, columns)
        else:
            null_list = [('no insights', '')]
            return_data = UserService.parseCursor(null_list, columns)
        
        return return_data