from flask import render_template, session, url_for, redirect
import data.db as db
import time
import datetime
import zipcodes
import json
from passlib.hash import sha256_crypt
from bleach import clean
from flask_mail import Mail, Message
from helpers.UserService import UserService, encrypt_password
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from typing import Any, TypeVar, AnyStr, Optional, overload, Union, Tuple, List



class MessagingService:
    def __init__(self, customer_id: int, admin_id: int=None, user='customer') -> None:
        self.customer_id = customer_id
        self.admin_id = admin_id
        self.user = user

    def get_messages(self) -> dict:
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