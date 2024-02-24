import tkinter as tk
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import ttk


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Email import Email
from Project import Project
from Login import Login


from SuperAdmin import SuperAdmin
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
        login_width = 260
        login_height = 260

        # Calculate login window position
        x = (screen_width - login_width) // 2
        y = (screen_height - login_height) // 2
        self.geometry(f"{login_width}x{login_height}+{x}+{y}")

        # Create a custom style for buttons
        style = ttk.Style()
        style.theme_use("clam")  # Use a pre-defined theme as a base

        # Configure buttons to be slightly bigger with bigger text
        style.configure("TButton", font=("Helvetica", 10, "bold"), padding=4)

        # Label for slogan
        slogan_label = tk.Label(self, text="TT Corp", font=("Stencil Std", 36, "bold"), fg="#1b3a81")
        slogan_label.grid(row=0, column=0, padx=20, pady=20, columnspan=2, sticky="nsew")

        # Create username label and entry
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Create password label and entry
        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Create login button
        self.login_button = ttk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

    def login(self):
        # Retrieve username and password
        username = self.username_entry.get()
        password = self.password_entry.get()
        l = Login()
        # Check users credentials
        validation = l.sign_in(username, password)
        if validation:
            self.withdraw()  # Hide the login window upon successful login
            self.destroy()  # Close the login window
            main_page = MainPage(self.master)  # Open the main page
            main_page.state('zoomed')
            Login.current_user = username
        else:
            messagebox.showerror("Login", "Invalid username or password")


class NewUserPopup(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("New User")
        # Create a custom style for buttons
        style = ttk.Style()
        style.theme_use("clam")  # Use a pre-defined theme as a base

        # Labels and entry boxes for user details
        self.login_username_label = tk.Label(self, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        self.is_admin_var = tk.IntVar()
        self.admin_checkbox = tk.Checkbutton(self, text="Admin", variable=self.is_admin_var)
        self.admin_checkbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Button to create the new user
        self.create_button = ttk.Button(self, text="Create User", command=self.create_user)
        self.create_button.grid(row=4, columnspan=2, padx=5, pady=10)

    def create_user(self):
        # Retrieve user details from entry boxes
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        is_admin = bool(self.is_admin_var.get())
        try:
            l = Login()
            login_attempt = l.create_login(username, password, email, is_admin)
            print(login_attempt)
            if login_attempt is None:
                self.destroy()
            else:
                messagebox.showinfo('Invalid details', login_attempt)
        except Exception as e:
            print('Create User error', e)
        # Close the popup window after creating the user


class MainPage(tk.Toplevel):
    def __init__(self, master=None):
        # Create a style
        style = ttk.Style()
        style.theme_use("clam")


        # Configure buttons to be slightly bigger with bigger text
        style.configure("TButton", font=("Helvetica", 10, "bold"), padding=4)

        # Configure the style for the notebook and tabs
        style.configure("Custom.TNotebook", background="white")
        style.configure("Custom.TNotebook.Tab", background="white", padding=[10, 5], font=("Helvetica", 12))


        # Configure the style of all treeview headings
        style.configure("Treeview.Heading", font=("Helvetica", 10))
        # Set height for treeview rows
        style.configure("Treeview", rowheight=30, font=("Helvetica", 12))

        super().__init__(master=None)
        self.title("Project Manager")
        self.geometry("800x600")  # Adjust the initial window size as needed

        # Create menu bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Create File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Switch User", command=self.switch_user)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_application)

        # Check if the current user is an admin and hide the admin menu if not
        print('current user')
        print(Login.current_user)
        if self.is_admin(Login.current_user):
            # Create Admin menu
            self.admin_menu = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label="Admin", menu=self.admin_menu)
            self.admin_menu.add_command(label="New User", command=self.open_new_user_popup)

        # Bind window close event to exit_application method
        self.protocol("WM_DELETE_WINDOW", self.exit_application)

        # Create the notebook
        self.tab_control = ttk.Notebook(self, style="Custom.TNotebook")
        self.tab_control.pack(expand=True, fill=tk.BOTH)

        # Create the tabs
        self.ListTab = tk.Frame(self.tab_control, background='white')
        self.tab_control.add(self.ListTab, text='Overview')

        self.TasksTab = tk.Frame(self.tab_control, background='white')
        self.tab_control.add(self.TasksTab, text='Tasks')

        self.TimelineTab = tk.Frame(self.tab_control, background='white')
        self.tab_control.add(self.TimelineTab, text='Timeline')

        ####------------------ LIST/ OVERVIEW TAB --------------------------###

        # Create frame for buttons and search box
        self.button_search_frame = tk.Frame(self.ListTab, background="white")
        self.button_search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Create buttons
        self.add_project_button = ttk.Button(self.button_search_frame, text="+ New Project",
                                             command=self.add_project_popup, style="Bold.TButton")
        self.add_project_button.grid(row=0, column=0, padx=(0, 10), pady=5)

        self.edit_project_button = ttk.Button(self.button_search_frame, text="Edit Project",
                                              command=self.edit_project_popup)
        self.edit_project_button.grid(row=0, column=1, padx=(0, 10), pady=5)

        # Create frame for search box and label
        self.search_frame = tk.Frame(self.button_search_frame, background="white")
        self.search_frame.grid(row=0, column=2, padx=(50, 10), pady=5, sticky="w")

        # Create search box label
        self.search_label = tk.Label(self.search_frame, text="Search:", font=("TkDefaultFont", 12), background="white")
        self.search_label.grid(row=0, column=0, padx=(0, 5))

        # Create search box
        self.search_entry = tk.Entry(self.search_frame, font=("TkDefaultFont", 12))
        self.search_entry.grid(row=0, column=1, padx=(0, 5))
        self.search_entry.bind("<KeyRelease>", self.search_projects)

        # Create frame for project tree and configure row and column weight
        self.project_tree_frame = tk.Frame(self.ListTab)
        self.project_tree_frame.grid(row=1, column=0,  padx=10, pady=10, sticky="nsew")
        self.project_tree_frame.grid_rowconfigure(0, weight=1)
        self.project_tree_frame.grid_columnconfigure(0, weight=1)

        # Create table to display all projects
        self.project_tree = ttk.Treeview(self.project_tree_frame, columns=(
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
        self.project_tree.heading("Progress", text="Progress %",
                                  command=lambda: self.treeview_sort_column(self.project_tree, "Progress", False))
        self.project_tree.column("Project Name", width=200, )
        self.project_tree.column("Description", width=400, )
        self.project_tree.grid(row=0, column=0, sticky="nsew")
        self.project_tree.bind("<<TreeviewSelect>>", self.update_project_members_treeview_bind)


        self.scrollbar = ttk.Scrollbar(self.project_tree_frame, orient="vertical", command=self.project_tree.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.project_tree.configure(yscrollcommand=self.scrollbar.set)

        # Create frame for project members tree and configure row weight
        self.project_members_tree_frame = tk.Frame(self.ListTab)
        self.project_members_tree_frame .grid(row=1, column=1,  padx=10, pady=10, sticky="nsew")
        self.project_members_tree_frame.grid_rowconfigure(0, weight=1)
        self.project_members_tree_frame.grid_columnconfigure(0, weight=1)

        # Project Members treeview
        self.project_members_tree = ttk.Treeview(self.project_members_tree_frame, columns=("Username"))
        self.project_members_tree.heading("Username", text="Project Members")
        self.project_members_tree['show'] = 'headings'
        self.project_members_tree.grid(row=0, column=0, sticky="nsew", columnspan = 2)
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        self.project_members_tree_scrollbar = ttk.Scrollbar(self.project_members_tree_frame, orient="vertical",
                                                            command=self.project_members_tree.yview)
        self.project_members_tree_scrollbar.grid(row=0, column=2, sticky='ns')
        self.project_members_tree.configure(yscrollcommand=self.project_members_tree_scrollbar.set)

        # Add buttons to add/remove members
        self.add_member_button = ttk.Button(self.project_members_tree_frame, text=" Add ", command=self.add_member_popup)
        self.add_member_button.grid(row=1, column=0, padx=2, pady=5, sticky="ew")

        self.remove_member_button = ttk.Button(self.project_members_tree_frame, text=" Remove ", command = self.remove_member_from_project)
        self.remove_member_button.grid(row=1, column=1, padx=2, pady=5, sticky="ew")

        self.ListTab.rowconfigure(1, weight=1)
        self.ListTab.columnconfigure(0, weight=1)
        self.ListTab.columnconfigure(1, weight=1)

        self.show_all_project_info()

        ####------------------ TASKS TAB --------------------------###

        # Create frame for buttons
        self.button_project_frame = tk.Frame(self.TasksTab, background="white")
        self.button_project_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.button_project_frame.grid_rowconfigure(0, weight=1)
        self.button_project_frame.grid_columnconfigure(0, weight=1)

        # Create buttons in tasks tab
        self.add_task_button = ttk.Button(self.button_project_frame, text=" + New Task ", command=self.add_tasks_popup)
        self.add_task_button.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")

        self.edit_task_button = ttk.Button(self.button_project_frame, text=" Edit Task ", command=self.edit_task_popup)
        self.edit_task_button.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="w")

        # Create dropdown to select a project
        self.project_dropdown_label = tk.Label(self.button_project_frame, text=" Project: ", font=("Helvetica", 12), background="white")
        self.project_dropdown_label.grid(row=0, column=2, padx=(50,5), pady=5)
        self.tasks = ttk.Combobox(self.button_project_frame, state="readonly", width=20, font=('Arial', 16))
        self.tasks.grid(row=0, column=3, padx=0, pady=5, sticky="w")
        self.tasks.bind("<<ComboboxSelected>>", self.update_task_treeview)

        # Configure row and column weights for the task_tree_frame
        self.TasksTab.grid_rowconfigure(1, weight=1)
        self.TasksTab.grid_columnconfigure(0, weight=1)

        # Create frame for task tree and configure row and column weight
        self.task_tree_frame = tk.Frame(self.TasksTab)
        self.task_tree_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.task_tree_frame.grid_rowconfigure(0, weight=1)
        self.task_tree_frame.grid_columnconfigure(0, weight=1)

        # Create table to display tasks related to chosen project
        self.task_tree = ttk.Treeview(self.task_tree_frame, columns=(
            "Task ID", "Task Name", "Description", "Assigned", "Status", "Start Date", "End Date", "Progress",
            "Comments"))
        self.task_tree['show'] = 'headings'

        self.task_tree.heading("Task ID", text="Task ID",
                               command=lambda: self.treeview_sort_column(self.task_tree, "Task ID", False))
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
        self.task_tree.heading("Progress", text="Progress %",
                               command=lambda: self.treeview_sort_column(self.task_tree, "Progress", False))
        self.task_tree.heading("Comments", text="Owner's Comments",
                               command=lambda: self.treeview_sort_column(self.task_tree, "Comments", False))
        self.task_tree.column("Task ID", width=80)
        self.task_tree.column("Progress", width=100)
        self.task_tree.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.task_tree_frame, orient="vertical", command=self.task_tree.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.task_tree.configure(yscrollcommand=self.scrollbar.set)


        ####------------------ TIMELINE TAB --------------------------###

        # Configure row weights of TimelineTab to allow vertical stretching for both rows
        self.TimelineTab.rowconfigure(1, weight=1)
        self.TimelineTab.columnconfigure(0, weight=1)

        # Create frame for buttons and dropdown
        self.add_message_project_frame = tk.Frame(self.TimelineTab, background="white")
        self.add_message_project_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.add_message_project_frame.grid_rowconfigure(0, weight=1)
        self.add_message_project_frame.grid_columnconfigure(0, weight=1)

        # Create buttons in timeline tab
        self.add_message_button = ttk.Button(self.add_message_project_frame, text=" + New Message ",
                                             command=self.add_timeline_msg_popup)
        self.add_message_button.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")


        # Create project dropdown list to choose project
        self.timeline_project_label = tk.Label(self.add_message_project_frame, text=" Project: ", font=("Helvetica", 12), background="white")
        self.timeline_project_label.grid(row=0, column=2, padx=(50,0), pady=5)
        self.timeline_project_list = ttk.Combobox(self.add_message_project_frame, state="readonly", width=20, font=('Arial', 16))
        self.timeline_project_list.grid(row=0, column=3, padx=(0,10), pady=5, sticky="e")
        self.timeline_project_list.bind("<<ComboboxSelected>>", self.create_timeline_plot)

        # Create frame for project messages treeview
        self.add_message_project_frame = tk.Frame(self.TimelineTab, background="white")
        self.add_message_project_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.add_message_project_frame.grid_rowconfigure(0, weight=1)
        self.add_message_project_frame.grid_columnconfigure(0, weight=1)

        # Create treeview to show project messages along with its timeline
        self.project_messages_treeview = ttk.Treeview(self.add_message_project_frame, columns=('Username', 'Message', 'Date Added'))
        self.project_messages_treeview.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.project_messages_treeview['show'] = 'headings'
        self.project_messages_treeview.heading('Username', text='Username')
        self.project_messages_treeview.heading('Message', text='Message')
        self.project_messages_treeview.heading('Date Added', text='Date Posted')

        self.project_messages_scrollbar = ttk.Scrollbar(self.add_message_project_frame, orient="vertical", command=self.project_messages_treeview.yview)
        self.project_messages_scrollbar.grid(row=0, column=1, sticky='ns')
        self.project_messages_treeview.configure(yscrollcommand=self.project_messages_scrollbar.set)

        # Create frame for timeline chart
        self.timeline_frame = tk.Frame(self.add_message_project_frame, background="white")
        self.timeline_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        self.timeline_frame.grid_rowconfigure(0, weight=1)
        self.timeline_frame.grid_columnconfigure(0, weight=1)
        self.timeline_frame.grid_columnconfigure(1, weight=1)
        self.create_timeline_plot()
        self.update_project_list()

    def create_timeline_plot(self, *event):
        # Retrieve project selected in timeline tab
        selected_project = self.timeline_project_list.get()
        p = Project()
        fig = p.create_timeline(selected_project)
        canvas = FigureCanvasTkAgg(fig, master=self.timeline_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.update_project_messages_treeview()

    def add_timeline_msg_popup(self):
        def validate_max_characters(text):
            # Ensures entry box is limited to 30 characters
            if len(text) <= 30:
                return True
            else:
                return False
        selected_project = self.timeline_project_list.get()
        # Check project has been selected
        if selected_project:

            popup = tk.Toplevel(self)
            popup.title("Add Message")

            # Add labels and entry boxes - project name is disabled
            tk.Label(popup, text="Project Name:").grid(row=0, column=0, padx=5, pady=5)
            self.project_name = tk.Entry(popup)
            self.project_name.insert(0, selected_project)
            self.project_name.grid(row=0, column=1, padx=5, pady=5)
            self.project_name.config(state=tk.DISABLED)


            validation = self.register(validate_max_characters)

            # Message is limited to 30 characters
            tk.Label(popup, text="Message (max 30 characters):").grid(row=1, column=0, padx=5, pady=5)
            self.timeline_msg_entry = tk.Entry(popup, validate="key", validatecommand=(validation, "%P"))
            self.timeline_msg_entry.grid(row=1, column=1, padx=5, pady=5)

            self.add_message_button = ttk.Button(popup, text=" OK ", command=self.validate_timeline_msg)
            self.add_message_button.grid(row=2, column=1, padx=0, pady=5, sticky="w")
        else:
            messagebox.showinfo('Missing Information', 'Please select a project')


    def validate_timeline_msg(self):
        messages = ["Are you sure you want to add this message?","Messages cannot be removed once created"]
        response = messagebox.askquestion("Confirm Changes", "\n".join(messages))
        if response == 'yes':
            try:
                comment = self.timeline_msg_entry.get()
                print(comment)
                project_name = self.project_name.get()
                print(project_name)
                p = Project()
                p.create_project_message(project_name, comment)
                self.update_project_messages_treeview()
                self.create_timeline_plot()
            except Exception as e:
                print('Error validating timeline message', e)

    def remove_member_from_project(self):

        current_project_selected = self.project_tree.focus()
        if not current_project_selected:
            messagebox.showerror("Error", "Please select a Project.")
            return
        current_member_selected = self.project_members_tree.focus()
        if not current_member_selected:
            messagebox.showerror("Error", "Please select a member to remove.")
            return

        selection = self.project_members_tree.item(current_member_selected)
        member_username = selection["values"][0]
        selected_project = self.project_tree.item(current_project_selected)
        project_name = selected_project["values"][0]
        try:
            response = messagebox.askquestion(messagebox.askquestion("Confirm Changes", "Are you sure you want to make these changes?"))
            if response == 'yes':
                p = Project()
                p.remove_members(project_name, member_username)
                self.refresh_project_members_treeview(project_name)
        except Exception as e:
            messagebox.showerror("Error removing member", f"An error occurred: {str(e)}")

    def is_admin(self, username):
        l = Login()
        print(f'is admin {username}')
        access = l.is_admin(username)

        return access

    def switch_user(self):
        # Close the main page
        self.destroy()

        # Open the login screen
        login_screen = LoginPage(self.master)
        login_screen.mainloop()

    def open_new_user_popup(self):
        # Open the New User popup
        new_user_popup = NewUserPopup(self)
        new_user_popup.mainloop()



    def exit_application(self):
        # Close the app and stop running in IDE
        self.master.destroy()
        self.quit()

    def add_member_popup(self):
        # Check if user has selected a project
        current_project_selected = self.project_tree.focus()
        if not current_project_selected:
            messagebox.showerror("Error", "Please select a Project.")
            return
        selected_project = self.project_tree.item(current_project_selected)
        project_name = selected_project["values"][0]
        # Open a new popup window for adding members to a project
        popup = tk.Toplevel(self)
        popup.title("Add Members")

        tk.Label(popup, text="Project Name:").grid(row=0, column=0, padx=5, pady=5)
        self.project_name_entry = tk.Entry(popup)
        self.project_name_entry.insert(0, project_name)
        self.project_name_entry.config(state='disabled')
        self.project_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Only shows members who aren't already assigned to the project
        self.member_options = self.get_unassigned_members_for_project(project_name)
        tk.Label(popup, text="Members:").grid(row=1, column=0, padx=5, pady=5)
        self.unassigned_members_listbox = tk.Listbox(popup, height=10, width=30, selectmode=tk.MULTIPLE)
        for mem in self.member_options:
            self.unassigned_members_listbox.insert(tk.END, mem)
        self.unassigned_members_listbox.grid(row=1, column=1, padx=5, pady=5)
        scrollbar = tk.Scrollbar(
            popup,
            orient=tk.VERTICAL,
            command=self.unassigned_members_listbox.yview)
        self.unassigned_members_listbox['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=1, column=2, sticky='ns')

        add_member_button = ttk.Button(popup, text=" Assign to Project ", command=lambda: self.add_members_to_project
        (project_name,
         popup))
        add_member_button.grid(row=2, column=1, padx=2, pady=5, sticky="w")


    def add_members_to_project(self, project_name, popup):
        current_project_selected = self.project_tree.focus()

        if not current_project_selected:
            messagebox.showerror("Error", "Please select a Project.")
            return

        make_changes = messagebox.askquestion("Confirm Changes", "Are you sure you want to make these changes?")
        if make_changes == 'yes':
            try:
                all_members = []
                for i in self.unassigned_members_listbox.curselection():
                    x = self.unassigned_members_listbox.get(i)
                    all_members.append(x)

                try:
                    p = Project()
                    p.add_members(project_name, all_members)
                    self.refresh_project_members_treeview(project_name)
                except Exception as e:
                    messagebox.showerror("Error adding members", f"{str(e)}")
                try:
                    e = Email()
                    e.send_project_emails(project_name)
                except Exception as e:
                    messagebox.showerror("Error sending emails", f"{str(e)}")
                popup.destroy()

            except Exception as e:
                messagebox.showerror("Error making member changes", f"An error occurred: {str(e)}")

    def edit_project_popup(self):

        current_project_selected = self.project_tree.focus()

        if not current_project_selected:
            messagebox.showerror("Error", "Please select a Project.")
            return
        selected_project = self.project_tree.item(current_project_selected)

        project_name = selected_project["values"][0]

        popup = tk.Toplevel(self)
        popup.title("Edit Project")

        # Labels and entry fields for project details
        tk.Label(popup, text="Project Name:").grid(row=0, column=0, padx=5, pady=5)
        self.project_name_entry = tk.Entry(popup)
        self.project_name_entry.insert(0, selected_project["values"][0])
        self.project_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create status entry options for standard users and admin users
        # Only admins can mark a project as completed
        admin_values = ["In-Progress", "Completed"]
        standard_user_values = ["In-Progress"]

        tk.Label(popup, text="Status:").grid(row=1, column=0, padx=5, pady=5)
        # check if user is admin
        if self.is_admin(Login.current_user):
            self.status_entry = ttk.Combobox(popup, values=admin_values, state="readonly")
        else:
            self.status_entry = ttk.Combobox(popup, values=standard_user_values, state="readonly")
        self.status_entry.set(selected_project["values"][3])
        self.status_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(popup, text="Description:").grid(row=2, column=0, padx=5, pady=5)
        self.description_entry = tk.Text(popup, height=5, width=30)
        self.description_entry.insert("1.0", selected_project["values"][1])
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(popup, text="Owner:").grid(row=3, column=0, padx=5, pady=5)
        self.owner_options = self.get_usernames()
        self.owner_entry = ttk.Combobox(popup, values=self.owner_options, state="readonly")
        self.owner_entry.set(selected_project["values"][2])
        self.owner_entry.grid(row=3, column=1, padx=5, pady=5)

        save_button = ttk.Button(popup, text="Save",
                                command=lambda: self.save_edited_project(self.project_name_entry.get(),
                                                                         self.status_entry.get(),
                                                                         self.description_entry.get("1.0", "end-1c"),
                                                                         self.owner_entry.get(),
                                                                         project_name,
                                                                         current_project_selected,
                                                                         popup))
        save_button.grid(row=4, columnspan=2, padx=5, pady=10)

    def save_edited_project(self, project_name, status, description, owner, old_project_name, current_project_selected,
                            popup):
        # Check user has entered all details
        if not (project_name and status and description and owner):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        # Confirm changes
        make_changes = messagebox.askquestion("Confirm Changes", "Are you sure you want to make these changes?")
        if make_changes == 'yes':
            try:
                p = Project()
                p.edit_project(old_project_name, project_name, owner, status, description)
                if status == 'Completed':
                    try:
                        e = Email()
                        e.send_project_completed_emails(project_name)
                    except Exception as e:
                        print('Error sending project complete emails', e)
                popup.destroy()
                # Reload projects in the treeview
                self.project_tree.focus(current_project_selected)
                self.project_tree.selection_set(current_project_selected)
                self.update_project_treeview()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_project_messages_treeview(self, *event):
        # Check project is selected
        selected_project = self.timeline_project_list.get()
        if selected_project:
            p = Project()
            project_messages = p.get_project_messages(selected_project)
            self.project_messages_treeview.delete(*self.project_messages_treeview.get_children())
            try:
                for msg in project_messages:
                    self.project_messages_treeview.insert("", "end", values=msg)
            except Exception as e:
                print("Error updating project members treeview:", e)



    def reload_project_members_treeview(self, project_name):
        # Used after project is edited as need to get project name to stop it deselecting in treeview
        # selected_item = self.project_tree.focus()
        # project_name = self.project_tree.item(selected_item, "values")[0]
        p = Project()
        project_members = p.get_project_members(project_name)
        print(project_name)

        self.project_members_tree.delete(*self.project_members_tree.get_children())  # Clear existing data
        try:
            for member in project_members:
                self.project_members_tree.insert("", "end", values=member)
        except Exception as e:
            print("Error reloading project members treeview:", e)

    def update_project_members_treeview_bind(self, *event):
        try:
            selected_item = self.project_tree.focus()
            project_name = self.project_tree.item(selected_item, "values")[0]
        except Exception as e:
            print('No project selected')
        if selected_item:

            p = Project()
            project_members = p.get_project_members(project_name)

            self.project_members_tree.delete(*self.project_members_tree.get_children())  # Clear existing data
            try:
                for member in project_members:
                    self.project_members_tree.insert("", "end", values=member)
            except Exception as e:
                print("Error updating project members treeview bind:", e)
    def refresh_project_members_treeview(self, project_name):
        if project_name:
            p = Project()
            project_members = p.get_project_members(project_name)
            self.project_members_tree.delete(*self.project_members_tree.get_children())  # Clear existing data
            try:
                for member in project_members:
                    self.project_members_tree.insert("", "end", values=member)
            except Exception as e:
                print("Error updating project members treeview:", e)
    def update_project_list(self):
        # Updates the dropdowns to display list of projects to select
        p = Project()
        all_projects = p.get_all_projects()
        self.tasks['values'] = all_projects
        # self.timeline_projects = all_projects
        self.timeline_project_list['values'] = all_projects
        return all_projects

    def check_task_access(self, task_id):
        this_user = Login.current_user
        print('The current user is')
        print(this_user)
        l = Login()
        admin = l.is_admin(this_user)
        t = Task()
        assigned_to = t.is_assigned_to(task_id)
        owner = t.get_owner_from_task(task_id)
        if admin or (this_user == assigned_to):
            return 'admin'
        if owner == this_user:
            return 'owner'
        else:
            return 'restricted'

    def edit_task_popup(self):
        # Get the currently selected task
        current_task_selected = self.task_tree.focus()

        if not current_task_selected:
            messagebox.showerror("Error", "Please select a task.")
            return
        selected_task = self.task_tree.item(current_task_selected)
        task_id = selected_task["values"][0]

        # Get the access for the current user
        access = self.check_task_access(task_id)
        if access == 'restricted':
            messagebox.showinfo('Restricted Access', 'Sorry, you dont have access to this task' )

        # Extract the selected project from the combobox
        selected_project = self.tasks.get()
        
        # Get the access for the current user
        access = self.check_task_access(task_id)

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

        # Get project members for project
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
        self.save_button = ttk.Button(popup, text="Save Changes",
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

        if access == 'owner':
            self.task_name_entry.config(state=tk.DISABLED)
            self.task_status_entry.config(state=tk.DISABLED)
            self.task_description_entry.config(state=tk.DISABLED)
            self.members_listbox.config(state=tk.DISABLED)
        elif access == 'admin':
            self.comments_entry.config(state=tk.DISABLED)


    def save_edit_task(self, task_name, task_id, status, progress, description, comment, popup):
        if not (task_name and status and description and task_id and self.members_listbox.curselection()):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        make_changes = messagebox.askquestion("Confirm Changes", "Are you sure you want to make these changes?")

        if make_changes == 'yes':
            try:
                t = Task()
                assigned = []
                for i in self.members_listbox.curselection():
                    x = self.members_listbox.get(i)
                    assigned.append(x)
                ass = [x for x in assigned]
                assigned_to = ass[0]
                print('assigned to')
                original_assigned_to = t.is_assigned_to(task_id)
                if assigned_to != original_assigned_to:
                    t = Task()
                    project_name = t.get_project_for_task(task_id)
                    e = Email()
                    e.send_task_assignmnent_email(assigned_to, project_name)
                t.edit_task(task_id, task_name, description, status, progress, assigned_to, comment)
                t.update_task_start_and_end_dates(task_id, status)
                self.update_project_percent_complete(task_id)
                self.update_task_treeview()
                self.update_project_treeview()
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_project_percent_complete(self, task_id):
        try:
            t = Task()
            project_name = t.get_project_for_task(task_id)
            p = Project()
            p.update_percentage_complete(project_name)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

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

    # def update_percent_complete(self, project):
    #     """ """
    #     self.percent = Project.get_percentage_complete(self, project)
    #     self.project_percent_box.config(state='normal')
    #     self.project_percent_box.delete(0, tk.END)
    #     self.project_percent_box.insert(0, self.percent)
    #     self.project_percent_box.config(state='readonly')

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
        self.save_button = ttk.Button(popup, text="Save",
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
        self.save_button = ttk.Button(popup, text="Save",
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
            e = Email()
            e.send_task_assignmnent_email(assigned_to, project_name)
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

            p = Project()
            p.create_project(project_name, owner, status, description)
            messagebox.showinfo("Success", "Project added successfully!")
            # self.selection = self.members_listbox.curselection()
            # print(self.selection)
            all_members = []
            for i in self.members_listbox.curselection():
                x = self.members_listbox.get(i)
                all_members.append(x)
            try:
                #p = Project()
                p.add_members(project_name, all_members)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            try:
                e = Email()
                e.send_project_emails(project_name)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            popup.destroy()
            self.update_project_treeview()
            self.update_project_list()
            p = Project()
            p.update_percentage_complete(project_name)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Function to update Treeview with new project
    def update_project_treeview(self):
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

    def get_unassigned_members_for_project(self, project_name):
        users = self.get_usernames()
        members = self.get_project_members(project_name)
        unnasigned_members = list((set(users) | set(members)) - (set(users) & set(members)))
        return unnasigned_members

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
