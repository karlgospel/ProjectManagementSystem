import re

import Login
from TeamMember import TeamMember
from Login import Login
import sqlite3
import bcrypt
import pandas as pd
import datetime
class SuperAdmin(TeamMember):

    def __init__(self):
        pass
        # super().__init__(username, email, admin)

    def set_project_status(self, projectName, status):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "UPDATE Project SET STATUS = (?) WHERE PROJECT_ID = (?)"
        cur.execute(sql, [status, projectName])
        conn.commit()
        conn.close()
        if status == 'In-Progress':
            self.set_project_start_date(projectName)
        else:
            pass
        #print(pd.read_sql("SELECT * FROM Project", conn))



    def set_project_start_date(self, projectName):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        now = datetime.datetime.now()
        sd = (now, projectName)
        sql = "UPDATE Project SET START_DATE = (?) WHERE PROJECT_NAME = (?)"
        cur.execute(sql, sd)
        print(pd.read_sql("SELECT * FROM Project", conn))

        conn.commit()
        conn.close()

    # def create_login(self, username, password,  email, is_admin):
    #
    #     # Validate email
    #     if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    #         print("Invalid email format")
    #         return False
    #     # Confirm username is not taken
    #     l = Login()
    #     if l.check_username_distinct(username):
    #         pass
    #     else:
    #         print('username taken')
    #         return False
    #     conn = sqlite3.connect("project.db")
    #     cur = conn.cursor()
    #
    #     hashable_password = password.encode('utf-8')
    #     hashed_password = bcrypt.hashpw(hashable_password, bcrypt.gensalt())
    #
    #     login_details = (username, hashed_password, is_admin, email)
    #     sql = ''' INSERT INTO Login(USERNAME, PASSWORD, ADMIN, EMAIL)
    #             VALUES(?,?,?,?) '''
    #     cur.execute(sql, login_details)
    #     print(pd.read_sql("SELECT * FROM Login", conn))
    #     conn.commit()
    #     conn.close()

