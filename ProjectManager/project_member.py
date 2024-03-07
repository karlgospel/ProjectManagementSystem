import sqlite3
from project import Project
class ProjectMember:
    """
            Class to handle project creation, editing, and retrieval.

            Attributes:
                None

            Methods:
                get_project_members(project_name):
                    Get the list of members associated with a project.
                add_members(project_name, *members):
                    Add members to a project.
                remove_members(project_name, username):
                    Remove a member from a project.
                is_project_member(username, project_name):
                    Check if a user is a member of a project.
        """
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
        p = Project()
        project_id = p.get_project_id(project_name)
        member_list = [x for x in members]
        member_list = member_list[0]
        for user in member_list:
            project_member = (project_name, user, project_id)
            sql = ''' INSERT INTO ProjectMembers (PROJECT_NAME, USERNAME, PROJECT_ID)
                            VALUES(?,?,?) '''
            cur.execute(sql, project_member)
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
            conn.commit()
            conn.close()

        except Exception as e:
            print("Error removing members from project:", e)

    def is_project_member(self, username, project_name):
        """
        Check if a user is a member of a project.

        Parameters:
            username (str): The username of the user.
            project_name (str): The name of the project.

        Returns:
            bool: True if the user is a member, False otherwise.
        """
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        sql = ''' SELECT * FROM ProjectMembers WHERE PROJECT_NAME = (?) AND USERNAME = (?) '''
        cur.execute(sql, [project_name, username])
        member = cur.fetchone()
        if member is not None:
            return True
        else:
            return False