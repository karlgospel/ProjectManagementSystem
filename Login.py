import bcrypt

import pandas as pd
import sqlite3








class Login:

    # def __init__(self, username, password):
    #     self.username = username
    #     self.password = password

    def sign_in(self,username, password):

        if self.check_password(username, password):
            global current_user
            current_user = username
            return True
        else:
            return False

    def check_password(self,username, password):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = ("SELECT PASSWORD FROM Login WHERE USERNAME = (?)")
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
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT ADMIN FROM Login WHERE USERNAME = (?)"
        cur.execute(sql, [username])
        user = cur.fetchone()[0]
        print(user)
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