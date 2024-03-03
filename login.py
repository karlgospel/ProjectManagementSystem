import re
import bcrypt
import pandas as pd
import sqlite3

class Login:
    """
    Class to handle login and user creation.

    Attributes:
        current_user: str
            The username of the current user who is logged in.

    Methods:
        sign_in(username, password):
            Sign in a user with the given username and password.
        check_password(username, password):
            Check if the provided password matches the stored password for the given username.
        check_username_distinct(username):
            Check if the username is distinct (not already in use).
        get_users():
            Get a list of all usernames stored in the database.
    """

    current_user = None

    def sign_in(self, username: str, password: str) -> bool:
        """
        Sign in a user with the given username and password.

        Parameters:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool: True if sign-in is successful, False otherwise.
        """
        if self.check_password(username, password):
            Login.current_user = username
            return True
        else:
            return False

    def check_password(self, username: str, password: str) -> bool:
        """
        Check if the provided password matches the stored password for the given username.

        Parameters:
            username (str): The username of the user.
            password (str): The password to be checked.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = ("SELECT PASSWORD FROM Login WHERE USERNAME = (?)")
        try:
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
        except:
            return False

    def check_username_distinct(self, username: str) -> bool:
        """
        Check if the username is distinct (not already in use).

        Parameters:
            username (str): The username to be checked.

        Returns:
            bool: True if the username is distinct, False otherwise.
        """
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

    def get_users(self) -> list[str]:
        """
        Get a list of all usernames stored in the database.

        Returns:
            list: A list of usernames.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = ("SELECT USERNAME FROM Login")
        cur.execute(sql)
        usernames = [row[0] for row in cur.fetchall()]
        return usernames
