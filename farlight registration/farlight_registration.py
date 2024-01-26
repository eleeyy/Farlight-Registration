from tkinter import *
from tkinter import messagebox
import time
import re
import mysql.connector

My_Window = Tk()
My_Window.geometry("1200x675+380+180")  # 1920x1080
My_Window.resizable(width=False, height=False)
My_Window.title("Farlight84")
My_Window.iconbitmap("icon.ico")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Lordallain1!",
    database="fldatabase",
)

cursor = db.cursor()

# ----- Validation functions
def validate_alphabets(text):
    return bool(re.match("^[a-zA-Z]*$", text))

def validate_integer(text):
    return bool(re.match("^\d*$", text))

# ----- Validate commands
vcmd_alphabets = (My_Window.register(validate_alphabets), '%P')
vcmd_integer = (My_Window.register(validate_integer), '%P')


def check_credentials():
    # ----- Get the values from the entry widgets
    entered_username = username_textbox.get()
    entered_password = password_textbox.get()

    # ----- Check if any field is empty
    if not all([entered_username, entered_password]):
        messagebox.showerror("Error", "Please fill out both fields")
        return

    # ----- Check if the username and password match in the database
    cursor.execute("SELECT * FROM users WHERE username = %s", (entered_username,))
    user_data = cursor.fetchone()

    if user_data:
        stored_password = user_data[5]  # Assuming the password column is at index 5
        if entered_password == stored_password:
            # Passwords match, proceed to homepage
            homepage()
        else:
            messagebox.showerror("Error", "Incorrect Password")
    else:
        messagebox.showerror("Error", "Username doesn't exist")

###################
### LOG IN PAGE ###
###################
def loginpage():
    loginpage_png = PhotoImage(file="page_login.png", master=My_Window)
    bg_loginpage = Label(My_Window, image=loginpage_png, borderwidth=0)
    bg_loginpage.place(x=0, y=0)

    # ----- add sign up button
    signup_png = PhotoImage(file="button_signup.png", master=My_Window)
    button_signup = Button(My_Window, image=signup_png, width=330, height=43, background="#1A1C67",
                          activebackground="#1A1C67", bd=0, borderwidth=0, relief=FLAT,
                          command=lambda: registrationpage())
    button_signup.place(x=96, y=460)

    # ----- add log in button
    login_png = PhotoImage(file="button_login.png", master=My_Window)
    button_login = Button(My_Window, image=login_png, width=330, height=43, background="#E87414",
                          activebackground="#E87414", bd=0, borderwidth=0, relief=FLAT, command=check_credentials)
    button_login.place(x=96, y=393)

    # ----- put textbox for username
    global username_textbox
    username_textbox = Entry(My_Window, width=17)
    username_textbox.configure(font=("Arial", 20))
    username_textbox.place(x=185, y=260)

    # ----- put textbox for password
    global password_textbox
    password_textbox = Entry(My_Window, width=17, show='*')
    password_textbox.configure(font=("Arial", 20))
    password_textbox.place(x=185, y=320)

    My_Window.mainloop()

#########################
### REGISTRATION PAGE ###
#########################
def registrationpage():
    registrationpage_png = PhotoImage(file="page_registration.png", master=My_Window)
    bg_registrationpage = Label(My_Window, image=registrationpage_png, borderwidth=0)
    bg_registrationpage.place(x=0, y=0)

    # ----- put textbox for first name
    firstname_textbox = Entry(My_Window, width=19, validate="key", validatecommand=vcmd_alphabets)
    firstname_textbox.configure(font=("Arial", 20))
    firstname_textbox.place(x=280, y=175)

    # ----- put textbox for last name
    lastname_textbox = Entry(My_Window, width=19, validate="key", validatecommand=vcmd_alphabets)
    lastname_textbox.configure(font=("Arial", 20))
    lastname_textbox.place(x=280, y=250)

    # ----- put textbox for age
    age_textbox = Entry(My_Window, width=19, validate="key", validatecommand=vcmd_integer)
    age_textbox.configure(font=("Arial", 20))
    age_textbox.place(x=280, y=325)

    # ----- put textbox for new username
    newusername_textbox = Entry(My_Window, width=19)
    newusername_textbox.configure(font=("Arial", 20))
    newusername_textbox.place(x=740, y=175)

    # ----- put textbox for new password
    newpass_textbox = Entry(My_Window, width=19)
    newpass_textbox.configure(font=("Arial", 20))
    newpass_textbox.place(x=740, y=250)

    # ----- add create account button
    createacount_png = PhotoImage(file="button_createaccount.png", master=My_Window)
    button_createaccount = Button(My_Window, image=createacount_png, width=335, height=45, background="#1A1C67",
                                  activebackground="#1A1C67", bd=0, borderwidth=0, relief=FLAT,
                                  command=lambda: loginpage())
    button_createaccount.place(x=425, y=446)

    def create_account():
        # ----- Get the values from the entry widgets
        first_name = firstname_textbox.get()
        last_name = lastname_textbox.get()
        age = age_textbox.get()
        username = newusername_textbox.get()
        password = newpass_textbox.get()

        # ----- Check if any field is empty
        if not all([first_name, last_name, age, username, password]):
            messagebox.showerror("Error", "Please fill out all the fields")
            return

        # ----- Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists")
            return

        # ----- Insert data into MySQL database
        sql = "INSERT INTO users (first_name, last_name, age, username, password) VALUES (%s, %s, %s, %s, %s)"
        values = (first_name, last_name, age, username, password)
        cursor.execute(sql, values)
        db.commit()

        # ----- Show a success message
        messagebox.showinfo("Success", "Account created successfully")

        # ----- Redirect to the login page (if needed)
        loginpage()

    # ----- add create account button
    createacount_png = PhotoImage(file="button_createaccount.png", master=My_Window)
    button_createaccount = Button(My_Window, image=createacount_png, width=335, height=45, background="#1A1C67",
                                  activebackground="#1A1C67", bd=0, borderwidth=0, relief=FLAT, command=create_account)
    button_createaccount.place(x=425, y=446)

    My_Window.mainloop()

#################
### HOME PAGE ###
#################
def homepage():
    homepage_png = PhotoImage(file="page_home.png", master=My_Window)
    bg_homepage = Label(My_Window,image=homepage_png, borderwidth=0)
    bg_homepage.place(x=0,y=0)

    My_Window.mainloop()

loginpage()
