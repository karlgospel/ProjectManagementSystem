import pandas as pd
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

from login import Login


class Project:
    """
    Class to handle project creation, editing, and retrieval.

    Attributes:
        None

    Methods:
        create_project(project_name, owner, status, description):
            Creates a project and adds it to the Project table in the database.
        edit_project(old_project_name, new_project_name, owner, status, description):
            Edit a project and update the Project table in the database.
        get_all_projects():
            Returns a list of all the project names in the Project table in the database.
        get_all_project_info():
            Returns all data from the Project table in the database.
        get_percentage_complete(project_name):
            Returns the percentage complete of a given project from the Project table in the database.
        get_project_id(project_name):
            Returns the ID related to a project from the Project table in the database.
        get_project_members(project_name):
            Get the list of members associated with a project.
        add_members(project_name, *members):
            Add members to a project.
        remove_members(project_name, username):
            Remove a member from a project.
        get_project_task_count(project_id):
            Get the count of tasks assigned to a project.
        get_project_completed_task_count(project_id):
            Get the count of completed tasks assigned to a project.
        update_percentage_complete(project_name):
            Update the percentage completion of a project based on its tasks percentage completion.
        get_description(project_id):
            Get the description of a project.
        check_owner(user, project_id):
            Check if a user is the owner of a project.
        create_project_message(project_name, message):
            Create a message associated with a project.
        create_timeline(project_name):
            Create a timeline plot for a project based on its messages.
        get_project_start_date(project_id):
            Get the start date of a project.
        get_project_end_date(project_id):
            Get the end date of a project.
        set_project_start_date(project_name):
            Set the start date of a project.
        set_project_end_date(project_name):
            Set the end date of a project.
        update_start_and_end_dates(project_name, status):
            Update the start and end dates of a project based on its status.
        set_project_status(project_name, status):
            Set the status of a project.
        get_project_status(project_name):
            Get the status of a project.
        delete_project_end_date(project_name):
            Delete the end date of a project.
        delete_project(project_name):
            Delete a project from the database.
        get_project_messages(project_name):
            Get all messages associated with a project.
    """



    def create_project(self, project_name: str, owner: str, status: str, description: str):
        """
        Creates a project and adds it to the Project table in the database.

        Parameters:
            project_name (str): The name of the project.
            owner (str): The owner of the project.
            status (str): The status of the project.
            description (str): The description of the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        try:
            if status == 'In-Progress':
                self.set_project_start_date(project_name)
        except Exception as e:
            print('Error updating dates for new project', e)
        try:
            # Strip whitespace for project name
            project = (project_name.strip(), owner, status, description, 0)
            sql = ''' INSERT INTO Project (PROJECT_NAME, OWNER, STATUS, DESCRIPTION, PERCENTAGE_COMPLETE)
                            VALUES(?,?,?,?,?) '''
            cur.execute(sql, project)
            conn.commit()
            conn.close()
        except Exception as e:
            print('Error creating new project', e)
        try:
            if status == 'In-Progress':
                self.set_project_start_date(project_name)
        except Exception as e:
            print('Error updating dates for new project', e)

    def edit_project(self, old_project_name: str, new_project_name: str, owner: str, status: str, description: str):
        """
        Edit a project and update the Project table in the database.

        Parameters:
            old_project_name (str): The current name of the project.
            new_project_name (str): The new name of the project.
            owner (str): The owner of the project.
            status (str): The status of the project.
            description (str): The description of the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        project_id = self.get_project_id(old_project_name)
        self.update_start_and_end_dates(old_project_name, status)
        # Strip whitespace for project name
        project = (new_project_name.strip() , owner, status, description, project_id)
        sql = '''   UPDATE Project  
                    SET PROJECT_NAME = (?), 
                    OWNER = (?), 
                    STATUS = (?), 
                    DESCRIPTION = (?)
                    WHERE PROJECT_ID = (?)'''
        cur.execute(sql, project)
        print('PROJECT  EDIT')
        print(pd.read_sql("SELECT * FROM Project", conn))
        conn.commit()
        conn.close()

    def get_all_projects(self) -> list:
        """
        Returns a list of all the project names in the Project table in the database.

        Returns:
            list: All the project names in the Project table.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT PROJECT_NAME FROM Project"
        cur.execute(sql)
        projects = [x[0] for x in cur.fetchall()]
        conn.commit()
        conn.close()

        return projects

    def get_all_project_info(self) -> list:
        """
        Returns all data from the Project table in the database.

        Returns:
            list: List of Tuples where each tuple contains an individual project's values.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """   SELECT PROJECT_NAME, 
                            DESCRIPTION,    
                            OWNER, 
                            STATUS, 
                            strftime('%Y-%m-%d %H:%M:%S', START_DATE) AS START_DATE, 
                            strftime('%Y-%m-%d %H:%M:%S', END_DATE) AS END_DATE, 
                            PERCENTAGE_COMPLETE 
                            FROM Project"""
        cur.execute(sql)
        projects = cur.fetchall()
        conn.commit()
        conn.close()
        return projects

    def get_percentage_complete(self, project_name: str) -> str:
        """
        Returns the percentage complete of a given project from the Project table in the database.

        Parameters:
            project_name (str): The name of the project.

        Returns:
            str: The percentage complete of the given project with '%' concatenated.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = ("SELECT PERCENTAGE_COMPLETE FROM Project WHERE PROJECT_NAME = (?)")
        cur.execute(sql, [project_name])
        per = cur.fetchone()
        percentage = per[0]
        conn.commit()
        conn.close()
        return str(percentage) + '%'

    def get_project_id(self, project_name: str) -> int:
        """
        Returns the ID related to a project from the Project table in the database.

        Parameters:
            project_name (str): The name of the project.

        Returns:
            int : The ID of the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql_id = '''SELECT PROJECT_ID FROM Project WHERE PROJECT_NAME = (?)'''
        cur.execute(sql_id, [project_name])
        x = cur.fetchone()
        project_id = x[0]
        print(project_id)
        conn.commit()
        conn.close()
        return project_id

    def get_project_members(self, project_name: str) -> list:
        """
        Get the list of members associated with a project.

        Parameters:
            project_name (str): The name of the project.

        Returns:
            list: A list of usernames associated with the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql_id = '''SELECT DISTINCT USERNAME FROM ProjectMembers WHERE PROJECT_NAME = (?)'''
        cur.execute(sql_id, [project_name])
        users = cur.fetchall()
        members = [x[0] for x in users]
        print(members)
        conn.commit()
        conn.close()
        return members

    def add_members(self, project_name: str, *members: str):
        """
        Add members to a project.

        Parameters:
            project_name (str): The name of the project.
            *members (str): Variable length argument list of usernames to add.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        project_id = self.get_project_id(project_name)
        member_list = [x for x in members]
        member_list = member_list[0]
        for user in member_list:
            project_member = (project_name, user, project_id)
            sql = ''' INSERT INTO ProjectMembers (PROJECT_NAME, USERNAME, PROJECT_ID)
                            VALUES(?,?,?) '''
            cur.execute(sql, project_member)
        print('PROJECT MEMBERS  ADD')
        print(pd.read_sql("SELECT * FROM ProjectMembers", conn))
        conn.commit()
        conn.close()

    def remove_members(self, project_name: str, username: str):
        """
        Remove a member from a project.

        Parameters:
            project_name (str): The name of the project.
            username (str): The username of the member to remove.
        """
        conn = sqlite3.connect("project.db")
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()
        try:
            project_member = (project_name, username)
            sql = """ DELETE FROM ProjectMembers WHERE PROJECT_NAME = (?) AND USERNAME = (?) """
            cur.execute(sql, project_member)
            print('PROJECT MEMBERS  REMOVE')
            print(pd.read_sql("SELECT * FROM ProjectMembers", conn))
            conn.commit()
            conn.close()

        except Exception as e:
            print("Error removing members from project:", e)

    def get_project_task_count(self, project_id: int) -> int:
        """
        Get the count of tasks assigned to a project.

        Parameters:
            project_id (int): The ID of the project.

        Returns:
            int: The count of tasks assigned to the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        # Count tasks assigned to project
        try:
            sql = "SELECT COUNT(TASK_ID) FROM Tasks WHERE PROJECT_ID = (?)"
            cur.execute(sql, [project_id])
            c = cur.fetchone()
            count = c[0]
            conn.commit()
            conn.close()
            return count
        except Exception as e:
            print("Error getting project task count:", e)

    def get_project_completed_task_count(self, project_id: int) -> int:
        """
        Get the count of completed tasks assigned to a project.

        Parameters:
            project_id (int): The ID of the project.

        Returns:
            int: The count of completed tasks assigned to the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        # Count tasks assigned to project
        try:
            sql = "SELECT COUNT(TASK_ID) FROM Tasks WHERE PROJECT_ID = (?) AND STATUS = 'Completed'"
            cur.execute(sql, [project_id])
            com = cur.fetchone()
            completed = com[0]
            conn.commit()
            conn.close()
            return completed
        except Exception as e:
            print("Error getting project completed task count:", e)

    def update_percentage_complete(self, project_name: str):
        """
        Update the percentage completion of a project based on its tasks completed.

        Parameters:
            project_name (str): The name of the project.
        """
        print('running update percentage complete')

        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        project_id = self.get_project_id(project_name)
        count = self.get_project_task_count(project_id)
        completed = self.get_project_completed_task_count(project_id)
        print(f'project_id {project_id} count {count} completed {completed}')
        try:
            perc = completed / count * 100
        except ZeroDivisionError:
            perc = 0
        print('percent {perc}')
        # Insert new percentage complete
        sql = "UPDATE Project SET PERCENTAGE_COMPLETE = (?) WHERE PROJECT_ID = (?)"
        cur.execute(sql, [perc, project_id])
        print(pd.read_sql("SELECT * FROM Project", conn))
        conn.commit()
        conn.close()

    def get_description(self, project_id: int) -> str:
        """
        Get the description of a project.

        Parameters:
            project_id (int): The ID of the project.

        Returns:
            str: The description of the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT DESCRIPTION FROM Project WHERE PROJECT_ID = (?)"
        cur.execute(sql, [project_id])
        try:
            des = cur.fetchone()[0]
            conn.commit()
            conn.close()
            return des
        except:
            print('No description found')
            conn.commit()
            conn.close()

    def check_owner(self, user: str, project_id: int) -> bool:
        """
        Check if a user is the owner of a project.

        Parameters:
            user (str): The username of the user.
            project_id (int): The ID of the project.

        Returns:
            bool: True if the user is the owner, False otherwise.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT OWNER FROM Project WHERE PROJECT_ID = (?)"
        cur.execute(sql, [project_id])
        per = cur.fetchone()
        print(per)
        if per is None:
            pass
        else:
            per = per[0]
        print(per, user)
        conn.commit()
        conn.close()
        if per == user:
            print('You are the one')
            return True
        else:
            print('Imposter')
            return False

    def create_project_message(self, project_name: str, message: str):
        """
        Create a message associated with a project.

        Parameters:
            project_name (str): The name of the project.
            message (str): The message content.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        username = Login.current_user
        project_id = self.get_project_id(project_name)
        try:
            project = (project_id, message, username)
            sql = ''' INSERT INTO ProjectMessages (PROJECT_ID, MESSAGE, USERNAME)
                            VALUES(?,?,?) '''
            cur.execute(sql, project)
            print('PROJECT  message create')
            print(pd.read_sql("SELECT * FROM ProjectMessages", conn))
            conn.commit()
            conn.close()
        except Exception as e:
            print('Error creating project message', e)

    def create_timeline(self, project_name: str):
        """
        Create a timeline plot for a project based on its messages.

        Parameters:
            project_name (str): The name of the project.

        Returns:
            fig: The matplotlib figure object.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT  MESSAGE, DATE_ADDED  FROM ProjectMessages pm INNER JOIN Project p on p.PROJECT_ID = pm.PROJECT_ID WHERE p.PROJECT_NAME = (?)"
        cur.execute(sql, [project_name])
        all_messages = cur.fetchall()
        messages = []
        dates = []
        start_date = self.get_project_start_date(project_name)
        end_date = self.get_project_end_date(project_name)
        for message, date in all_messages:
            messages.append(message)
            dates.append(pd.to_datetime(date))

        # Calculate levels for the stem plot
        levels = np.linspace(0, 1, len(dates))

        # Create the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot vertical lines representing messages
        ax.vlines(dates, ymin=0, ymax=levels, color='lightgray', linewidth=1, alpha=0.7)

        # Annotate each message with its text
        for d, l, r in zip(dates, levels, messages):
            ax.text(d, l, r, fontsize=10, ha='left', va='center', color='black')

        # Set plot title and axis labels
        ax.set(title=f'Timeline of {project_name}',
               xlabel='Date', ylabel='')

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
        return fig

    def get_project_start_date(self, project_id: int) -> datetime:
        """
        Get the start date of a project.

        Parameters:
            project_id (int): The ID of the project.

        Returns:
            datetime: The start date of the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """       SELECT strftime('%Y-%m-%d %H:%M:%S', START_DATE) AS START_DATE
                        FROM Project WHERE PROJECT_ID = (?)"""
        cur.execute(sql, [project_id])
        per = cur.fetchone()
        if per is None:
            start_date = datetime.now()
        else:
            start_date = datetime.strptime(per[0], '%Y-%m-%d %H:%M:%S')
        conn.commit()
        conn.close()
        return start_date

    def get_project_end_date(self, project_id: int) -> datetime:
        """
        Get the end date of a project.

        Parameters:
            project_id (int): The ID of the project.

        Returns:
            datetime: The end date of the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """       SELECT strftime('%Y-%m-%d %H:%M:%S', END_DATE) AS END_DATE
                        FROM Project WHERE PROJECT_ID = (?)"""
        cur.execute(sql, [project_id])
        per = cur.fetchone()
        if per is None:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(per[0], '%Y-%m-%d %H:%M:%S')
        conn.commit()
        conn.close()
        return end_date

    def set_project_start_date(self, project_name: str):
        """
        Set the start date of a project.

        Parameters:
            project_name (str): The name of the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """       UPDATE Project 
                        SET START_DATE = CURRENT_TIMESTAMP 
                        WHERE PROJECT_NAME = (?)"""
        cur.execute(sql, [project_name])
        conn.commit()
        conn.close()

    def set_project_end_date(self, project_name: str):
        """
        Set the end date of a project.

        Parameters:
            project_name (str): The name of the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """       UPDATE Project 
                        SET END_DATE = CURRENT_TIMESTAMP 
                        WHERE PROJECT_NAME = (?)"""
        cur.execute(sql, [project_name])
        conn.commit()
        conn.close()

    def update_start_and_end_dates(self, project_name: str, status: str):
        """
        Update the start and end dates of a project based on its status.

        Parameters:
            project_name (str): The name of the project.
            status (str): The status of the project.
        """
        try:
            current_status = self.get_project_status(project_name)
            print('current status')
            print(current_status)
            print('new status')
            print(status)
            if current_status == 'Not Started' and status == 'In-Progress':
                self.set_project_start_date(project_name)
            elif current_status == 'In-Progress' and status == 'Completed':
                self.set_project_end_date(project_name)
            elif current_status == 'Not Started' and status == 'Completed':
                self.set_project_start_date(project_name)
                self.set_project_end_date(project_name)
            elif current_status == 'Completed' and status == 'In-Progress':
                self.delete_project_end_date(project_name)

        except sqlite3.Error as e:
            print("Error updating start and end dates :", e)
    def set_project_status(self, project_name: str, status: str):
        """
        Set the status of a project.

        Parameters:
            project_name (str): The name of the project.
            status (str): The status to set for the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """       UPDATE Project 
                        SET STATUS = (?) 
                        WHERE PROJECT_NAME = (?)"""
        cur.execute(sql, [status, project_name])
        conn.commit()
        conn.close()

    def get_project_status(self, project_name: str) -> str:
        """
        Get the status of a project.

        Parameters:
            project_name (str): The name of the project.

        Returns:
            str: The status of the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """       SELECT STATUS 
                        FROM Project 
                        WHERE PROJECT_NAME = (?)"""
        cur.execute(sql, [project_name])
        status = cur.fetchone()[0]
        conn.commit()
        conn.close()
        return status

    def delete_project_end_date(self, project_name: str):
        """
        Delete the end date of a project.

        Parameters:
            project_name (str): The name of the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """       UPDATE Project 
                        SET END_DATE = NULL 
                        WHERE PROJECT_NAME = (?)"""
        cur.execute(sql, [project_name])
        conn.commit()
        conn.close()

    def delete_project(self, project_name: str):
        """
        Delete a project from the database.

        Parameters:
            project_name (str): The name of the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """       DELETE FROM Project 
                        WHERE PROJECT_NAME = (?)"""
        cur.execute(sql, [project_name])
        print(pd.read_sql("SELECT * FROM Project", conn))
        conn.commit()
        conn.close()

    def get_project_messages(self, project_name: str) -> list:
        """
        Get all messages associated with a project.

        Parameters:
            project_name (str): The name of the project.

        Returns:
            list: A list of messages associated with the project.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """       SELECT MESSAGE, USERNAME, DATE_ADDED
                        FROM ProjectMessages pm 
                        INNER JOIN Project p ON p.PROJECT_ID = pm.PROJECT_ID 
                        WHERE p.PROJECT_NAME = (?)"""
        cur.execute(sql, [project_name])
        messages = cur.fetchall()
        conn.commit()
        conn.close()
        return messages
