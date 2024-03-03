from login import Login
import pandas as pd
import sqlite3
import bcrypt


class TeamMember:
    """
    Class representing a team member in a project management system.

    Attributes:
        None

    Methods:
        change_password(username, old_password, new_password):
            Changes the password of a team member.
        is_admin(username):
            Checks if the specified user is an admin.
    """

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """
        Changes the password of a team member.

        Parameters:
            username (str): The username of the team member.
            old_password (str): The old password.
            new_password (str): The new password.

        Returns:
            Boolean: True if password change successful, false otherwise
        """
        # Instantiate a Login object
        l = Login()

        # Check if the old password matches the current password
        if l.check_password(username, old_password):
            pass
        else:
            return False

        # Connect to the database
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()

        # Hash the new password
        hashable_password = new_password.encode('utf-8')
        hashed_password = bcrypt.hashpw(hashable_password, bcrypt.gensalt())

        # Update the password in the database
        new_login_details = (hashed_password, username)
        sql = ''' UPDATE Login SET PASSWORD = (?) WHERE USERNAME = (?)'''
        try:
            cur.execute(sql, new_login_details)

            # Commit changes and close connection
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print('Error changing password', e)

    def is_admin(self, username: str) -> bool:
        """
        Checks if the specified user is an admin.

        Parameters:
            username (str): The username of the team member.

        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        # Connect to the database
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()

        # Retrieve admin status from the database
        sql = "SELECT ADMIN FROM Login WHERE USERNAME = (?)"
        cur.execute(sql, [username])
        x = cur.fetchone()
        user = x[0]

        # Check if the user is an admin
        if user == 1:
            conn.commit()
            conn.close()
            return True
        else:
            conn.commit()
            conn.close()
            return False
