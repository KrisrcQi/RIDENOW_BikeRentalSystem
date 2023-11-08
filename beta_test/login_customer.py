from tkinter import *
from register_1 import Register
from Customer_3 import CustomerUI
import sqlite3
from tkinter import messagebox



class LoginUI:

    def __init__(self) -> None:
        # Create log_in windows
        self.log_in = Tk()
        self.log_in.title("2BIKE UofG Log-in")
        # identify the window size by the recognized screen size
        S_W = self.log_in.winfo_screenwidth()
        S_H = self.log_in.winfo_screenheight()
        self.log_in.geometry("{}x{}".format(S_W,S_H))

        # insert image:

        # create labels:
        self.label_guid = Label(self.log_in, text = "GUID: ",
                                    font=("Arial", 14, "bold"))
        self.label_guid.place(x = S_W *(38/144), y = S_H * (38/90))
        self.label_password = Label(self.log_in, text = "Password: ",
                                    font=("Arial", 14,"bold"))
        self.label_password.place(x=S_W*(38/144), y=S_H*(46/90))

        # create textboxs:
        self.textbox_guid = Entry(self.log_in, text = "", font=("Arial", 16))
        self.textbox_guid.place(x=S_W*(50/144), y=S_H*(37/90), width = 400, height = 50)
        self.textbox_password = Entry(self.log_in, text = "", show="*", font=("Arial", 16))
        self.textbox_password.place(x=S_W*(50/144), y=S_H*(45/90), width=400, height=50)
        #textbox_name["justify"] = "center"
        self.textbox_guid.focus()

        self.textbox3 = Label(self.log_in, text = "Please login here using your GUID if you "
                              "do not have a UofG email address",
                              font=("Arial", 22))
        self.textbox3.place(x=S_W*(10/144),y=S_H*(24/90), width=1200, height=35)
        self.textbox4 = Label(self.log_in, text = "If you have a UofG email address, please"
                              " close your browser and try again",
                              font=("Arial", 16,"bold"))
        self.textbox4.place(x=S_W*(30/144), y=S_H*(295/900), width=800, height=30)

        # create log-in button
        self.button_login = Button(self.log_in, text = "Log-in", font=("Arial", 16,"bold"),
                                   command = self.login)
        self.button_login.place(x=S_W*(425/1440), y=S_H*(55/90), width=200, height=50)

        # create register button
        self.button_register = Button(self.log_in, text = "Register now",
                                      font=("Arial", 16,"bold"),
                                      command = self.register)
        self.button_register.place(x=S_W*(725/1440), y=S_H*(55/90), width=200, height=50)


        self.textbox3 = Message(self.log_in, text="")
        self.textbox3.place(x=S_W*(600/1440), y=S_H*(610/900), width = 200, height = 35)
        # textbox3["bg"] = "gray"
        # textbox3["fg"] = "white"



    def login(self):
        id = self.textbox_guid.get()
        conn = sqlite3.connect("RIDENOW.db")
        c = conn.cursor()
        c.execute("SELECT * FROM Customer WHERE customer_id = ?", [id])
        id = c.fetchall()
        if id != []:
            e_password = self.textbox_password.get()
            print(id)
            if e_password == id[0][3]:
                id = self.textbox_guid.get()
                c.execute("SELECT username FROM Customer WHERE customer_id = ?", [id])
                name = c.fetchall()
                username = name[0][0]
                click = messagebox.askyesno("Login successfully!", "Hello {}, welcome come to 2BIKE!".format(username))
                if click:
                    self.ShowSuccess()
            else:
                # Password not matched
                click = messagebox.showerror("Login failed", "Invalid GUID or Password.")
                if click:
                    self.log_in.mainloop()
        else:
            # Invalid ID
            click = messagebox.showerror("Login failed", "Invalid GUID or Password.")
            if click:
                self.log_in.mainloop()

    def ShowSuccess(self):
        self.log_in.destroy()
        customer = CustomerUI()
        customer.show()

    def register(self):
        r = Register()
        r.show()


    def show(self):
        self.log_in.mainloop()
