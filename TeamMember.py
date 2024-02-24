from email.mime.text import MIMEText

import Login
from Project import Project
from Login import Login
import pandas as pd
import sqlite3
from Task import Task
import bcrypt
import smtplib, ssl
class TeamMember:

    def __init__(self):
        pass
        # self.username = username
        # self.email = email
        # self.admin = admin

    def create_task(self, project_name, task_name, description, status, assigned):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        p = Project()
        project_id = p.get_project_id(project_name)
        task = (project_id, description, status, 0, assigned, task_name)
        sql = ''' INSERT INTO Tasks (PROJECT_ID, DESCRIPTION, STATUS, PERCENTAGE_COMPLETE, ASSIGNED_TO, TASK_NAME)
                        VALUES(?,?,?,?,?,?) '''
        cur.execute(sql, task)
        print('PROJECT  create')
        print(pd.read_sql("SELECT * FROM Tasks", conn))
        conn.commit()
        conn.close()

    def allocate_task(self, taskID, assignedTo):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()

        task = (assignedTo, taskID)
        sql = ''' UPDATE Tasks SET ASSIGNED_TO = (?) WHERE TASK_ID = (?)'''
        cur.execute(sql, task)
        print('allocate task')
        print(pd.read_sql("SELECT * FROM Tasks", conn))
        conn.commit()
        conn.close()

    # def edit_task(self, taskID, taskName, description, status):
    #     conn = sqlite3.connect("project.db")
    #     cur = conn.cursor()
    #
    #     task = (taskName, description, status, taskID)
    #     sql = ''' UPDATE Tasks SET TASK_NAME = (?), DESCRIPTION = (?), STATUS = (?) WHERE TASK_ID = (?)'''
    #     cur.execute(sql, task)
    #     print('PROJECT  create')
    #     print(pd.read_sql("SELECT * FROM Tasks", conn))
    #     conn.commit()
    #     conn.close()

    # def create_project(self, projectName, owner, status, description):
    #
    #     conn = sqlite3.connect("project.db")
    #     cur = conn.cursor()
    #     self.update_start_and_end_dates(old_project_name, status)
    #     project = (projectName, owner, status, description, 0)
    #     sql = ''' INSERT INTO Project (PROJECT_NAME, OWNER, STATUS, DESCRIPTION, PERCENTAGE_COMPLETE)
    #                     VALUES(?,?,?,?,?) '''
    #     cur.execute(sql, project)
    #     print('PROJECT  create')
    #     print(pd.read_sql("SELECT * FROM Project", conn))
    #     conn.commit()
    #     conn.close()


    def change_password(self, username, old_password, new_password):
        l = Login()
        if l.check_password(username, old_password):
            pass
        else:
            return False
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        # sql = ("SELECT PASSWORD FROM Login WHERE USERNAME = (?)")
        # cur.execute(sql, [username])
        # user = cur.fetchone()
        # current_password_hash = user[0]
        # old_password_encoded = old_password.encode('utf-8')
        #
        # if bcrypt.checkpw(old_password_encoded,current_password_hash):
        #
        #     print('correct password')
        #     pass
        # else:
        #     print('No dice')
        #     return False

        hashable_password = new_password.encode('utf-8')
        hashed_password = bcrypt.hashpw(hashable_password, bcrypt.gensalt())
        new_login_details = (hashed_password,username)
        sql = ''' UPDATE Login SET PASSWORD = (?) WHERE USERNAME = (?)'''
        cur.execute(sql, new_login_details)
        print(pd.read_sql("SELECT * FROM Login", conn))
        conn.commit()
        conn.close()


    def allocate_task(self, taskID, username):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        task = (username , taskID)
        sql = ''' UPDATE Tasks SET ASSIGNED_TO = (?) WHERE TASK_ID = (?)'''
        cur.execute(sql, task)
        print(pd.read_sql("SELECT * FROM Tasks", conn))
        conn.commit()
        conn.close()

    # def send_project_email(self, senderEmail, receiverEmail, project_name):
    #     port = 587  # For starttls
    #     smtp_server = "smtp.gmail.com"
    #     senderEmail = "karl.gospel25@gmail.com"
    #     #receiver_email = "karl.gospel25@gmail.com"
    #     password = 'pggl orbw ozjs smth'
    #     text_subtype = 'plain'
    #     subject = 'Subject: Project Assignment'
    #     content = f"""\
    #     You have been assigned to the project {project_name}."""
    #     msg = MIMEText(content, text_subtype)
    #     msg['Subject'] = subject
    #     msg['From'] = senderEmail
    #     context = ssl.create_default_context()
    #     with smtplib.SMTP(smtp_server, port) as server:
    #         server.ehlo()  # Can be omitted
    #         server.starttls(context=context)
    #         server.ehlo()  # Can be omitted
    #         server.login(senderEmail, password)
    #         server.sendmail(senderEmail, receiverEmail, msg.as_string())


