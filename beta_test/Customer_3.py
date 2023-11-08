import os.path
import random
import sqlite3
import time
from datetime import timedelta
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkintermapview
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import *
from PIL import Image, ImageTk
from ManipulateDatabase import CusOpenDatabase




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
        self.get_current_trackingInfo()
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

    def get_current_trackingInfo(self):

        current_info = CusOpenDatabase()
        cur_tracking_data = current_info.get_currentBikeInfo()

        return cur_tracking_data

    def confirm_unlock(self):
        click = messagebox.askyesno("Unlock", "Unlocking bike is flashing!")
        if click:
            insert_tracking_history = CusOpenDatabase()
            insert_tracking_history.insert_rentTrackData(self.comb_type.get(), self.comb_location.get())
            self.start_stop()
            self.ShowSuccess()
            self.get_current_trackingInfo()

    def ShowSuccess(self):
        Unlockpassword_window = Tk()
        Unlockpassword_window.title("Unlocking password")
        unlockpassword_1 = random.random()
        unlockpassword_2 = int(unlockpassword_1*100000)
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

    def charge_fees(self):
        fee = CusOpenDatabase()
        cost = fee.get_price()
        current_credit = fee.get_current_credit()
        new_credit = current_credit - cost
        if new_credit > 0:
            fee.charge_fee()
            fee.insert_account_history_spend()
        else:
            click = messagebox.showerror("No enough amount", "Insufficient balance，please charge now")
            if click:
                self.show_frame_rent()

    def paied_successfully(self):
        self.charge_fees()

        click = messagebox.askyesno("finished payment", "Thanks for your payment to finish renting!")
        if click:
            self.show_frame_rent()

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
        self.comb_location.set("Where to start?")
        self.comb_type = ttk.Combobox(self.frame_rent, values=["electric_bike", "electric_scooter"])
        self.comb_type.set("Choose Bike Type")

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
        self.l_avail.place(x=S_W * (5 / 10), y=S_H * (3 / 5), width=S_W * (600/1440), height=S_H * (40/900))
        # place combs:
        self.comb_location.place(x=S_W * (5 / 10), y=S_H * (1 / 5), width=S_W * (330/1440), height=S_H * (40/900))
        self.comb_type.place(x=S_W * (5 / 10), y=S_H * (2 / 5), width=S_W * (330/1440), height=S_H * (40/900))
        # place buttons:
        self.btn.place(x=S_W * (22 / 50), y=S_H * (23 / 30), width=S_W * (200/1440), height=S_H * (40/900))
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
        self.current_rent_bike = self.get_current_trackingInfo()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        # create the label for showing renting bike info
        self.l_bike_id_show = Label(self.frame_current_riding, text='{}'.format(self.current_rent_bike[1]),
                                    font=FONT_TOP)
        self.l_bike_type_show = Label(self.frame_current_riding, text='{}'.format(self.current_rent_bike[7]),
                                      font=FONT_TOP)
        self.l_startTime_show = Label(self.frame_current_riding, text='{}'.format(current_time), font=FONT_TOP)

        # set a mapview showing the current rent postion
        adr = CusOpenDatabase()
        address = adr.get_address(self.current_rent_bike[2])
        values = [float(x) for x in address[0][0].strip('[]').split(', ')]
        self.l_map = LabelFrame(self.frame_current_riding)
        self.l_map.place(x=S_H*(6/10), y=S_H*(2/10))

        map_widget = tkintermapview.TkinterMapView(self.l_map, width=S_W * (800/1440), height=S_H * (600/900),
                                                   corner_radius=0)
        map_widget.set_position(values[0], values[1])
        map_widget.set_zoom(15)
        map_widget.set_marker(values[0], values[1], text="{}".format(self.current_rent_bike[2]))
        map_widget.grid()


        # set a stopwatch for store riding_time
        self.start_time = None
        self.stop_time = None
        self.running = False
        self.label_var = StringVar()
        self.label_var.set("00:00:00.00")
        self.riding_time_var =StringVar()
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

        # place label
        self.frame_current_riding_title.place(x=S_W*(8/50), y=S_H*(2/15), width=200, height=50)
        self.l_bike_id.place(x=S_W*(2/25), y=S_H*(4/15))
        self.l_bike_id_show.place(x=S_W * (40 / 250), y=S_H * (79 / 300), width=S_W * (200/1440), height=S_H * (40/900))
        self.l_bike_type.place(x=S_W*(2/25), y=S_H*(6/15))
        self.l_bike_type_show.place(x=S_W * (40 / 250), y=S_H * (119 / 300), width=S_W * (200/1440), height=S_H * (40/900))
        self.l_start_time.place(x=S_W*(2/25), y=S_H*(8/15))
        self.l_startTime_show.place(x=S_W * (40 / 250), y=S_H * (159 / 300), width=S_W * (200/1440), height=S_H * (40/900))
        self.l_riding_time.place(x=S_W*(2/25), y=S_H*(10/15))
        self.l_ridingTime_show.place(x=S_W * (40 / 250), y=S_H * (199 / 300), width=S_W * (200/1440), height=S_H * (40/900))
        self.l_select_return_location.place(x=S_W * (2 / 25), y=S_H * (23 / 30))

        # place button:
        self.btn_return_bike.place(x=S_W*(8/50), y=S_H*(13/15), width=S_W * (200/1440), height=S_H * (40/900))

        # place combobox:
        self.comb_location_return.place(x=S_W * (5 / 25), y=S_H * (23 / 30), width=S_W * (200/1440),
                                        height=S_H * (30/900))

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
        self.current_riding_data = CusOpenDatabase()
        self.payment_info_data = self.current_riding_data.get_currentBikeInfo()
        self.price = self.current_riding_data.get_price()
        # show these labels:
        self.l_bike_id_show = Label(self.frame_make_payment, text='{}'.format(self.payment_info_data[1]), font=FONT)
        self.l_bike_type_show = Label(self.frame_make_payment, text='{}'.format(self.payment_info_data[7]), font=FONT)
        self.l_start_time_show = Label(self.frame_make_payment, text='{}'.format(self.payment_info_data[4]), font=FONT)
        self.l_end_time_show = Label(self.frame_make_payment, text='{}'.format(self.payment_info_data[5]), font=FONT)
        self.l_riding_time_show = Label(self.frame_make_payment, text='{}'.format(self.payment_info_data[6]), font=FONT)
        self.l_price_show = Label(self.frame_make_payment, text='£{:.2f}'.format(self.price), font=FONT)


        # create button:
        self.btn_comf_pay = Button(self.frame_make_payment, text='Confirm Payment',
                                   font=FONT, command=self.paied_successfully)

        # place labels:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.frame_make_payment_title.place(x=S_W*(22/50), y=S_H*(2/15))
        self.l_bike_id.place(x=S_W*(4/25), y=S_H*(4/15))
        self.l_bike_type.place(x=S_W*(15/25), y=S_H*(4/15))
        self.l_start_time.place(x=S_W*(4/25), y=S_H*(6/15))
        self.l_end_time.place(x=S_W*(15/25), y=S_H*(6/15))
        self.l_riding_time.place(x=S_W*(4/25), y=S_H*(8/15))
        self.l_price.place(x=S_W*(15/25), y=S_H*(8/15))

        self.l_bike_id_show.place(x=S_W * (6 / 25), y=S_H * (4 / 15), width=S_W * (200/1440), height=S_H * (30/900))
        self.l_bike_type_show.place(x=S_W * (17 / 25), y=S_H * (4 / 15), width=S_W * (200/1440), height=S_H * (30/900))
        self.l_start_time_show.place(x=S_W * (6 / 25), y=S_H * (6 / 15), width=S_W * (200/1440), height=S_H * (30/900))
        self.l_end_time_show.place(x=S_W * (17 / 25), y=S_H * (6 / 15), width=S_W * (200/1440), height=S_H * (30/900))
        self.l_riding_time_show.place(x=S_W * (6 / 25), y=S_H * (8 / 15), width=S_W * (200/1440), height=S_H * (30/900))
        self.l_price_show.place(x=S_W * (17 / 25), y=S_H * (8 / 15), width=S_W * (200/1440), height=S_H * (30/900))
        # place button:
        self.btn_comf_pay.place(x=S_W*(21/50), y=S_H*(12/15), width=200, height=50)


class Report:

    def __init__(self, master) -> None:

        self.master = master
        self.img_path = None
        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()
        # edition: frame_1 = frame_report; frame_2 = frame_create_new_rp; frame_3 = frame_processing
        self.frame_report = Frame(self.master, width=S_W, height=S_H)
        self.frame_create_new_rp = Frame(self.master, width=S_W, height=S_H)
        self.frame_processing = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_report, self.frame_create_new_rp, self.frame_processing]

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
        self.forget_all()
        self.frame_processing.pack()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

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
        lb1.place(x=S_W * (11 / 25), y=S_H * (110 / 150))

    def get_guid(self):

        get_guid_info = CusOpenDatabase()
        cus_info = get_guid_info.get_loginData()
        guid = cus_info[2]

        return guid

    def insert_Error_report(self, report_time, location, bike_type, desc, img_path, err_type):
        insertReport = CusOpenDatabase()
        insertReport.insert_report(report_time, location, bike_type, desc, img_path, err_type)

    def submit(self):

        report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        location = self.selected_value_2.get()
        bike_type = self.bike_type.get()
        err_type = self.err_type.get()
        desc = self.e_desc.get()
        img_path = ''
        if self.img_path:
            img_path = os.path.join('image', self.img_path.get())
        if not location:
            messagebox.showerror('error', "lack location!")
            return
        if not bike_type:
            messagebox.showerror('error', "lack err_type!")
            return
        if not desc:
            messagebox.showerror('error', "lack desc!")
            return

        self.insert_Error_report(report_time, location, bike_type, desc, img_path, err_type)

        click = messagebox.showinfo('success', "report success!")
        if click:
            self.show_frame_report()

    def onSelect(self, e):

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

        get_report_detail = CusOpenDatabase()
        record = get_report_detail.select_report_detail(report_id)
        canvas = Canvas(top1, width=400, height=600)
        Label(canvas, text='Report_time: {}'.format(record[-4]), font=FONT).place(x=30, y=30)
        Label(canvas, text='Location：{}'.format(record[5]), font=FONT).place(x=30, y=80)
        Label(canvas, text='Error_type：{}'.format(record[6]), font=FONT).place(x=30, y=130)
        Label(canvas, text='Desc：{}'.format(record[-1]), font=FONT).place(x=30, y=180)
        Label(canvas, text='Status：{}'.format(record[8]), font=FONT).place(x=30, y=230)
        canvas.pack()
        top1.mainloop()

    def freport(self):

        # create buttons:
        self.btn_new_report = Button(self.frame_report, text='Create New Report', font=FONT,
                                     command=self.show_frame_create_new_rp)
        self.btn_pro = Button(self.frame_report, text='Processing', font=FONT,
                              command=self.show_frame_processing)

        # place buttons:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.btn_new_report.place(x=S_W*(2/25), y=S_H*(4/15), width=200, height=50)
        self.btn_pro.place(x=S_W*(2/25), y=S_H*(1/2), width=200, height=50)

    def fcreate_new_rp(self):

        # create labels:
        self.l_bike_id = Label(self.frame_create_new_rp, text='Bike id:', font=FONT)
        self.l_bike_type = Label(self.frame_create_new_rp, text='Bike type:', font=FONT)
        self.l_time = Label(self.frame_create_new_rp, text='Time:', font=FONT)
        self.l_loca = Label(self.frame_create_new_rp, text='*Location:', font=FONT)
        self.l_err_type = Label(self.frame_create_new_rp, text='*Bike & Error Type:', font=FONT)
        self.l_desc = Label(self.frame_create_new_rp, text='*Description(0-100):', font=FONT)
        self.desc = StringVar()
        self.e_desc = Entry(self.frame_create_new_rp, textvariable=self.desc, font=FONT)
        self.l_pic = Label(self.frame_create_new_rp, text='Picture(Option):', font=FONT)


        # create entries and combos:
        self.now_time = StringVar()
        self.now_time.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.l_time_show = Label(self.frame_create_new_rp, textvariable=self.now_time, font=FONT)

        select_parking_location_2 = CusOpenDatabase()
        self.selected_value_2 = StringVar()
        parking_location = select_parking_location_2.select_parking_location()
        self.comb_loca = ttk.Combobox(self.frame_create_new_rp, textvariable=self.selected_value_2,
                                      values=parking_location)
        self.comb_loca.set("Choose Location")

        self.bike_type = StringVar()
        self.comb_bike_type = ttk.Combobox(self.frame_create_new_rp, values=["electric_bike", "electric_scooter"],
                                           textvariable=self.bike_type)
        self.comb_bike_type.set("Choose Bike Type")

        self.err_type = StringVar()
        self.comb_err_type = ttk.Combobox(self.frame_create_new_rp,
                                          values=["Wheels", "seats", "fronts", "chains", "tires", "brakes", "frames"],
                                          textvariable=self.err_type)
        self.comb_err_type.set("Choose Error Type")

        # create buttons:
        self.btn_upload = Button(self.frame_create_new_rp, text='upload', font=FONT,
                                 command=self.upload_img)
        self.btn_return = Button(self.frame_create_new_rp, text='Return', font=FONT,
                                 command=self.show_frame_report)
        self.btn_submit = Button(self.frame_create_new_rp, text='Submit', font=FONT,
                                 command=self.submit)

        # place components:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.l_bike_id.place(x=S_W * (6 / 25), y=S_H * (1 / 15))
        self.l_bike_type.place(x=S_W * (15 / 25), y=S_H * (1 / 15))
        self.l_time.place(x=S_W * (6 / 25), y=S_H * (2 / 15))
        self.l_time_show.place(x=S_W * (11 / 25), y=S_H * (2 / 15), width=S_W * (400/1440), height=S_H * (30/900))
        self.l_loca.place(x=S_W * (6 / 25), y=S_H * (4 / 15))
        self.comb_loca.place(x=S_W * (11 / 25), y=S_H * (4 / 15), width=S_W * (400/1440), height=S_H * (30/900))
        self.l_err_type.place(x=S_W * (6 / 25), y=S_H * (6 / 15))
        self.comb_bike_type.place(x=S_W * (11 / 25), y=S_H * (6 / 15), width=S_W * (200/1440), height=S_H * (30/900))
        self.l_desc.place(x=S_W * (6 / 25), y=S_H * (8 / 15))
        self.e_desc.place(x=S_W * (11 / 25), y=S_H * (8 / 15), width=S_W * (400/1440), height=S_H * (100/900))
        self.comb_err_type.place(x=S_W * (145 / 250), y=S_H * (6 / 15), width=S_W * (200/1440), height=S_H * (30/900))
        self.l_pic.place(x=S_W * (6 / 25), y=S_H * (10 / 15))
        self.btn_upload.place(x=S_W * (11 / 25), y=S_H * (10 / 15), width=S_W * (200/1440), height=S_H * (50/900))
        self.btn_return.place(x=S_W * (2 / 25), y=S_H * (12 / 15), width=S_W * (200/1440), height=S_H * (50/900))
        self.btn_submit.place(x=S_W * (20 / 25), y=S_H * (12 / 15), width=S_W * (200/1440), height=S_H * (50/900))

    def fprocessing(self):

        # create button
        self.btn_return = Button(self.frame_processing, text='Return', font=FONT,
                                 command=self.show_frame_report)
        self.btn_detail = Button(self.frame_processing, text='Detail', font=FONT,
                                 command=self.show_deatil)
        # place button
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        Label(self.frame_processing, text='Error Journals', font=FONT).place(x=S_W * (5 / 25), y=S_H * (3 / 15))
        self.btn_return.place(x=S_W*(2/25), y=S_H*(13/15), width=200, height=50)
        self.btn_detail.place(x=S_W * (20 / 25), y=S_H * (13 / 15), width=200, height=50)

        # create a list tree
        record_info = CusOpenDatabase()
        records =record_info.select_processingRecords()
        columns = ("report_id", "report_time", "location", "bike_type", "desc", "err_type")
        self.tree = ttk.Treeview(self.frame_processing, height=20, show="headings", columns=columns)
        self.tree.column("report_id", width=200, anchor=CENTER)
        self.tree.column("report_time", width=200, anchor=CENTER)
        self.tree.column("location", width=200, anchor=CENTER)
        self.tree.column("bike_type", width=200, anchor=CENTER)
        self.tree.column("desc", width=200, anchor=CENTER)
        self.tree.column("err_type", width=200, anchor=CENTER)
        self.tree.place(x=S_W*(100 / 1440), y=S_H * (4 / 15))
        self.tree.heading("report_id", text='Journal_id', anchor=CENTER)
        self.tree.heading("report_time", text='Report_time', anchor=CENTER)
        self.tree.heading("location", text='Location', anchor=CENTER)
        self.tree.heading("bike_type", text='Bike_type', anchor=CENTER)
        self.tree.heading("desc", text='Description', anchor=CENTER)
        self.tree.heading("err_type", text='Error_type', anchor=CENTER)
        for record in records:
            self.tree.insert("", 0, values=(record[0], record[10], record[5], record[2], record[-1], record[6]))
        self.tree.bind("<<TreeviewSelect>>", self.onSelect)


class My:

    def __init__(self, master) -> None:

        self.master = master
        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()
        self.card_num = None

        self.frame_my = Frame(self.master, width=S_W, height=S_H)
        self.frame_top_up = Frame(self.master, width=S_W, height=S_H)
        self.frame_transaction_history = Frame(self.master, width=S_W, height=S_H)
        self.frame_rent_history = Frame(self.master, width=S_W, height=S_H)
        self.frame_rent_detail = Frame(self.master, width=S_W, height=S_H)
        self.frame_report_history = Frame(self.master, width=S_W, height=S_H)
        self.frame_report_detail = Frame(self.master, width=S_W, height=S_H)
        self.frame_change_password = Frame(self.master, width=S_W, height=S_H)
        self.frame_payment_selection = Frame(self.master, width=S_W, height=S_H)
        # self.frame_confirm_payment_info = Frame(self.master, width=S_W, height=S_H)
        self.frame_new_password = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_my, self.frame_top_up, self.frame_transaction_history,
                       self.frame_rent_history, self.frame_report_history, self.frame_change_password,
                       self.frame_payment_selection, self.frame_new_password,
                       self.frame_report_detail, self.frame_rent_detail]

        self.init_frames()
        self.frame_my.pack()

    def init_frames(self):
        self.fmy()
        self.ftop_up()
        self.fpayment_selection()
        # self.fconfirm_payment_info()
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
        self.forget_all()
        self.frame_payment_selection.pack()

    # def show_frame_confirm_payment_info(self):
    #     self.forget_all()
    #     self.frame_confirm_payment_info.pack()

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

    def edit_name(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.entry_username = Entry(self.frame_my, font=FONT)
        self.entry_username.place(x=S_W*(9/14), y=S_H*(15/80), width=WIDTH, height=HEIGHT)
        self.entry_username.focus()

    def confirm_newName(self):
        new_username = self.entry_username.get()
        updateInfo_1 = CusOpenDatabase()
        updateInfo_1.update_newUsername(new_username)

        self.entry_username.destroy()
        self.l_user_name_show_1["text"] = new_username

    def edit_email(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.entry_email = Entry(self.frame_my, font=FONT)
        self.entry_email.place(x=S_W * (5 / 14), y=S_H * (23 / 80), width=WIDTH, height=HEIGHT)
        self.entry_email.focus()

    def confirm_newEmail(self):
        new_userEmail = self.entry_email.get()
        updateInfo_2 = CusOpenDatabase()
        updateInfo_2.update_newEmail(new_userEmail)

        self.btn_confirm_newEmail.pack_forget()
        self.entry_email.destroy()
        self.l_email_show["text"] = new_userEmail

    def GBP5(self):
        self.amount = 5
        message = "£5"
        self.l_top_up_amount_show["text"] = message
        return 5

    def GBP10(self):
        self.amount = 10
        message = "£10"
        self.l_top_up_amount_show["text"] = message
        return 10

    def GBP20(self):
        self.amount = 20
        message = "£20"
        self.l_top_up_amount_show["text"] = message
        return 20

    def GBP50(self):
        self.amount=50
        message = "£50"
        self.l_top_up_amount_show["text"] = message
        return 50

    def GBP_others(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.entry_other_GBP = Entry(self.frame_top_up, font=FONT)
        self.entry_other_GBP.place(x=S_W * (9 / 28), y=S_H * (23 / 90), width=WIDTH, height=HEIGHT)
        self.entry_other_GBP.focus()
        return self.entry_other_GBP.get()

    def confirm_otherGBP(self):
        other_amount = self.entry_other_GBP.get()

        self.btn_confirm_otherGBP.pack_forget()
        self.entry_other_GBP.destroy()
        self.l_top_up_amount_show["text"] = "£", other_amount


    def confirm_pay(self):
        value_to_update = self.amount if self.amount is not None else self.entry_other_GBP.get()
        credit_update = CusOpenDatabase()
        credit_update.update_credit(value_to_update)
        click = messagebox.askyesno("Payment Accomplished", "Successful Payment!")
        new_credit = credit_update.get_customer_credit()
        if click:
            self.l_account_credit_show["text"] = "£", new_credit
            self.show_frame_my()

    def check_old_password(self):
        entry_password = self.e_old_password.get()
        checkPassword = CusOpenDatabase()
        my_password = checkPassword.check_myPassword()
        if entry_password == my_password:
            self.show_frame_new_password()
        else:
            click = messagebox.askyesno("Error","Password is not matched! Please try again")
            if click:
                self.show_frame_change_password()

    def confirm_new_password(self):

        new_entry = self.e_new_password.get()
        repeat_entry = self.e_repeat_password.get()
        if new_entry == repeat_entry:
            self.update_new_password()
            messagebox.askyesno("Matched","Success!")
            self.show_frame_my()
        else:
            messagebox.askyesno("Error","Your entry passwords are not matched!")

    def update_new_password(self):
        new_pword = self.e_new_password.get()
        updatePassword = CusOpenDatabase()
        updatePassword.update_myNewPassword(new_pword)

    def get_current_userInfo(self):
        current_user = CusOpenDatabase()
        user_data = current_user.get_loginData()

        return user_data

    def card_number(self):
        cardInfo = CusOpenDatabase()
        card_number = cardInfo.get_card_number()

        # change the tuple type to list
        numbers = [num for tup in card_number for num in tup]

        # hide card numbers except last 4 digits
        maskedCard = []
        for card_number in numbers:
            masked_card = self.mask_card_number(card_number)
            maskedCard.append(masked_card)

        return maskedCard

    def mask_card_number(self, card_number):
        # Ensure the card number is a string
        card_number = str(card_number)

        # Keep the last 4 digits
        last_4_digits = card_number[-4:]

        # Mask the rest with "x"
        masked_part = "x" * (len(card_number) - 4)

        # Add spaces every 4 "x" characters
        masked_number = " ".join([masked_part[i:i + 4] for i in range(0, len(masked_part), 4)])

        # Combine the masked part with the last 4 digits
        masked_card_number = masked_number + last_4_digits

        return masked_card_number

    def add_new_card(self):
        click = messagebox.askyesno("Attention", "Do you intend to add a new card for payment?")
        if click:
            self.ShowAddCard()

    def ShowAddCard(self):
        self.add_card = Tk()
        self.add_card.title("Adding a New card")
        self.add_card.geometry("800x600")
        self.l_title = Label(self.add_card, text="Please entry your card information:", font=FONT_TOP)
        self.l_card_num = Label(self.add_card, text="Card Number: ", font=FONT)
        self.l_expired_date = Label(self.add_card, text="Expiry Date: ", font=FONT)
        self.l_holder = Label(self.add_card, text="Card Holder: ", font=FONT)
        self.l_cv_num = Label(self.add_card, text="Security code: ", font=FONT)
        self.e_card_num = Entry(self.add_card, text="", font=FONT)
        self.e_expired_date = Entry(self.add_card, text="", font=FONT)
        self.e_holder = Entry(self.add_card, text="", font=FONT)
        self.e_cv_num = Entry(self.add_card, text="", font=FONT)
        self.l_hit = Label(self.add_card, text="Enter the name exactly as it appears on your debit or credit card.")

        self.btn_cancel = Button(self.add_card, text="Cancel", font=FONT,
                                 command = self.show_frame_payment_selection)
        self.btn_confirm = Button(self.add_card, text="Confirm", font=FONT,
                             command = self.insert_new_card)


        # image = Image.open("/Users/ruochenqi/Documents/Fintech in UofG/System programming/Group project/pic/creditCardIssuer.png")
        # photo = ImageTk.PhotoImage(image)
        # l_pic = Label(add_card, image=photo)

        self.l_title.place(x=150, y=50)
        self.l_card_num.place(x=180, y=100)
        self.l_cv_num.place(x=180, y=150, )
        self.l_expired_date.place(x=180, y=200)
        self.l_holder.place(x=180, y=250)
        self.l_hit.place(x=340, y=300)
        self.e_card_num.place(x=340, y=100)
        self.e_cv_num.place(x=340, y=150, width=50, height=35)
        self.e_expired_date.place(x=340, y=200, width=100, height=35)
        self.e_holder.place(x=340, y=250)
        self.btn_cancel.place(x=80, y=380)
        self.btn_confirm.place(x=620, y=380)
        # l_pic.place(x=0, y=400)

    def insert_new_card(self):
        entry_cardNum = self.e_card_num.get()
        entry_cv = self.e_cv_num.get()
        entry_expiry = self.e_expired_date.get()
        entry_holder = self.e_holder.get()

        insertData = CusOpenDatabase()
        insertData.insert_newCardInfo(entry_cardNum, entry_cv, entry_expiry, entry_holder)
        click = messagebox.askyesno("New Card inserted",
                            "Successfully added a new card, please go back.")
        if click:
            self.show_frame_my()

    def payment_successful(self):
        click = messagebox.askyesno("Payment made",
                                    "Thanks for your payment, please go back!")
        if click:
            self.confirm_pay()


    def fmy(self):

        user_data = self.get_current_userInfo()
        print("Current tracking: ", user_data)
        user_id = user_data[2]
        user_name = user_data[3]
        user_email = user_data[4]
        user_credit = user_data[-1]

        # create labels:
        self.l_user_id = Label(self.frame_my, text="User ID: ", font=FONT)
        self.l_user_id_show = Label(self.frame_my, text=user_id, font=FONT)
        self.l_user_name_1 = Label(self.frame_my, text="Username: ", font=FONT)
        self.l_user_name_show_1 = Label(self.frame_my, text="{}".format(user_name), font=FONT)
        self.l_email = Label(self.frame_my, text="E-mail: ", font=FONT)
        self.l_email_show = Label(self.frame_my, text="{}".format(user_email), font=FONT)
        self.l_account_credit = Label(self.frame_my, text="Account credit: ", font=FONT)
        self.l_account_credit_show = Label(self.frame_my, text="{}".format(user_credit), font=FONT)

        # create buttons:
        self.btn_edit_name = Button(self.frame_my, text="Edit", font=FONT,
                                  command=self.edit_name)
        self.btn_edit_email = Button(self.frame_my, text="Edit", font=FONT,
                                   command=self.edit_email)
        self.btn_confirm_newName = Button(self.frame_my, text="Confirm", font=FONT,
                                    command=self.confirm_newName)
        self.btn_confirm_newEmail = Button(self.frame_my, text="Confirm", font=FONT,
                                     command=self.confirm_newEmail)
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
        self.l_user_name_1.place(x=S_W * (8 / 14), y=S_H * (4 / 20))
        self.l_user_name_show_1.place(x=S_W * (9 / 14), y=S_H * (4 / 20))
        self.l_email.place(x=S_W * (3 / 14), y=S_H * (12 / 40))
        self.l_email_show.place(x=S_W * (5 / 14), y=S_H * (12 / 40))
        self.l_account_credit.place(x=S_W * (3 / 14), y=S_H * (16 / 40))
        self.l_account_credit_show.place(x=S_W * (5 / 14), y=S_H * (16 / 40))

        # place buttons:
        self.btn_edit_name.place(x=S_W * (12 / 14), y=S_H * (38 / 200), width=90, height=40)
        self.btn_confirm_newName.place(x=S_W * (13 / 14), y=S_H * (38 / 200), width=90, height=40)
        self.btn_edit_email.place(x=S_W * (8 / 14), y=S_H * (58 / 200), width=90, height=40)
        self.btn_confirm_newEmail.place(x=S_W * (9 / 14), y=S_H * (58 / 200), width=90, height=40)
        self.btn_top_up.place(x=S_W * (3 / 14), y=S_H * (20 / 40), width=200, height=50)
        self.btn_transaction_history.place(x=S_W * (3 / 14), y=S_H * (24 / 40), width=200, height=50)
        self.btn_rent_history.place(x=S_W * (3 / 14), y=S_H * (28/ 40), width=200, height=50)
        self.btn_report_history.place(x=S_W * (8 / 14), y=S_H * (28/ 40), width=200, height=50)
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
        self.btn_others = Button(self.frame_top_up, text="Others", font=FONT,
                                 command=self.GBP_others)
        self.btn_confirm_otherGBP = Button(self.frame_top_up, text="Confirm Amount", font=FONT,
                                           command=self.confirm_otherGBP)
        self.btn_go_back = Button(self.frame_top_up, text="Return", font=FONT,
                                  command=self.show_frame_my)
        self.btn_confirm = Button(self.frame_top_up, text="Confirm", font=FONT,
                                  command=self.show_frame_payment_selection)

        # place components:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_top_up_amount.place(x=S_W * (3 / 14), y=S_H * (24 / 90))
        self.l_top_up_amount_show.place(x=S_W * (5 / 14), y=S_H * (24 / 90))
        self.btn_GBP5.place(x=S_W * (35/ 140), y=S_H * (30 / 90), width=150, height=50)
        self.btn_GBP10.place(x=S_W * (55 / 140), y=S_H * (30 / 90), width=150, height=50)
        self.btn_GBP20.place(x=S_W * (75 / 140), y=S_H * (30 / 90), width=150, height=50)
        self.btn_GBP50.place(x=S_W * (95 / 140), y=S_H * (30 / 90), width=150, height=50)
        self.btn_others.place(x=S_W * (65 / 140), y=S_H * (40 / 90), width=150, height=50)
        self.btn_confirm_otherGBP.place(x=S_W * (8 / 14), y=S_H * (23 / 90), width=170, height=50)
        self.btn_go_back.place(x=S_W * (20 / 140), y=S_H * (60 / 90), width=150, height=50)
        self.btn_confirm.place(x=S_W * (11 / 14), y=S_H * (60 / 90), width=150, height=50)

    def fpayment_selection(self):

        # create labels:
        self.l_pay_by_your_card = Label(self.frame_payment_selection, text="Please pay by your card:", font=FONT_TITLE)
        self.l_card = Label(self.frame_payment_selection, text="Card:", font=FONT_TITLE)

        # create selection:
        self.selected_card_3 = StringVar()
        cards = self.card_number()
        self.optionmenu_card = ttk.Combobox(self.frame_payment_selection, textvariable=self.selected_card_3,
                                            values=cards)
        # self.optionmenu_card.bind("<<ComboboxSelected>>", self.get_card_num)

        # create buttons:
        self.btn_go_back = Button(self.frame_payment_selection, text="Return", font=FONT,
                                command=self.show_frame_top_up)
        self.btn_pay = Button(self.frame_payment_selection, text="Choose this card", font=FONT,
                                       command=self.payment_successful)
        self.btn_add_newcard = Button(self.frame_payment_selection, text="Add New Cards", font=FONT,
                                      command=self.add_new_card)

        # place components:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_pay_by_your_card.place(x=S_W * (45 / 140), y=S_H * (30 / 90))
        self.l_card.place(x=S_W * (45 / 140), y=S_H * (40 / 90))
        self.optionmenu_card.place(x=S_W * (60 / 140), y=S_H * (413 / 900), width=S_W * (400/1440), height=S_H * (50/900))
        self.btn_go_back.place(x=S_W * (20 / 140), y=S_H * (60 / 90), width=S_W * (200/1440), height=S_H * (50/900))
        self.btn_pay.place(x=S_W * (11 / 14), y=S_H * (60 / 90), width=S_W * (200/1440), height=S_H * (50/900))
        self.btn_add_newcard.place(x=S_W * (100 / 140), y=S_H * (413 / 900), width=S_W * (200/1440), height=S_H * (50/900))


    # def fconfirm_payment_info(self):
    #
    #     user_data = self.get_current_userInfo()
    #     user_id = user_data[2]
    #     user_name = user_data[3]
    #     amount = user_data[-1]
    #     card_num = self.card_num
    #     print(card_num)
    #     # create label:
    #     self.l_user_id = Label(self.frame_confirm_payment_info, text="User ID: ", font=FONT)
    #     self.l_user_id_show = Label(self.frame_confirm_payment_info, text="{}".format(user_id), font=FONT)
    #     self.l_user_name = Label(self.frame_confirm_payment_info, text="Username: ", font=FONT)
    #     self.l_user_name_show = Label(self.frame_confirm_payment_info, text="{}".format(user_name), font=FONT)
    #     self.l_amount = Label(self.frame_confirm_payment_info, text="Amount: ", font=FONT)
    #     self.l_amount_show = Label(self.frame_confirm_payment_info, text="{}".format(amount), font=FONT)
    #     # self.l_top_up_account = Label(self.frame_confirm_payment_info, text="Top-up Account: ", font=FONT)
    #     # self.l_top_up_account_show = Label(self.frame_confirm_payment_info, text="{}".format(top_up_amount), font=FONT)
    #     self.l_card_info = Label(self.frame_confirm_payment_info, text="Card: ", font=FONT)
    #     self.l_card_info_show = Label(self.frame_confirm_payment_info, text="{}".format(card_num),
    #                                   font=FONT)
    #
    #     # create buttons:
    #     self.btn_go_back = Button(self.frame_confirm_payment_info, text="Return", font=FONT,
    #                              command=self.show_frame_payment_selection)
    #     self.btn_pay = Button(self.frame_confirm_payment_info, text="Confirm", font=FONT,
    #                           command=self.confirm_pay)
    #
    #     # place components
    #     S_W = self.master.winfo_screenwidth()
    #     S_H = self.master.winfo_screenheight()
    #
    #     self.l_user_id.place(x=S_W * (35 / 140), y=S_H * (24 / 90))
    #     self.l_user_id_show.place(x=S_W * (45 / 140), y=S_H * (24 / 90), width=S_W * (200/1440), height=S_H * (30/900))
    #     self.l_user_name.place(x=S_W * (75 / 140), y=S_H * (24 / 90))
    #     self.l_user_name_show.place(x=S_W * (85 / 140), y=S_H * (24 / 90), width=S_W * (200/1440), height=S_H * (30/900))
    #     self.l_amount.place(x=S_W * (35 / 140), y=S_H * (34 / 90))
    #     self.l_amount_show.place(x=S_W * (45 / 140), y=S_H * (34 / 90), width=S_W * (200/1440), height=S_H * (30/900))
    #     # self.l_top_up_account.place(x=S_W * (35 / 140), y=S_H * (34 / 90))
    #     # self.l_top_up_account_show.place(x=S_W * (5 / 14), y=S_H * (34 / 90))
    #     self.l_card_info.place(x=S_W * (35 / 140), y=S_H * (44 / 90))
    #     self.l_card_info_show.place(x=S_W * (45 / 140), y=S_H * (44 / 90), width=S_W * (200/1440), height=S_H * (30/900))
    #     self.btn_go_back.place(x=S_W * (2 / 14), y=S_H * (60 / 90), width=150, height=50)
    #     self.btn_pay.place(x=S_W * (11 / 14), y=S_H * (60 / 90), width=150, height=50)


    def ftransaction_history(self):

        # create label
        self.l_transaction_history_type = Label(self.frame_transaction_history, text="Type: ", font=FONT)

        # create options:
        self.selected_transaction_type = StringVar()
        types = ["Spend", "Top-up"]
        self.optionmenu_transaction_type = ttk.Combobox(self.frame_transaction_history, values=types,
                                                        textvariable=self.selected_transaction_type)

        # create button:
        self.transaction_s_btn = Button(self.frame_transaction_history, text="Search", font=FONT,
                                        command=self.search_transaction)
        self.btn_go_back = Button(self.frame_transaction_history, text = "Return", font=FONT,
                                  command = self.show_frame_my)

        # place label:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.search_transaction()
        self.l_transaction_history_type.place(x=S_W * (2 / 14), y=S_H * (15 / 90))
        self.transaction_s_btn.place(x=S_W * (9 / 14), y=S_H * (14 / 90), width=150, height=50)
        self.optionmenu_transaction_type.place(x=S_W * (32 / 140), y=S_H * (14 / 90), width=300, height=50)
        self.btn_go_back.place(x=S_W * (2 / 14), y=S_H * (60 / 90), width=150, height=50)

    def search_transaction(self):       # create for transaction search button and the list tree display

        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        selected_transaction_type=self.selected_transaction_type.get()
        print(selected_transaction_type)
        transactionRecord = CusOpenDatabase()
        records = transactionRecord.select_transactionRecords(selected_transaction_type)

        # create chat tree
        columns = ("id", "amount", "type", "date")
        self.tree = ttk.Treeview(self.frame_transaction_history, height=14, show="headings", columns=columns)
        self.tree.column("id", width=250,anchor=CENTER)
        self.tree.column("amount", width=250,anchor=CENTER)
        self.tree.column("type", width=250,anchor=CENTER)
        self.tree.column("date", width=250,anchor=CENTER)
        self.tree.heading("id", text='Record ID', anchor=CENTER)
        self.tree.heading("amount", text='Amount', anchor=CENTER)
        self.tree.heading("type", text='In/Out Flow', anchor=CENTER)
        self.tree.heading("date", text='Date', anchor=CENTER)
        for record in records:
            if record[2] != None:
                self.tree.insert("", 0, values=(record[0], record[2], record[-1], record[4]))
            else:
                self.tree.insert("", 0, values=(record[0], ("-",record[8]), record[-1], record[5]))
        self.tree.place(x=S_W * (2 / 14), y=S_H * (27 / 90), width=1000, height=300)

    def frent_history(self):
        # create label
        self.l_rent_history_type = Label(self.frame_rent_history, text="Bike Type: ", font=FONT)
        self.l_rent_date = Label(self.frame_rent_history, text="Location: ", font=FONT)

        # create options:
        self.selected_rentbike_type = StringVar()
        types = ["electric_bike", "electric_scooter"]
        self.optionmenu_bike_type = ttk.Combobox(self.frame_rent_history, values=types,
                                                 textvariable=self.selected_rentbike_type)
        select_parking_location_1 = CusOpenDatabase()
        parking_location = select_parking_location_1.select_parking_location()
        self.select_rent_location = StringVar()
        self.optionmenu_rent_location = ttk.Combobox(self.frame_rent_history, values=parking_location,
                                                     textvariable=self.select_rent_location)
        # create button:
        self.btn_go_back = Button(self.frame_rent_history, text="Return", font=FONT,
                                  command=self.show_frame_my)
        self.rent_go_query = Button(self.frame_rent_history, text="Search", font=FONT,
                                    command=self.rent_go_query_btn)
        # display list tree
        self.rent_go_query_btn()

        # place label:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()


        self.l_rent_history_type.place(x=S_W * (2 / 14), y=S_H * (15 / 90))
        self.l_rent_date.place(x=S_W * (8 / 14), y=S_H * (15 / 90))
        self.optionmenu_bike_type.place(x=S_W * (32 / 140), y=S_H * (14 / 90), width=300, height=50)
        self.optionmenu_rent_location.place(x=S_W * (90 / 140), y=S_H * (14 / 90), width=300, height=50)
        self.btn_go_back.place(x=S_W * (2 / 14), y=S_H * (60 / 90), width=150, height=50)
        self.rent_go_query.place(x=S_W * (10 / 14), y=S_H * (60 / 90), width=150, height=50)

    def rent_go_query_btn(self):

        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        select_rent_location = self.select_rent_location.get()
        selected_rentbike_type = self.selected_rentbike_type.get()
        get_rentalHistory = CusOpenDatabase()
        records = get_rentalHistory.select_rentalHistory(select_rent_location, selected_rentbike_type)

        columns = ("bike_type", "start_location", "end_location", "start_time", "end_time", "price")
        self.tree = ttk.Treeview(self.frame_rent_history, height=14, show="headings", columns=columns)
        self.tree.column("bike_type", width=200, anchor=CENTER)
        self.tree.column("start_location", width=200, anchor=CENTER)
        self.tree.column("end_location", width=200, anchor=CENTER)
        self.tree.column("start_time", width=200, anchor=CENTER)
        self.tree.column("end_time", width=200, anchor=CENTER)
        self.tree.column("price", width=200, anchor=CENTER)

        self.tree.heading("bike_type", text='Bike Type', anchor=CENTER)
        self.tree.heading("start_location", text='Where to Start', anchor=CENTER)
        self.tree.heading("end_location", text='Return To', anchor=CENTER)
        self.tree.heading("start_time", text='Start Time', anchor=CENTER)
        self.tree.heading("end_time", text='End Time', anchor=CENTER)
        self.tree.heading("price", text='Cost', anchor=CENTER)
        for record in records:
            self.tree.insert("", 0, values=(record[-5], record[2], record[3], record[4], record[5], "£"+record[-4]))
        self.tree.place(x=S_W * (1 / 14), y=S_H * (27 / 90), width=1200, height=300)

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

    def freport_history(self):

        # create label
        self.l_bike_type = Label(self.frame_report_history, text="Bike Type: ", font=FONT)
        self.l_report_type = Label(self.frame_report_history, text="Report Type: ", font=FONT)

        # create options:
        select_parking_location_3 = CusOpenDatabase()
        parking_location = select_parking_location_3.select_parking_location()
        self.report_history_location = StringVar()
        self.optionmenu_location = ttk.Combobox(self.frame_report_history, values=parking_location,
                                                textvariable=self.report_history_location)
        error_types = ["Wheels", "seats", "fronts", "chains", "tires", "brakes", "frames"]
        self.report_err_type = StringVar()
        self.optionmenu_report_type = ttk.Combobox(self.frame_report_history, values=error_types,
                                                   textvariable=self.report_err_type)

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
        self.btn_go_back.place(x=S_W * (2 / 14), y=S_H * (60 / 90), width=150, height=50)
        self.report_go_query.place(x=S_W * (10 / 14), y=S_H * (60 / 90), width=150, height=50)

    def report_go_query_btn(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        report_history_location = self.report_history_location.get()
        report_err_type = self.report_err_type.get()
        get_report = CusOpenDatabase()
        records = get_report.select_errHistory(report_history_location, report_err_type)

        columns = ("report_time", "location", "err_type", "desc", "status")
        self.tree = ttk.Treeview(self.frame_report_history, height=14, show="headings", columns=columns)
        self.tree.column("report_time", width=200, anchor=CENTER)
        self.tree.column("location", width=200, anchor=CENTER)
        self.tree.column("err_type", width=200, anchor=CENTER)
        self.tree.column("desc", width=200, anchor=CENTER)
        self.tree.column("status", width=200, anchor=CENTER)
        self.tree.heading("report_time", text='Report Time', anchor=CENTER)
        self.tree.heading("location", text='Location', anchor=CENTER)
        self.tree.heading("err_type", text='Err_type', anchor=CENTER)
        self.tree.heading("desc", text='Description', anchor=CENTER)
        self.tree.heading("status", text='Status', anchor=CENTER)
        for record in records:
            self.tree.insert("", 0, values=(record[-4], record[5], record[6], record[-1], record[8]))
        self.tree.place(x=S_W * (2 / 14), y=S_H * (27 / 90), width=1000, height=300)

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
        self.l_change_password_title = Label(self.frame_change_password, text="Please enter your current password", font=FONT_TITLE)
        # create Entry:
        self.e_old_password = Entry(self.frame_change_password, text="", font=FONT_TITLE)
        # create button:
        self.btn_check_old_password = Button(self.frame_change_password, text="Enter", font=FONT,
                                             command=self.check_old_password)

        self.btn_go_back = Button(self.frame_change_password, text = "Return", font=FONT,
                                  command = self.show_frame_my)

        # place components:
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_change_password_title.place(x=S_W * (33 / 140), y=S_H * (30 / 90))
        self.e_old_password.place(x=S_W * (5 / 14), y=S_H * (4 / 9), width=400, height=50)
        self.btn_check_old_password.place(x=S_W * (105 / 140), y=S_H * (6 / 9), width=150, height=50)
        self.btn_go_back.place(x=S_W * (2 / 14), y=S_H * (6 / 9), width=150, height = 50)

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
        self.btn_go_back = Button(self.frame_new_password, text = "Return", font = FONT,
                                  command = self.show_frame_change_password)

        # place components
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_enter_new_password.place(x=S_W * (45 / 140), y=S_H * (25 / 90))
        self.l_repeat_password.place(x=S_W * (45 / 140), y=S_H * (39 / 90))
        self.e_new_password.place(x=S_W * (45 / 140), y=S_H * (31 / 90), width=500, height=50)
        self.e_repeat_password.place(x=S_W * (45 / 140), y=S_H * (45 / 90), width=500, height=50)
        self.btn_confirm_new_password.place(x=S_W * (105 / 140), y=S_H * (6 / 9), width=150, height=50)
        self.btn_go_back.place(x=S_W * (2 / 14), y=S_H * (6 / 9), width=150, height=50)


class CustomerUI:

    def __init__(self) -> None:

        self.master = Tk()
        self.master.title("Customer")

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
        self.report = Report(self.frame_report)
        self.my = My(self.frame_my)

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



