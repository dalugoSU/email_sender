import smtplib
import tkinter as tk
from tkinter import StringVar
from tkinter import messagebox

root = tk.Tk() # Create Window
root.title("Simple Mail Service")
root.minsize(500,500)
root.maxsize(500,500)

# These allow me to pull email and pass from log in page to auth the send email function which needs another log in
user_mail = ""
user_passs = ""

# Count keeps track of emails sent per session. Reset when window is closed. Connection serves to open window if authentication is valid
count = 0
connection = False

# These help pull values from the entry boxes
who_is_sending = StringVar()
who_is_receiving = StringVar()
email_subject = StringVar()
body_entry_text = StringVar()
variable_email = StringVar()
variable_log_in_pass = StringVar()

# This function authenticates email log in. If valid, destroys all and opens email sending UI. 
def authenticate(email, pws):

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    try:
        server.login(email, pws)
        global connection
        connection = True
        if connection == True:
            log_in_frame.destroy()
            log_in_button.destroy()
            log_in_password.destroy()
            log_label_email.destroy()
            log_label_password.destroy()
            log_in_email.destroy()
            main_frame_sender.insert(tk.END, user_mail) # This places email used to log in into the from: entry box. It has to match, if changed you get error
        print("\nSuccessful Connection Established...")
    except smtplib.SMTPAuthenticationError:
        error_pop_up()
        print("\nCould not Establish Connection\nEmail or Password Incorrect")

    server.quit()

# This function sends emails once valid connection is made.
def send_mail(email, psw, email_subject, email_body, to_who, from_who):
    global count
    count += 1

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(email, psw)

    subject = email_subject
    body = email_body

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        from_who,
        to_who,
        msg
    )
    print(f"Email Sent...\nNumber: {count}\n")
    sent_pop_up()

    server.quit()

# All these functions get data from the entry boxes and feed them into the send email/ authenticate functions.
def fromm():

    deliverer = who_is_sending.get()
    return deliverer

def to():

    to = who_is_receiving.get()
    return to

def subject():

    subject = email_subject.get()
    return subject

def body():
    global body_entry_content

    body = body_entry.get(1.0, "end-1c")
    body_entry_content.set(body)

    return body_entry_content


def get_email():
    global user_mail

    email = variable_email.get()
    user_mail = email

    return email


def get_pass():
    global user_passs

    password = variable_log_in_pass.get()
    user_passs = password

    return password

# Pop ups to signal error, or email sent
def sent_pop_up():
    messagebox.showinfo("Success", "Email Sent!")


def error_pop_up():
    messagebox.showinfo("Error", "Could not Establish Connection\nEmail or Password Incorrect")

# GUI Code
main_frame = tk.Frame(root, bg='#2F2E2E')
main_frame.pack(fill='both', expand=True)

main_frame_sender = tk.Entry(main_frame, textvariable=who_is_sending)
main_frame_sender.place(relx=0.25, rely=0.05, relwidth=0.6)

main_frame_rec = tk.Entry(main_frame, textvariable=who_is_receiving)
main_frame_rec.place(relx=0.25, rely=0.125, relwidth=0.6)

main_frame_subject = tk.Entry(main_frame, textvariable=email_subject)
main_frame_subject.place(relx=0.25, rely=0.2, relwidth=0.6)

log_label_password = tk.Label(main_frame, text="From :")
log_label_password.place(rely=0.05, relx=0.05, relwidth=0.15)

log_label_password = tk.Label(main_frame, text="To :")
log_label_password.place(rely=0.125, relx=0.05, relwidth=0.15)

log_label_password = tk.Label(main_frame, text="Subject :")
log_label_password.place(rely=0.2, relx=0.05, relwidth=0.15)

body_entry_content = tk.StringVar()

send_mail_button = tk.Button(main_frame, text='Send', command=lambda: [send_mail(user_mail, user_passs, subject(), body(), to(), fromm())])
send_mail_button.place(relx=0.88, rely=0.1, relheight=0.1)

body_entry = tk.Text(main_frame, bg="light grey")
body_entry.place(relheight=0.65, relwidth=0.7, relx=0.15, rely=0.3)

log_in_frame = tk.Frame(main_frame, bg='#2F2E2E')
log_in_frame.pack(fill='both', expand=True)

log_in_email = tk.Entry(log_in_frame, textvariable=variable_email)
log_in_email.place(relx=0.4, rely=0.4, relwidth=0.4)

log_in_password = tk.Entry(log_in_frame, show="#", textvariable=variable_log_in_pass)
log_in_password.place(relx=0.4, rely=0.5, relwidth=0.4)

log_label_email = tk.Label(log_in_frame, text="Email")
log_label_email.place(rely=0.4, relx=0.2, relwidth=0.15)

log_label_password = tk.Label(log_in_frame, text="Password")
log_label_password.place(rely=0.5, relx=0.2, relwidth=0.15)

log_in_button = tk.Button(log_in_frame, text='Log In', command=lambda: [authenticate(get_email(), get_pass())])
log_in_button.place(relx=0.6, rely=0.6, relwidth=0.2)


root.mainloop() # Keeps window running until closed
