

import smtplib, ssl
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


def send_email(sender_email, receiver_email, message):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    # sender_email = "karl.gospel25@gmail.com"
    # receiver_email = "karl.gospel25@gmail.com"
    password = 'pggl orbw ozjs smth'
    # message = """\
    # Subject: Hi there
    #
    # This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

root = tk.Tk()
root.title("CineSort")
root.state('zoomed')
# root.update_idletasks()
# root.attributes('-fullscreen', True)
# root.state('iconic')
# root.winfo_geometry()
# root.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), weight=1)
# root.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
root.config(bg="#f0f8ff")
bg_color = "#f0f8ff"
# Set color scheme
widget_color = "#590808"
button_color = "#D9AB73"

sender_email_label = tk.Label(root, text = "Enter your email :", font = ('Arial', 16))
sender_email_label.grid(column = 0, row = 0, padx=10, pady=10, columnspan=1)

sender_email = tk.Entry(root, text = "", font = ('Arial', 14), width = 8)
sender_email.grid(column=1, row=0, columnspan=1, padx=0, pady=0)

receiever_email_label = tk.Label(root, text = "Enter recipients email :", font = ('Arial', 16))
receiever_email_label.grid(column = 0, row = 1, padx=10, pady=10, columnspan=1)

receiever_email = tk.Entry(root, text = "", font = ('Arial', 14), width = 8)
receiever_email.grid(column=1, row=1, columnspan=1, padx=0, pady=0)

message_label = tk.Label(root, text = "Message :", font = ('Arial', 16))
message_label.grid(column = 0, row = 2, padx=10, pady=10, columnspan=1)

message = tk.Entry(root, text = "", font = ('Arial', 14), width = 8)
message.grid(column=1, row=2, columnspan=1, padx=0, pady=0)

textfield = ScrolledText(root, wrap=tk.WORD)

textfield.grid(column=1, row=2, columnspan=1, padx=0, pady=0)
root.mainloop()