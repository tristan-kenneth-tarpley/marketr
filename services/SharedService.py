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
from services.NotificationsService import NotificationsService, EmailService, GoogleChatService
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from typing import Any, TypeVar, AnyStr, Optional, overload, Union, Tuple, List
import math
import pandas as pd




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
        data, cursor = db.execute(query, True, (self.customer_id,))
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

    def get_tests(self):
        query = """SELECT * FROM get_tests(?)"""
        data, cursor = db.execute(query, True, (self.customer_id,))
        data = cursor.fetchall()
        columns = [
            'views', 'conversion', 'variant', 'best_worst_binary', 'hypothesis'
        ]
        return_data = UserService.parseCursor(data, columns)
        return return_data
    



class MessagingService:
    def __init__(self, customer_id: int, admin_id: int=None, user='customer') -> None:
        self.customer_id = customer_id
        self.admin_id = admin_id
        self.user = user

    def get_messages(self) -> dict:
        query = """SELECT * FROM prep_messages(?)"""
        result, cursor = db.execute(query, True, (self.customer_id))
        # columns = ['message_string', 'admin_id', 'customer_id', 'from', 'timestamp']
        result = cursor.fetchone()
        # result = UserService.parseCursor(result, columns)
        try:
            return eval(result[0])
        except:
            return None

    def post_message(self, msg):
        tup = (msg, self.admin_id, self.customer_id, self.user)
        query = """
                INSERT INTO messages
                (message_string, admin_id, customer_id, _from)
                VALUES
                (?, ?, ?, ?)
                """
        db.execute(query, False, tup, commit=True)

        query = 'select customer_id from customer_account_reps where customer_id = ?'
        assigned, cursor = db.execute(query, True, (self.customer_id,))
        assigned = cursor.fetchone()


        admin_email = """
                select top 1 email from get_acct_mgr(?)
                """
        data, cursor = db.execute(admin_email, True, (self.customer_id,))

        admin_email = cursor.fetchone()
        admin_email = admin_email[0] if admin_email else 'tristan@marketr.life'


        customer_email = 'select top 1 email from customer_basic where id = ?'
        data, cursor = db.execute(customer_email, True, (self.customer_id,))

        customer_email = cursor.fetchone()
        customer_email = customer_email[0] if customer_email else 'tristan@marketr.life'

        if self.user == 'customer':
            notification = NotificationsService(self.customer_id)
            notification.ChatNotification(admin_email)
            email = admin_email
        elif self.user == 'admin':
            notification = NotificationsService(self.customer_id)
            notification.ChatNotification(customer_email)
            email = customer_email


        google = GoogleChatService()
        google.chat(
            email=email,
            admin_added = assigned,
            msg=msg
        )


class TaskService:
    def __init__(self, customer_id: int = None, admin_id: int = None, user='customer') -> None:
        self.customer_id = customer_id
        self.admin_id = admin_id
        self.user = user
 
    def get_tasks(self) -> dict:
        query = """SELECT * FROM prep_tasks(?)"""
        result, cursor = db.execute(query, True, (self.customer_id))
        # columns = ['task_title', 'complete_binary']
        result = cursor.fetchone()
        # result = UserService.parseCursor(result, columns)
        try:
            return eval(result[0])
        except:
            return None

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

        if self.user == 'customer':
            email = 'select top 1 email from customer_basic where id = ?'
            data, cursor = db.execute(email, True, (self.customer_id,))
        elif self.user == 'admin':
            email = 'select top 1 email from admins where id = ?'
            data, cursor = db.execute(email, True, (self.admin_id,))

        email = cursor.fetchone()
        email = email[0]
        notification = NotificationsService(self.customer_id)
        notification.TaskNotification(email)

    def complete_task(self, task):
        tup = (task, self.customer_id)
        query = """
                UPDATE to_do SET completed_binary = 1 WHERE task_title like ? and customer_id = ?
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
            query = """select * from prep_admin_insights(?, ?)"""
            tup = (self.customer_id, self.admin_id)
        data, cursor = db.execute(query, True, tup)
        data = cursor.fetchone()
        
        try:
            return eval(data[0])
        except:
            return None

class ScoreService:
    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        self.spread = 550
        self.min_score = 200
        
    def pop_suffix(self, string):
        try:
            if string[-1].isdigit() and not string[-2].isdigit():
                return string[:-2]
            elif string[-2].isdigit():
                return string[:-3]
            else:
                return string
        except:
            return string
        
    def aggregate(self):
        pass
        
    def clean(self):
        df = db.sql_to_df(f'exec prep_marketr_score @customer_id = {self.customer_id}')
    
        df['html_name'] = df['html_name'].apply(self.pop_suffix)
        df.drop_duplicates(subset="html_name", keep = 'first', inplace=True)
        self.df = df
        self.total_possible = df['score_weight_factor'].sum()
        self.sum_completed = df[df['answer'] != 'null'].score_weight_factor.sum()
  
        
    def get(self):
        self.clean()
        return str(math.ceil(self.sum_completed/self.total_possible * self.spread + self.min_score))
        # else:
        #     return 'n/a'
    
    def get_head(self):
        self.clean()
        return self.df