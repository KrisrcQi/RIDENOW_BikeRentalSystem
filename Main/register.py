from tkinter import *
import sqlite3
import random
import string
from tkinter import messagebox



class Register:

    def __init__(self) -> None:

        self.window = Tk()
        self.window.title("Register user")
        self.window.geometry("500x300+500+300")

        font = ('Arial', 14)
        # create labels
        self.l_email = Label(self.window, text='Email:', font=font)
        self.l_email.place(x=80, y=50)

        self.l_userid = Label(self.window, text='User ID:', font=font)
        self.l_userid.place(x=80, y=100)

        self.l_password = Label(self.window, text='password:', font=font)
        self.l_password.place(x=80, y=150)

        # create entries
        self.e_email = Entry(self.window, font=font)
        self.e_email.place(x=200, y=50, width=200, height=30)

        self.e_userid = Entry(self.window, font=font)
        self.e_userid.place(x=200, y=100, width=200, height=30)

        self.e_password = Entry(self.window, font=font)
        self.e_password.place(x=200, y=150, width=200, height=30)

        # create button
        self.bt_reg = Button(self.window, text='Register & sign in',
                             font=font, command=self.register)
        self.bt_reg.place(x=200, y=220)

    def generate_username(self, length=8):

        # customize the characters or words used in the username
        characters = string.ascii_letters + string.digits  # includes letters and digits
        username = ''.join(random.choice(characters) for _ in range(length))
        return username

    def store_new_user(self):

        userid_get = self.e_userid.get()
        email_get = self.e_email.get()
        password_get = self.e_password.get()
        random_username = "User{}".format(self.generate_username(12))
        # Connect database and insert data for new users
        conn = sqlite3.connect("RIDENOW.db")
        self.c = conn.cursor()
        self.c.execute("""INSERT INTO Customer (customer_id, username, email, password) 
                        VALUES (?, ?, ?, ?)""", (userid_get, random_username, email_get, password_get))
        conn.commit()
        return print("Successfully insert the new user data in database")


    def register(self):

        # Get the userid from database
        conn = sqlite3.connect("RIDENOW.db")
        self.c = conn.cursor()
        self.c.execute("""SELECT customer_id FROM Customer""")
        existing_id = self.c.fetchall()
        # Extract the integers and convert them to strings
        id_strings = [str(item[0]) for item in existing_id]
        # Join the strings into a single string
        result_string_id = ', '.join(id_strings)
        # Print or use the result
        print(result_string_id)

        userid_get = self.e_userid.get()
        # Check the duplicated userid:
        if userid_get in result_string_id:
            click_1 = messagebox.showerror("UserID existing", "This UserID is already registered, please go back login.")
            if click_1:
                self.window.destroy()
        else:
            # Store the new user's data into database Customer table:
            self.store_new_user()
            click_2 = messagebox.showinfo("Successfully registered", "{}, please login".format(userid_get))
            if click_2:
                self.window.destroy()

    def show(self):
        self.window.mainloop()