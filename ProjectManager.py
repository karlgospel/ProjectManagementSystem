
import tkinter as tk

import Project
from Project import *

class ProjectManager(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self,parent)
        self.project_percent_box = None
        self.status_clicked = None

    def optionMenu_projectSelection(self,project):
        #project = project_clicked.get()
        self.update_percent_complete(project)
        print()

    def optionMenu_statusSelection(self,status):
        status = self.status_clicked.get()
        print()

    def update_percent_complete(self,project):
        """ Updates the total cost of a material to be added to the database in the addJobTab"""
        #project = project_clicked.get()
        percent = Project.get_percentage_complete(self,project)
        print(percent)
        #Decimal(c).quantize(Decimal('.01'), rounding=ROUND_UP)
        self.project_percent_box.config(state='normal')
        self.project_percent_box.delete(0, tk.END)
        self.project_percent_box.insert(0, percent)
        self.project_percent_box.config(state='readonly')

    def show_project_list(self):
        all_projects = Project.get_all_projects()
        return all_projects