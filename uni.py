import tkinter as tk
from tkinter import messagebox


class LoginPage(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Login Page")

        # Calculate screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate login window dimensions
        login_width = 300
        login_height = 150

        # Calculate login window position
        x = (screen_width - login_width) // 2
        y = (screen_height - login_height) // 2
        self.geometry(f"{login_width}x{login_height}+{x}+{y}")

        # Create username label and entry
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        # Create password label and entry
        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        # Create login button
        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if username and password are correct
        if username == "admin" and password == "password":
            messagebox.showinfo("Login", "Login successful!")
            self.withdraw()  # Hide the login window upon successful login
            self.master.deiconify()  # Show the main window
            self.destroy()  # Close the login window
            MainPage(self.master)  # Open the main page
        else:
            messagebox.showerror("Login", "Invalid username or password")


class MainPage(tk.Tk):
    def __init__(self, master=None):
        super().__init__()
        self.title("Main Page")

        # Here you can define what you want to include in the main page
        print("Main Page opened!")


def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window initially
    LoginPage(root)
    root.mainloop()


if __name__ == "__main__":
    main()
