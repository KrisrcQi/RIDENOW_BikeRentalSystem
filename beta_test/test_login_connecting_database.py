from tkinter import *
import sqlite3



def login():
    e_name = textbox_name.get()
    conn = sqlite3.connect("test.db")
    print("Database creating successfully")
    c = conn.cursor()
    c.execute("SELECT * FROM Customer WHERE username = ?",[e_name])
    id = c.fetchall()
    e_password = textbox_password.get()
    print(id)
    if e_password == id[0][3]:
        name = textbox_name.get()
        msg = str(" Welcome {}".format(name))
        textbox3["bg"] = "white"
        textbox3["fg"] = "black"
        textbox3["text"] = msg





# define click function:


# create a Log-in window:
window = Tk()
window.title("UofG Log-in")
window.geometry("1400x800")
# window.configure(background = "white")


# insert image:
logo = PhotoImage(file = "/Users/ruochenqi/Documents/Fintech in UofG/WechatIMG574.jpg")
logoimage = Label(image = logo)
logoimage.place(x = 380 , y = 20, width = 647, height = 200)

# create labels:
label_username = Label(text = "Username: ", font=("Arial", 16,"bold"))
label_username.place(x=400, y=380)
label_password = Label(text = "Password: ", font=("Arial", 16,"bold"))
label_password.place(x=400, y=460)

# create textboxs:
textbox_name = Entry(text = "", font=("Arial", 16))
textbox_name.place(x=500,y=370, width = 400, height = 50)
textbox_password = Entry(text = "", font=("Arial", 16))
textbox_password.place(x=500,y=450, width = 400, height = 50)
#textbox_name["justify"] = "center"
textbox_name.focus()

textbox3 = Label(text = "Please login here using your GUID if you do not have a UofG email address", font=("Arial", 22))
textbox3.place(x=300,y=240, width = 807, height = 30)
textbox4 = Label(text = "If you have a UofG email address, please close your browser and try again", font=("Arial", 16,"bold"))
textbox4.place(x=300,y=295, width = 807, height = 30)


# create log-in button
button_login = Button(text = "Log-in", font=("Arial", 16,"bold"), command = login)
button_login.place(x = 625, y = 550, width = 150, height = 50)


textbox3 = Message(text = "")
textbox3.place(x=600, y=610, width = 200, height = 35)
# textbox3["bg"] = "gray"
# textbox3["fg"] = "white"

window.mainloop()

