from tkinter import *
from register import Register
from Customer import CustomerUI
from Operator import OperatorUI
from Manager import ManagerUI
import sqlite3
from tkinter import messagebox
from datetime import datetime
from tkinter import PhotoImage
from PIL import Image, ImageTk

# Size of text:
FONT = ('Arial', 20)
FONT_TOP = ('Arial', 20, 'bold')
FONT_TITLE = ('Arial', 50, 'bold')

# Size of entry
HEIGHT = 50
WIDTH = 150

class LoginUI:

    def __init__(self) -> None:
        # Create log_in windows
        self.log_in = Tk()
        self.log_in.title("RIDENOW Log-in")
        # identify the window size by the recognized screen size
        S_W = self.log_in.winfo_screenwidth()
        S_H = self.log_in.winfo_screenheight()
        self.log_in.geometry("{}x{}".format(S_W, S_H))
        self.login_user = 0

        # create labels
        self.label_userid = Label(self.log_in, text="User ID: ", font=FONT)
        self.label_password = Label(self.log_in, text="Password: ", font=FONT)

        # create textboxs
        self.textbox_userid = Entry(self.log_in, text="", font=FONT)
        self.textbox_password = Entry(self.log_in, text="", show="*", font=FONT)
        # textbox_name["justify"] = "center"     # centerlization the input
        self.textbox_userid.focus()
        self.textbox_title = Label(self.log_in, text="E-Vehicle Share System", font=FONT_TITLE)
        self.textbox_identity_selection = Label(self.log_in, text="Please choose an identity to log in: ",
                                                font=FONT)
        # insert image:
        original_image = Image.open("logo.png")
        resized_image = original_image.resize((300, 75), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(resized_image)

        self.logo_label = Label(self.log_in, image=self.logo)
        self.logo_label.photo = self.logo


        # create log-in button
        self.button_login = Button(self.log_in, text="Log-in", font=FONT_TOP,
                                   command=self.login_connect)
        # create register button
        self.button_register = Button(self.log_in, text="Register now", font=FONT_TOP,
                                      command=self.register)
        # create login identification selection button
        self.button_customer = Button(self.log_in, text="customer", font=FONT_TOP,
                                      command=lambda item="1": self.login(item))
        self.button_operator = Button(self.log_in, text="operator", font=FONT_TOP,
                                      command=lambda item="2": self.login(item))
        self.button_manager = Button(self.log_in, text="manager", font=FONT_TOP,
                                     command=lambda item="3": self.login(item))

        # place labels & textbox & buttons & logo pic
        self.label_userid.place(x=S_W * (380 / 1440), y=S_H * (400 / 900))
        self.label_password.place(x=S_W * (380 / 1440), y=S_H * (480 / 900))
        self.textbox_userid.place(x=S_W * (550 / 1440), y=S_H * (390 / 900), width=400, height=50)
        self.textbox_password.place(x=S_W * (550 / 1440), y=S_H * (470 / 900), width=400, height=50)
        self.textbox_title.place(x=S_W * (100 / 1440), y=S_H * (100 / 900), width=1200, height=80)
        self.textbox_identity_selection.place(x=S_W * (160 / 1440), y=S_H * (240 / 900), width=800, height=30)
        self.button_customer.place(x=S_W * (400 / 1440), y=S_H * (300 / 900), width=WIDTH, height=HEIGHT)
        self.button_operator.place(x=S_W * (580 / 1440), y=S_H * (300 / 900), width=WIDTH, height=HEIGHT)
        self.button_manager.place(x=S_W * (760 / 1440), y=S_H * (300 / 900), width=WIDTH, height=HEIGHT)
        self.button_login.place(x=S_W * (425 / 1440), y=S_H * (570 / 900), width=200, height=50)
        self.button_register.place(x=S_W*(700/1440), y=S_H*(570/900), width=200, height=50)
        self.logo_label.place(x=10, y=10)

    def login_connect(self):
        if self.login_user == "1":
            self.Customer_login()
        elif self.login_user == "2":
            self.Operator_login()
        elif self.login_user == "3":
            self.Manager_login()

    def login(self,item):
        if item =="1":
            self.login_user = "1"
            self.change_color(self.button_customer, "yellow")
        elif item =="2":
            self.login_user = "2"
            self.change_color(self.button_operator, "yellow")
        elif item =="3":
            self.login_user = "3"
            self.change_color(self.button_manager, "yellow")

    def Customer_login(self):
        id = self.textbox_userid.get()
        conn = sqlite3.connect("RIDENOW.db")
        c = conn.cursor()
        c.execute("SELECT * FROM Customer WHERE customer_id = ?", [id])
        id = c.fetchall()
        if id != []:
            e_password = self.textbox_password.get()
            print("The info of login user: ", "\n", id)
            if e_password == id[0][3]:
                id = self.textbox_userid.get()
                c.execute("SELECT username FROM Customer WHERE customer_id = ?", [id])
                name = c.fetchall()
                username = name[0][0]
                click = messagebox.showinfo("Login successfully!", "Hello {}, welcome come to RideNow!".format(username))
                if click:
                    self.insert_cus_login_history()
                    self.ShowCustomer()
            else:
                # Password not matched
                click = messagebox.showerror("Login failed", "Invalid UserID or Password.")
                if click:
                    self.log_in.mainloop()
        else:
            # Invalid ID
            click = messagebox.showerror("Login failed", "Invalid UserID or Password.")
            if click:
                self.log_in.mainloop()

    def ShowCustomer(self):
        self.log_in.destroy()
        customer = CustomerUI()
        customer.show()

    def ShowOperator(self):
        self.log_in.destroy()
        operator = OperatorUI()
        operator.show()

    def ShowManager(self):
        self.log_in.destroy()
        manager = ManagerUI()
        manager.show()


    def register(self):
        r = Register()
        r.show()

    def show(self):
        self.log_in.mainloop()

    def change_color(self, selected_button, new_color):
        selected_button.config(bg=new_color)
        # recover the unselected button color
        for button in [self.button_customer, self.button_operator, self.button_manager]:
            if button != selected_button:
                button.config(bg="lightgray")

    def Operator_login(self):
        #self.change_color(self.button_operator,"yellow")
        id = self.textbox_userid.get()
        conn = sqlite3.connect("RIDENOW.db")
        c = conn.cursor()
        c.execute("SELECT * FROM Operator WHERE operator_id = ?", [id])
        id = c.fetchall()
        if id != []:
            e_password = self.textbox_password.get()
            print(id)
            if e_password == id[0][3]:
                id = self.textbox_userid.get()
                c.execute("SELECT username FROM Operator WHERE operator_id = ?", [id])
                name = c.fetchall()
                username = name[0][0]
                click = messagebox.askyesno("Login successfully!", "Hello {}, welcome come to RideNow!".format(username))
                if click:
                    self.insert_ope_login_history()
                    self.ShowOperator()
            else:
                # Password not matched
                click = messagebox.showerror("Login failed", "Invalid UserID or Password.")
                if click:

                    self.log_in.mainloop()
        else:
            # Invalid ID
            click = messagebox.showerror("Login failed", "Invalid UserID or Password.")
            if click:
                self.log_in.mainloop()

    def Manager_login(self):
        id = self.textbox_userid.get()
        conn = sqlite3.connect("RIDENOW.db")
        c = conn.cursor()
        c.execute("SELECT * FROM Manager WHERE manager_id = ?", [id])
        id = c.fetchall()
        if id != []:
            e_password = self.textbox_password.get()
            print(id)
            if e_password == id[0][3]:
                id = self.textbox_userid.get()
                c.execute("SELECT username FROM Manager WHERE manager_id = ?", [id])
                name = c.fetchall()
                username = name[0][0]
                click = messagebox.askyesno("Login successfully!", "Hello {}, welcome come to RideNow!".format(username))
                if click:
                    self.insert_mag_login_history()
                    self.ShowManager()
            else:
                # Password not matched
                click = messagebox.showerror("Login failed", "Invalid UserID or Password.")
                if click:
                    self.log_in.mainloop()
        else:
            # Invalid ID
            click = messagebox.showerror("Login failed", "Invalid UserID or Password.")
            if click:
                self.log_in.mainloop()

    def insert_cus_login_history(self):
        conn = sqlite3.connect("RIDENOW.db")
        c = conn.cursor()
        id = self.textbox_userid.get()
        c.execute("SELECT * FROM Customer WHERE customer_id = ?", [id])
        customer_info = c.fetchall()
        print(customer_info)
        acct_type = "customer"
        current_time = datetime.now()
        c.execute("""
            INSERT INTO login_history (type, id, password, email, username, credit, login_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (acct_type, id, customer_info[0][3], customer_info[0][2], customer_info[0][1], customer_info[0][4],
                 current_time))
        conn.commit()
        print("Login history record inserted successfully.")

    def insert_ope_login_history(self):
        conn = sqlite3.connect("RIDENOW.db")
        c = conn.cursor()
        id = self.textbox_userid.get()
        c.execute("""SELECT * FROM Operator WHERE operator_id = ?""", [id])
        customer_info = c.fetchall()
        print(customer_info)
        acct_type = "operator"
        current_time = datetime.now()
        c.execute("""
            INSERT INTO login_history (type, id, password, email, username, login_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (acct_type, id, customer_info[0][3], customer_info[0][2], customer_info[0][1], current_time))
        conn.commit()
        print("Login history record inserted successfully.")


    def insert_mag_login_history(self):
        conn = sqlite3.connect("RIDENOW.db")
        c = conn.cursor()
        id = self.textbox_userid.get()
        c.execute("""SELECT * FROM Manager WHERE manager_id = ?""", [id])
        customer_info = c.fetchall()
        print(customer_info)
        acct_type = "manager"
        current_time = datetime.now()
        c.execute("""
            INSERT INTO login_history (type, id, password, email, username, login_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (acct_type, id, customer_info[0][3], customer_info[0][2], customer_info[0][1], current_time))
        conn.commit()
        print("Login history record inserted successfully.")

