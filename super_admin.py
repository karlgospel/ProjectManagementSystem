import re
from team_member import TeamMember
from login import Login
import sqlite3
import bcrypt
import pandas as pd
import datetime

class SuperAdmin(TeamMember):
    """
    Class representing a super admin in a project management system.

    Attributes:
        None

    Methods:
        create_login(username, password, email, is_admin):
            Creates a new login for a user.
        set_project_start_date(projectName):
            Sets the start date for a project.
    """

    def create_login(self, username: str, password: str, email: str, is_admin: int) -> str:
        """
        Creates a new login for a user.

        Parameters:
            username (str): The username of the user.
            password (str): The password for the user.
            email (str): The email address of the user.
            is_admin (int): Flag indicating if the user is an admin (1 for admin, 0 for regular user).

        Returns:
            str: A message indicating the outcome of the operation.
        """
        # Validate email
        if not self.validate_email(email):
            return 'Invalid email address'

        l = Login()
        # Check password is not empty
        if not password:
            return 'Please enter a valid password'
        # Confirm username is not taken
        if l.check_username_distinct(username):
            pass
        else:
            return 'Username is already taken'

        # Connect to the database
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()

        # Hash the password
        hashable_password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(hashable_password, bcrypt.gensalt())

        # Insert login details into the database
        login_details = (username, hashed_password, is_admin, email)
        sql = ''' INSERT INTO Login(USERNAME, PASSWORD, ADMIN, EMAIL)
                VALUES(?,?,?,?) '''
        try:
            cur.execute(sql, login_details)
            conn.commit()
            conn.close()
        except Exception as e:
            return 'Invalid details'

    def validate_email(self,email: str) -> bool:
        """
        Validates an email address.

        Parameters:
            email (str): The email address to be validated.

        Returns:
            bool: True if the email address is valid, False otherwise.
        """
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False
        return True

    def set_project_start_date(self, projectName: str) -> None:
        """
        Sets the start date for a project.

        Parameters:
            projectName (str): The name of the project.

        Returns:
            None
        """
        # Connect to the database
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()

        # Get the current datetime
        now = datetime.datetime.now()

        # Update the project start date in the database
        sd = (now, projectName)
        sql = "UPDATE Project SET START_DATE = (?) WHERE PROJECT_NAME = (?)"
        cur.execute(sql, sd)
        print(pd.read_sql("SELECT * FROM Project", conn))

        # Commit changes and close connection
        conn.commit()
        conn.close()
