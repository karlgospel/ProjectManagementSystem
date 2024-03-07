import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import sqlite3
import matplotlib.dates as mdates
from login import Login
from project import Project


class ProjectMessages:
    """
        Class to handle project creation, editing, and retrieval.

        Attributes:
            None

        Methods:
            create_project_message(project_name, message):
                Create a message associated with a project.
            get_project_messages(project_name):
                Get all messages associated with a project.
            create_timeline(project_name):
                Create a timeline plot for a project based on its messages.
    """

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
        p = Project()
        project_id = p.get_project_id(project_name)
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
        p = Project()
        start_date = p.get_project_start_date(project_name)
        end_date = p.get_project_end_date(project_name)
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