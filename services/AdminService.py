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
from services.NotificationsService import NotificationsService
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from typing import Any, TypeVar, AnyStr, Optional, overload, Union, Tuple, List
from services.SharedService import MessagingService, TaskService

class AdminService:
    def __init__(self):
        self.temp = 'test'

    def login(self, email, password, form=None):
        try:
            tup = (email,)
            query = "SELECT email, password, ID, first_name, last_name, permissions FROM dbo.admins WHERE email = ?"
            data, cursor = db.execute(query, True, tup)
            data = cursor.fetchall()
            pw = data[0][1]
            uid = data[0][2]
            admin_first = data[0][3]
            admin_last = data[0][4]
            permissions = data[0][5]
            cursor.close()

            if sha256_crypt.verify(password, pw):
                session['logged_in'] = False
                session['customer'] = False
                session['admin'] = int(uid)
                session['email'] = data[0][0]
                session['admin_first'] = admin_first
                session['admin_last'] = admin_last

                if permissions == 'owner':
                    session['owner_logged_in'] = True
                    session['admin_logged_in'] = True
                    session['manager_logged_in'] = True
                    session['permissions'] = 'owner'
                elif permissions == 'admin':
                    session['owner_logged_in'] = False
                    session['admin_logged_in'] = True
                    session['manager_logged_in'] = True
                    session['permissions'] = 'admin'
                elif permissions == 'manager':
                    session['owner_logged_in'] = False
                    session['admin_logged_in'] = False
                    session['manager_logged_in'] = True
                    session['permissions'] = 'manager'

                session.permanent = True
                session.remember = True
                return redirect(url_for('customers'))

            else:
                error = "Invalid credentials. Try again!"
                return render_template("admin_view/login.html", error = error, form=form)  

        except:
        # except AssertionError:
            error = "Invalid credentials. Try again!"
            return render_template("admin_view/login.html", error = error, form=form)  


    def update_password(self, a_id, supplied_password, current_password):

        if supplied_password == current_password:
            new_password = encrypt_password(str(supplied_password))
            tup = (new_password, a_id)
            db.execute('UPDATE dbo.admins SET password = ? WHERE id = ?', False, tup, commit=True)
            return redirect(url_for('personnel'))
        else:
            error = "passwords don't match"
            return redirect(url_for('personnel', error=error))

    def get_admins(self):
        query = "select (first_name + ' ' + last_name) as name, id from admins"
        data, cursor = db.execute(query, True, ())

        data = cursor.fetchall()
        return_data = []

        for row in data:
            to_append = {
                "name": row[0],
                "id": row[1]
            }
            return_data.append(to_append)
        cursor.close()
        return return_data
    
    def get_admin_info(self):
        tup = ()
        query = 'SELECT first_name, last_name, email, permissions, id, position, phone_num FROM dbo.admins'
        data, cursor = db.execute(query, True, tup)
        data = data.fetchall()
        cursor.close()

        return data

    def get_customer_name(self, customer_id):
        query = """select company_name from customer_basic where id = ?"""
        data, cursor = db.execute(query, True, (customer_id,))
        data = cursor.fetchone()
        return data[0]
    
    def validate_view(self, admin_id, customer_id) -> bool:
        validate_tup = (admin_id, customer_id)
        query = """
                SELECT * FROM validate_admin_view(?, ?)
                """
        returned, cursor = db.execute(query, True, validate_tup)
        returned = cursor.fetchone()
        cursor.close()
        if returned != None:
            return True
        else:
            return False


    def get_customers(self, conditional=None):
        query = """
                    SELECT * FROM customer_list
                """
            
        if conditional != None:
            query += conditional
            
        data, cursor = db.execute(query, True, ())
        data = cursor.fetchall()
        cursor.close()

        columns = ['name', 'email', 'company_name', 'customer_id', 'mgr', 'admin_id']
        
        if len(data) > 0:
            return_data = UserService.parseCursor(data, columns)
        else:
            null_list = [('no customers assigned yet', '', '', '', '', '')]
            return_data = UserService.parseCursor(null_list, columns)

        return return_data





        


class AdminActions(object):
    def __init__(self, id: str, admin_id: int, debug: bool = False) -> None:
        self.id = id
        self.admin_id = admin_id
        self.debug = debug

    def add_rep(self, form, customer_id):
        acct_mgr: str = form['account_mgr']

        am_tup = (customer_id, acct_mgr)
        am_query = """EXEC update_account_mgr @customer_id = ?, @admin_id = ?"""

        if not self.debug and acct_mgr != "":
            db.execute(am_query, False, am_tup, commit=True)
        elif self.debug:
            print(am_query)
            print(am_tup)

        rep_query = """EXEC update_account_rep @customer_id = ?, @admin_id = ?"""
        for item in form:
            if len(item) > 8 and item[:9] == 'add_admin' and form[item] != acct_mgr and form[item] != "":
                rep = form[item]
                rep_tup = (customer_id, rep)
        
                if not self.debug:
                    db.execute(rep_query, False, rep_tup, commit=True)
                else:
                    print(rep_query)
    
    def send_insight(self, insight, customer_id=None, admin_id=None):
        note = NotificationsService(customer_id)
        note.Insight(insight)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        query = """
                EXEC add_insight
                    @customer_id = ?,
                    @admin_id = ?,
                    @body = ?,
                    @time = ?
                """
        tup = (self.id, self.admin_id, insight, st)
        db.execute(query, False, tup, commit=True)
        #come back




class AdminUserService(object):
    def __init__(self, customer_id: int = None, admin_id: int = None) -> None:
        self.customer_id = customer_id
        self.admin_id = admin_id

        self.messaging = MessagingService(
            customer_id=self.customer_id,
            admin_id=self.admin_id
        )
        self.tasks = TaskService(
            customer_id=self.customer_id,
            admin_id=self.admin_id
        )



class TacticService(object):
    def __init__(self, tag_id=None):
        self.tag_id = tag_id
    
    def add(self, data):
        for_query = {}
        tup = []
        for val in data:
            if data[val] == True:
                proc_tup = (data['search'], val)
                query = """EXEC add_tactic_tag @tactic_id=?, @tag_val=?"""
                db.execute(query, False, proc_tup, commit=True)
                for_query.update([ (val, data[val]) ])
                tup.append(val)

    def count(self):
        query = "SELECT count(tactic_id) FROM tactic_tags WHERE tactic_id = ?"
        tup = (self.tag_id,)
        data, cursor = db.execute(query, True, tup)
        data = cursor.fetchone()
        return str(data[0])

    def meta(self):
        query = 'SELECT tactic_id, title, description, image, category FROM tactics WHERE tactic_id = ?'
        tup = (self.tag_id,)
        data, cursor = db.execute(query, True, tup)
        data = cursor.fetchall()
        columns = [
            'tactic_id',
            'title',
            'description',
            'image',
            'category'
        ]
        data = UserService.parseCursor(data, columns)
        return data

class TempDataService:
    def __init__(self):
        pass

    def add_record(self, form, customer_id):
        query = """
        INSERT INTO temp_ad_view
        (customer_id, start_date, end_date, spend, active_ads, ads_last_30, cpc_last_7, ctr_last_7, google, facebook, bing, capterra)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """
        tup = (customer_id, form.start_date.data, form.end_date.data, form.spend.data, form.active_ads.data, form.ads_last_30.data, form.cpc_last_7.data, form.ctr_last_7.data, form.google.data, form.facebook.data, form.bing.data, form.capterra.data)

        db.execute(query, False, tup, commit=True)
