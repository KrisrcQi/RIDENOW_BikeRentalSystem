from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random

FONT = ('Arial', 20)

class RentBike:

    def __init__(self, master) -> None:

        self.master = master

        # create frames
        self.frame_1 = Frame(self.master, width=500, height=300)
        self.frame_2 = Frame(self.master, width=500, height=300)
        self.frame_3 = Frame(self.master, width=500, height=300)
        self.frames = [self.frame_1, self.frame_2, self.frame_3]

        self.init_frame()
        self.show_f1()

    def forget_all(self):

        for frame in self.frames:
            frame.pack_forget()

    def show_f1(self):
        self.forget_all()
        self.frame_1.pack()

    def show_f2(self):
        self.forget_all()
        self.frame_2.pack()

    def show_f3(self):
        self.forget_all()
        self.frame_3.pack()

    def init_frame(self):
        self.f1()
        self.f2()
        self.f3()

    def confirm_unlock(self):
        click = messagebox.askyesno("Unlock", "The Unlocking bike is flashing!")
        if click:
            self.ShowSuccess()

    def ShowSuccess(self):
        Unlockpassword_window = Tk()
        Unlockpassword_window.title("Unlocking password")
        unlockpassword_1 = random.random()
        unlockpassword_2 = int(unlockpassword_1*10000)
        label = Label(Unlockpassword_window, text="{}".format(unlockpassword_2),font=FONT)
        label.place(x=100, y=50)
        Unlockpassword_window.geometry("250x150+575+325")
        self.show_f2()
    def f1(self):
        self.l_location = Label(self.frame_1, text='Location:', font=FONT)
        self.l_location.place(x=50, y=60)
        self.comb_location = ttk.Combobox(self.frame_1)
        self.comb_location.place(x=200, y=60, width=180, height=30)

        self.l_type = Label(self.frame_1, text='Bike Type:', font=FONT)
        self.l_type.place(x=50, y=120)
        self.comb_type = ttk.Combobox(self.frame_1)
        self.comb_type.place(x=200, y=120, width=180, height=30)

        self.l_avail = Label(self.frame_1, text='Bike Available:',
                             font=FONT)
        self.l_avail.place(x=50, y=180)
        self.comb_avail = ttk.Combobox(self.frame_1)
        self.comb_avail.place(x=200, y=180, width=180, height=30)

        self.btn = Button(self.frame_1, text="Rent", font=FONT,
                          command=self.confirm_unlock)
        self.btn.place(x=170, y=230, width=160, height=50)

    def f2(self):

        # crate labels
        self.f2_title = Label(self.frame_2, text='Current Riding', font=FONT)
        self.l_bike_id = Label(self.frame_2, text='Bike id:', font=FONT)
        self.l_bike_type = Label(self.frame_2, text='Bike Type:', font=FONT)
        self.l_start_time = Label(self.frame_2, text='Start Time:', font=FONT)
        self.l_riding_time = Label(self.frame_2, text='Riding Time', font=FONT)

        self.btn_return_bike = Button(self.frame_2, text='Return Bike',
                                      font=FONT, command=self.show_f3)

        self.f2_title.place(x=200, y=40)
        self.l_bike_id.place(x=40, y=80)
        self.l_bike_type.place(x=40, y=120)
        self.l_start_time.place(x=40, y=160)
        self.l_riding_time.place(x=40, y=200)

        self.btn_return_bike.place(x=170, y=240, width=150)

    def f3(self):

        self.f3_title = Label(self.frame_3, text='Make your Payment', font=FONT)
        self.l_bike_id = Label(self.frame_3, text='Bike id:', font=FONT)
        self.l_bike_type = Label(self.frame_3, text='Bike Type:', font=FONT)
        self.l_start_time = Label(self.frame_3, text='Start Time:', font=FONT)
        self.l_end_time = Label(self.frame_3, text='End Time:',font=FONT)
        self.l_riding_time = Label(self.frame_3, text='Riding Time:', font=FONT)
        self.l_price = Label(self.frame_3, text='Price', font=FONT)

        self.btn_comf_pay = Button(self.frame_3, text='Confirm Payment',
                                   font=FONT, command=self.show_f1)

        self.f3_title.place(x=180, y=40)
        self.l_bike_id.place(x=40, y=80)
        self.l_bike_type.place(x=260, y=80)
        self.l_start_time.place(x=40, y=120)
        self.l_end_time.place(x=260, y=120)
        self.l_riding_time.place(x=40, y=160)
        self.l_price.place(x=260, y=160)

        self.btn_comf_pay.place(x=160, y=240)


class Report:

    def __init__(self, master) -> None:

        self.master = master

        self.frame_1 = Frame(self.master, width=500, height=400)
        self.frame_2 = Frame(self.master, width=500, height=400)
        self.frame_3 = Frame(self.master, width=500, height=400)
        self.frames = [self.frame_1, self.frame_2, self.frame_3]

        self.init_frames()
        self.frame_1.pack()


    def init_frames(self):
        self.f1()
        self.f2()
        self.f3()

    def show_f1(self):
        self.forget_all()
        self.frame_1.pack()

    def show_f2(self):
        self.forget_all()
        self.frame_2.pack()

    def show_f3(self):
        self.forget_all()
        self.frame_3.pack()


    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def f1(self):
        self.btn_new_report = Button(self.frame_1, text='Create New Report',
                                     font=FONT, command=self.show_f2)
        self.btn_pro = Button(self.frame_1, text='Processing', font=FONT,
                              command=self.show_f3)

        self.btn_new_report.place(x=40, y=80)
        self.btn_pro.place(x=40, y=150)

    def f2(self):

        self.l_bike_id = Label(self.frame_2, text='Bike id:', font=FONT)
        self.l_bike_type = Label(self.frame_2, text='Bike type:', font=FONT)
        self.l_time = Label(self.frame_2, text='Time:', font=FONT)
        self.l_loca = Label(self.frame_2, text='*Location:', font=FONT)
        self.l_err_type = Label(self.frame_2, text='*Error Type:', font=FONT)
        self.l_desc = Label(self.frame_2, text='*Description(0-100):', font=FONT)
        self.l_pic = Label(self.frame_2, text='Picture(Option):', font=FONT)

        self.e_time = Entry(self.frame_2)
        self.comb_loca = ttk.Combobox(self.frame_2)
        self.comb_err = ttk.Combobox(self.frame_2)
        self.btn_upload = Button(self.frame_2, text='upload', font=FONT)
        self.btn_return = Button(self.frame_2, text='Return', font=FONT,
                                 command=self.show_f1)
        self.btn_submit = Button(self.frame_2, text='Submit', font=FONT)

        self.l_bike_id.place(x=40, y=40)
        self.l_bike_type.place(x=260, y=40)
        self.l_time.place(x=40, y=80)
        self.e_time.place(x=220, y=80, height=30, width=200)
        self.l_loca.place(x=40, y=120)
        self.comb_loca.place(x=220, y=120, height=30, width=200)
        self.l_err_type.place(x=40, y=160)
        self.comb_err.place(x=220, y=160, height=30, width=200)
        self.l_desc.place(x=40, y=200)
        self.l_pic.place(x=40, y=240)
        self.btn_upload.place(x=220, y=240, height=30, width=200)
        self.btn_return.place(x=40, y=280, height=30, width=120)
        self.btn_submit.place(x=260, y=280, height=30, width=120)



    def f3(self):
        self.btn_return = Button(self.frame_3, text='Return', font=FONT,
                                 command=self.show_f1)
        self.btn_return.place(x=40, y=280, height=30, width=120)



class My:

    def __init__(self) -> None:
        pass


class CustomerUI:

    def __init__(self) -> None:

        self.master = Tk()
        self.master.title("Customer")
        self.master.geometry("500x320+500+300")
        self.font = ('Arial', 14)

        # create frames
        self.frame_1 = Frame(self.master, width=500, height=300)
        self.frame_2 = Frame(self.master, width=500, height=300)
        self.frame_3 = Frame(self.master, width=500, height=300)
        self.frames = [self.frame_1, self.frame_2, self.frame_3]

        self.btn_1 = Button(self.master, text='Rent Bike',
                            command=self.show_frame1, font=('Arial', 14))
        self.btn_1.place(x=0, y=0, width=500/3., height=30)

        self.btn_2 = Button(self.master, text='Report',
                            command=self.show_frame2, font=('Arial', 14))
        self.btn_2.place(x=500/3, y=0, width=500/3., height=30)

        self.btn_3 = Button(self.master, text='My',
                            command=self.show_frame3, font=('Arial', 14))
        self.btn_3.place(x=500/3*2, y=0, width=500/3., height=30)
        self.btns = [self.btn_1, self.btn_2, self.btn_3]

        # init frame
        self.rent_bike = RentBike(self.frame_1)
        self.report = Report(self.frame_2)

        self.show_frame1()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def reset_btn_bg(self):
        for btn in self.btns:
            btn.configure(bg='SystemButtonFace')

    def show_frame1(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_1.configure(bg='red')
        self.frame_1.pack()


    def show_frame2(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_2.configure(bg='red')
        self.frame_2.pack()

    def show_frame3(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_3.configure(bg='red')
        self.frame_3.pack()

    def show(self):
        self.master.mainloop()


if __name__ == '__main__':
    c = CustomerUI()
    c.show()
