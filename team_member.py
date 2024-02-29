from login import Login
import pandas as pd
import sqlite3
import bcrypt

class TeamMember:


    def change_password(self, username, old_password, new_password):
        l = Login()
        if l.check_password(username, old_password):
            pass
        else:
            return False
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        hashable_password = new_password.encode('utf-8')
        hashed_password = bcrypt.hashpw(hashable_password, bcrypt.gensalt())
        new_login_details = (hashed_password,username)
        sql = ''' UPDATE Login SET PASSWORD = (?) WHERE USERNAME = (?)'''
        cur.execute(sql, new_login_details)
        print(pd.read_sql("SELECT * FROM Login", conn))
        conn.commit()
        conn.close()


    def is_admin(self, username):
        print('given username')
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


