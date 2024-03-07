import sqlite3
from datetime import datetime
from project import Project
from team_member import TeamMember


class Task:
    """
    Class representing a task in a project management system.

    Attributes:
        None

    Methods:
        create_task(project_name, task_name, description, status, assigned):
            Creates a new task in the database with the provided details.
        get_task(task_id):
            Retrieves the name of the task corresponding to the given task ID.
        delete_task(task_id):
            Deletes the task from the database.
        update_task_start_and_end_dates(task_id, status):
            Updates the start and end dates of the task based on the provided status.
        get_project_for_task(task_id):
            Retrieves the project name associated with the given task ID.
        edit_task(task_id, task_name, description, status, progress, assigned, comment):
            Modifies the details of an existing task.
        check_task_access(username, task_id):
            Checks the access level of the current user for the given task.
        set_task_percent_complete(task_id, progress):
            Sets the percentage completion of the task.
        set_start_date(task_id):
            Sets the start date of the task.
        set_end_date(task_id):
            Sets the end date of the task.
        delete_task_end_date(task_id):
            Deletes the end date of the task.
        add_comment(comment, task_id, username):
            Adds a comment to the task with the given ID.
        get_all_tasks(projectName):
            Retrieves all tasks associated with the specified project.
        get_percentage_complete(task_id):
            Retrieves the percentage completion of the task.
        set_percentage_complete(perc, task_id):
            Sets the percentage completion of the task.
        get_status(task_id):
            Retrieves the status of the task.
        set_status(status, task_id):
            Sets the status of the task.
        get_description(task_id):
            Retrieves the description of the task.
        set_description(task_id, desc):
            Sets the description of the task.
        assign_task(task_id, username):
            Assigns the task to the specified user.
        is_assigned_to(task_id):
            Checks if the task is assigned to any user.
        get_owner_from_task(task_id):
            Retrieves the owner of the project associated with the given task.
    """

    def create_task(self, project_name: str, task_name: str, description: str, status: str, assigned: str) -> None:
        """
        Creates a new task in the database.

        Parameters:
            project_name (str): The name of the project to which the task belongs.
            task_name (str): The name of the task.
            description (str): Description of the task.
            status (str): Current status of the task.
            assigned (str): Username of the user to whom the task is assigned.

        Returns:
            None
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        p = Project()
        project_id = p.get_project_id(project_name)
        # Strip whitespace for task name
        task = (project_id, description, status, 0, assigned, task_name.strip())
        sql = ''' INSERT INTO Tasks (PROJECT_ID, DESCRIPTION, STATUS, PERCENTAGE_COMPLETE, ASSIGNED_TO, TASK_NAME)
                        VALUES(?,?,?,?,?,?) '''
        cur.execute(sql, task)
        conn.commit()
        conn.close()
        if status == 'In-Progress':
            self.set_start_date(cur.lastrowid)


    def get_task(self, task_id: int) -> str:
        """
        Retrieves the name of the task corresponding to the given task ID.

        Parameters:
            task_id (int): The ID of the task.

        Returns:
            str: The name of the task.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """   SELECT  t.TASK_NAME
                            FROM Tasks t 
                            WHERE t.TASK_ID = (?)"""
        cur.execute(sql, [task_id])
        task = cur.fetchone()
        task = task[0]
        conn.commit()
        conn.close()
        return task

    def delete_task(self,task_id):
        """
        Deletes the task from the database.

        Parameters:
         task_id (int): The ID of the task.

        Returns:
            None
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """DELETE FROM Tasks WHERE TASK_ID = (?)"""
        try:
            cur.execute(sql, [task_id])
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error deleting task:", e)
            conn.commit()
            conn.close()


    def update_task_start_and_end_dates(self, task_id: int, status: str) -> None:
        """
        Updates the start and end dates of the task based on the provided status.

        Parameters:
            task_id (int): The ID of the task.
            status (str): The new status of the task.

        Returns:
            None
        """
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

    def get_project_for_task(self, task_id: int) -> str:
        """
        Retrieves the project name associated with the given task ID.

        Parameters:
            task_id (int): The ID of the task.

        Returns:
            str: The name of the project associated with the task.
        """
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

    def edit_task(self, task_id: int, task_name: str, description: str, status: str, progress: int, assigned: str, comment: str) -> None:
        """
        Modifies the details of an existing task.

        Parameters:
            task_id (int): The ID of the task to be edited.
            task_name (str): New name for the task.
            description (str): New description for the task.
            status (str): New status for the task.
            progress (int): New progress percentage for the task.
            assigned (str): New user to whom the task is assigned.
            comment (str): New comment for the task.

        Returns:
            None
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()

        try:
            if status == 'Completed':
                self.set_task_percent_complete(task_id, 100)
            else:
                self.set_task_percent_complete(task_id, progress)
            self.update_task_start_and_end_dates(task_id, status)
            task_details = (task_name.strip(), description, status, assigned, comment, task_id)
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

    def check_task_access(self, username, task_id):
        """
        Checks the access level of the current user for the given task.

        Parameters:
            task_id (int): The ID of the task.
            username (str): The username of the user.

        Returns:
            str: The access level ('admin', 'owner', 'restricted') for the current user.
        """
        this_user = username
        tm = TeamMember()
        admin = tm.is_admin(this_user)
        assigned_to = self.is_assigned_to(task_id)
        owner = self.get_owner_from_task(task_id)
        if admin or (this_user == assigned_to):
            return 'admin'
        if owner == this_user:
            return 'owner'
        else:
            return 'restricted'
    def set_task_percent_complete(self, task_id: int, progress: int) -> None:
        """
        Sets the percentage completion of the task.

        Parameters:
            task_id (int): The ID of the task.
            progress (int): The new progress percentage.

        Returns:
            None
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        try:
            completed = (progress, task_id)

            sql = """ UPDATE Tasks 
                        SET PERCENTAGE_COMPLETE = (?) 
                        WHERE TASK_ID = (?)
                        """
            cur.execute(sql, completed)
            conn.commit()
            conn.close()
        except Exception as e:
            print("Error setting task percent complete :", e)

    def set_start_date(self, task_id: int) -> None:
        """
        Sets the start date of the task.

        Parameters:
            task_id (int): The ID of the task.

        Returns:
            None
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        try:
            new_date = (datetime.now(), task_id)

            sql = """ UPDATE Tasks 
                        SET START_DATE = (?) 
                        WHERE TASK_ID = (?)
                        """

            cur.execute(sql, new_date)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error setting task start date:", e)
            conn.commit()
            conn.close()

    def set_end_date(self, task_id: int) -> None:
        """
        Sets the end date of the task.

        Parameters:
            task_id (int): The ID of the task.

        Returns:
            None
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        try:
            new_date = (datetime.now(), task_id)

            sql = """ UPDATE Tasks 
                        SET END_DATE = (?) 
                        WHERE TASK_ID = (?)
                        """
            cur.execute(sql, new_date)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error setting task end date:", e)
            conn.commit()
            conn.close()

    def delete_task_end_date(self, task_id: int) -> None:
        """
        Deletes the end date of the task.

        Parameters:
            task_id (int): The ID of the task.

        Returns:
            None
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = """   UPDATE Tasks 
                    SET END_DATE = NULL
                    WHERE TASK_ID = (?)"""
        cur.execute(sql, [task_id])
        conn.commit()
        conn.close()

    def add_comment(self, comment: str, task_id: int, username: str) -> bool:
        """
        Adds a comment to the task with the given ID.

        Parameters:
            comment (str): The comment to be added.
            task_id (int): The ID of the task.
            username (str): The username of the user adding the comment.

        Returns:
            bool: True if the comment was added successfully, False otherwise.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()

        new_comment = (comment, task_id, username)
        sql = ''' INSERT INTO TaskMessages (MESSAGE, TASK_ID, USERNAME)
                                VALUES(?,?,?) '''
        try:
            cur.execute(sql, new_comment)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print('Error adding task comment', e)
            return False

    def get_all_tasks(self, projectName: str) -> list:
        """
        Retrieves all tasks associated with the specified project.

        Parameters:
            projectName (str): The name of the project.

        Returns:
            list: A list of tuples containing details of all tasks associated with the project.
        """
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

    def get_percentage_complete(self, task_id: int) -> int:
        """
        Retrieves the percentage completion of the task.

        Parameters:
            task_id (int): The ID of the task.

        Returns:
            int: The percentage completion of the task.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = "SELECT PERCENTAGE_COMPLETE FROM Tasks WHERE TASK_ID = (?)"
        cur.execute(sql, task_id)
        per = cur.fetchone()
        percentage = per[0]
        conn.commit()
        conn.close()
        return percentage

    def set_percentage_complete(self, perc: int, task_id: int) -> None:
        """
        Sets the percentage completion of the task.

        Parameters:
            perc (int): The new percentage completion.
            task_id (int): The ID of the task.

        Returns:
            None
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        percent_complete = (perc, task_id)
        # Insert new percentage complete
        sql = "UPDATE Tasks SET PERCENTAGE_COMPLETE = (?) WHERE TASK_ID = (?)"
        cur.execute(sql, percent_complete)
        conn.commit()
        conn.close()

    def get_status(self, task_id: int) -> str:
        """
        Retrieves the status of the task.

        Parameters:
            task_id (int): The ID of the task.

        Returns:
            str: The status of the task.
        """
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

    def set_status(self, status: str, task_id: int) -> None:
        """
        Sets the status of the task.

        Parameters:
            status (str): The new status of the task.
            task_id (int): The ID of the task.

        Returns:
            None
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        new_status = (status, task_id)
        # Insert new percentage complete
        sql = "UPDATE Tasks SET STATUS = (?) WHERE TASK_ID = (?)"
        cur.execute(sql, new_status)
        conn.commit()
        conn.close()
        if status == 'Complete':
            self.set_percentage_complete(100, task_id)

    def get_description(self, task_id: int) -> str:
        """
        Retrieves the description of the task.

        Parameters:
            task_id (int): The ID of the task.

        Returns:
            str: The description of the task.
        """
        try:
            conn = sqlite3.connect('project.db')
            cur = conn.cursor()
            sql = "SELECT description FROM tasks WHERE TASK_ID = ?"
            cur.execute(sql, (task_id,))
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

    def set_description(self, task_id: int, desc: str) -> None:
        """
        Sets the description of the task.

        Parameters:
            task_id (int): The ID of the task.
            desc (str): The new description for the task.

        Returns:
            None
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        new_desc = (desc, task_id)
        # Insert new percentage complete
        sql = "UPDATE Tasks SET DESCRIPTION = (?) WHERE TASK_ID = (?)"
        cur.execute(sql, new_desc)
        conn.commit()
        conn.close()

    def assign_task(self, task_id: int, username: str) -> None:
        """
        Assigns the task to the specified user.

        Parameters:
            task_id (int): The ID of the task.
            username (str): The username of the user to whom the task is assigned.

        Returns:
            None
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        assign = (username, task_id)
        # Insert new percentage complete
        sql = "UPDATE Tasks SET ASSIGNED_TO = (?) WHERE TASK_ID = (?)"
        cur.execute(sql, assign)
        conn.commit()
        conn.close()

    def is_assigned_to(self, task_id: int) -> str:
        """
        Checks if the task is assigned to any user.

        Parameters:
            task_id (int): The ID of the task.

        Returns:
            str: The username of the user to whom the task is assigned, or None if unassigned.
        """
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

    def get_owner_from_task(self, task_id: int) -> str:
        """
        Retrieves the owner of the project associated with the given task.

        Parameters:
            task_id (int): The ID of the task.

        Returns:
            str: The owner of the project associated with the task.
        """
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
