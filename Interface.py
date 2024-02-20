import tkinter as tk
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import filedialog
from os import path
from tkinter import Menu
import tkinter.scrolledtext
from tkinter import simpledialog
from ProjectManager import ProjectManager as pm
from Project import Project
from Login import Login
from tkcalendar import Calendar

from Task import Task
from TeamMember import TeamMember


class LoginPage(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Login Page")
        # Calculate screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Calculate login window dimensions
        login_width = 250
        login_height = 150

        # Calculate login window position
        x = (screen_width - login_width) // 2
        y = (screen_height - login_height) // 2
        self.geometry(f"{login_width}x{login_height}+{x}+{y}")
        # Create username label and entry
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack(padx=10, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(padx=10, pady=5)

        # Create password label and entry
        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack(padx=10, pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(padx=10, pady=5)

        # Create login button
        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack(padx=10, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(username)
        print(password)
        l = Login()
        validation = l.check_password(username, password)
        print(validation)
        if validation == True:
            global current_user
            self.withdraw()  # Hide the login window upon successful login
            self.destroy()  # Close the login window
            MainPage(self.master)  # Open the main page
            current_user = username
            print(current_user)
        else:
            messagebox.showerror("Login", "Invalid username or password")


class MainPage(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=None)
        self.title("Project Manager")
        self.geometry("800x600")  # Adjust the initial window size as needed

        # Create the notebook
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=True, fill='both')

        # Create the tabs
        self.ListTab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.ListTab, text='List')

        self.TasksTab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.TasksTab, text='Tasks')

        self.TimelineTab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.TimelineTab, text='Timeline')

        self.Login = ttk.Frame(self.tab_control)
        self.tab_control.add(self.Login, text='Login')

        ####------------------ LIST TAB --------------------------###

        # Create buttons in the ListTab
        self.add_project_button = tk.Button(self.ListTab, text=" + New Project ", command=self.add_project_popup)
        self.add_project_button.grid(row=0, column=0, padx=2, pady=5)

        self.show_name_button = tk.Button(self.ListTab, text=" Add / Assign Tasks ", command=self.add_tasks_popup)
        self.show_name_button.grid(row=0, column=1, padx=2, pady=5)

        # Create Search bar in ListTab
        self.search_label = tk.Label(self.ListTab, text="Search:")
        self.search_label.grid(row=0, column=2, padx=2, pady=5, sticky="e")
        self.search_entry = tk.Entry(self.ListTab)
        self.search_entry.grid(row=0, column=3, padx=2, pady=5, sticky="we")
        self.search_entry.bind("<KeyRelease>", self.search_projects)

        # Create table to display all projects
        self.project_tree = ttk.Treeview(self.ListTab, columns=(
            "Project Name", "Description", "Owner", "Status", "Start Date", "End Date", "Progress"))
        self.project_tree['show'] = 'headings'

        self.project_tree.heading("Project Name", text="Project Name",
                                  command=lambda: self.treeview_sort_column(self.project_tree, "Project Name", False))
        self.project_tree.heading("Description", text="Description",
                                  command=lambda: self.treeview_sort_column(self.project_tree, "Description", False))
        self.project_tree.heading("Owner", text="Owner",
                                  command=lambda: self.treeview_sort_column(self.project_tree, "Owner", False))
        self.project_tree.heading("Status", text="Status",
                                  command=lambda: self.treeview_sort_column(self.project_tree, "Status", False))
        self.project_tree.heading("Start Date", text="Start Date",
                                  command=lambda: self.treeview_sort_column(self.project_tree, "Start Date", False))
        self.project_tree.heading("End Date", text="End Date",
                                  command=lambda: self.treeview_sort_column(self.project_tree, "End Date", False))
        self.project_tree.heading("Progress", text="Progress",
                                  command=lambda: self.treeview_sort_column(self.project_tree, "Progress", False))

        self.project_tree.grid(row=1, column=0, sticky="nsew", columnspan=4)

        self.scrollbar = ttk.Scrollbar(self.ListTab, orient="vertical", command=self.project_tree.yview)
        self.scrollbar.grid(row=1, column=4, sticky='ns')
        self.project_tree.configure(yscrollcommand=self.scrollbar.set)

        self.ListTab.rowconfigure(1, weight=1)
        self.ListTab.columnconfigure(0, weight=1)
        self.ListTab.columnconfigure(1, weight=1)

        self.show_all_project_info()

        ####------------------ TASKS TAB --------------------------###

        # Create buttons in tasks tab
        tk.Label(self.TasksTab, text=" Select Project: ").grid(row=0, column=0, padx=5, pady=5)
        self.tasks = self.show_project_list()

        self.tasks = ttk.Combobox(self.TasksTab, values=self.tasks, state="readonly")
        self.tasks.grid(row=0, column=1, padx=5, pady=5)
        self.tasks.bind("<<ComboboxSelected>>", self.update_task_treeview)

        self.add_task_button = tk.Button(self.TasksTab, text=" + New Task ", command=self.add_tasks_popup)
        self.add_task_button.grid(row=0, column=2, padx=2, pady=5)

        self.edit_task_button = tk.Button(self.TasksTab, text=" Edit Task ", command=self.edit_task_popup)
        self.edit_task_button.grid(row=0, column=3, padx=2, pady=5)

        self.assign_task_button = tk.Button(self.TasksTab, text=" Assign Task ", command=self.assign_task_popup)
        self.assign_task_button.grid(row=0, column=4, padx=2, pady=5)

        # Create table to display all TASKS
        self.task_tree = ttk.Treeview(self.TasksTab, columns=(
            "Task ID", "Task Name", "Description", "Assigned", "Status", "Start Date", "End Date", "Progress",
            "Comments"))
        self.task_tree['show'] = 'headings'

        self.task_tree.heading("Task ID", text="Task ID",
                               command=lambda: self.treeview_sort_column(self.task_tree, "Task ID", False))
        self.task_tree.column("Task ID", width=50)
        self.task_tree.heading("Task Name", text="Task Name",
                               command=lambda: self.treeview_sort_column(self.task_tree, "Task Name", False))
        self.task_tree.heading("Description", text="Description",
                               command=lambda: self.treeview_sort_column(self.task_tree, "Description", False))
        self.task_tree.heading("Assigned", text="Assigned",
                               command=lambda: self.treeview_sort_column(self.task_tree, "Assigned", False))
        self.task_tree.heading("Status", text="Status",
                               command=lambda: self.treeview_sort_column(self.task_tree, "Status", False))
        self.task_tree.heading("Start Date", text="Start Date",
                               command=lambda: self.treeview_sort_column(self.task_tree, "Start Date", False))
        self.task_tree.heading("End Date", text="End Date",
                               command=lambda: self.treeview_sort_column(self.task_tree, "End Date", False))
        self.task_tree.heading("Progress", text="Progress",
                               command=lambda: self.treeview_sort_column(self.task_tree, "Progress", False))
        self.task_tree.heading("Comments", text="Comments",
                               command=lambda: self.treeview_sort_column(self.task_tree, "Comments", False))
        self.task_tree.column("Progress", width=100)
        self.task_tree.grid(row=1, column=0, sticky="nsew", columnspan=4)

        self.scrollbar = ttk.Scrollbar(self.ListTab, orient="vertical", command=self.task_tree.yview)
        self.scrollbar.grid(row=1, column=4, sticky='ns')
        self.task_tree.configure(yscrollcommand=self.scrollbar.set)

        self.ListTab.rowconfigure(1, weight=1)
        self.ListTab.columnconfigure(0, weight=1)
        self.ListTab.columnconfigure(1, weight=1)

    def edit_task_popup(self):
        # Get the currently selected task
        current_task_selected = self.task_tree.focus()
        selected_task = self.task_tree.item(current_task_selected)

        if not selected_task:
            messagebox.showerror("Error", "Please select a task.")
            return
        task_id = selected_task["values"][0]

        # Extract the selected project from the combobox
        selected_project = self.tasks.get()

        # Open a new popup window for editing the task
        popup = tk.Toplevel(self)
        popup.title("Edit Task")

        # Labels and entry fields for task details
        tk.Label(popup, text="Task Name:").grid(row=0, column=0, padx=5, pady=5)
        self.task_name_entry = tk.Entry(popup)
        self.task_name_entry.insert(0, selected_task["values"][1])  # Insert the current task name
        self.task_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(popup, text="Status:").grid(row=1, column=0, padx=5, pady=5)
        self.task_status_entry = ttk.Combobox(popup, values=["In-Progress", "Completed"], state="readonly")
        self.task_status_entry.grid(row=1, column=1, padx=5, pady=5)
        self.task_status_entry.set(selected_task["values"][4])  # Set the current status

        tk.Label(popup, text="Description:").grid(row=2, column=0, padx=5, pady=5)
        self.task_description_entry = tk.Text(popup, height=5, width=30)
        self.task_description_entry.grid(row=2, column=1, padx=5, pady=5)
        self.task_description_entry.insert("1.0", selected_task["values"][2])  # Insert the current description

        tk.Label(popup, text="Progress:").grid(row=3, column=0, padx=5, pady=5)
        self.progress = Spinbox(popup, font=('Arial', 14), from_=0, to=100, width=5)
        self.progress.grid(column=1, row=4, padx=40, pady=10)
        self.progress.set(selected_task["values"][7])

        tk.Label(popup, text="Comments:").grid(row=5, column=0, padx=5, pady=5)
        self.comments_entry = tk.Text(popup, height=5, width=30)
        self.comments_entry.grid(row=6, column=1, padx=5, pady=5)
        self.comments_entry.insert("1.0", selected_task["values"][8])  # Insert the current description

        # Get project members for assignment
        self.project_members = self.get_project_members(selected_project)
        tk.Label(popup, text="Assign Task To:").grid(row=7, column=0, padx=5, pady=5)
        self.members_listbox = tk.Listbox(popup, height=10, width=30, selectmode=tk.MULTIPLE)
        for mem in self.project_members:
            self.members_listbox.insert(tk.END, mem)
        self.members_listbox.grid(row=8, column=1, padx=5, pady=5)
        scrollbar = tk.Scrollbar(
            popup,
            orient=tk.VERTICAL,
            command=self.members_listbox.yview)
        self.members_listbox['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=9, column=2, sticky='ns')

        # Button to edit task
        self.save_button = tk.Button(popup, text="Save Changes",
                                     command=lambda: self.save_edit_task(self.task_name_entry.get(),
                                                                        task_id,
                                                                        self.task_status_entry.get(),
                                                                        self.progress.get(),
                                                                        self.task_description_entry.get("1.0",
                                                                                                        "end-1c"),
                                                                        self.comments_entry.get("1.0",
                                                                                                "end-1c"),
                                                                        popup))
        self.save_button.grid(row=10, columnspan=2, padx=5, pady=10)

    def save_edit_task(self, task_name, task_id, status, progress, description, comment, popup):
        if not (task_name and status and description and task_id and self.members_listbox.curselection()):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        try:
            t = Task()
            assigned = []
            for i in self.members_listbox.curselection():
                x = self.members_listbox.get(i)
                assigned.append(x)
            ass = [x for x in assigned]
            assigned_to = ass[0]
            print('assigned to')

            t.edit_task(task_id, task_name, description, status, progress, assigned_to, comment)
            self.update_task_treeview()
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")



    def update_timeline(self, project_name):
        pass

    def update_task_treeview(self, *event):
        selected_project = self.tasks.get()
        self.task_tree.delete(*self.task_tree.get_children())  # Clear existing data
        if selected_project:
            t = Task()
            tasks_for_project = t.get_all_tasks(selected_project)
            # Insert tasks into the treeview
            for task in tasks_for_project:
                self.task_tree.insert("", "end", values=task)

    def assign_task_popup(self):
        self.selected_item = self.task_tree.selection()
        if not self.selected_item:
            messagebox.showerror("Error", "Please select a task.")
            return
        popup = tk.Toplevel(self)
        popup.title("Reassign Task")

    def optionMenu_projectSelection(self, project):
        # project = project_clicked.get()
        # self.update_percent_complete(project)
        # self.show_description(project)
        self.show_all_task_info()

    def optionMenu_statusSelection(self, status):
        self.status = self.status_clicked.get()
        print()

    def update_percent_complete(self, project):
        """ """
        self.percent = Project.get_percentage_complete(self, project)
        self.project_percent_box.config(state='normal')
        self.project_percent_box.delete(0, tk.END)
        self.project_percent_box.insert(0, self.percent)
        self.project_percent_box.config(state='readonly')

    def show_project_list(self):
        p = Project()
        self.all_projects = p.get_all_projects()
        return self.all_projects

    def show_all_project_info(self):
        p = Project()
        self.projects = p.get_all_project_info()
        for project in self.projects:
            self.project_tree.insert("", "end", values=project)

    # def show_all_task_info(self, projectName):
    #     t = Task()
    #     self.tasks = t.get_all_tasks(projectName)
    #     for task in self.tasks:
    #         self.task_tree.insert("", "end", values=task)
    def show_description(self, project):

        self.description = Project.get_description(project)
        self.description_text.delete('1.0', tk.END)  # Clear previous description
        self.description_text.insert(tk.END, self.description)

    def add_project_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Add New Project")

        # Labels and entry fields for project details
        tk.Label(popup, text="Project Name:").grid(row=0, column=0, padx=5, pady=5)
        self.project_name_entry = tk.Entry(popup)
        self.project_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(popup, text="Status:").grid(row=1, column=0, padx=5, pady=5)
        self.status_entry = ttk.Combobox(popup, values=["Not Started", "In-Progress"], state="readonly")
        self.status_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(popup, text="Description:").grid(row=2, column=0, padx=5, pady=5)
        self.description_entry = tk.Text(popup, height=5, width=30)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(popup, text="Owner:").grid(row=3, column=0, padx=5, pady=5)
        self.owner_options = self.get_usernames()
        self.owner_entry = ttk.Combobox(popup, values=self.owner_options, state="readonly")
        self.owner_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(popup, text="Project Members:").grid(row=4, column=0, padx=5, pady=0)
        self.members_listbox = tk.Listbox(popup, selectmode=tk.MULTIPLE, height=20, width=30)
        for owner in self.owner_options:
            self.members_listbox.insert(tk.END, owner)
        self.members_listbox.grid(row=4, column=1, padx=5, pady=5)
        scrollbar = tk.Scrollbar(
            popup,
            orient=tk.VERTICAL,
            command=self.members_listbox.yview)
        self.members_listbox['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=4, column=2, sticky='ns')

        # Button to save new project
        self.save_button = tk.Button(popup, text="Save",
                                     command=lambda: self.save_new_project(self.project_name_entry.get(),
                                                                           self.status_entry.get(),
                                                                           self.description_entry.get("1.0", "end-1c"),
                                                                           self.owner_entry.get(),
                                                                           popup))
        self.save_button.grid(row=6, columnspan=2, padx=5, pady=10)

    def add_tasks_popup(self):
        self.selected_project = self.tasks.get()
        if not self.selected_project:
            messagebox.showerror("Error", "Please select a project.")
            return
        # self.selected_project = self.project_tree.item(self.selected_item, "values")[1]
        popup = tk.Toplevel(self)
        popup.title("Add New Tasks")

        # Labels and entry fields for project details
        tk.Label(popup, text="Task Name:").grid(row=0, column=0, padx=5, pady=5)
        self.task_name_entry = tk.Entry(popup)
        self.task_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(popup, text="Status:").grid(row=1, column=0, padx=5, pady=5)
        self.task_status_entry = ttk.Combobox(popup, values=["Not Started", "In-Progress"], state="readonly")
        self.task_status_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(popup, text="Description:").grid(row=2, column=0, padx=5, pady=5)
        self.task_description_entry = tk.Text(popup, height=5, width=30)
        self.task_description_entry.grid(row=2, column=1, padx=5, pady=5)

        self.project_members = self.get_project_members(self.selected_project)
        tk.Label(popup, text="Assign Task To:").grid(row=4, column=0, padx=5, pady=0)
        self.members_listbox = tk.Listbox(popup, height=10, width=30)
        for mem in self.project_members:
            self.members_listbox.insert(tk.END, mem)
        self.members_listbox.grid(row=4, column=1, padx=5, pady=5)
        scrollbar = tk.Scrollbar(
            popup,
            orient=tk.VERTICAL,
            command=self.members_listbox.yview)
        self.members_listbox['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=4, column=2, sticky='ns')

        # Button to save new task
        self.save_button = tk.Button(popup, text="Save",
                                     command=lambda: self.save_new_task(self.task_name_entry.get(),
                                                                        self.selected_project,
                                                                        self.task_status_entry.get(),
                                                                        self.task_description_entry.get("1.0",
                                                                                                        "end-1c"),
                                                                        popup))
        self.save_button.grid(row=6, columnspan=2, padx=5, pady=10)

    def save_new_task(self, task_name, project_name, status, description, popup):
        if not (task_name and status and description and project_name and self.members_listbox.curselection()):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        try:
            t = TeamMember()
            assigned = []
            for i in self.members_listbox.curselection():
                x = self.members_listbox.get(i)
                assigned.append(x)
            ass = [x for x in assigned]
            assigned_to = ass[0]
            print('assigned to')
            print(assigned_to)
            print(project_name, task_name, description, status, assigned_to)
            t.create_task(project_name, task_name, description, status, assigned_to)
            self.update_task_treeview()
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Function to save new project to the database and update Treeview
    def save_new_project(self, project_name, status, description, owner, popup):
        if not (project_name and status and description and owner and self.members_listbox.curselection()):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        try:

            t = TeamMember()
            t.create_project(project_name, owner, status, description)
            messagebox.showinfo("Success", "Project added successfully!")
            # self.selection = self.members_listbox.curselection()
            # print(self.selection)
            all_members = []
            for i in self.members_listbox.curselection():
                x = self.members_listbox.get(i)
                all_members.append(x)
            try:
                p = Project()
                p.add_members(project_name, all_members)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            try:
                p.send_project_emails(project_name)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            popup.destroy()
            self.update_treeview()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Function to update Treeview with new project
    def update_treeview(self):
        self.project_tree.delete(*self.project_tree.get_children())
        self.show_all_project_info()

    def get_usernames(self):
        l = Login()
        self.user_list = l.get_users()
        print(self.user_list)
        return self.user_list

    def get_project_members(self, projectName):
        p = Project()
        members = p.get_project_members(projectName)
        return members

    def search_projects(self, event):
        query = self.search_entry.get().lower()
        for child in self.project_tree.get_children():
            project_name = self.project_tree.item(child, "values")[1].lower()
            if query in project_name:
                self.project_tree.item(child, open=True)
                self.project_tree.selection_set(child)
            else:
                self.project_tree.item(child, open=False)
                self.project_tree.selection_remove(child)

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        # reverse sort next time
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))


def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window initially
    login_page = LoginPage(root)
    # main_page = MainPage(root)  # Create an instance of MainPage but keep it hidden initially
    root.mainloop()


if __name__ == '__main__':
    main()
