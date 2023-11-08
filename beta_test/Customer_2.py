import os.path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import sqlite3
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import *
from PIL import Image, ImageTk
from tkinterweb import HtmlFrame
from datetime import datetime
from ManipulateDatabase import CusOpenDatabase
from datetime import timedelta
import time

# Size of text:
FONT = ('Arial', 20)
FONT_TOP = ('Arial', 20, 'bold')
FONT_TITLE = ('Arial', 50, 'bold')

# Size of entry
HEIGHT = 50
WIDTH = 300


class RentBike:

    def __init__(self, master) -> None:

        self.master = master
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        print("The current opening window size is: {}x{}".format(S_W, S_H))
        # create frames
        # Edition: f1 = frame_rent; f2 = frame_current_riding; f3 = frame_make_payment
        self.frame_rent = Frame(self.master, width=S_W, height=S_H)
        self.frame_current_riding = Frame(self.master, width=S_W, height=S_H)
        self.frame_make_payment = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_rent, self.frame_current_riding, self.frame_make_payment]

        self.init_frames()
        self.show_frame_rent()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def show_frame_rent(self):
        self.forget_all()
        self.frame_rent.pack()

    def show_frame_current_riding(self):
        self.forget_all()
        self.frame_current_riding.pack()

    def show_frame_make_payment(self):
        self.forget_all()
        self.insertReturnBikeInfo()
        self.frame_make_payment.pack()

    def init_frames(self):
        self.frent()
        self.fcurrent_riding()
        self.fmake_payment()

    def insertReturnBikeInfo(self):
        riding_time = self.reset()
        return_bike_1 = CusOpenDatabase()
        return_bike_1.insert_returnBikeTrackData(riding_time)
        return_bike_1.insert_return_location(self.selected_where_return.get())

    def confirm_unlock(self):
        click = messagebox.askyesno("Unlock", "Unlocking bike is flashing!")
        if click:
            insert_tracking_history = CusOpenDatabase()
            insert_tracking_history.insert_rentTrackData(self.comb_type.get(), self.comb_location.get())
            self.start_stop()
            self.ShowSuccess()

    def ShowSuccess(self):
        Unlockpassword_window = Tk()
        Unlockpassword_window.title("Unlocking password")
        unlockpassword_1 = random.random()
        unlockpassword_2 = int(unlockpassword_1 * 100000)
        label = Label(Unlockpassword_window, text="{}".format(unlockpassword_2), font=FONT)
        label.place(x=100, y=50)
        Unlockpassword_window.geometry("250x150+575+325")
        self.show_frame_current_riding()

    def open_database(self):
        self.conn = sqlite3.connect("RIDENOW.db")
        self.c = self.conn.cursor()

    def start_stop(self):
        if self.running:
            self.stop_time = self.elapsed_time()
            self.running = False
            self.riding_time_var.set(self.format_time(self.stop_time))
        else:
            self.start()

    def start(self):
        self.running = True
        self.start_time = time.time()

    def reset(self):
        if not self.running:
            self.start()
        else:
            self.stop_time = self.elapsed_time()
            self.running = False
            self.riding_time_var.set(self.format_time(self.stop_time))
        riding_time = self.riding_time_var.get()
        print("Running Time:", riding_time)
        self.riding_time_var.set("")
        return riding_time

    def elapsed_time(self):
        if self.start_time is None:
            return 0
        return time.time() - self.start_time

    def format_time(self, seconds):
        return str(timedelta(seconds=seconds))[:-4]  # Remove milliseconds

    def update(self):
        if self.running:
            elapsed_time = self.elapsed_time()
            formatted_time = self.format_time(elapsed_time)
            self.label_var.set(formatted_time)
        else:
            if self.stop_time is not None:
                formatted_time = self.format_time(self.stop_time)
                self.label_var.set(formatted_time)
            else:
                self.label_var.set("00:00:00.00")

        self.frame_current_riding.after(10, self.update)  # Update every 10 milliseconds

    def check_available_bike(self):
        get_bike_number_1 = CusOpenDatabase()
        selected_bike_number = get_bike_number_1.get_bike_number(self.comb_type.get(), self.comb_location.get())
        message = str("{} bikes are available in {} now".format(selected_bike_number[0][0], self.comb_location.get()))
        self.l_avail["text"] = message

    def select_where_return(self):
        location_selection = CusOpenDatabase()
        loc_selected = location_selection.select_parking_location()
        return loc_selected

    def frent(self):

        # create labels:
        self.l_location = Label(self.frame_rent, text='Location:', font=FONT)
        self.l_type = Label(self.frame_rent, text='Bike Type:', font=FONT)
        self.l_avail = Label(self.frame_rent, text="", font=FONT)

        # create comboboxs based on the parking_lots selection:
        self.selected_value_1 = StringVar()
        select_parking_location_1 = CusOpenDatabase()
        parking_location = select_parking_location_1.select_parking_location()
        self.comb_location = ttk.Combobox(self.frame_rent, textvariable=self.selected_value_1, values=parking_location)
        self.comb_type = ttk.Combobox(self.frame_rent, values=["electric_bike", "foot_bike"])

        # create button:
        self.btn_avail = Button(self.frame_rent, text='Check Availability:', font=FONT,
                                command=self.check_available_bike)
        self.btn = Button(self.frame_rent, text="Rent", font=FONT,
                          command=self.confirm_unlock)

        # place labels:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_location.place(x=S_W * (3 / 10), y=S_H * (1 / 5))
        self.l_type.place(x=S_W * (3 / 10), y=S_H * (2 / 5))
        self.l_avail.place(x=S_W * (5 / 10), y=S_H * (3 / 5), width=400, height=40)
        # place combs:
        self.comb_location.place(x=S_W * (5 / 10), y=S_H * (1 / 5), width=330, height=40)
        self.comb_type.place(x=S_W * (5 / 10), y=S_H * (2 / 5), width=330, height=40)
        # place buttons:
        self.btn.place(x=S_W * (22 / 50), y=S_H * (23 / 30), width=200, height=50)
        self.btn_avail.place(x=S_W * (3 / 10), y=S_H * (3 / 5))

    def fcurrent_riding(self):

        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        # create labels
        self.frame_current_riding_title = Label(self.frame_current_riding, text='Current Riding', font=FONT)
        self.l_bike_id = Label(self.frame_current_riding, text='Bike id:', font=FONT)
        self.l_bike_type = Label(self.frame_current_riding, text='Bike Type:', font=FONT)
        self.l_start_time = Label(self.frame_current_riding, text='Start Time:', font=FONT)
        self.l_riding_time = Label(self.frame_current_riding, text='Riding Time:', font=FONT)
        self.l_select_return_location = Label(self.frame_current_riding, text='Where to Return:', font=FONT)

        # get the current rent bike info by the funtion in class ManipulateDatabase
        current_BikeInfo = CusOpenDatabase()
        current_rent_bike = current_BikeInfo.get_currentBikeInfo()
        current_time = datetime.now()

        # create the label for showing renting bike info
        self.l_bike_id_show = Label(self.frame_current_riding, text='{}'.format(current_rent_bike[1]), font=FONT_TOP)
        self.l_bike_type_show = Label(self.frame_current_riding, text='{}'.format(current_rent_bike[7]), font=FONT_TOP)
        self.l_startTime_show = Label(self.frame_current_riding, text='{}'.format(current_time), font=FONT_TOP)

        # set a stopwatch for store riding_time
        self.start_time = None
        self.stop_time = None
        self.running = False
        self.label_var = StringVar()
        self.label_var.set("00:00:00.00")
        self.riding_time_var = StringVar()
        self.update()
        self.l_ridingTime_show = Label(self.frame_current_riding, textvariable=self.label_var, font=FONT_TOP)

        # create button
        self.btn_return_bike = Button(self.frame_current_riding, text='Return Bike', font=FONT,
                                      command=self.show_frame_make_payment)

        # create selection combobox
        self.selected_where_return = StringVar()
        select_parking_location_1 = CusOpenDatabase()
        parking_location = select_parking_location_1.select_parking_location()
        self.comb_location_return = ttk.Combobox(self.frame_current_riding, textvariable=self.selected_where_return,
                                                 values=parking_location)

        # create map frame
        # self.myhtmlframe = HtmlFrame(self.frame_current_riding, width=S_W/6, height=S_H*(4/10))
        # self.myhtmlframe.place(x=S_W*(2/5), y=S_H*(2/10))
        # self.myhtmlframe.load_file("/Users/ruochenqi/PycharmProjects/pythonProject/Bike rental system/Map_for_2BIKE.html")

        # place label
        self.frame_current_riding_title.place(x=S_W * (8 / 50), y=S_H * (2 / 15), width=200, height=50)
        self.l_bike_id.place(x=S_W * (2 / 25), y=S_H * (4 / 15))
        self.l_bike_id_show.place(x=S_W * (4 / 25), y=S_H * (4 / 15))
        self.l_bike_type.place(x=S_W * (2 / 25), y=S_H * (6 / 15))
        self.l_bike_type_show.place(x=S_W * (4 / 25), y=S_H * (6 / 15))
        self.l_start_time.place(x=S_W * (2 / 25), y=S_H * (8 / 15))
        self.l_startTime_show.place(x=S_W * (4 / 25), y=S_H * (8 / 15))
        self.l_riding_time.place(x=S_W * (2 / 25), y=S_H * (10 / 15))
        self.l_ridingTime_show.place(x=S_W * (4 / 25), y=S_H * (10 / 15))
        self.l_select_return_location.place(x=S_W * (2 / 25), y=S_H * (23 / 30))

        # place button:
        self.btn_return_bike.place(x=S_W * (8 / 50), y=S_H * (13 / 15), width=200, height=50)

        # place combobox:
        self.comb_location_return.place(x=S_W * (5 / 25), y=S_H * (23 / 30), width=200, height=30)

    def fmake_payment(self):

        # create labels:
        self.frame_make_payment_title = Label(self.frame_make_payment, text='Make your Payment', font=FONT)
        self.l_bike_id = Label(self.frame_make_payment, text='Bike id:', font=FONT)
        self.l_bike_type = Label(self.frame_make_payment, text='Bike Type:', font=FONT)
        self.l_start_time = Label(self.frame_make_payment, text='Start Time:', font=FONT)
        self.l_end_time = Label(self.frame_make_payment, text='End Time:', font=FONT)
        self.l_riding_time = Label(self.frame_make_payment, text='Riding Time:', font=FONT)
        self.l_price = Label(self.frame_make_payment, text='Price:', font=FONT)

        # get the payment_info_data and price
        current_riding_data = CusOpenDatabase()
        payment_info_data = current_riding_data.get_currentBikeInfo()
        price = current_riding_data.get_price()
        # show these labels:
        self.l_bike_id_show = Label(self.frame_make_payment, text='{}'.format(payment_info_data[1]), font=FONT)
        self.l_bike_type_show = Label(self.frame_make_payment, text='{}'.format(payment_info_data[7]), font=FONT)
        self.l_start_time_show = Label(self.frame_make_payment, text='{}'.format(payment_info_data[4]), font=FONT)
        self.l_end_time_show = Label(self.frame_make_payment, text='{}'.format(payment_info_data[5]), font=FONT)
        self.l_riding_time_show = Label(self.frame_make_payment, text='{}'.format(payment_info_data[6]), font=FONT)
        self.l_price_show = Label(self.frame_make_payment, text='${}'.format(price), font=FONT)

        # create button:
        self.btn_comf_pay = Button(self.frame_make_payment, text='Confirm Payment',
                                   font=FONT, command=self.show_frame_rent)

        # place labels:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.frame_make_payment_title.place(x=S_W * (22 / 50), y=S_H * (2 / 15))
        self.l_bike_id.place(x=S_W * (4 / 25), y=S_H * (4 / 15))
        self.l_bike_type.place(x=S_W * (15 / 25), y=S_H * (4 / 15))
        self.l_start_time.place(x=S_W * (4 / 25), y=S_H * (6 / 15))
        self.l_end_time.place(x=S_W * (15 / 25), y=S_H * (6 / 15))
        self.l_riding_time.place(x=S_W * (4 / 25), y=S_H * (8 / 15))
        self.l_price.place(x=S_W * (15 / 25), y=S_H * (8 / 15))

        self.l_bike_id_show.place(x=S_W * (6 / 25), y=S_H * (4 / 15))
        self.l_bike_type_show.place(x=S_W * (17 / 25), y=S_H * (4 / 15))
        self.l_start_time_show.place(x=S_W * (6 / 25), y=S_H * (6 / 15))
        self.l_end_time_show.place(x=S_W * (17 / 25), y=S_H * (6 / 15))
        self.l_riding_time_show.place(x=S_W * (6 / 25), y=S_H * (8 / 15))
        self.l_price_show.place(x=S_W * (17 / 25), y=S_H * (8 / 15))
        # place button:
        self.btn_comf_pay.place(x=S_W * (21 / 50), y=S_H * (12 / 15), width=200, height=50)


class Report:

    def __init__(self, master, guid=None) -> None:

        self.master = master
        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()
        self.guid = guid
        # edition: frame_1 = frame_report; frame_2 = frame_create_new_rp; frame_3 = frame_processing
        self.frame_report = Frame(self.master, width=S_W, height=S_H)
        self.frame_create_new_rp = Frame(self.master, width=S_W, height=S_H)
        self.frame_processing = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_report, self.frame_create_new_rp, self.frame_processing]
        self.img_path = None
        self.init_frames()
        self.frame_report.pack()

    def init_frames(self):
        self.freport()
        self.fcreate_new_rp()
        self.fprocessing()

    def show_frame_report(self):
        self.forget_all()
        self.frame_report.pack()

    def show_frame_create_new_rp(self):
        self.forget_all()
        self.frame_create_new_rp.pack()

    def show_frame_processing(self):
        self.fprocessing()
        self.forget_all()
        self.frame_processing.pack()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def freport(self):

        # create buttons:
        self.btn_new_report = Button(self.frame_report, text='Create New Report', font=FONT,
                                     command=self.show_frame_create_new_rp)
        self.btn_pro = Button(self.frame_report, text='Processing', font=FONT,
                              command=self.show_frame_processing)

        # place buttons:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.btn_new_report.place(x=S_W * (2 / 25), y=S_H * (4 / 15), width=200, height=50)
        self.btn_pro.place(x=S_W * (2 / 25), y=S_H * (1 / 2), width=200, height=50)

    def upload_img(self):
        filename = askopenfilename(title='Select Picture', filetypes=[(('JPG', '*.jpg')), ('All Files', '*')])
        with open(filename, 'rb') as w:
            with open(os.path.join('image', filename), 'wb') as f:
                f.write(w.read())
        self.img_path = StringVar()
        self.img_path.set(filename)
        lb1 = Label(self.frame_create_new_rp, text=filename, textvariable=self.img_path)
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        lb1.place(x=S_W * (10 / 25), y=S_H * (10 / 15))

    def submit(self):
        print(self.guid)
        report_time = self.e_time.get()
        location = self.selected_value_1.get()
        err_type = self.err_type.get()
        desc = self.r_desc.get()
        img_path = ''
        if self.img_path:
            img_path = os.path.join('image', self.img_path.get())
        if not location:
            messagebox.showerror('error', "lack location!")
            return
        if not err_type:
            messagebox.showerror('error', "lack err_type!")
            return
        if not desc:
            messagebox.showerror('error', "lack desc!")
            return
        conn = sqlite3.connect("2BIKE_1.db")
        c = conn.cursor()

        c.execute(
            """insert into report (username,report_time,location,err_type,Desc,img_path,Status) values(?,?,?,?,?,?,?)""",
            [self.guid, report_time, location, err_type, desc, img_path, "processing"])
        conn.commit()
        conn.close()
        messagebox.showinfo('success', "report success!")

    def fcreate_new_rp(self):

        # create labels:
        self.l_bike_id = Label(self.frame_create_new_rp, text='Bike id:', font=FONT)
        self.l_bike_type = Label(self.frame_create_new_rp, text='Bike type:', font=FONT)
        self.l_time = Label(self.frame_create_new_rp, text='Time:', font=FONT)
        self.l_loca = Label(self.frame_create_new_rp, text='*Location:', font=FONT)
        self.l_err_type = Label(self.frame_create_new_rp, text='*Error Type:', font=FONT)
        self.l_desc = Label(self.frame_create_new_rp, text='*Description(0-100):', font=FONT)
        self.desc = StringVar()
        self.r_desc = Entry(self.frame_create_new_rp, textvariable=self.desc, font=FONT, )
        self.l_pic = Label(self.frame_create_new_rp, text='Picture(Option):', font=FONT)
        # create entries and combos:
        self.now_time = StringVar()
        self.now_time.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.e_time = Entry(self.frame_create_new_rp, textvariable=self.now_time)
        select_parking_location_1 = CusOpenDatabase()
        self.selected_value_1 = StringVar()
        parking_location = select_parking_location_1.select_parking_location()
        self.comb_loca = ttk.Combobox(self.frame_create_new_rp, textvariable=self.selected_value_1,
                                      values=parking_location)
        self.err_type = StringVar()
        self.comb_err = ttk.Combobox(self.frame_create_new_rp, values=["electric_bike", "foot_bike"],
                                     textvariable=self.err_type)
        # create buttons:
        self.btn_upload = Button(self.frame_create_new_rp, text='upload', font=FONT, command=self.upload_img)
        self.btn_return = Button(self.frame_create_new_rp, text='Return', font=FONT,
                                 command=self.show_frame_report)
        self.btn_submit = Button(self.frame_create_new_rp, text='Submit', font=FONT, command=self.submit)

        # place components:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.l_bike_id.place(x=S_W * (6 / 25), y=S_H * (1 / 15))
        self.l_bike_type.place(x=S_W * (15 / 25), y=S_H * (1 / 15))
        self.l_time.place(x=S_W * (6 / 25), y=S_H * (2 / 15))
        self.e_time.place(x=S_W * (11 / 25), y=S_H * (2 / 15), height=30, width=400)
        self.l_loca.place(x=S_W * (6 / 25), y=S_H * (4 / 15))
        self.comb_loca.place(x=S_W * (11 / 25), y=S_H * (4 / 15), height=30, width=400)
        self.l_err_type.place(x=S_W * (6 / 25), y=S_H * (6 / 15))
        self.comb_err.place(x=S_W * (11 / 25), y=S_H * (6 / 15), height=30, width=400)
        self.l_desc.place(x=S_W * (6 / 25), y=S_H * (8 / 15))
        self.r_desc.place(x=S_W * (11 / 25), y=S_H * (8 / 15), height=100, width=400)
        self.l_pic.place(x=S_W * (6 / 25), y=S_H * (10 / 15))
        self.btn_upload.place(x=S_W * (11 / 25), y=S_H * (11 / 15), height=30, width=200)
        self.btn_return.place(x=S_W * (2 / 25), y=S_H * (11 / 15), height=30, width=120)
        self.btn_submit.place(x=S_W * (20 / 25), y=S_H * (11 / 15), height=30, width=120)

    def onSelect(self, e):
        # 切换
        ss = self.tree.selection()
        for s in ss:
            itm = self.tree.set(s)
            self.report_id = itm.get('report_id')

    def show_deatil(self):
        report_id = self.report_id
        top1 = Toplevel()
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        top1.title('report detail')
        top1.geometry("{}x{}".format(S_W - 1000, S_H - 600))
        conn = sqlite3.connect("2BIKE_1.db")
        c = conn.cursor()

        c.execute(
            """select * from report where report_id=?""",
            [report_id])
        record = c.fetchone()
        canvas = Canvas(top1, width=400, height=600)
        Label(canvas, text='report_time:{}'.format(record[2]), font=FONT).place(x=30, y=30)
        Label(canvas, text='location：{}'.format(record[3]), font=FONT).place(x=30, y=80)
        Label(canvas, text='err_type：{}'.format(record[4]), font=FONT).place(x=30, y=130)
        Label(canvas, text='desc：{}'.format(record[5]), font=FONT).place(x=30, y=180)
        Label(canvas, text='status：{}'.format(record[7]), font=FONT).place(x=30, y=230)
        canvas.pack()
        top1.mainloop()

    def fprocessing(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        Label(self.frame_processing, text='report records', font=FONT).place(x=S_W * (5 / 25), y=S_H * (3 / 15))
        conn = sqlite3.connect("2BIKE_1.db")
        c = conn.cursor()

        c.execute(
            """select * from report where username=? and status='processing'""",
            [self.guid])
        records = c.fetchall()
        columns = ("report_id", "report_time", "location", "err_type", "desc", "option")
        self.tree = ttk.Treeview(self.frame_processing, height=14, show="headings", columns=columns)
        self.tree.column("report_id", width=250)
        self.tree.column("report_time", width=250)
        self.tree.column("location", width=250)
        self.tree.column("err_type", width=250)
        self.tree.column("desc", width=250)
        self.tree.place(x=S_W * (3 / 25), y=S_H * (4 / 15))
        self.tree.heading("report_id", text='report_id', anchor=CENTER)
        self.tree.heading("report_time", text='report_time', anchor=CENTER)
        self.tree.heading("location", text='location', anchor=CENTER)
        self.tree.heading("err_type", text='err_type', anchor=CENTER)
        self.tree.heading("desc", text='desc', anchor=CENTER)
        for record in records:
            self.tree.insert("", 0, values=(record[0], record[2], record[3], record[4], record[5]))
        self.tree.bind("<<TreeviewSelect>>", self.onSelect)
        conn.commit()
        conn.close()
        self.detail_btn = Button(self.frame_processing, text='Detail', font=FONT,
                                 command=self.show_deatil)
        # create button:
        self.btn_return = Button(self.frame_processing, text='Return', font=FONT,
                                 command=self.show_frame_report)
        # place button:
        self.btn_return.place(x=S_W * (2 / 25), y=S_H * (11 / 15), height=30, width=120)
        self.detail_btn.place(x=S_W * (8 / 25), y=S_H * (11 / 15), height=30, width=120)


class My:

    def __init__(self, master, guid) -> None:

        self.master = master
        self.guid = guid
        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()
        self.amount = 0
        self.conn = sqlite3.connect("2BIKE_1.db")
        self.c = self.conn.cursor()
        self.frame_my = Frame(self.master, width=S_W, height=S_H)
        self.frame_top_up = Frame(self.master, width=S_W, height=S_H)
        self.frame_transaction_history = Frame(self.master, width=S_W, height=S_H)
        self.frame_rent_history = Frame(self.master, width=S_W, height=S_H)
        self.frame_rent_detail = Frame(self.master, width=S_W, height=S_H)
        self.frame_report_history = Frame(self.master, width=S_W, height=S_H)
        self.frame_report_detail = Frame(self.master, width=S_W, height=S_H)
        self.frame_change_password = Frame(self.master, width=S_W, height=S_H)
        self.frame_payment_selection = Frame(self.master, width=S_W, height=S_H)
        self.frame_confirm_payment_info = Frame(self.master, width=S_W, height=S_H)
        self.frame_new_password = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_my, self.frame_top_up, self.frame_transaction_history,
                       self.frame_rent_history, self.frame_report_history, self.frame_change_password,
                       self.frame_payment_selection, self.frame_confirm_payment_info, self.frame_new_password,
                       self.frame_report_detail, self.frame_rent_detail]

        self.init_frames()
        self.frame_my.pack()

    def init_frames(self):
        self.fmy()
        self.ftop_up()
        self.fpayment_selection()
        self.fconfirm_payment_info()
        self.ftransaction_history()
        self.frent_history()
        self.frent_detail()
        self.freport_history()
        self.freport_detail()
        self.fchange_password()
        self.fnew_password()

    def show_frame_my(self):
        self.forget_all()
        self.frame_my.pack()

    def show_frame_top_up(self):
        self.forget_all()
        self.frame_top_up.pack()

    def show_frame_payment_selection(self):
        if not self.amount:
            messagebox.showerror(message='Please select the recharge amount')
            return
        self.forget_all()
        self.frame_payment_selection.pack()

    def show_frame_confirm_payment_info(self):

        if not self.card.get():
            messagebox.showerror(message='Please select the card')
            return
        self.fconfirm_payment_info()
        self.forget_all()
        self.frame_confirm_payment_info.pack()

    def show_frame_transaction_history(self):
        self.forget_all()
        self.frame_transaction_history.pack()

    def show_frame_rent_history(self):
        self.forget_all()
        self.frame_rent_history.pack()

    def show_frame_rent_detail(self):
        self.forget_all()
        self.frame_rent_detail.pack()

    def show_frame_report_history(self):
        self.forget_all()
        self.frame_report_history.pack()

    def show_frame_report_detail(self):
        self.forget_all()
        self.frame_report_detail.pack()

    def show_frame_change_password(self):
        self.forget_all()
        self.frame_change_password.pack()

    def show_frame_new_password(self):
        self.forget_all()
        self.frame_new_password.pack()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def open_database(self):
        self.conn = sqlite3.connect("2BIKE_1.db")
        self.c = self.conn.cursor()

    def edit_name(self):
        username = askstring('Please enter username', prompt='username:', initialvalue='')
        if not username:
            messagebox.showerror(message='username error')
            return
        self.c.execute("update Customer set username=? where customer_id=?", (username, self.guid))
        self.conn.commit()
        self.init_frames()
        return

    def edit_email(self):
        email = askstring('Please enter email', prompt='email:', initialvalue='')
        if not email:
            messagebox.showerror(message='email error')
            return
        self.c.execute("update Customer set email=? where customer_id=?", (email, self.guid))
        self.conn.commit()
        self.init_frames()
        return

    def GBP5(self):
        self.amount = 5
        return

    def GBP10(self):
        self.amount = 10
        return

    def GBP20(self):
        self.amount = 20
        return

    def GBP50(self):
        self.amount = 50
        return

    def confirm_pay(self):
        if self.Amount < self.amount:
            messagebox.showerror(message="Insufficient account amount")
            return
        self.Amount -= self.amount
        self.c.execute("update Customer set credit=? where customer_id=? ", (self.Amount, self.guid))
        self.c.execute("insert into Credit_log (amount,type,Customer_ID,Date) values(?,?,?,?)",
                       (self.amount, "top-up", self.guid, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
        click = messagebox.askyesno(message="Successful Payment!")
        if click:
            self.show_frame_my()

    def check_old_password(self):
        his_password=self.his_password.get()
        if not his_password:
            messagebox.showerror(message='Please enter the password')
            return
        self.c.execute("select password from Customer where customer_id=?",(self.guid,))
        password=self.c.fetchone()[0]
        if password!=his_password:
            messagebox.showerror(message='The password is incorrect')
            return
        self.fconfirm_payment_info()
        self.forget_all()
        self.frame_new_password.pack()

    def confirm_new_password(self):

        new_entry = self.e_new_password.get()
        repeat_entry = self.e_repeat_password.get()
        if new_entry and new_entry == repeat_entry:
            self.c.execute("update Customer set password=? where customer_id=?",(new_entry,self.guid,))
            messagebox.showinfo(message="Success!")
            self.show_frame_my()
        else:
            messagebox.showerror(message="Passwords are not matched!")

    def fmy(self):
        conn = sqlite3.connect("2BIKE_1.db")
        c = conn.cursor()
        c.execute(
            """select * from Customer where customer_id=?""",
            [self.guid])
        user = c.fetchone()
        conn.close()
        # create labels:
        self.l_user_id = Label(self.frame_my, text="User ID: ", font=FONT)
        self.l_user_id_show = Label(self.frame_my, text=user[0], font=FONT)
        self.l_user_name = Label(self.frame_my, text="Username: ", font=FONT)
        self.l_user_name_show = Label(self.frame_my, text=user[1], font=FONT)
        self.l_email = Label(self.frame_my, text="E-mail: ", font=FONT)
        self.l_email_show = Label(self.frame_my, text=user[2], font=FONT)
        self.l_account_credit = Label(self.frame_my, text="Account credit: ", font=FONT)
        self.l_account_credit_show = Label(self.frame_my, text=user[3], font=FONT)

        # create buttons:
        self.btn_edit_name = Button(self.frame_my, text="Edit", font=FONT,
                                    command=self.edit_name)
        self.btn_edit_email = Button(self.frame_my, text="Edit", font=FONT,
                                     command=self.edit_email)
        self.btn_top_up = Button(self.frame_my, text="Top-up", font=FONT,
                                 command=self.show_frame_top_up)
        self.btn_transaction_history = Button(self.frame_my, text="Transaction History", font=FONT,
                                              command=self.show_frame_transaction_history)
        self.btn_rent_history = Button(self.frame_my, text="Rent History", font=FONT,
                                       command=self.show_frame_rent_history)
        self.btn_report_history = Button(self.frame_my, text="Report History", font=FONT,
                                         command=self.show_frame_report_history)
        self.btn_change_password = Button(self.frame_my, text="Change Password", font=FONT,
                                          command=self.show_frame_change_password)

        # place labels:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_user_id.place(x=S_W * (3 / 14), y=S_H * (4 / 20))
        self.l_user_id_show.place(x=S_W * (5 / 14), y=S_H * (4 / 20))
        self.l_user_name.place(x=S_W * (8 / 14), y=S_H * (4 / 20))
        self.l_user_name_show.place(x=S_W * (9 / 14), y=S_H * (4 / 20))
        self.l_email.place(x=S_W * (3 / 14), y=S_H * (12 / 40))
        self.l_email_show.place(x=S_W * (5 / 14), y=S_H * (12 / 40))
        self.l_account_credit.place(x=S_W * (3 / 14), y=S_H * (16 / 40))
        self.l_account_credit_show.place(x=S_W * (5 / 14), y=S_H * (16 / 40))
        # place buttons:
        self.btn_edit_name.place(x=S_W * (12 / 14), y=S_H * (38 / 200), width=150, height=50)
        self.btn_edit_email.place(x=S_W * (8 / 14), y=S_H * (58 / 200), width=150, height=50)
        self.btn_top_up.place(x=S_W * (3 / 14), y=S_H * (20 / 40), width=200, height=50)
        self.btn_transaction_history.place(x=S_W * (3 / 14), y=S_H * (24 / 40), width=200, height=50)
        self.btn_rent_history.place(x=S_W * (3 / 14), y=S_H * (28 / 40), width=200, height=50)
        self.btn_report_history.place(x=S_W * (8 / 14), y=S_H * (28 / 40), width=200, height=50)
        self.btn_change_password.place(x=S_W * (8 / 14), y=S_H * (20 / 40), width=200, height=50)

    def ftop_up(self):

        # create labels:
        self.l_top_up_amount = Label(self.frame_top_up, text="Top-up amount: ", font=FONT)
        self.l_top_up_amount_show = Label(self.frame_top_up, text="", font=FONT)

        # create buttons:
        self.btn_GBP5 = Button(self.frame_top_up, text="£5", font=FONT,
                               command=self.GBP5)
        self.btn_GBP10 = Button(self.frame_top_up, text="£10", font=FONT,
                                command=self.GBP10)
        self.btn_GBP20 = Button(self.frame_top_up, text="£20", font=FONT,
                                command=self.GBP20)
        self.btn_GBP50 = Button(self.frame_top_up, text="£50", font=FONT,
                                command=self.GBP50)
        self.btn_go_back = Button(self.frame_top_up, text="Return", font=FONT,
                                  command=self.show_frame_my)
        self.btn_confirm = Button(self.frame_top_up, text="Confirm", font=FONT,
                                  command=self.show_frame_payment_selection)

        # place components:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_top_up_amount.place(x=S_W * (3 / 14), y=S_H * (24 / 90))
        self.l_top_up_amount_show.place(x=S_W * (5 / 14), y=S_H * (24 / 90))
        self.btn_GBP5.place(x=S_W * (35 / 140), y=S_H * (30 / 90), width=150, height=50)
        self.btn_GBP10.place(x=S_W * (55 / 140), y=S_H * (30 / 90), width=150, height=50)
        self.btn_GBP20.place(x=S_W * (75 / 140), y=S_H * (30 / 90), width=150, height=50)
        self.btn_GBP50.place(x=S_W * (95 / 140), y=S_H * (30 / 90), width=150, height=50)
        self.btn_go_back.place(x=S_W * (20 / 140), y=S_H * (60 / 90), width=150, height=50)
        self.btn_confirm.place(x=S_W * (11 / 14), y=S_H * (60 / 90), width=150, height=50)

    def add_card(self):
        top1 = Toplevel()
        top1.title('add card')
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        top1.geometry("{}x{}".format(S_W - 1000, S_H - 600))
        canvas = Canvas(top1, width=S_W - 1000, height=S_H - 600)
        Label(canvas, text='card_number:', font=FONT).place(x=30, y=30)
        Label(canvas, text='date：', font=FONT).place(x=30, y=80)
        Label(canvas, text='expired_date：', font=FONT).place(x=30, y=130)
        Label(canvas, text='holder_name：', font=FONT).place(x=30, y=180)
        Label(canvas, text='CV_number：', font=FONT).place(x=30, y=230)
        self.card_number = StringVar()
        self.date = StringVar()
        self.expired_date = StringVar()
        self.card_holder_name = StringVar()
        self.CV_number = StringVar()
        Entry(canvas, textvariable=self.card_number, font=FONT).place(x=160, y=30)
        Entry(canvas, textvariable=self.date, font=FONT).place(x=160, y=80)
        Entry(canvas, textvariable=self.expired_date, font=FONT).place(x=160, y=130)
        Entry(canvas, textvariable=self.card_holder_name, font=FONT).place(x=160, y=180)
        Entry(canvas, textvariable=self.CV_number, font=FONT).place(x=160, y=230)
        Button(canvas, text="Add", font=FONT, command=self.insert_card).place(x=100, y=280)
        canvas.pack()
        top1.mainloop()

    def insert_card(self):
        card_number = self.card_number.get()
        date = self.date.get()
        expired_date = self.expired_date.get()
        card_holder_name = self.card_holder_name.get()
        CV_number = self.CV_number.get()
        if not card_number:
            messagebox.showerror(message='lack card_number')
            return
        if not date:
            messagebox.showerror(message='lack date')
            return
        if not expired_date:
            messagebox.showerror(message='lack expired_date')
            return
        if not card_holder_name:
            messagebox.showerror(message='lack card_holder_name')
            return
        if not CV_number:
            messagebox.showerror(message='lack CV_number')
            return
        self.c.execute(
            "insert into Credit_card (card_number,date,expired_date,card_holder_name,CV_number,customer_id) values(?,?,?,?,?,?)",
            (
                card_number, date, expired_date, card_holder_name, CV_number, self.guid
            ))
        self.conn.commit()
        self.fpayment_selection()
        messagebox.showinfo(message="add card success")

    def fpayment_selection(self):

        # create labels:
        self.l_pay_by_your_card = Label(self.frame_payment_selection, text="Please pay by your card:", font=FONT_TITLE)
        self.l_card = Label(self.frame_payment_selection, text="Card:", font=FONT_TITLE)

        # create selection:
        selected_card = StringVar()
        cards = ["xxxx xxxx xxxx 0479", "xxxx xxxx xxxx 5545", "Add another card"]  # Three testing cards
        self.c.execute("select * from Credit_card where customer_id=?", (self.guid,))
        cards = self.c.fetchall()
        cards = [i[1] for i in cards]
        self.card = StringVar()
        self.optionmenu_card = ttk.Combobox(self.frame_payment_selection, values=cards,
                                            textvariable=self.card)

        # create buttons:
        self.btn_go_back = Button(self.frame_payment_selection, text="Return", font=FONT,
                                  command=self.show_frame_top_up)
        self.add_car = Button(self.frame_payment_selection, text="Add Card", font=FONT,
                              command=self.add_card)

        self.btn_pay = Button(self.frame_payment_selection, text="Choose this card", font=FONT,
                              command=self.show_frame_confirm_payment_info)

        # place components:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_pay_by_your_card.place(x=S_W * (45 / 140), y=S_H * (30 / 90))
        self.l_card.place(x=S_W * (45 / 140), y=S_H * (40 / 90))
        self.optionmenu_card.place(x=S_W * (60 / 140), y=S_H * (413 / 900), width=400, height=50)
        self.btn_go_back.place(x=S_W * (20 / 140), y=S_H * (60 / 90), width=200, height=50)
        self.btn_pay.place(x=S_W * (11 / 14), y=S_H * (60 / 90), width=200, height=50)
        self.add_car.place(x=S_W * (7 / 14), y=S_H * (60 / 90), width=200, height=50)

    def fconfirm_payment_info(self):
        self.c.execute(
            """select * from Customer where customer_id=?""",
            [self.guid])
        user = self.c.fetchone()
        # create label:
        Amount = user[-1]
        if not Amount:
            Amount = 0
        self.Amount = Amount
        self.l_user_id = Label(self.frame_confirm_payment_info, text="User ID: ", font=FONT)
        self.l_user_id_show = Label(self.frame_confirm_payment_info, text=user[0], font=FONT)
        self.l_user_name = Label(self.frame_confirm_payment_info, text="Username: ", font=FONT)
        self.l_user_name_show = Label(self.frame_confirm_payment_info, text=user[1], font=FONT)
        self.l_amount = Label(self.frame_confirm_payment_info, text="Amount: ", font=FONT)
        self.l_amount_show = Label(self.frame_confirm_payment_info, text=Amount, font=FONT)
        self.l_top_up_account = Label(self.frame_confirm_payment_info, text="Top-up Account: ", font=FONT)
        self.l_top_up_account_show = Label(self.frame_confirm_payment_info, text=self.amount, font=FONT)
        self.l_card_info = Label(self.frame_confirm_payment_info, text="Card: ", font=FONT)
        self.l_card_info_show = Label(self.frame_confirm_payment_info, text=self.card.get(), font=FONT)

        # create buttons:
        self.btn_go_back = Button(self.frame_confirm_payment_info, text="Return", font=FONT,
                                  command=self.show_frame_payment_selection)
        self.btn_pay = Button(self.frame_confirm_payment_info, text="Confirm", font=FONT,
                              command=self.confirm_pay)

        # place components
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_user_id.place(x=S_W * (35 / 140), y=S_H * (14 / 90))
        self.l_user_id_show.place(x=S_W * (45 / 140), y=S_H * (14 / 90))
        self.l_user_name.place(x=S_W * (75 / 140), y=S_H * (14 / 90))
        self.l_user_name_show.place(x=S_W * (85 / 140), y=S_H * (14 / 90))
        self.l_amount.place(x=S_W * (35 / 140), y=S_H * (24 / 90))
        self.l_amount_show.place(x=S_W * (45 / 140), y=S_H * (24 / 90))
        self.l_top_up_account.place(x=S_W * (35 / 140), y=S_H * (34 / 90))
        self.l_top_up_account_show.place(x=S_W * (5 / 14), y=S_H * (34 / 90))
        self.l_card_info.place(x=S_W * (35 / 140), y=S_H * (44 / 90))
        self.l_card_info_show.place(x=S_W * (45 / 140), y=S_H * (44 / 90))
        self.btn_go_back.place(x=S_W * (2 / 14), y=S_H * (60 / 90), width=150, height=50)
        self.btn_pay.place(x=S_W * (11 / 14), y=S_H * (60 / 90), width=150, height=50)


    def search_transaction(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        selected_transaction_type=self.selected_transaction_type.get()
        if not selected_transaction_type:
            selected_transaction_type="top-up"
        self.c.execute("select * from Credit_log where Customer_ID=? and type=?", (self.guid,selected_transaction_type,))
        records = self.c.fetchall()
        columns = ("id", "amount", "type", "date")
        self.tree = ttk.Treeview(self.frame_transaction_history, height=14, show="headings", columns=columns)
        self.tree.column("id", width=250)
        self.tree.column("amount", width=250)
        self.tree.column("type", width=250)
        self.tree.column("date", width=250)
        self.tree.heading("id", text='id', anchor=CENTER)
        self.tree.heading("amount", text='amount', anchor=CENTER)
        self.tree.heading("type", text='type', anchor=CENTER)
        self.tree.heading("date", text='date', anchor=CENTER)
        for record in records:
            self.tree.insert("", 0, values=(record[0], record[1], record[2], record[4]))
        self.tree.place(x=S_W * (2 / 14), y=S_H * (27 / 90), width=1000, height=300)

    def ftransaction_history(self):
        # create label
        self.l_transaction_history_type = Label(self.frame_transaction_history, text="Type: ", font=FONT)
        # self.l_transaction_date = Label(self.frame_transaction_history, text="Date: ", font=FONT)
        # create options:
        self.selected_transaction_type = StringVar()
        types = ["pay", "top-up"]
        self.optionmenu_transaction_type = ttk.Combobox(self.frame_transaction_history, values=types,textvariable=self.selected_transaction_type)
        selected_transaction_date = StringVar()
        # dates = ["Oct 2", "Oct 1", "Sep 30"]
        # self.optionmenu_transaction_date = OptionMenu(self.frame_transaction_history, selected_transaction_date, *dates)
        # create list:

        # self.transaction_list = Listbox(self.frame_transaction_history)
        # create button:
        self.transaction_s_btn = Button(self.frame_transaction_history, text="Search", font=FONT,
                                  command=self.search_transaction)
        self.btn_go_back = Button(self.frame_transaction_history, text="Return", font=FONT,
                                  command=self.show_frame_my)

        # place label:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.search_transaction()
        self.l_transaction_history_type.place(x=S_W * (2 / 14), y=S_H * (15 / 90))
        # self.l_transaction_date.place(x=S_W * (8 / 14), y=S_H * (15 / 90))
        self.transaction_s_btn.place(x=S_W * (8 / 14), y=S_H * (15 / 90),width=150, height=50)
        self.optionmenu_transaction_type.place(x=S_W * (32 / 140), y=S_H * (14 / 90), width=300, height=50)
        # self.optionmenu_transaction_date.place(x=S_W * (88 / 140), y=S_H * (14 / 90), width=300, height=50)
        self.btn_go_back.place(x=S_W * (2 / 14), y=S_H * (60 / 90), width=150, height=50)

    def rent_go_query_btn(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        select_rent_location = self.select_rent_location.get()
        selected_rentbike_type = self.selected_rentbike_type.get()
        sql = "select * from rent_log where Customer_ID=? "
        args = [self.guid]
        if select_rent_location:
            sql += " and location=? "
            args.append(select_rent_location)
        if selected_rentbike_type:
            sql += " and bike_type=? "
            args.append(selected_rentbike_type)
        self.c.execute(sql, tuple(args))
        records = self.c.fetchall()
        columns = ("bike_type", "location", "start_time", "end_time", "rent")
        self.tree = ttk.Treeview(self.frame_rent_history, height=14, show="headings", columns=columns)
        self.tree.column("bike_type", width=200)
        self.tree.column("location", width=200)
        self.tree.column("start_time", width=200)
        self.tree.column("end_time", width=200)
        self.tree.column("rent", width=200)
        self.tree.heading("bike_type", text='bike_type', anchor=CENTER)
        self.tree.heading("location", text='location', anchor=CENTER)
        self.tree.heading("start_time", text='start_time', anchor=CENTER)
        self.tree.heading("end_time", text='end_time', anchor=CENTER)
        self.tree.heading("rent", text='rent', anchor=CENTER)
        for record in records:
            self.tree.insert("", 0, values=(record[1], record[2], record[5], record[6], record[4]))
        self.tree.place(x=S_W * (2 / 14), y=S_H * (27 / 90), width=1000, height=300)

    def frent_history(self):

        # create label
        self.l_rent_history_type = Label(self.frame_rent_history, text="Bike Type: ", font=FONT)
        self.l_rent_date = Label(self.frame_rent_history, text="Location: ", font=FONT)
        # create options:
        self.selected_rentbike_type = StringVar()
        types = ["Electric bike", "Foot bike"]
        self.optionmenu_bike_type = ttk.Combobox(self.frame_rent_history,values=types,textvariable= self.selected_rentbike_type)
        select_parking_location_1 = CusOpenDatabase()
        parking_location = select_parking_location_1.select_parking_location()
        self.select_rent_location=StringVar()
        self.optionmenu_rent_location = ttk.Combobox(self.frame_rent_history, values=parking_location,textvariable=self.select_rent_location)
        # create list:
        # self.rent_list = Listbox(self.frame_rent_history, )
        # create button:
        self.btn_go_back = Button(self.frame_rent_history, text="Return", font=FONT,
                                  command=self.show_frame_my)
        self.rent_go_query = Button(self.frame_report_history, text="Search", font=FONT,
                                      command=self.rent_go_query_btn)
        self.rent_go_query_btn()
        # place label:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.rent_go_query.place(x=S_W * (25 / 140), y=S_H * (200 / 900), width=300, height=50)

        self.l_rent_history_type.place(x=S_W * (2 / 14), y=S_H * (15 / 90))
        self.l_rent_date.place(x=S_W * (8 / 14), y=S_H * (15 / 90))
        self.optionmenu_bike_type.place(x=S_W * (32 / 140), y=S_H * (14 / 90), width=300, height=50)
        self.optionmenu_rent_location.place(x=S_W * (88 / 140), y=S_H * (14 / 90), width=300, height=50)
        # self.rent_list.place(x=S_W * (2 / 14), y=S_H * (27 / 90), width=1000, height=300)
        self.btn_go_back.place(x=S_W * (2 / 14), y=S_H * (60 / 90), width=150, height=50)

    def frent_detail(self):

        # create label:
        self.l_bike_id = Label(self.frame_rent_detail, text="Bike ID: ", font=FONT)
        self.l_bike_id_show = Label(self.frame_rent_detail, text="", font=FONT)
        self.l_bike_type = Label(self.frame_rent_detail, text="Bike Type: ", font=FONT)
        self.l_bike_type_show = Label(self.frame_rent_detail, text="", font=FONT)
        self.l_start_location = Label(self.frame_rent_detail, text="Start Location: ", font=FONT)
        self.l_start_location_show = Label(self.frame_rent_detail, text="", font=FONT)
        self.l_end_location = Label(self.frame_rent_detail, text="End Location: ", font=FONT)
        self.l_end_location_show = Label(self.frame_rent_detail, text="", font=FONT)
        self.l_start_time = Label(self.frame_rent_detail, text="Start Time: ", font=FONT)
        self.l_start_time_show = Label(self.frame_rent_detail, text="", font=FONT)
        self.l_end_time = Label(self.frame_rent_detail, text="End time: ", font=FONT)
        self.l_end_time_show = Label(self.frame_rent_detail, text="", font=FONT)
        self.l_price = Label(self.frame_rent_detail, text="Price: ", font=FONT)
        self.l_price_show = Label(self.frame_rent_detail, text="", font=FONT)

        ## create buttons:
        self.btn_go_back_4 = Button(self.frame_rent_detail, text="Return", font=FONT,
                                    command=self.show_frame_rent_history)

        # place components
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_bike_id.place(x=S_W * (35 / 140), y=S_H * (18 / 90))
        self.l_bike_id_show.place(x=S_W * (45 / 140), y=S_H * (18 / 90))
        self.l_bike_type.place(x=S_W * (75 / 140), y=S_H * (18 / 90))
        self.l_bike_type_show.place(x=S_W * (85 / 140), y=S_H * (18 / 90))
        self.l_start_location.place(x=S_W * (35 / 140), y=S_H * (24 / 90))
        self.l_start_location_show.place(x=S_W * (47 / 140), y=S_H * (24 / 90))
        self.l_end_location.place(x=S_W * (75 / 140), y=S_H * (24 / 90))
        self.l_end_location_show.place(x=S_W * (87 / 140), y=S_H * (24 / 90))
        self.l_start_time.place(x=S_W * (35 / 140), y=S_H * (30 / 90))
        self.l_start_time_show.place(x=S_W * (45 / 140), y=S_H * (30 / 90))
        self.l_end_time.place(x=S_W * (75 / 140), y=S_H * (30 / 90))
        self.l_end_time_show.place(x=S_W * (85 / 140), y=S_H * (30 / 90))
        self.l_price.place(x=S_W * (35 / 140), y=S_H * (36 / 90))
        self.l_price_show.place(x=S_W * (45 / 140), y=S_H * (36 / 90))
        self.btn_go_back_4.place(x=S_W * (2 / 14), y=S_H * (60 / 90), width=150, height=50)

    def report_go_query_btn(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        report_history_location = self.report_history_location.get()
        report_err_type = self.report_err_type.get()
        sql="select * from report where username=? "
        args=[self.guid]
        if report_history_location:
            sql+=" and location=? "
            args.append(report_history_location)
        if report_err_type:
            sql += " and err_type=? "
            args.append(report_err_type)
        self.c.execute(sql,tuple(args))
        records = self.c.fetchall()
        columns = ("report_time", "location", "err_type", "desc","status")
        self.tree = ttk.Treeview(self.frame_report_history, height=14, show="headings", columns=columns)
        self.tree.column("report_time", width=200)
        self.tree.column("location", width=200)
        self.tree.column("err_type", width=200)
        self.tree.column("desc", width=200)
        self.tree.column("status", width=200)
        self.tree.heading("report_time", text='report_time', anchor=CENTER)
        self.tree.heading("location", text='location', anchor=CENTER)
        self.tree.heading("err_type", text='err_type', anchor=CENTER)
        self.tree.heading("desc", text='desc', anchor=CENTER)
        self.tree.heading("status", text='status', anchor=CENTER)
        for record in records:
            self.tree.insert("", 0, values=(record[2], record[3], record[4], record[5],record[7]))
        self.tree.place(x=S_W * (2 / 14), y=S_H * (27 / 90), width=1000, height=300)

    def freport_history(self):

        # create label
        self.l_bike_type = Label(self.frame_report_history, text="Location: ", font=FONT)
        self.l_report_type = Label(self.frame_report_history, text="Error Type: ", font=FONT)
        # create options:
        selected_bike_type = StringVar()
        # types = ["Electric bike", "Foot bike"]
        select_parking_location_1 = CusOpenDatabase()
        parking_location = select_parking_location_1.select_parking_location()
        self.report_history_location=StringVar()
        self.optionmenu_location = ttk.Combobox(self.frame_report_history, values=parking_location,textvariable=self.report_history_location)
        error_types = ["electric_bike", "foot_bike"]
        self.report_err_type=StringVar()
        self.optionmenu_report_type = ttk.Combobox(self.frame_report_history, values=error_types,textvariable=self.report_err_type)
        # create list:
        # self.report_list = Listbox(self.frame_report_history, )
        # create button:
        self.btn_go_back = Button(self.frame_report_history, text="Return", font=FONT,
                                  command=self.show_frame_my)
        self.report_go_query = Button(self.frame_report_history, text="Search", font=FONT,
                                  command=self.report_go_query_btn)

        # place label:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.report_go_query_btn()
        self.l_bike_type.place(x=S_W * (2 / 14), y=S_H * (15 / 90))
        self.l_report_type.place(x=S_W * (8 / 14), y=S_H * (15 / 90))
        self.optionmenu_location.place(x=S_W * (32 / 140), y=S_H * (143 / 900), width=300, height=50)
        self.optionmenu_report_type.place(x=S_W * (94 / 140), y=S_H * (143 / 900), width=300, height=50)
        # self.report_list.place(x=S_W * (2 / 14), y=S_H * (27 / 90), width=1000, height=300)
        self.btn_go_back.place(x=S_W * (2 / 14), y=S_H * (60 / 90), width=150, height=50)
        self.report_go_query.place(x=S_W * (25 / 140), y=S_H * (200 / 900), width=300, height=50)

    def freport_detail(self):

        # create label:
        self.l_bike_id = Label(self.frame_report_detail, text="Bike ID: ", font=FONT)
        self.l_bike_id_show = Label(self.frame_report_detail, text="", font=FONT)
        self.l_bike_type = Label(self.frame_report_detail, text="Bike Type: ", font=FONT)
        self.l_bike_type_show = Label(self.frame_report_detail, text="", font=FONT)
        self.l_error_type = Label(self.frame_report_detail, text="Error Type: ", font=FONT)
        self.l_error_type_show = Label(self.frame_report_detail, text="", font=FONT)
        self.l_location = Label(self.frame_report_detail, text="Location: ", font=FONT)
        self.l_location_show = Label(self.frame_report_detail, text="", font=FONT)
        self.l_description = Label(self.frame_report_detail, text="Description: ", font=FONT)
        self.l_description_show = Label(self.frame_report_detail, text="", font=FONT)
        self.l_pic = Label(self.frame_report_detail, text="Pic: ", font=FONT)
        self.l_pic_show = Label(self.frame_report_detail, text="", font=FONT)
        self.l_status = Label(self.frame_report_detail, text="Status: ", font=FONT)
        self.l_status_show = Label(self.frame_report_detail, text="", font=FONT)

        ## create buttons:
        self.btn_go_back = Button(self.frame_report_detail, text="Return", font=FONT,
                                  command=self.show_frame_report_history)

        # place components
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_bike_id.place(x=S_W * (35 / 140), y=S_H * (18 / 90))
        self.l_bike_id_show.place(x=S_W * (45 / 140), y=S_H * (18 / 90))
        self.l_bike_type.place(x=S_W * (75 / 140), y=S_H * (18 / 90))
        self.l_bike_type_show.place(x=S_W * (85 / 140), y=S_H * (18 / 90))
        self.l_error_type.place(x=S_W * (35 / 140), y=S_H * (24 / 90))
        self.l_error_type_show.place(x=S_W * (47 / 140), y=S_H * (24 / 90))
        self.l_location.place(x=S_W * (75 / 140), y=S_H * (24 / 90))
        self.l_location_show.place(x=S_W * (87 / 140), y=S_H * (24 / 90))
        self.l_description.place(x=S_W * (35 / 140), y=S_H * (30 / 90))
        self.l_description_show.place(x=S_W * (45 / 140), y=S_H * (30 / 90))
        self.l_pic.place(x=S_W * (75 / 140), y=S_H * (30 / 90))
        self.l_pic_show.place(x=S_W * (85 / 140), y=S_H * (30 / 90))
        self.l_status.place(x=S_W * (35 / 140), y=S_H * (36 / 90))
        self.l_status_show.place(x=S_W * (45 / 140), y=S_H * (36 / 90))
        self.btn_go_back.place(x=S_W * (2 / 14), y=S_H * (60 / 90), width=150, height=50)

    def fchange_password(self):

        # create labels:
        self.l_change_password_title = Label(self.frame_change_password, text="Please enter your current password",
                                             font=FONT_TITLE)
        # create Entry:
        self.his_password=StringVar()
        self.e_old_password = Entry(self.frame_change_password,textvariable=self.his_password, font=FONT_TITLE)
        # create button:
        self.btn_check_old_password = Button(self.frame_change_password, text="Enter", font=FONT,
                                             command=self.check_old_password)

        self.btn_go_back = Button(self.frame_change_password, text="Return", font=FONT,
                                  command=self.show_frame_my)

        # place components:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_change_password_title.place(x=S_W * (33 / 140), y=S_H * (30 / 90))
        self.e_old_password.place(x=S_W * (5 / 14), y=S_H * (4 / 9), width=400, height=50)
        self.btn_check_old_password.place(x=S_W * (105 / 140), y=S_H * (6 / 9), width=150, height=50)
        self.btn_go_back.place(x=S_W * (2 / 14), y=S_H * (6 / 9), width=150, height=50)

    def fnew_password(self):

        # create labels:
        self.l_enter_new_password = Label(self.frame_new_password, text="Enter new Password:", font=FONT_TITLE)
        self.l_repeat_password = Label(self.frame_new_password, text="Repeat Password:", font=FONT_TITLE)
        # create a Entry:
        self.e_new_password = Entry(self.frame_new_password, text="", font=FONT)
        self.e_repeat_password = Entry(self.frame_new_password, text="", font=FONT)

        ## create button:
        self.btn_confirm_new_password = Button(self.frame_new_password, text="Confirm", font=FONT,
                                               command=self.confirm_new_password)
        self.btn_go_back = Button(self.frame_new_password, text="Return", font=FONT,
                                  command=self.show_frame_change_password)

        # place components
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_enter_new_password.place(x=S_W * (15 / 140), y=S_H * (31 / 90))
        self.l_repeat_password.place(x=S_W * (15 / 140), y=S_H * (39 / 90))
        self.e_new_password.place(x=S_W * (65 / 140), y=S_H * (30 / 90), width=500, height=50)
        self.e_repeat_password.place(x=S_W * (65 / 140), y=S_H * (38 / 90), width=500, height=50)
        self.btn_confirm_new_password.place(x=S_W * (105 / 140), y=S_H * (6 / 9), width=150, height=50)
        self.btn_go_back.place(x=S_W * (2 / 14), y=S_H * (6 / 9), width=150, height=50)


class CustomerUI:

    def __init__(self, guid=None) -> None:

        self.master = Tk()
        self.master.title("Customer")
        self.guid = guid

        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.master.geometry("{}x{}".format(S_W, S_H))
        self.font = FONT

        # create frames
        self.frame_rent = Frame(self.master, width=S_W, height=S_H)
        self.frame_report = Frame(self.master, width=S_W, height=S_H)
        self.frame_my = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_rent, self.frame_report, self.frame_my]

        # create buttons:
        self.btn_rent = Button(self.master, text='Rent Bike',
                               command=self.show_frame_rent, font=FONT_TOP)
        self.btn_report = Button(self.master, text='Report',
                                 command=self.show_frame_report, font=FONT_TOP)
        self.btn_my = Button(self.master, text='My',
                             command=self.show_frame_my, font=FONT_TOP)
        self.btns = [self.btn_rent, self.btn_report, self.btn_my]

        # place buttons:
        self.btn_rent.place(x=0, y=0, width=S_W / 3., height=S_H / 10)
        self.btn_report.place(x=S_W / 3, y=0, width=S_W / 3., height=S_H / 10)
        self.btn_my.place(x=S_W / 3 * 2, y=0, width=S_W / 3., height=S_H / 10)

        # init frames
        self.rent_bike = RentBike(self.frame_rent)
        self.report = Report(self.frame_report, self.guid)
        self.my = My(self.frame_my, self.guid)

        self.show_frame_rent()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def reset_btn_bg(self):
        for btn in self.btns:
            btn.configure(bg='SystemButtonFace')

    def show_frame_rent(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_rent.configure(bg='red')
        self.frame_rent.pack()

    def show_frame_report(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_report.configure(bg='red')
        self.frame_report.pack()

    def show_frame_my(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_my.configure(bg='red')
        self.frame_my.pack()

    def show(self):
        self.master.mainloop()


if __name__ == '__main__':
    c = CustomerUI()
    c.show()
