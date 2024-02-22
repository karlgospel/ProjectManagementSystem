import smtplib
import sqlite3
import ssl
from email.mime.text import MIMEText
from tkinter import messagebox

from Task import Task


class Email:

    def send_project_emails(self, project_name):

        conn = sqlite3.connect("project.db")
        cur = conn.cursor()

        sql = (f"""SELECT l.email 
                    FROM Login l 
                    INNER JOIN ProjectMembers pm ON pm.USERNAME = l.USERNAME 
                    INNER JOIN Project p on p.PROJECT_ID = pm.PROJECT_ID
                    where p.PROJECT_NAME = (?)
                    AND l.EMAIL IS NOT NULL""")
        try:
            print(project_name)
            cur.execute(sql, [project_name])
        except Exception as e:
            messagebox.showerror("Error sending project emails", f"An error occurred: {str(e)}")
        email_addresses = [row[0] for row in cur.fetchall()]


        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        senderEmail = "karl.gospel25@gmail.com"
        #receiver_email = "karl.gospel25@gmail.com"
        password = 'pggl orbw ozjs smth'
        text_subtype = 'plain'
        subject = 'Subject: Project Assignment'
        content = f"""\
        You have been assigned to the project {project_name}."""
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = senderEmail
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(senderEmail, password)
            for email in email_addresses:
                server.sendmail(senderEmail, email, msg.as_string())

    def send_project_completed_emails(self, project_name):

        conn = sqlite3.connect("project.db")
        cur = conn.cursor()

        sql = (f"""SELECT l.email 
                    FROM Login l 
                    INNER JOIN ProjectMembers pm ON pm.USERNAME = l.USERNAME 
                    INNER JOIN Project p on p.PROJECT_ID = pm.PROJECT_ID
                    where p.PROJECT_NAME = (?)
                    AND l.EMAIL IS NOT NULL""")
        try:
            print(project_name)
            cur.execute(sql, [project_name])
        except Exception as e:
            messagebox.showerror("Error sending project completed emails", f"An error occurred: {str(e)}")
        email_addresses = [row[0] for row in cur.fetchall()]


        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        senderEmail = "karl.gospel25@gmail.com"
        #receiver_email = "karl.gospel25@gmail.com"
        password = 'pggl orbw ozjs smth'
        text_subtype = 'plain'
        subject = 'Subject: Project Completed'
        content = f"""\
        {project_name} has been marked as completed. Well done for all your hard work"""
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = senderEmail
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(senderEmail, password)
            for email in email_addresses:
                server.sendmail(senderEmail, email, msg.as_string())

    def send_task_assignmnent_email(self, username, project_name):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        t = Task()
        #project_name = t.get_project_for_task(task_id)
        #task_name = t.get_task(task_id)
        #print(f'email {project_name}')
        sql = (f"""SELECT l.email 
                    FROM Login l 
                    WHERE USERNAME = (?)
                    AND l.EMAIL IS NOT NULL""")
        try:
            print(project_name)
            cur.execute(sql, [username])
        except Exception as e:
            messagebox.showerror("Error sending project emails", f"An error occurred: {str(e)}")
        email_addresses = cur.fetchone()
        print(email_addresses)
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        senderEmail = "karl.gospel25@gmail.com"
        # receiver_email = "karl.gospel25@gmail.com"
        password = 'pggl orbw ozjs smth'
        text_subtype = 'plain'
        subject = 'Subject: Task Assignment'
        content = f"""\
        You have been assigned a new task for the project {project_name}."""
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = senderEmail
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(senderEmail, password)
                for email in email_addresses:
                    server.sendmail(senderEmail, email, msg.as_string())
        except Exception as e:
            print('Error sending task assignment email', e)