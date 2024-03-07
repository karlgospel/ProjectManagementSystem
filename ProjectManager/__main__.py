import tkinter as tk
from interface import LoginPage
def main():

    root = tk.Tk()
    root.withdraw()  # Hide the root window initially
    login_page = LoginPage(root)
    root.mainloop()


if __name__ == '__main__':
    main()
