import textwrap
from super_admin import SuperAdmin
import tkinter as tk
from project import Project
from interface import LoginPage
import pydoc
def main():

    root = tk.Tk()
    root.withdraw()  # Hide the root window initially
    login_page = LoginPage(root)
    root.mainloop()


if __name__ == '__main__':
    #main()
    pydoc.writedoc('login')
    pydoc.writedoc('project')
    pydoc.writedoc('Email')
    pydoc.writedoc('interface')
    pydoc.writedoc('task')
    pydoc.writedoc('team_member')
    pydoc.writedoc('super_admin')
    pydoc.writedoc('project_member')
    pydoc.writedoc('project_messages')
