import sqlite3
import pandas as pd
from datetime import datetime
from project import Project


class Task:

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

    def get_task(self, taskID):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """   SELECT  t.TASK_NAME
                            FROM Tasks t 
                            WHERE t.TASK_ID = (?)"""
        cur.execute(sql, [taskID])
        task = cur.fetchone()
        task = task[0]
        conn.commit()
        conn.close()
        return task

    def update_task_start_and_end_dates(self, task_id, status):
        # Set start and end dates based on if status has been updated
        # Users options are limited to minimise errors
        try:
            current_status = self.get_status(task_id)
            if current_status == 'Not Started' and status == 'In-Progress':
                self.set_start_date(task_id)
            elif current_status == 'In-Progress' and status == 'Completed':
                self.set_end_date(task_id)
            elif current_status == 'Not Started' and status == 'Completed':
                self.set_start_date(task_id)
                self.set_end_date(task_id)
            elif current_status == 'Completed' and status == 'In-Progress':
                self.delete_task_end_date(task_id)
        except sqlite3.Error as e:
            print("Error updating task start and end dates:", e)

    def get_project_for_task(self, task_id):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """   SELECT p.PROJECT_NAME 
                    FROM Tasks t
                    INNER JOIN Project p
                    ON p.PROJECT_ID = t.PROJECT_ID
                    WHERE t.TASK_ID = (?)
        """

        cur.execute(sql, [task_id])
        project_name = cur.fetchone()[0]
        conn.commit()
        conn.close()
        return project_name

    def edit_task(self, task_id, task_name, description, status, progress, assigned, comment):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()

        try:
            if status == 'Completed':
                self.set_task_percent_complete(task_id, 100)
            else:
                self.set_task_percent_complete(task_id, progress)
            self.update_task_start_and_end_dates(task_id, status)
            task_details = (task_name, description, status, assigned, comment, task_id)
            sql = """UPDATE Tasks 
                        SET TASK_NAME = (?), 
                        DESCRIPTION = (?), 
                        STATUS = (?), 
                        ASSIGNED_TO = (?),
                        COMMENT = (?)
                        WHERE TASK_ID = (?)
                        """
            cur.execute(sql, task_details)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error editing task:", e)
            conn.commit()
            conn.close()

    def set_task_percent_complete(self, task_id, progress):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        try:
            completed = (progress, task_id)

            sql = """ UPDATE Tasks 
                        SET PERCENTAGE_COMPLETE = (?) 
                        WHERE TASK_ID = (?)
                        """
            cur.execute(sql, completed)
            print(pd.read_sql("SELECT * FROM Tasks", conn))
            conn.commit()
            conn.close()
        except Exception as e:
            print("Error setting task percent complete :", e)

    def set_start_date(self, task_id):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        try:
            new_date = (datetime.now(), task_id)

            sql = """ UPDATE Tasks 
                        SET START_DATE = (?) 
                        WHERE TASK_ID = (?)
                        """

            cur.execute(sql, new_date)
            print(pd.read_sql("SELECT * FROM Tasks", conn))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error setting task start date:", e)
            conn.commit()
            conn.close()
    def set_end_date(self, task_id):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        try:
            new_date = (datetime.now(), task_id)

            sql = """ UPDATE Tasks 
                        SET END_DATE = (?) 
                        WHERE TASK_ID = (?)
                        """
            cur.execute(sql, new_date)
            print(pd.read_sql("SELECT * FROM Tasks", conn))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error setting task end date:", e)
            conn.commit()
            conn.close()

    def delete_task_end_date(self, task_id):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """   UPDATE Tasks 
                    SET END_DATE = NULL
                    WHERE TASK_ID = (?)"""
        cur.execute(sql, [task_id])
        conn.commit()
        conn.close()

    def add_comment(self, comment, task_id, username):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()

        new_comment = (comment, task_id, username)
        sql = ''' INSERT INTO TaskMessages (MESSAGE, TASK_ID, USERNAME)
                                VALUES(?,?,?) '''
        try:
            cur.execute(sql, new_comment)
            print('TASK MESSAGE  ADD')
            print(pd.read_sql("SELECT * FROM TaskMessages", conn))
            conn.commit()
            conn.close()
        except Exception as e:
            print('Error adding task comment', e)
            return False


    def get_all_tasks(self, projectName):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """SELECT t.TASK_ID,
                        t.TASK_NAME, 
                        t.DESCRIPTION, 
                        t.ASSIGNED_TO, 
                        t.STATUS, 
                        strftime('%Y-%m-%d %H:%M:%S', t.START_DATE) AS START_DATE, 
                        t.END_DATE, 
                        t.PERCENTAGE_COMPLETE, 
                        t.COMMENT
                        FROM Tasks t 
                        INNER JOIN Project p ON p.PROJECT_ID = t.PROJECT_ID
                        WHERE p.PROJECT_NAME = (?)"""
        cur.execute(sql, [projectName])
        tasks = cur.fetchall()
        conn.commit()
        conn.close()
        return tasks

    def get_percentage_complete(self, taskID):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT PERCENTAGE_COMPLETE FROM Tasks WHERE TASK_ID = (?)"
        cur.execute(sql, taskID)
        per = cur.fetchone()
        percentage = per[0]
        conn.commit()
        conn.close()
        return percentage

    def set_percentage_complete(self, perc, taskID):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        percent_complete = (perc, taskID)
        # Insert new percentage complete
        sql = "UPDATE Tasks SET PERCENTAGE_COMPLETE = (?) WHERE TASK_ID = (?)"
        cur.execute(sql, percent_complete)
        print(pd.read_sql("SELECT * FROM Tasks", conn))
        conn.commit()
        conn.close()

    def get_status(self, task_id):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT STATUS FROM Tasks WHERE TASK_ID = (?)"
        try:
            cur.execute(sql, (task_id,))
            per = cur.fetchone()
            status = per[0]
            conn.commit()
            conn.close()
            return status
        except sqlite3.Error as e:
            print("Error fetching task status:", e)
            conn.commit()
            conn.close()


    def set_status(self, status, taskID):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        new_status = (status, taskID)
        # Insert new percentage complete
        sql = "UPDATE Tasks SET STATUS = (?) WHERE TASK_ID = (?)"
        cur.execute(sql, new_status)
        conn.commit()
        conn.close()
        if status == 'Complete':
            self.set_percentage_complete(100, taskID)

    def get_description(self, taskID):
        """Get the description of a task."""
        try:
            conn = sqlite3.connect('project.db')
            cur = conn.cursor()
            sql = "SELECT description FROM tasks WHERE TASK_ID = ?"
            cur.execute(sql, (taskID,))
            description_tuple = cur.fetchone()
            if description_tuple:
                description = description_tuple[0]
                conn.close()
                return description
            else:
                conn.close()
                return
            conn.close()
            return description
        except sqlite3.Error as e:
            print("Error fetching task description:", e)

    def set_description(self, taskID, desc):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        new_desc = ( desc, taskID)
        # Insert new percentage complete
        sql = "UPDATE Tasks SET DESCRIPTION = (?) WHERE TASK_ID = (?)"
        cur.execute(sql, new_desc)
        print(pd.read_sql("SELECT * FROM Tasks", conn))
        conn.commit()
        conn.close()

    def assign_task(self, taskID, username):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        assign = (username, taskID)
        # Insert new percentage complete
        sql = "UPDATE Tasks SET ASSIGNED_TO = (?) WHERE TASK_ID = (?)"
        cur.execute(sql, assign)
        print(pd.read_sql("SELECT * FROM Tasks", conn))
        conn.commit()
        conn.close()

    def is_assigned_to(self, task_id):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT ASSIGNED_TO FROM Tasks WHERE TASK_ID = (?)"
        try:
            cur.execute(sql, (task_id,))
            per = cur.fetchone()
            per = per[0]
            conn.commit()
            conn.close()
            return per
        except Exception as e:
            print("Error fetching is assigned to :", e)
            conn.commit()
            conn.close()

    def get_owner_from_task(self, task_id):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """   SELECT p.OWNER 
                    FROM Tasks t
                    INNER JOIN Project p ON p.PROJECT_ID = t.PROJECT_ID
                    WHERE TASK_ID = (?)"""
        try:
            cur.execute(sql, [task_id])
            per = cur.fetchone()
            per = per[0]
            conn.commit()
            conn.close()
            return per
        except Exception as e:
            print("Error fetching owner from task:", e)
            conn.commit()
            conn.close()


