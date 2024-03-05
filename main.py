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
    main()
