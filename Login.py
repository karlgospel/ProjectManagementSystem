import re

import bcrypt

import pandas as pd
import sqlite3








class Login:

    current_user = None

    def create_login(self, username, password,  email, is_admin):

        # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Invalid email format")
            return 'Invalid email address'
        # Confirm username is not taken
        l = Login()
        if not password:
            return 'Please enter a valid password'
        if l.check_username_distinct(username):
            pass
        else:
            print('username taken')
            return 'Username is already taken'
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()

        hashable_password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(hashable_password, bcrypt.gensalt())

        login_details = (username, hashed_password, is_admin, email)
        sql = ''' INSERT INTO Login(USERNAME, PASSWORD, ADMIN, EMAIL)
                VALUES(?,?,?,?) '''
        try:
            cur.execute(sql, login_details)
            print(pd.read_sql("SELECT * FROM Login", conn))
            conn.commit()
            conn.close()
        except Exception as e:
            return 'Invalid details'

    def sign_in(self,username, password):

        if self.check_password(username, password):
            #global current_user
            Login.current_user = username
            return True
        else:
            return False

    def check_password(self,username, password):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = ("SELECT PASSWORD FROM Login WHERE USERNAME = (?)")
        try:
            cur.execute(sql, [username])
            user = cur.fetchone()
            current_password_hash = user[0]
            password_encoded = password.encode('utf-8')
            if bcrypt.checkpw(password_encoded, current_password_hash):
                conn.commit()
                conn.close()
                return True
            else:
                conn.commit()
                conn.close()
                return False
        except:
            return False
    def check_username_distinct(self,username):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = ("SELECT USERNAME FROM Login WHERE USERNAME = (?)")
        cur.execute(sql, [username])
        user = cur.fetchone()
        if user is None:
            conn.commit()
            conn.close()
            return True
        else:
            conn.commit()
            conn.close()
            return False

    def is_admin(self, username):
        print('given username' )
        print(username)
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT ADMIN FROM Login WHERE USERNAME = (?)"
        cur.execute(sql, [username])
        x = cur.fetchone()
        print(x)
        user = x[0]
        print(user)
        print(pd.read_sql("SELECT * FROM Login", conn))
        if user == 1:
            conn.commit()
            conn.close()
            print('You are an admin')
            return True
        else:
            print('You are NOT an admin')
            conn.commit()
            conn.close()
            return False

    def get_users(self):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = ("SELECT USERNAME FROM Login")
        cur.execute(sql)
        #user = cur.fetchall()
        usernames = [row[0] for row in cur.fetchall()]

        return usernames

    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)