from email.mime.text import MIMEText
from tkinter import messagebox

import pandas as pd
import sqlite3
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import smtplib, ssl
from matplotlib.patches import Rectangle
class Project():

    def __init__(self):
        self.projectName = ''
        self.owner = ''
        self.percentageComplete = 0
        self.status = 'Not Started'

    def get_all_projects(self):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT PROJECT_NAME FROM Project"
        cur.execute(sql)
        projects = [x[0] for x in cur.fetchall()]
        conn.commit()
        conn.close()

        return projects

    def get_all_project_info(self):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT PROJECT_NAME, DESCRIPTION, OWNER, STATUS, START_DATE, END_DATE, PERCENTAGE_COMPLETE FROM Project"
        cur.execute(sql)
        projects = cur.fetchall()
        conn.commit()
        conn.close()
        return projects
    def get_percentage_complete(self,projectName):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = ("SELECT PERCENTAGE_COMPLETE FROM Project WHERE PROJECT_NAME = (?)")
        cur.execute(sql, [projectName])
        per = cur.fetchone()
        percentage = per[0]
        conn.commit()
        conn.close()
        return str(percentage) + '%'

    def get_project_id(self, projectName):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql_id = '''SELECT PROJECT_ID FROM Project WHERE PROJECT_NAME = (?)'''
        cur.execute(sql_id, [projectName])
        x = cur.fetchone()
        project_id = x[0]
        print(project_id)
        conn.commit()
        conn.close()
        return project_id

    def get_project_members(self, projectName):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql_id = '''SELECT DISTINCT USERNAME FROM ProjectMembers WHERE PROJECT_NAME = (?)'''
        cur.execute(sql_id, [projectName])
        users = cur.fetchall()
        members = [x[0] for x in users]
        print(members)
        conn.commit()
        conn.close()
        return members
    def add_members(self,projectName, *members):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        project_id = self.get_project_id(projectName)
        member_list = [x for x in members]
        member_list = member_list[0]
        for user in member_list:
            project_member = (projectName, user, project_id)
            sql = ''' INSERT INTO ProjectMembers (PROJECT_NAME, USERNAME, PROJECT_ID)
                            VALUES(?,?,?) '''
            cur.execute(sql, project_member)
        print('PROJECT MEMBERS  ADD')
        print(pd.read_sql("SELECT * FROM ProjectMembers", conn))
        conn.commit()
        conn.close()

    def remove_members(self, projectID, username):
        conn = sqlite3.connect("project.db")
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()

        project_member = (projectID, username)
        sql = ''' DELETE FROM ProjectMembers WHERE PROJECT_ID = ? AND member_ID = ?
                                VALUES(?,?) '''
        cur.execute(sql, project_member)
        print('PROJECT MEMBERS  REMOVE')
        print(pd.read_sql("SELECT * FROM ProjectMembers", conn))
        conn.commit()
        conn.close()

    def update_percentage_complete(self, projectID):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        # Count tasks assigned to project
        sql = "SELECT COUNT(TASK_ID) FROM Tasks WHERE PROJECT_ID = (?)"
        cur.execute(sql, [projectID])
        c = cur.fetchone()
        count = c[0]
        print(pd.read_sql("SELECT * FROM Project", conn))
        # Count completed tasks assigned to project
        sql = "SELECT COUNT(TASK_ID) FROM Tasks WHERE PROJECT_NAME = (?) AND STATUS = 'Completed'"
        cur.execute(sql, [projectID])
        com = cur.fetchone()
        completed = com[0]

        perc = completed / count * 100
        # Insert new percentage complete
        sql = "UPDATE Project SET PERCENTAGE_COMPLETE = (?) WHERE PROJECT_NAME = (?)"
        cur.execute(sql, [perc,projectID])
        print(pd.read_sql("SELECT * FROM Project", conn))
        conn.commit()
        conn.close()

    def get_description(self,projectID):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT DESCRIPTION FROM Project WHERE PROJECT_ID = (?)"
        cur.execute(sql, [projectID])
        try:
            des = cur.fetchone()[0]
            conn.commit()
            conn.close()
            return des
        except:
            print('No description found')
            conn.commit()
            conn.close()


    def get_status(self,projectID):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT PERCENTAGE_COMPLETE FROM Project WHERE PROJECT_ID = (?)"
        cur.execute(sql, [projectID])
        per = cur.fetchone()
        percentage = per[0]
        conn.commit()
        conn.close()
        return str(percentage) + '%'

    def check_owner(self, user, projectID):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT OWNER FROM Project WHERE PROJECT_ID = (?)"
        cur.execute(sql, [projectID])
        #print(cur.fetchone())
        per = cur.fetchone()
        print(per)
        if per is None:
            pass
        else:
            per = per[0]
            #print('per is ok')
        print(per, user)
        conn.commit()
        conn.close()
        if per == user:
            print('You are the one')
            return True
        else:
            print('Imposter')
            return False

    def create_project_message(self,projectID, message):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()

        project = (projectID, message)
        sql = ''' INSERT INTO ProjectMessages (PROJECT_ID, MESSAGE)
                        VALUES(?,?) '''
        cur.execute(sql, project)
        print('PROJECT  message create')
        print(pd.read_sql("SELECT * FROM ProjectMessages", conn))
        conn.commit()
        conn.close()

    def create_timeline(self, projectName):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT  MESSAGE, DATE_ADDED  FROM ProjectMessages pm INNER JOIN Project p on p.PROJECT_ID = pm.PROJECT_ID WHERE p.PROJECT_NAME = (?)"
        cur.execute(sql, [projectName])
        all_messages = cur.fetchall()
        messages = []
        dates = []
        start_date = self.get_project_start_date(projectName)
        end_date = self.get_project_end_date(projectName)
        for message, date in all_messages:
            messages.append(message)
            dates.append(pd.to_datetime(date))

        # Calculate levels for the stem plot
        levels = np.linspace(-1, 1, len(dates))

        # Create the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot vertical lines representing messages
        ax.vlines(dates, 0, levels, color='lightgray', linewidth=3)

        # Plot markers for each message
        ax.plot(dates, levels, "o", color="blue", markersize=10)

        # Annotate each message with its text
        for d, l, r in zip(dates, levels, messages):
            ax.text(d, l, r, fontsize=12, ha='left', va='center', color='black')

        # Set plot title and axis labels
        ax.set(title=f'Timeline of {projectName}',
               xlabel='Date', ylabel='Task Importance')

        # Format x-axis with date intervals
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))

        # Rotate x-axis labels for better readability
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

        # Remove spines
        ax.spines[["left", "top", "right"]].set_visible(False)

        # Set y-axis ticks and labels invisible
        ax.set_yticks([])
        ax.set_yticklabels([])

        plt.tight_layout()
        plt.show()

    def create_task_messages_timeline(self, projectID):
        # Connect to the database
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()

        # Retrieve data from the TaskMessages table
        sql = """SELECT tm.USERNAME, tm.MESSAGE, tm.DATE_ADDED,p.PROJECT_NAME, p.START_DATE, p.END_DATE
                    FROM TaskMessages tm 
                    INNER JOIN Tasks t ON t.TASK_ID = tm.TASK_ID 
                    INNER JOIN Project p ON p.PROJECT_ID = t.PROJECT_ID
                    WHERE t.PROJECT_ID = (?)"""
        cur.execute(sql, [projectID])
        project_messages = cur.fetchall()

        # Convert data to DataFrame
        df = pd.DataFrame(project_messages,
                          columns=["username", "message", "date_added", "project_name", "start_date", "end_date"])
        project_name = df["project_name"][0]
        start_date = df["start_date"][0]
        end_date = df["end_date"][0]

        if start_date is None:
            start_date = datetime.now()
        if end_date is None:
            end_date = datetime.now()

        # Convert date_added column to datetime
        df['date_added'] = pd.to_datetime(df['date_added'])

        # Sort DataFrame by date_added
        df = df.sort_values(by='date_added')

        # Get unique usernames
        unique_usernames = df['username'].unique()

        # Plot the Timeline chart
        fig, ax = plt.subplots(figsize=(12, len(unique_usernames) + 1))

        # Generate a color map
        color_map = plt.cm.get_cmap('tab10', len(unique_usernames))

        for i, username in enumerate(unique_usernames):
            messages = df[df['username'] == username]

            # Add messages
            for j, (date_added, message) in enumerate(messages[['date_added', 'message']].values):
                num_date_added = mdates.date2num(date_added)
                message_y_pos = i + 1  # Each user's timeline starts from 1 and increments by 1 for each user
                # Adjust text color based on rectangle color for readability
                text_color = 'black'
                ax.hlines(message_y_pos, start_date, num_date_added, color=color_map(i))
                ax.text(num_date_added, message_y_pos, message,
                        va='center', ha='left', color=text_color)

        # Set labels and title
        ax.set_yticks(range(1, len(unique_usernames) + 1))
        ax.set_yticklabels(unique_usernames)
        ax.set_title(f'Timeline of {project_name}')

        # Set x-axis format
        interval = max(1, int((end_date - start_date).days))  # Ensure interval is at least 1 day
        ax.xaxis.set_major_locator(
            mdates.DayLocator(interval=interval))  # Set interval to number of days between start_date and end_date
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))

        # Increment end_date by one day if start_date and end_date are the same
        if start_date == end_date:
            end_date += timedelta(days=1)

        # Adjust plot limits
        ax.set_xlim(start_date,
                    end_date + timedelta(days=1))  # Increment end_date by one day to avoid singular transformation
        ax.set_ylim(0.5, len(unique_usernames) + 0.5)

        plt.show()

        # Close the database connection
        conn.close()

    def get_project_start_date(self, projectID):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT START_DATE FROM Project WHERE PROJECT_ID = (?)"
        cur.execute(sql, [projectID])
        per = cur.fetchone()
        if per is None:
            start_date = datetime.now()
        else:
            start_date = per[0]
            print('per is ok')

        conn.commit()
        conn.close()
        print(pd.to_datetime(start_date))
        return pd.to_datetime(start_date)

    def get_project_end_date(self, projectID):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT END_DATE FROM Project WHERE PROJECT_ID = (?)"
        cur.execute(sql, [projectID])
        per = cur.fetchone()
        if per is None:
            end_date = datetime.now()
        else:
            end_date = per[0]
            print('per is ok')

        conn.commit()
        conn.close()
        print(pd.to_datetime(end_date))
        return pd.to_datetime(end_date)

    def delete_project(self, projectID):
        conn = sqlite3.connect("project.db")
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        print('before delete')
        print(pd.read_sql("SELECT * FROM Project", conn))
        print(pd.read_sql("SELECT * FROM ProjectMessages", conn))
        print(pd.read_sql("SELECT * FROM Tasks", conn))
        sql = "DELETE FROM Project WHERE PROJECT_ID = (?)"
        cur.execute(sql, [projectID])
        print('after delete')

        print(pd.read_sql("SELECT * FROM Project", conn))
        print(pd.read_sql("SELECT * FROM ProjectMessages", conn))
        print(pd.read_sql("SELECT * FROM Tasks", conn))

    def send_project_emails(self, project_name):

        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = ("""SELECT l.email 
                    FROM Login l 
                    INNER JOIN ProjectMembers pm ON pm.USERNAME = l.USERNAME 
                    INNER JOIN Project p on p.PROJECT_ID = pm.PROJECT_ID
                    where p.PROJECT_NAME = (?)
                    AND EMAIL IS NOT NULL""")
        try:
            print(project_name)
            cur.execute(sql, [project_name])
        except Exception as e:
            print('email is shit')
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
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