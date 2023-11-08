from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
import sqlite3
from datetime import datetime
from ManipulateDatabase import CusOpenDatabase, OperatorDatabase

import numpy as np

FONT = ('Arial', 20)  # 文本大小

FONT_TOP = ('Arial', 20, 'bold')  # 顶部框字体大小

FONT_TITLE = ('Arial', 50, 'bold')  # 中部标题大小

# 每个entry/选项框大小
HEIGHT = 50
WIDTH = 300


# OPERATOR
class Track:
    def __init__(self) -> None:
        pass


class Charge:
    def __init__(self, master) -> None:

        self.master = master
        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()

        # create frames
        self.frame_charge_main = Frame(self.master, width=S_W, height=S_H)
        self.frame_charge_confirm = Frame(self.master, width=S_W, height=S_H)
        self.frame_charge_history = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_charge_main, self.frame_charge_confirm, self.frame_charge_history]

        self.init_frame()
        self.show_frame_charge_main()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def show_frame_charge_main(self):
        self.forget_all()
        self.frame_charge_main.pack()

    def show_frame_charge_confirm(self):
        self.forget_all()
        self.frame_charge_confirm.pack()

    def show_frame_charge_history(self):
        self.forget_all()
        self.frame_charge_history.pack()

    def init_frame(self):
        self.fcharge_main()
        self.fcharge_confirm()
        self.fcharge_history()

    # 确认充电,充电成功小弹窗，自动跳转回charge界面
    def confim_charge(self):
        result = messagebox.askyesno("Confirm", "Confirm Charge？")
        if result:  # 如果用户点击了确认按钮
            self.ShowSuccess()

    def ShowSuccess(self):
        success_window = Tk()
        success_window.title("success window")
        label = Label(success_window, text="Charge Successful !", font=FONT)
        label.place(x=0, y=50)
        success_window.geometry("250x150+575+325")
        self.show_frame_charge_main()

    # get Location for combobox
    def select_location(self):
        location_data = CusOpenDatabase()
        locationData = location_data.select_parking_location()
        return locationData

    # get bike type for combobox
    def select_type(self):
        type_data = OperatorDatabase()
        typeData = type_data.bikeType()
        print("database has type: ", typeData)
        return typeData

    def fcharge_main(self):

        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.selected_location = StringVar()
        self.l_location = Label(self.frame_charge_main, text='Location:', font=FONT)
        self.l_location.place(x=S_W / 1440 * 150, y=S_H / 900 * 150)
        self.comb_location = ttk.Combobox(self.frame_charge_main, values=self.select_location(),
                                          textvariable=self.selected_location, font=FONT)
        self.comb_location.bind("<<ComboboxSelected>>", self.show_charge_tabel)  # Bind an event handler
        self.comb_location.set("Choose Location")
        self.comb_location.place(x=S_W / 1440 * (150 + 150), y=S_H / 900 * 150, width=WIDTH, height=HEIGHT)


        self.l_type = Label(self.frame_charge_main, text='Bike Type:', font=FONT)
        self.l_type.place(x=S_W / 1440 * (300 + WIDTH +150), y=S_H / 900 * 150)
        self.selected_type_1 = StringVar()
        self.comb_t = ttk.Combobox(self.frame_charge_main, values=self.select_type(),
                                   textvariable=self.selected_type_1, font=FONT)
        self.comb_t.bind("<<ComboboxSelected>>", self.show_charge_tabel)  # Bind an event handler
        self.comb_t.set("Choose Type")
        self.comb_t.place(x=S_W / 1440 * (300 + WIDTH + 300), y=S_H / 900 * 150, width=WIDTH, height=HEIGHT)

        self.btn_confirm = Button(self.frame_charge_main, text="Fliter", font=FONT,
                                  command=self.show_charge_tabel)
        self.btn_confirm.place(x=S_W / 1440 * (300 + WIDTH), y=S_H / 900 * 200, width=WIDTH, height=HEIGHT)

        self.l_box = Label(self.frame_charge_main, text='List of Information:', font=FONT)
        self.l_box.place(x=S_W / 1440 * 150, y=S_H / 900 * 250)

        self.btn_history = Button(self.frame_charge_main, text="History", font=FONT,
                                  command=self.show_frame_charge_history)
        self.btn_history.place(x=S_W / 1440 * 1120, y=S_H / 900 * 60, width=WIDTH, height=HEIGHT)

    def show_charge_tabel(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        print("get a type: ", self.selected_type_1.get())
        print("we get a location: ", self.selected_location.get())

        columns = ['No.', 'Bike ID', 'Bike Type', 'Battery', 'Location']

        self.table = ChargeTable(self.frame_charge_main, columns=columns,
                                 comb_location=self.selected_location.get(),
                                 comb_type=self.selected_type_1.get())
        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

    def fcharge_confirm(self):

        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_title = Label(self.frame_charge_confirm, text='CONFIRM CHARGE', font=FONT_TITLE)
        self.l_title.place(x=S_W / 1440 * 400, y=S_H / 900 * 100)

        self.l_operatorid = Label(self.frame_charge_confirm, text='Operator ID:', font=FONT)
        self.l_operatorid.place(x=S_W / 1440 * 500, y=S_H / 900 * 300)

        self.l_oid = Label(self.frame_charge_confirm, text="id", font=FONT)
        self.l_oid.place(x=S_W / 1440 * (500 + 200), y=S_H / 900 * 300)

        self.l_location = Label(self.frame_charge_confirm, text='Location:', font=FONT)
        self.l_location.place(x=S_W / 1440 * 500, y=S_H / 900 * 400)
        self.comb_location = ttk.Combobox(self.frame_charge_confirm, values=self.select_location(), font=FONT)
        self.comb_location.place(x=S_W / 1440 * (500 + 200), y=S_H / 900 * 400, width=WIDTH, height=HEIGHT)

        self.l_date = Label(self.frame_charge_confirm, text='Date:', font=FONT)
        self.l_date.place(x=S_W / 1440 * 500, y=S_H / 900 * 500)
        self.l_date = Label(self.frame_charge_confirm, text=datetime.now(), font=FONT)
        self.l_date.place(x=S_W / 1440 * (500 + 200), y=S_H / 900 * 500)

        self.btn_return = Button(self.frame_charge_confirm, text="Return", font=FONT,
                                 command=self.show_frame_charge_main)
        self.btn_return.place(x=S_W / 1440 * 400, y=S_H / 900 * 600, width=WIDTH, height=HEIGHT)

        self.btn_confirm = Button(self.frame_charge_confirm, text="Confirm", font=FONT,
                                  command=self.confim_charge)
        self.btn_confirm.place(x=S_W / 1440 * 750, y=S_H / 900 * 600, width=WIDTH, height=HEIGHT)

    def fcharge_history(self):

        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_title = Label(self.frame_charge_history, text='CHARGE HISTORY', font=FONT_TITLE)
        self.l_title.place(x=S_W / 1440 * 400, y=S_H / 900 * 100)

        self.current_datetime = datetime.now()
        self.current_date = self.current_datetime.date()
        self.year = list(range(2021, self.current_date.year + 1))
        self.month = list(range(1, 13))
        self.day = list(range(1, 32))

        self.selected_day = StringVar()
        self.selected_month = StringVar()
        self.selected_year = StringVar()
        self.selected_type_2 = StringVar()

        self.l_date = Label(self.frame_charge_history, text='Date:', font=FONT)
        self.l_date.place(x=S_W / 1440 * 150, y=S_H / 900 * 200)
        self.comb_day = ttk.Combobox(self.frame_charge_history, values=self.day,
                                     textvariable=self.selected_day,font=FONT)
        self.comb_day.insert(0, "day")
        self.comb_day.place(x=S_W / 1440 * (150 + 150), y=S_H / 900 * 200, width=WIDTH / 3, height=HEIGHT)
        self.comb_month = ttk.Combobox(self.frame_charge_history, values=self.month,
                                       textvariable=self.selected_month,font=FONT)
        self.comb_month.insert(0, "month")
        self.comb_month.place(x=S_W / 1440 * (150 + 150) + WIDTH / 3, y=S_H / 900 * 200, width=WIDTH / 3, height=HEIGHT)
        self.comb_year = ttk.Combobox(self.frame_charge_history, values=self.year,
                                      textvariable=self.selected_year,font=FONT)
        self.comb_year.insert(0, "year")
        self.comb_year.place(x=S_W / 1440 * (150 + 150) + 2 * WIDTH / 3, y=S_H / 900 * 200, width=WIDTH / 3,
                             height=HEIGHT)

        self.l_type = Label(self.frame_charge_history, text='Bike Type:', font=FONT)
        self.l_type.place(x=S_W / 1440 * (300 + WIDTH + 150), y=S_H / 900 * 200)
        self.comb_type = ttk.Combobox(self.frame_charge_history, values=self.select_type(),
                                      textvariable=self.selected_type_2,font=FONT)
        self.comb_type.place(x=S_W / 1440 * (300 + WIDTH + 300), y=S_H / 900 * 200, width=WIDTH, height=HEIGHT)

        self.btn_confirm = Button(self.frame_charge_history, text="Fliter", font=FONT,
                                  command=self.show_charge_history_tabel)
        self.btn_confirm.place(x=S_W / 1440 * (300 + WIDTH), y=S_H / 900 * 250, width=WIDTH, height=HEIGHT)

        self.l_box = Label(self.frame_charge_history, text='List of Information:', font=FONT)
        self.l_box.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

        self.btn_return = Button(self.frame_charge_history, text="Return", font=FONT,
                                 command=self.show_frame_charge_main)
        self.btn_return.place(x=S_W / 1440 * 150, y=S_H / 900 * 760, width=WIDTH, height=HEIGHT)

    def show_charge_history_tabel(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        columns = ['No.', 'Bike ID', 'Bike Type', 'Error Type', 'Location']

        day = self.selected_day.get()
        month = self.selected_month.get()
        year = self.selected_year.get()
        self.date = "{}-{}-{}".format(year, month, day)

        self.table = ChargeHistoryTable(self.frame_charge_history, columns=columns,
                                        comb_date=self.date,
                                        comb_type="foot_bike")
                                        #comb_type=self.selected_type_2.get())
        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

class ChargeTable(ttk.Treeview, Charge):

    # def __init__(self, master, columns) -> None:
    def __init__(self, master, columns, comb_location, comb_type) -> None:
        super().__init__(
            master=master,
            columns=columns,
            show='headings',
            style='Treeview',
        )

        self.cl = comb_location
        self.ct = comb_type
        self.getdata = self.getChargeData()

        style = ttk.Style(master)
        style.configure('Treeview', font=('Arial', 14), rowheight=30)
        style.configure('Treeview.Heading', font=('Arial', 20))

        for column in columns:
            self.heading(column, text=column, anchor=CENTER)
            self.column(column, width=220, anchor=CENTER)

        self.bind("<Double-1>", self.show_window)

        self.datas = self.add_row(self.getdata)

    def getChargeData(self):
        # comb_location, comb_type = super().get_lc_tp()
        chargeList = OperatorDatabase()
        chargeData = chargeList.get_chargeData(self.cl, self.ct)
        return chargeData

    def add_row(self, datas):
        self.datalist = []
        count = 1
        for data in datas:
            row_data = [count] + list(data)
            self.insert("", END, values=row_data)
            self.datalist.append(row_data)
            count += 1
        return self.datalist

    def show_window(self, event):
        # 获取 Treeview 实例
        tree = event.widget
        # 获取当前选中项的ID
        selected_item_id = tree.focus()
        # 获取该项的索引，即第几行
        row_index = tree.index(selected_item_id)
        if (selected_item_id):
            record = ChargeDetail(*self.datas[row_index])
            record_ui = ChargeDetails(record)
            record_ui.show()

class ChargeDetail:

    def __init__(self, no=None, BID=None, Btype=None, Battery=None,
                 Location=None, Time=None) -> None:
        self.no = no
        self.BID = BID
        self.BType = Btype
        self.Battery = Battery
        self.Location = Location
        self.Time = Time

class ChargeDetails:
    """显示维修记录的界面"""

    def confim_charge(self):
        result = messagebox.askyesno("Confirm", "Confirm Charge？")
        if result:  # 如果用户点击了确认按钮
            self.ShowSuccess()

    def ShowSuccess(self):
        success_window = Tk()
        success_window.title("success window")
        label = Label(success_window, text="Charge Successful !", font=FONT)
        label.place(x=0, y=50)
        success_window.geometry("250x150+575+325")
        self.show_frame_charge_main()

    def __init__(self, record: ChargeDetail) -> None:
        self.record = record

        self.master = Tk()
        self.master.title('Charge Detail')
        self.master.geometry('600x400+400+200')

        self.init_ui()

    def init_ui(self):
        font = ('Arial', 16)
        # create widget
        self.l_title = Label(self.master, text='Repair Record', font=FONT)
        self.l_title.place(x=220, y=20)

        self.l_bike_id = Label(self.master, text='Bike ID:', font=font)
        self.l_bike_id.place(x=80, y=70)
        self.e_bike_id = Entry(self.master, font=font)
        self.e_bike_id.insert(0, self.record.BID)
        self.e_bike_id.configure(state='readonly')
        self.e_bike_id.place(x=200, y=70, width=300)

        self.l_bike_type = Label(self.master, text='Bike type:', font=font)
        self.l_bike_type.place(x=80, y=120)
        self.e_bike_type = Entry(self.master, font=font)
        self.e_bike_type.insert(0, self.record.BType)
        self.e_bike_type.configure(state='readonly')
        self.e_bike_type.place(x=200, y=120, width=300)

        self.l_battery = Label(self.master, text='Battery:', font=font)
        self.l_battery.place(x=80, y=170)
        self.e_battery = Entry(self.master, font=font)
        self.e_battery.insert(0, self.record.Battery)
        self.e_battery.configure(state='readonly')
        self.e_battery.place(x=200, y=170, width=300)

        self.l_location = Label(self.master, text='Location:', font=font)
        self.l_location.place(x=80, y=220)
        self.e_location = Entry(self.master, font=font)
        self.e_location.insert(0, self.record.Location)
        self.e_location.configure(state='readonly')
        self.e_location.place(x=200, y=220, width=300)

        self.l_time = Label(self.master, text='time:', font=font)
        self.l_time.place(x=80, y=270)
        self.e_time = Entry(self.master, font=font)
        self.e_time.insert(0, datetime.now())
        self.e_time.configure(state='readonly')
        self.e_time.place(x=200, y=270, width=300)

        self.btn_return = Button(self.master, text='Return', font=font,
                                 command=self.master.destroy)
        self.btn_return.place(x=100, y=330, height=50, width=150)

        self.btn_charge = Button(self.master, text='Charge', font=font,
                                 command=self.confim_charge)
        self.btn_charge.place(x=350, y=330, height=50, width=150)

    def show(self):
        self.master.mainloop()

class ChargeHistoryTable(ttk.Treeview):
    def __init__(self, master, columns,comb_date, comb_type) -> None:
        super().__init__(
            master=master,
            columns=columns,
            show='headings',
            style='Treeview',
        )

        self.cd = comb_date
        self.ct = comb_type
        self.getdata = self.getChargeHistoryData()

        style = ttk.Style(master)
        style.configure('Treeview', font=('Arial', 14), rowheight=30)
        style.configure('Treeview.Heading', font=('Arial', 20))

        for column in columns:
            self.heading(column, text=column, anchor=CENTER)
            self.column(column, width=220, anchor=CENTER)

        self.bind("<Double-1>", self.show_window)

        self.datas = self.add_row(self.getdata)

    def getChargeHistoryData(self):
        # comb_location, comb_type = super().get_lc_tp()
        chargeHistList = OperatorDatabase()
        chargeHistoryData = chargeHistList.get_chargeHistory(self.cd, self.ct)
        return chargeHistoryData

    def add_row(self, datas):
        self.datalist = []
        count = 1
        for data in datas:
            row_data = [count] + list(data)
            self.insert("", END, values=row_data)
            self.datalist.append(row_data)
            count += 1
        return self.datalist

    def show_window(self, event):
        # 获取 Treeview 实例
        tree = event.widget
        # 获取当前选中项的ID
        selected_item_id = tree.focus()
        # 获取该项的索引，即第几行
        row_index = tree.index(selected_item_id)
        if (selected_item_id):
            record = ChargeHistoryDetail(*self.datas[row_index])
            record_ui = ChargeHistoryDetails(record)
            record_ui.show()


class ChargeHistoryDetail:

    def __init__(self, no=None, BID=None, Btype=None, Time=None,
                 Location=None, Operator=None) -> None:
        self.no = no
        self.BID = BID
        self.BType = Btype
        self.Time = Time
        self.Location = Location
        self.Operator = Operator


class ChargeHistoryDetails:
    """显示维修记录的界面"""

    def __init__(self, record: ChargeHistoryDetail) -> None:
        self.record = record

        self.master = Tk()
        self.master.title('Charge History Detail')
        self.master.geometry('600x400+400+200')

        self.init_ui()

    def init_ui(self):
        font = ('Arial', 16)
        # create widget
        self.l_title = Label(self.master, text='Charge Record', font=FONT)
        self.l_title.place(x=220, y=20)

        self.l_bike_id = Label(self.master, text='Bike ID:', font=font)
        self.l_bike_id.place(x=80, y=70)
        self.e_bike_id = Entry(self.master, font=font)
        self.e_bike_id.insert(0, self.record.BID)
        self.e_bike_id.configure(state='readonly')
        self.e_bike_id.place(x=200, y=70, width=300)

        self.l_bike_type = Label(self.master, text='Bike type:', font=font)
        self.l_bike_type.place(x=80, y=120)
        self.e_bike_type = Entry(self.master, font=font)
        self.e_bike_type.insert(0, self.record.BType)
        self.e_bike_type.configure(state='readonly')
        self.e_bike_type.place(x=200, y=120, width=300)

        self.l_battery = Label(self.master, text='Charge Time:', font=font)
        self.l_battery.place(x=80, y=170)
        self.e_battery = Entry(self.master, font=font)
        self.e_battery.insert(0, self.record.Time)
        self.e_battery.configure(state='readonly')
        self.e_battery.place(x=200, y=170, width=300)

        self.l_location = Label(self.master, text='Location:', font=font)
        self.l_location.place(x=80, y=220)
        self.e_location = Entry(self.master, font=font)
        self.e_location.insert(0, self.record.Location)
        self.e_location.configure(state='readonly')
        self.e_location.place(x=200, y=220, width=300)

        self.l_time = Label(self.master, text='Operator ID:', font=font)
        self.l_time.place(x=80, y=270)
        self.e_time = Entry(self.master, font=font)
        self.e_time.insert(0, self.record.Operator)
        self.e_time.configure(state='readonly')
        self.e_time.place(x=200, y=270, width=300)

        self.btn_return = Button(self.master, text='Return', font=font,
                                 command=self.master.destroy)
        self.btn_return.place(x=200, y=330, height=50, width=200)

    def show(self):
        self.master.mainloop()


class Repair:

    def __init__(self, master) -> None:
        self.master = master
        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()

        # create frames
        self.frame_repair_main = Frame(self.master, width=S_W, height=S_H)
        self.frame_repair_history = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_repair_main, self.frame_repair_history]

        self.init_frame()
        self.show_frame_repair_main()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def show_frame_repair_main(self):
        self.forget_all()
        self.frame_repair_main.pack()

    def show_frame_repair_history(self):
        self.forget_all()
        self.frame_repair_history.pack()

    def init_frame(self):
        self.frepair_main()
        self.frepair_history()

    def select_location(self):
        location_data = CusOpenDatabase()
        locationData = location_data.select_parking_location()
        return locationData

    def select_biketype(self):
        type_data = OperatorDatabase()
        typeData = type_data.bikeType()
        return typeData

    def frepair_main(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.selected_location = StringVar()
        self.l_location = Label(self.frame_repair_main, text='Location:', font=FONT)
        self.l_location.place(x=S_W / 1440 * 150, y=S_H / 900 * 150)
        self.comb_location = ttk.Combobox(self.frame_repair_main, values=list(self.select_location()),
                                          textvariable=self.selected_location, font=FONT)
        self.comb_location.set("Choose Location")
        self.comb_location.place(x=S_W / 1440 * (150 + 150), y=S_H / 900 * 150, width=WIDTH, height=HEIGHT)

        self.selected_type_3 = StringVar()
        self.l_type = Label(self.frame_repair_main, text='Bike Type:', font=FONT)
        self.l_type.place(x=S_W / 1440 * (300 + WIDTH + 150), y=S_H / 900 * 150)
        self.comb_type = ttk.Combobox(self.frame_repair_main, values=list(self.select_biketype()),
                                      textvariable=self.selected_type_3, font=FONT)
        self.comb_type.set("Choose Type")
        self.comb_type.place(x=S_W / 1440 * (300 + WIDTH + 300), y=S_H / 900 * 150, width=WIDTH, height=HEIGHT)

        self.btn_confirm = Button(self.frame_repair_main, text="Fliter", font=FONT,
                                  command=self.show_repair_tabel)
        self.btn_confirm.place(x=S_W / 1440 * (300 + WIDTH), y=S_H / 900 * 200, width=WIDTH, height=HEIGHT)

        self.l_box = Label(self.frame_repair_main, text='List of Information:', font=FONT)
        self.l_box.place(x=S_W / 1440 * 150, y=S_H / 900 * 250)

        self.btn_history = Button(self.frame_repair_main, text="History", font=FONT,
                                  command=self.show_frame_repair_history)
        self.btn_history.place(x=S_W / 1440 * 1120, y=S_H / 900 * 60, width=WIDTH, height=HEIGHT)

    def show_repair_tabel(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        columns = ['No.', 'Bike ID', 'Bike Type', 'Error Type', 'Location']

        self.table = RepairTable(self.frame_repair_main, columns=columns,
                                 comb_location=self.selected_location.get(),
                                 comb_type="Wheel")
                                 #comb_type=self.selected_type_3.get())
        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

    def frepair_history(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_title = Label(self.frame_repair_history, text='REPAIR HISTORY', font=FONT_TITLE)
        self.l_title.place(x=S_W / 1440 * 400, y=S_H / 900 * 100)

        self.current_datetime = datetime.now()
        self.current_date = self.current_datetime.date()
        self.year = list(range(2021, self.current_date.year + 1))
        self.month = list(range(1, 13))
        self.day = list(range(1, 32))

        self.selected_day = StringVar()
        self.selected_month = StringVar()
        self.selected_year = StringVar()
        self.selected_type_4 = StringVar()
        self.l_date = Label(self.frame_repair_history, text='Date:', font=FONT)
        self.l_date.place(x=S_W / 1440 * 150, y=S_H / 900 * 200)
        self.comb_day = ttk.Combobox(self.frame_repair_history, values=self.day,
                                     textvariable=self.selected_day,font=FONT)
        self.comb_day.insert(0, "day")
        self.comb_day.place(x=S_W / 1440 * (150 + 150), y=S_H / 900 * 200, width=WIDTH / 3, height=HEIGHT)
        self.comb_month = ttk.Combobox(self.frame_repair_history, values=self.month,
                                       textvariable=self.selected_month,font=FONT)
        self.comb_month.insert(0, "month")
        self.comb_month.place(x=S_W / 1440 * ((150 + 150) + WIDTH / 3), y=S_H / 900 * 200, width=WIDTH / 3,
                              height=HEIGHT)
        self.comb_year = ttk.Combobox(self.frame_repair_history, values=self.year,
                                      textvariable=self.selected_year,font=FONT)
        self.comb_year.insert(0, "year")
        self.comb_year.place(x=S_W / 1440 * ((150 + 150) + 2 * WIDTH / 3), y=S_H / 900 * 200, width=WIDTH / 3,
                             height=HEIGHT)

        self.l_type = Label(self.frame_repair_history, text='Bike Type:', font=FONT)
        self.l_type.place(x=S_W / 1440 * (300 + WIDTH + 150), y=S_H / 900 * 200)
        self.comb_type = ttk.Combobox(self.frame_repair_history, values=self.select_biketype(),
                                      textvariable=self.selected_type_4,font=FONT)
        self.comb_type.set("Choose Type")
        self.comb_type.place(x=S_W / 1440 * (300 + WIDTH + 300), y=S_H / 900 * 200, width=WIDTH, height=HEIGHT)

        self.btn_confirm = Button(self.frame_repair_history, text="Fliter", font=FONT,
                                  command=self.show_repair_history_tabel)
        self.btn_confirm.place(x=S_W / 1440 * (300 + WIDTH), y=S_H / 900 * 250, width=WIDTH, height=HEIGHT)

        self.l_box = Label(self.frame_repair_history, text='List of Information:', font=FONT)
        self.l_box.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

        self.btn_return = Button(self.frame_repair_history, text="Return", font=FONT,
                                 command=self.show_frame_repair_main)
        self.btn_return.place(x=S_W / 1440 * 150, y=S_H / 900 * 760, width=WIDTH, height=HEIGHT)

    def show_repair_history_tabel(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        columns = ['No.', 'Bike ID', 'Bike Type', 'Error Type', 'Location']

        day=self.selected_day.get()
        month = self.selected_month.get()
        year = self.selected_year.get()
        self.date="{}-{}-{}".format(year,month,day)
        print(self.date)
        print(type(self.date))

        self.table = RepairHistoryTable(self.frame_repair_history, columns=columns,
                                 comb_date=self.date,
                                 comb_type=self.selected_type_4.get())
        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)


class RepairTable(ttk.Treeview, Repair):

    def __init__(self, master, columns, comb_location, comb_type) -> None:
        super().__init__(
            master=master,
            columns=columns,
            show='headings',
            style='Treeview',
        )

        self.cl = comb_location
        self.ct = comb_type
        self.getdata = self.getRepairData()

        style = ttk.Style(master)
        style.configure('Treeview', font=('Arial', 14), rowheight=30)
        style.configure('Treeview.Heading', font=('Arial', 20))

        for column in columns:
            self.heading(column, text=column, anchor=CENTER)
            self.column(column, width=220, anchor=CENTER)

        self.bind("<Double-1>", self.show_window)

        self.datas = self.add_row(self.getdata)

    def getRepairData(self):
        # comb_location, comb_type = super().get_lc_tp()
        repairList = OperatorDatabase()
        repairData = repairList.get_repairData(self.cl, self.ct)
        return repairData

    def add_row(self, datas):
        self.datalist = []
        count = 1
        for data in datas:
            row_data = [count] + list(data)
            self.insert("", END, values=row_data)
            self.datalist.append(row_data)
            count += 1
        return self.datalist

    def show_window(self, event):
        tree = event.widget
        selected_item_id = tree.focus()
        row_index = tree.index(selected_item_id)
        if (selected_item_id):
            record = RepairDetail(*self.datas[row_index])
            record_ui = RepairDetails(record)
            record_ui.show()

class RepairDetail:

    def __init__(self, no=None, BID=None, Btype=None, Errortype=None,
                 Location=None, Time=None) -> None:
        self.no = no
        self.BID = BID
        self.BType = Btype
        self.Errortype = Errortype
        self.Location = Location
        self.Time = Time

class RepairDetails:
    """显示维修记录的界面"""

    def __init__(self, record: RepairDetail) -> None:
        self.record = record

        self.master = Tk()
        self.master.title('Repair Detail')
        self.master.geometry('1440x900')

        self.master.lift()
        self.master.focus_force()

        self.init_ui()

    def confim_repair(self):
        result = messagebox.askyesno("Confirm", "Confirm Repair？")
        if result:  # 如果用户点击了确认按钮
            self.ShowSuccess()
            self.master.destroy()

    def ShowSuccess(self):
        success_window = Tk()
        success_window.title("success window")

        label = Label(success_window, text="Repair Successful !", font=FONT)
        label.place(x=0, y=50)
        success_window.geometry("250x150+575+325")
        # self.show_frame_charge_main()

    def init_ui(self):
        font = ('Arial', 16)
        # create widget

        self.l_title = Label(self.master, text='REPAIR DETAIL', font=FONT_TITLE)
        self.l_title.place(x=450, y=100)

        bid = self.record.BID
        self.l_bikeid = Label(self.master, text="Bike ID: ", font=FONT)
        self.l_bikeid.place(x=500, y=200)
        self.l_bid = Label(self.master, text=bid, font=FONT)
        self.l_bid.place(x=(500 + 200), y=200)

        btype = self.record.BType
        self.l_biketype = Label(self.master, text='Bike Type:', font=FONT)
        self.l_biketype.place(x=500, y=300)
        self.l_btype = Label(self.master, text=btype, font=FONT)
        self.l_btype.place(x=(500 + 200), y=300)

        berror = self.record.Errortype
        self.l_errortype = Label(self.master, text='Error Type:', font=FONT)
        self.l_errortype.place(x=500, y=400)
        self.l_etype = Label(self.master, text=berror, font=FONT)
        self.l_etype.place(x=(500 + 200), y=400)

        location = self.record.Location
        self.l_Location = Label(self.master, text='Location:', font=FONT)
        self.l_Location.place(x=500, y=500)
        self.l_Location = Label(self.master, text=location, font=FONT)
        self.l_Location.place(x=(500 + 200), y=500)

        time = self.record.Time
        self.l_time = Label(self.master, text='Time:', font=FONT)
        self.l_time.place(x=500, y=600)
        self.l_time = Label(self.master, text=time, font=FONT)
        self.l_time.place(x=(500 + 200), y=600)

        # self.l_picture = Label(self.master, text='Picture:', font=FONT)
        # self.l_picture.place(x=500, y=500)
        # self.test = PhotoImage(file="pic.png")

        # self.lp = Label(self.master, image=self.test)
        # self.lp.place(x=(500 + 200), y=500, width=200, height=150)
        # self.lp["bg"] = "black"

        self.btn_return = Button(self.master, text="Return", font=FONT,
                                 command=self.master.destroy)
        self.btn_return.place(x=400, y=700, width=WIDTH, height=HEIGHT)

        self.btn_confirm = Button(self.master, text="Confirm", font=FONT,
                                  command=self.confim_repair)
        self.btn_confirm.place(x=750, y=700, width=WIDTH, height=HEIGHT)

    def show(self):
        self.master.mainloop()

# 没有实现的confirm。。。。。！！！！！！！！！！！！！！！！/////////////////

# class RRepairDetails:
#     def __init__(self, record: RepairDetail) -> None:
#
#         self.record = record
#
#         self.master = Tk()
#         self.master.title('Repair Detail')
#         self.master.geometry('1440x900')
#
#         # create frames
#         self.frame_repair_details = Frame(self.master, width=1440, height=900)
#         self.frame_repair_confirm = Frame(self.master, width=1440, height=900)
#         self.frames = [self.frame_repair_details, self.frame_repair_confirm]
#
#         self.init_frame()
#         self.frame_repair_details()
#
#     def forget_all(self):
#         for frame in self.frames:
#             frame.pack_forget()
#
#     def show_frame_repair_details(self):
#         self.forget_all()
#         self.frame_repair_details.pack()
#
#     def show_frame_repair_confirm(self):
#         self.forget_all()
#         self.frame_repair_confirm.pack()
#
#     def init_frame(self):
#         self.frepair_details()
#         self.frepair_confirm()
#
#     def frepair_details(self):
#         self.l_title = Label(self.master, text='REPAIR DETAIL', font=FONT_TITLE)
#         self.l_title.place(x=450, y=100)
#
#         bid = self.record.BID
#         self.l_bikeid = Label(self.master, text="Bike ID: ", font=FONT)
#         self.l_bikeid.place(x=500, y=200)
#         self.l_bid = Label(self.master, text=bid, font=FONT)
#         self.l_bid.place(x=(500 + 200), y=200)
#
#         btype = self.record.BType
#         self.l_biketype = Label(self.master, text='Bike Type:', font=FONT)
#         self.l_biketype.place(x=500, y=300)
#         self.l_btype = Label(self.master, text=btype, font=FONT)
#         self.l_btype.place(x=(500 + 200), y=300)
#
#         berror = self.record.Errortype
#         self.l_errortype = Label(self.master, text='Error Type:', font=FONT)
#         self.l_errortype.place(x=500, y=400)
#         self.l_etype = Label(self.master, text=berror, font=FONT)
#         self.l_etype.place(x=(500 + 200), y=400)
#
#         location = self.record.Location
#         self.l_Location = Label(self.master, text='Location:', font=FONT)
#         self.l_Location.place(x=500, y=500)
#         self.l_Location = Label(self.master, text=location, font=FONT)
#         self.l_Location.place(x=(500 + 200), y=500)
#
#         time = self.record.Time
#         self.l_time = Label(self.master, text='Time:', font=FONT)
#         self.l_time.place(x=500, y=600)
#         self.l_time = Label(self.master, text=time, font=FONT)
#         self.l_time.place(x=(500 + 200), y=600)
#
#         # self.l_picture = Label(self.master, text='Picture:', font=FONT)
#         # self.l_picture.place(x=500, y=500)
#         # self.test = PhotoImage(file="pic.png")
#
#         # self.lp = Label(self.master, image=self.test)
#         # self.lp.place(x=(500 + 200), y=500, width=200, height=150)
#         # self.lp["bg"] = "black"
#
#         self.btn_return = Button(self.master, text="Return", font=FONT,
#                                  command=self.master.destroy)
#         self.btn_return.place(x=400, y=700, width=WIDTH, height=HEIGHT)
#
#         self.btn_confirm = Button(self.master, text="Confirm", font=FONT,
#                                   command=self.show_frame_repair_confirm)
#         self.btn_confirm.place(x=750, y=700, width=WIDTH, height=HEIGHT)
#
#     def confim_repair(self):
#         result = messagebox.askyesno("Confirm", "Confirm Repair？")
#         if result:  # 如果用户点击了确认按钮
#             self.ShowSuccess()
#             self.master.destroy()
#
#     def ShowSuccess(self):
#         success_window = Tk()
#         success_window.title("success window")
#         label = Label(success_window, text="Repair Successful !", font=FONT)
#         label.place(x=0, y=50)
#         success_window.geometry("250x150+575+325")
#
#     def frepair_confirm(self):
#         self.l_title = Label(self.frame_repair_confirm, text='CONFIRM REPAIR', font=FONT_TITLE)
#         self.l_title.place(x=400, y=100)
#
#         self.l_operatorid = Label(self.frame_repair_confirm, text='Operator ID:', font=FONT)
#         self.l_operatorid.place(x=500, y=250)
#         self.l_oid = Label(self.frame_repair_confirm, text='1111', font=FONT)
#         self.l_oid.place(x=(500 + 200), y=250)
#
#         bid = self.record.BID
#         self.l_bikeid = Label(self.frame_repair_confirm, text='Bike ID:', font=FONT)
#         self.l_bikeid.place(x=500, y=350)
#         self.l_bid = Label(self.frame_repair_confirm, text=bid, font=FONT)
#         self.l_bid.place(x=(500 + 200), y=350)
#
#         lcation = self.record.Location
#         self.l_location = Label(self.frame_repair_confirm, text='Location:', font=FONT)
#         self.l_location.place(x=500, y=450)
#         self.l_location = Label(self.frame_repair_confirm, text=lcation, font=FONT)
#         self.l_location.place(x=(500 + 200), y=450)
#
#         time = self.record.Time
#         self.l_date = Label(self.frame_repair_confirm, text='Date:', font=FONT)
#         self.l_date.place(x=500, y=550)
#         self.l_date = Label(self.frame_repair_confirm, text=time)
#         self.l_date.place(x=(500 + 200), y=550, width=WIDTH, height=HEIGHT)
#
#         # 现在先用button实现进入detail界面功能，以后通过每一条具体信息进入detail界面
#         self.btn_return = Button(self.frame_repair_confirm, text="Return", font=FONT,
#                                  command=self.show_frame_repair_details)
#         self.btn_return.place(x=400, y=700, width=WIDTH, height=HEIGHT)
#
#         self.btn_return = Button(self.frame_repair_confirm, text="Confirm", font=FONT,
#                                  command=self.confim_repair)
#         self.btn_return.place(x=750, y=700, width=WIDTH, height=HEIGHT)

class RepairHistoryTable(ttk.Treeview, Repair):

    def __init__(self, master, columns,comb_date, comb_type) -> None:
        super().__init__(
            master=master,
            columns=columns,
            show='headings',
            style='Treeview',
        )

        self.cd = comb_date
        self.ct = comb_type
        self.getdata = self.getRepairHistoryData()

        style = ttk.Style(master)
        style.configure('Treeview', font=('Arial', 14), rowheight=30)
        style.configure('Treeview.Heading', font=('Arial', 20))

        for column in columns:
            self.heading(column, text=column, anchor=CENTER)
            self.column(column, width=220, anchor=CENTER)

        self.bind("<Double-1>", self.show_window)
        self.datas = self.add_row(self.getdata)

    def getRepairHistoryData(self):
        # comb_location, comb_type = super().get_lc_tp()
        repairhistoryList = OperatorDatabase()
        repair_Hist_Data = repairhistoryList.get_repairHistory(self.cd, self.ct)
        return repair_Hist_Data

    def add_row(self, datas):
        self.datalist = []
        count = 1
        for data in datas:
            row_data = [count] + list(data)
            self.insert("", END, values=row_data)
            self.datalist.append(row_data)
            count += 1
        return self.datalist

    def show_window(self, event):
        # 获取 Treeview 实例
        tree = event.widget
        # 获取当前选中项的ID
        selected_item_id = tree.focus()
        # 获取该项的索引，即第几行
        row_index = tree.index(selected_item_id)
        if (selected_item_id):
            record = RepairDetail(*self.datas[row_index])
            record_ui = RepairHistoryDetails(record)
            record_ui.show()

# class RepairHistoryDetail:
#
#     def __init__(self, no=None, BID=None, Btype=None, Errortype=None,
#                  Location=None, Time=None) -> None:
#         self.no = no
#         self.BID = BID
#         self.BType = Btype
#         self.Errortype = Errortype
#         self.Location = Location
#         self.Time = Time

class RepairHistoryDetails:
    """显示维修记录的界面"""

    def __init__(self, record: RepairDetail) -> None:
        self.record = record

        self.master = Tk()
        self.master.title('Repair Detail')
        self.master.geometry('1440x900')

        self.init_ui()

    def init_ui(self):
        font = ('Arial', 16)
        # create widget

        self.l_title = Label(self.master, text='REPAIR DETAIL', font=FONT_TITLE)
        self.l_title.place(x=450, y=100)

        bid = self.record.BID
        self.l_bikeid = Label(self.master, text="Bike ID: ", font=FONT)
        self.l_bikeid.place(x=500, y=200)
        self.l_bid = Label(self.master, text=bid, font=FONT)
        self.l_bid.place(x=(500 + 200), y=200)

        btype = self.record.BType
        self.l_biketype = Label(self.master, text='Bike Type:', font=FONT)
        self.l_biketype.place(x=500, y=300)
        self.l_btype = Label(self.master, text=btype, font=FONT)
        self.l_btype.place(x=(500 + 200), y=300)

        berror = self.record.Errortype
        self.l_errortype = Label(self.master, text='Error Type:', font=FONT)
        self.l_errortype.place(x=500, y=400)
        self.l_etype = Label(self.master, text=berror, font=FONT)
        self.l_etype.place(x=(500 + 200), y=400)

        location = self.record.Location
        self.l_Location = Label(self.master, text='Location:', font=FONT)
        self.l_Location.place(x=500, y=500)
        self.l_Location = Label(self.master, text=location, font=FONT)
        self.l_Location.place(x=(500 + 200), y=500)

        time = self.record.Time
        self.l_time = Label(self.master, text='Time:', font=FONT)
        self.l_time.place(x=500, y=600)
        self.l_time = Label(self.master, text=time, font=FONT)
        self.l_time.place(x=(500 + 200), y=600)

        # self.l_picture = Label(self.master, text='Picture:', font=FONT)
        # self.l_picture.place(x=500, y=500)
        # self.test = PhotoImage(file="pic.png")

        # self.lp = Label(self.master, image=self.test)
        # self.lp.place(x=(500 + 200), y=500, width=200, height=150)
        # self.lp["bg"] = "black"

        self.btn_return = Button(self.master, text="Return", font=FONT,
                                 command=self.master.destroy)
        self.btn_return.place(x=570, y=700, width=WIDTH, height=HEIGHT)

    def show(self):
        self.master.mainloop()


class Move:
    def __init__(self, master) -> None:
        self.master = master

        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()

        # create frames
        self.frame_move_main = Frame(self.master, width=S_W, height=S_H)
        # self.frame_move_detail = Frame(self.master, width=S_W, height=S_H)
        # self.frame_repair_detail_his = Frame(self.master, width=S_W, height=S_H)
        self.frame_move_confirm = Frame(self.master, width=S_W, height=S_H)
        self.frame_move_history = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_move_main, self.frame_move_confirm, self.frame_move_history]

        self.init_frame()
        self.show_frame_move_main()

    def init_frame(self):
        self.fmove_main()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def show_frame_move_main(self):
        self.forget_all()
        self.frame_move_main.pack()

    # def show_frame_move_detail(self):
    #     self.forget_all()
    #     self.frame_move_detail.pack()

    def show_frame_move_confirm(self):
        self.forget_all()
        self.frame_move_confirm.pack()

    def show_frame_move_history(self):
        self.forget_all()
        self.frame_move_history.pack()

    def confim_move(self):
        result = messagebox.askyesno("Confirm", "Confirm Move？")
        if result:  # 如果用户点击了确认按钮
            self.ShowSuccess()

    def ShowSuccess(self):
        success_window = Tk()
        success_window.title("success window")
        label = Label(success_window, text="Move Successful !", font=FONT)
        label.place(x=0, y=50)
        success_window.geometry("250x150+575+325")
        self.show_frame_move_main()

    def init_frame(self):
        self.fmove_main()
        # self.fmove_detail()
        self.fmove_confirm()
        self.fmove_history()

    def open_database(self):
        conn = sqlite3.connect("RIDENOW.db")
        self.c = conn.cursor()

    def select_location(self):
        self.open_database()
        self.c.execute("""SELECT name FROM Parking_lot""")
        parking_location = self.c.fetchall()
        return parking_location

    def fmove_main(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_location = Label(self.frame_move_main, text='Location:', font=FONT)
        self.l_location.place(x=S_W / 1440 * 150, y=S_H / 900 * 150)
        self.comb_location = ttk.Combobox(self.frame_move_main, values=self.select_location(), font=FONT)
        self.comb_location.place(x=S_W / 1440 * (150 + 150), y=S_H / 900 * 150, width=WIDTH, height=HEIGHT)

        self.l_type = Label(self.frame_move_main, text='Bike Type:', font=FONT)
        self.l_type.place(x=S_W / 1440 * (300 + WIDTH + 150), y=S_H / 900 * 150)
        self.comb_type = ttk.Combobox(self.frame_move_main, values=["Electric Bike", "Foot Bike"], font=FONT)
        self.comb_type.place(x=S_W / 1440 * (300 + WIDTH + 300), y=S_H / 900 * 150, width=WIDTH, height=HEIGHT)

        self.l_box = Label(self.frame_move_main, text='List of Information:', font=FONT)
        self.l_box.place(x=S_W / 1440 * 150, y=S_H / 900 * 250)
        columns = ['No.', 'Bike ID', 'Bike Type', 'Location']
        self.table = MoveTable(self.frame_move_main, columns=columns)
        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

        self.btn_history = Button(self.frame_move_main, text="History", font=FONT,
                                  command=self.show_frame_move_history)
        self.btn_history.place(x=S_W / 1440 * 1120, y=S_H / 900 * 60, width=WIDTH, height=HEIGHT)

    # def fmove_detail(self):
    #     S_W = self.master.winfo_screenwidth()
    #     S_H = self.master.winfo_screenheight()
    #
    #     self.l_title = Label(self.frame_move_detail, text='MOVE DETAIL', font=FONT_TITLE)
    #     self.l_title.place(x=S_W/1440*450, y=S_H/900*100)
    #
    #     self.l_type = Label(self.frame_move_detail, text='Bike Type:', font=FONT)
    #     self.l_type.place(x=S_W/1440*400, y=S_H/900*220)
    #     self.comb_type = ttk.Combobox(self.frame_move_detail,values = ["Electric Bike", "Foot Bike"],font=FONT)
    #     self.comb_type.place(x=S_W/1440*(400+200), y=S_H/900*220, width=WIDTH, height=HEIGHT)
    #
    #     self.l_locationid= Label(self.frame_move_detail, text='Location ID:', font=FONT)
    #     self.l_locationid.place(x=S_W/1440*400, y=S_H/900*320)
    #     self.l_lid = Label(self.frame_move_detail, text='1111', font=FONT)
    #     self.l_lid.place(x=S_W/1440*(400 + 200), y=S_H/900*320)
    #
    #     self.l_box = Label(self.frame_move_detail, text='List of Information:',font=FONT)
    #     self.l_box.place(x=S_W/1440*150, y=S_H/900*350)
    #     self.listbox = Listbox(self.frame_move_detail)
    #     self.listbox.place(x=S_W/1440*150, y=S_H/900*400, width=1100, height=300)
    #
    #     self.btn_return = Button(self.frame_move_detail, text="Return", font=FONT,
    #                              command=self.show_frame_move_main)
    #     self.btn_return.place(x=S_W/1440*400, y=S_H/900*700, width=WIDTH, height=HEIGHT)
    #
    #     self.btn_confirm = Button(self.frame_move_detail, text="Confirm", font=FONT,
    #                               command=self.show_frame_move_confirm)
    #     self.btn_confirm.place(x=S_W/1440*750, y=S_H/900*700, width=WIDTH, height=HEIGHT)

    def fmove_confirm(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_title = Label(self.frame_move_confirm, text='CONFIRM REPAIR', font=FONT_TITLE)
        self.l_title.place(x=S_W / 1440 * 400, y=S_H / 900 * 100)

        self.l_operatorid = Label(self.frame_move_confirm, text='Operator ID:', font=FONT)
        self.l_operatorid.place(x=S_W / 1440 * 300, y=S_H / 900 * 250)
        self.l_oid = Label(self.frame_move_confirm, text='11111', font=FONT)
        self.l_oid.place(x=S_W / 1440 * (300 + 200), y=S_H / 900 * 250)

        self.l_from = Label(self.frame_move_confirm, text='From:', font=FONT)
        self.l_from.place(x=S_W / 1440 * 300, y=S_H / 900 * 350)
        self.comb_from = ttk.Combobox(self.frame_move_confirm)
        self.comb_from.place(x=S_W / 1440 * (300 + 200), y=S_H / 900 * 350, width=WIDTH, height=HEIGHT)

        self.to = Label(self.frame_move_confirm, text='To:', font=FONT)
        self.to.place(x=S_W / 1440 * 850, y=S_H / 900 * 350)
        self.to = ttk.Combobox(self.frame_move_confirm)
        self.to.place(x=S_W / 1440 * (850 + 120), y=S_H / 900 * 350, width=WIDTH, height=HEIGHT)

        self.l_date = Label(self.frame_move_confirm, text='Date:', font=FONT)
        self.l_date.place(x=S_W / 1440 * 300, y=S_H / 900 * 450)
        self.l_date = Label(self.frame_move_confirm, text=datetime.now(), font=FONT)
        self.l_date.place(x=S_W / 1440 * (300 + 200), y=S_H / 900 * 450)

        # 现在先用button实现进入detail界面功能，以后通过每一条具体信息进入detail界面
        self.btn_return = Button(self.frame_move_confirm, text="Return", font=FONT,
                                 command=self.show_frame_move_main)
        self.btn_return.place(x=S_W / 1440 * 400, y=S_H / 900 * 600, width=WIDTH, height=HEIGHT)

        self.btn_return = Button(self.frame_move_confirm, text="Confirm", font=FONT,
                                 command=self.confim_move)
        self.btn_return.place(x=S_W / 1440 * 750, y=S_H / 900 * 600, width=WIDTH, height=HEIGHT)

    def fmove_history(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.current_datetime = datetime.now()
        self.current_date = self.current_datetime.date()
        self.year = list(range(2021, self.current_date.year + 1))
        self.month = list(range(1, 13))
        self.day = list(range(1, 32))

        self.l_title = Label(self.frame_move_history, text='MOVE HISTORY', font=FONT_TITLE)
        self.l_title.place(x=S_W / 1440 * 400, y=S_H / 900 * 100)

        self.l_date = Label(self.frame_move_history, text='Date:', font=FONT)
        self.l_date.place(x=S_W / 1440 * 150, y=S_H / 900 * 200)
        self.comb_day = ttk.Combobox(self.frame_move_history, values=self.day, font=FONT)
        self.comb_day.insert(0, "day")
        self.comb_day.place(x=S_W / 1440 * (150 + 150), y=S_H / 900 * 200, width=WIDTH / 3, height=HEIGHT)
        self.comb_month = ttk.Combobox(self.frame_move_history, values=self.month, font=FONT)
        self.comb_month.insert(0, "month")
        self.comb_month.place(x=S_W / 1440 * (150 + 150) + WIDTH / 3, y=S_H / 900 * 200, width=WIDTH / 3, height=HEIGHT)
        self.comb_year = ttk.Combobox(self.frame_move_history, values=self.year, font=FONT)
        self.comb_year.insert(0, "year")
        self.comb_year.place(x=S_W / 1440 * (150 + 150) + 2 * WIDTH / 3, y=S_H / 900 * 200, width=WIDTH / 3,
                             height=HEIGHT)

        self.l_type = Label(self.frame_move_history, text='Bike Type:', font=FONT)
        self.l_type.place(x=S_W / 1440 * 300 + WIDTH + 150, y=S_H / 900 * 200)
        self.comb_type = ttk.Combobox(self.frame_move_history, values=["Electric Bike", "Foot Bike"], font=FONT)
        self.comb_type.place(x=S_W / 1440 * 300 + WIDTH + 300, y=S_H / 900 * 200, width=WIDTH, height=HEIGHT)

        self.l_box = Label(self.frame_move_history, text='List of Information:', font=FONT)
        self.l_box.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)
        # self.listbox = Listbox(self.frame_move_history)
        # self.listbox.place(x=S_W/1440*150, y=S_H/900*350, width=1100, height=400)
        columns = ['No.', 'Bike ID', 'Bike Type', 'current location', 'original location']
        self.table = MoveHistoryTable(self.frame_move_history, columns=columns)
        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

        self.btn_return = Button(self.frame_move_history, text="Return", font=FONT,
                                 command=self.show_frame_move_main)
        self.btn_return.place(x=S_W / 1440 * 150, y=S_H / 900 * 760, width=WIDTH, height=HEIGHT)


class MoveTable(ttk.Treeview):

    def __init__(self, master, columns) -> None:
        super().__init__(
            master=master,
            columns=columns,
            show='headings',
            style='Treeview',
        )
        style = ttk.Style(master)
        style.configure('Treeview', font=('Arial', 14), rowheight=30)
        style.configure('Treeview.Heading', font=('Arial', 20))

        for column in columns:
            self.heading(column, text=column, anchor=CENTER)
            self.column(column, width=220, anchor=CENTER)

        self.bind("<Double-1>", self.show_window)

        self.datas = []  # 保存表中的数据
        self.add_row(['1', '1002', 'type1', "Main Building", "time"])
        self.add_row(['2', '1002', 'type1', "Main Building", "time"])
        self.add_row(['3', '1002', 'type1', "Main Building", "time"])
        self.add_row(['4', '1002', 'type1', "Main Building", "time"])
        self.add_row(['5', '1002', 'type1', "Main Building", "time"])
        self.add_row(['6', '1002', 'type1', "Main Building", "time"])
        self.add_row(['7', '1002', 'type1', "Main Building", "time"])
        self.add_row(['8', '1002', 'type1', "Main Building", "time"])
        self.add_row(['9', '1002', 'type1', "Main Building", "time"])
        self.add_row(['10', '1002', 'type1', "Main Building", "time"])
        self.add_row(['11', '1002', 'type1', "Main Building", "time"])
        self.add_row(['12', '1002', 'type1', "Main Building", "time"])
        self.add_row(['13', '1002', 'type1', "Main Building", "time"])

    def add_row(self, row):
        self.insert("", END, values=row)
        self.datas.append(row)

    def show_window(self, event):
        # 获取 Treeview 实例
        tree = event.widget
        # 获取当前选中项的ID
        selected_item_id = tree.focus()
        # 获取该项的索引，即第几行
        row_index = tree.index(selected_item_id)
        if (selected_item_id):
            record = MoveDetail(*self.datas[row_index])
            record_ui = MoveDetails(record)
            record_ui.show()


class MoveDetail:

    def __init__(self, no=None, BID=None, Btype=None, Battery=None,
                 Location=None, Time=None) -> None:
        self.no = no
        self.BID = BID
        self.BType = Btype
        # self.Battery = Battery
        self.Location = Location
        self.Time = Time


class MoveDetails:
    """显示维修记录的界面"""

    def confim_move(self):
        result = messagebox.askyesno("Confirm", "Confirm Move？")
        if result:  # 如果用户点击了确认按钮
            self.ShowSuccess()

    def ShowSuccess(self):
        success_window = Tk()
        success_window.title("success window")
        label = Label(success_window, text="Move Successful !", font=FONT)
        label.place(x=0, y=50)
        success_window.geometry("250x150+575+325")
        self.show_frame_move_main()

    def __init__(self, record: MoveDetail) -> None:
        self.record = record

        self.master = Tk()
        self.master.title('Move Detail')
        self.master.geometry('600x400+400+200')

        self.init_ui()

    def init_ui(self):
        font = ('Arial', 16)
        # create widget
        self.l_title = Label(self.master, text='Move Record', font=FONT)
        self.l_title.place(x=220, y=20)

        self.l_bike_id = Label(self.master, text='Bike ID:', font=font)
        self.l_bike_id.place(x=80, y=70)
        self.e_bike_id = Entry(self.master, font=font)
        self.e_bike_id.insert(0, self.record.BID)
        self.e_bike_id.configure(state='readonly')
        self.e_bike_id.place(x=200, y=70, width=300)

        self.l_bike_type = Label(self.master, text='Bike type:', font=font)
        self.l_bike_type.place(x=80, y=120)
        self.e_bike_type = Entry(self.master, font=font)
        self.e_bike_type.insert(0, self.record.BType)
        self.e_bike_type.configure(state='readonly')
        self.e_bike_type.place(x=200, y=120, width=300)

        # self.l_battery = Label(self.master, text='Battery:', font=font)
        # self.l_battery.place(x=80, y=170)
        # self.e_battery = Entry(self.master, font=font)
        # self.e_battery.insert(0, self.record.Battery)
        # self.e_battery.configure(state='readonly')
        # self.e_battery.place(x=200, y=170,width=300)

        self.l_location = Label(self.master, text='Location:', font=font)
        self.l_location.place(x=80, y=170)
        self.e_location = Entry(self.master, font=font)
        self.e_location.insert(0, self.record.Location)
        self.e_location.configure(state='readonly')
        self.e_location.place(x=200, y=170, width=300)

        self.l_moveto = Label(self.master, text='Move To:', font=font)
        self.l_moveto.place(x=80, y=220)
        self.c_moveto = ttk.Combobox(self.master, font=font)
        # self.e_location.insert(0, self.record.Location)
        # self.e_location.configure(state='readonly')
        self.c_moveto.place(x=200, y=220, width=300)

        self.l_time = Label(self.master, text='time:', font=font)
        self.l_time.place(x=80, y=270)
        self.e_time = Entry(self.master, font=font)
        self.e_time.insert(0, datetime.now())
        self.e_time.configure(state='readonly')
        self.e_time.place(x=200, y=270, width=300)

        self.btn_return = Button(self.master, text='Return', font=font,
                                 command=self.master.destroy)
        self.btn_return.place(x=100, y=330, height=50, width=150)

        self.btn_move = Button(self.master, text='Move', font=font,
                               command=self.confim_move)
        self.btn_move.place(x=350, y=330, height=50, width=150)

    def show(self):
        self.master.mainloop()


class MoveHistoryTable(ttk.Treeview):
    def __init__(self, master, columns) -> None:
        super().__init__(
            master=master,
            columns=columns,
            show='headings',
            style='Treeview',
        )
        style = ttk.Style(master)
        style.configure('Treeview', font=('Arial', 14), rowheight=30)
        style.configure('Treeview.Heading', font=('Arial', 20))

        for column in columns:
            self.heading(column, text=column, anchor=CENTER)
            self.column(column, width=220, anchor=CENTER)

        self.bind("<Double-1>", self.show_window)

        self.datas = []  # 保存表中的数据
        self.add_row(['1', 'h1002', 'type1', "learninghub", "Main Building", "operator1"])
        self.add_row(['2', 'h1002', 'type1', "learninghub", "Main Building", "operator1"])
        self.add_row(['3', 'h1002', 'type1', "learninghub", "Main Building", "operator1"])
        self.add_row(['4', 'h1002', 'type1', "learninghub", "Main Building", "operator1"])
        self.add_row(['5', 'h1002', 'type1', "learninghub", "Main Building", "operator1"])
        self.add_row(['6', 'h1002', 'type1', "learninghub", "Main Building", "operator1"])
        self.add_row(['7', 'h1002', 'type1', "learninghub", "Main Building", "operator1"])
        self.add_row(['8', 'h1002', 'type1', "learninghub", "Main Building", "operator1"])
        self.add_row(['9', 'h1002', 'type1', "learninghub", "Main Building", "operator1"])
        self.add_row(['10', 'h1002', 'type1', "learninghub", "Main Building", "operator1"])
        self.add_row(['11', 'h1002', 'type1', "learninghub", "Main Building", "operator1"])
        self.add_row(['12', 'h1002', 'type1', "learninghub", "Main Building", "operator1"])
        self.add_row(['13', 'h1002', 'type1', "learninghub", "Main Building", "operator1"])

    def add_row(self, row):
        self.insert("", END, values=row)
        self.datas.append(row)

    def show_window(self, event):
        # 获取 Treeview 实例
        tree = event.widget
        # 获取当前选中项的ID
        selected_item_id = tree.focus()
        # 获取该项的索引，即第几行
        row_index = tree.index(selected_item_id)
        if (selected_item_id):
            record = MoveHistoryDetail(*self.datas[row_index])
            record_ui = MoveHistoryDetails(record)
            record_ui.show()


class MoveHistoryDetail:

    def __init__(self, no=None, BID=None, Btype=None, Time=None,
                 Location=None, Operator=None) -> None:
        self.no = no
        self.BID = BID
        self.BType = Btype
        self.Time = Time
        self.Location = Location
        self.Operator = Operator


class MoveHistoryDetails:
    """显示维修记录的界面"""

    def __init__(self, record: MoveHistoryDetail) -> None:
        self.record = record

        self.master = Tk()
        self.master.title('Move History Detail')
        self.master.geometry('600x400+400+200')

        self.init_ui()

    def init_ui(self):
        font = ('Arial', 16)
        # create widget
        self.l_title = Label(self.master, text='Move Record', font=FONT)
        self.l_title.place(x=220, y=20)

        self.l_bike_id = Label(self.master, text='Bike ID:', font=font)
        self.l_bike_id.place(x=60, y=70)
        self.e_bike_id = Entry(self.master, font=font)
        self.e_bike_id.insert(0, self.record.BID)
        self.e_bike_id.configure(state='readonly')
        self.e_bike_id.place(x=220, y=70, width=300)

        self.l_bike_type = Label(self.master, text='Bike type:', font=font)
        self.l_bike_type.place(x=60, y=120)
        self.e_bike_type = Entry(self.master, font=font)
        self.e_bike_type.insert(0, self.record.BType)
        self.e_bike_type.configure(state='readonly')
        self.e_bike_type.place(x=220, y=120, width=300)

        self.l_battery = Label(self.master, text='current location:', font=font)
        self.l_battery.place(x=60, y=170)
        self.e_battery = Entry(self.master, font=font)
        self.e_battery.insert(0, self.record.Time)
        self.e_battery.configure(state='readonly')
        self.e_battery.place(x=220, y=170, width=300)

        self.l_location = Label(self.master, text='original location:', font=font)
        self.l_location.place(x=60, y=220)
        self.e_location = Entry(self.master, font=font)
        self.e_location.insert(0, self.record.Location)
        self.e_location.configure(state='readonly')
        self.e_location.place(x=220, y=220, width=300)

        self.l_time = Label(self.master, text='Operator ID:', font=font)
        self.l_time.place(x=60, y=270)
        self.e_time = Entry(self.master, font=font)
        self.e_time.insert(0, self.record.Operator)
        self.e_time.configure(state='readonly')
        self.e_time.place(x=220, y=270, width=300)

        self.btn_return = Button(self.master, text='Return', font=font,
                                 command=self.master.destroy)
        self.btn_return.place(x=200, y=330, height=50, width=200)

    def show(self):
        self.master.mainloop()


class My:
    def __init__(self, master) -> None:
        self.master = master
        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()

        # create frames
        self.frame_my_main = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_my_main]

        self.init_frame()
        self.show_frame_my_main()

    def init_frame(self):
        self.fmy_main()

    def show_frame_my_confirm(self):
        self.forget_all()
        self.frame_my_main.pack()

    def show_frame_my_main(self):
        self.forget_all()
        self.frame_my_main.pack()

    def edit_username(self):
        self.entry_username.delete(0, END)
        self.entry_username.focus()

    def edit_password(self):
        self.entry_password.delete(0, END)
        self.entry_password.focus()

    def edit_email(self):
        self.entry_email.delete(0, END)
        self.entry_email.focus()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def fmy_main(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.l_title = Label(self.frame_my_main, text='MY ACCOUNT', font=FONT_TITLE)
        self.l_title.place(x=S_W / 1440 * 400, y=S_H / 900 * 100)

        self.l_operatorid = Label(self.frame_my_main, text='Operator ID:', font=FONT)
        self.l_operatorid.place(x=S_W / 1440 * 400, y=S_H / 900 * 300)
        self.l_oid = Label(self.frame_my_main, text='XXXX', font=FONT)
        self.l_oid.place(x=S_W / 1440 * (400 + 200), y=S_H / 900 * 300)

        self.l_username = Label(self.frame_my_main, text='Username:', font=FONT)
        self.l_username.place(x=S_W / 1440 * 400, y=S_H / 900 * 400)
        self.entry_username = Entry(self.frame_my_main)
        self.entry_username.place(x=S_W / 1440 * (400 + 200), y=S_H / 900 * 400, width=WIDTH, height=HEIGHT)

        self.l_password = Label(self.frame_my_main, text='Password:', font=FONT)
        self.l_password.place(x=S_W / 1440 * 400, y=S_H / 900 * 500)
        self.entry_password = Entry(self.frame_my_main)
        self.entry_password.place(x=S_W / 1440 * (400 + 200), y=S_H / 900 * 500, width=WIDTH, height=HEIGHT)

        self.l_email = Label(self.frame_my_main, text='Email:', font=FONT)
        self.l_email.place(x=S_W / 1440 * 400, y=S_H / 900 * 600)
        self.entry_email = Entry(self.frame_my_main)
        self.entry_email.place(x=S_W / 1440 * (400 + 200), y=S_H / 900 * 600, width=WIDTH, height=HEIGHT)

        self.btn_edit_username = Button(self.frame_my_main, text="Edit", font=FONT,
                                        command=self.edit_username)
        self.btn_edit_username.place(x=S_W / 1440 * 950, y=S_H / 900 * 400, width=100, height=50)

        self.btn_edit_password = Button(self.frame_my_main, text="Edit", font=FONT,
                                        command=self.edit_password)
        self.btn_edit_password.place(x=S_W / 1440 * 950, y=S_H / 900 * 500, width=100, height=50)

        self.btn_edit_email = Button(self.frame_my_main, text="Edit", font=FONT,
                                     command=self.edit_email)
        self.btn_edit_email.place(x=S_W / 1440 * 950, y=S_H / 900 * 600, width=100, height=50)


class OperatorUI:

    def __init__(self) -> None:

        self.master = Tk()
        self.master.title("Operator")
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.master.geometry(f"{S_W}x{S_H}")
        self.font = ('Arial', 14)

        # create frames
        self.frame_track = Frame(self.master, width=S_W, height=S_H)
        self.frame_charge = Frame(self.master, width=S_W, height=S_H)
        self.frame_repair = Frame(self.master, width=S_W, height=S_H)
        self.frame_move = Frame(self.master, width=S_W, height=S_H)
        self.frame_my = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_track, self.frame_charge, self.frame_repair, self.frame_move, self.frame_my]

        self.btn_track = Button(self.master, text='Track',
                                command=self.show_frame_track, font=FONT_TOP)
        self.btn_track.place(x=0, y=0, width=S_W / 5., height=HEIGHT)

        self.btn_charge = Button(self.master, text='Charge',
                                 command=self.show_frame_charge, font=FONT_TOP)
        self.btn_charge.place(x=S_W / 5, y=0, width=S_W / 5., height=HEIGHT)
        self.btn_repair = Button(self.master, text='Repair',
                                 command=self.show_frame_repair, font=FONT_TOP)
        self.btn_repair.place(x=S_W / 5 * 2, y=0, width=S_W / 5., height=HEIGHT)
        self.btn_move = Button(self.master, text='Move',
                               command=self.show_frame_move, font=FONT_TOP)
        self.btn_move.place(x=S_W / 5 * 3, y=0, width=S_W / 5., height=HEIGHT)
        self.btn_my = Button(self.master, text='My',
                             command=self.show_frame_my, font=FONT_TOP)
        self.btn_my.place(x=S_W / 5 * 4, y=0, width=S_W / 5., height=HEIGHT)
        self.btns = [self.btn_track, self.btn_charge, self.btn_repair, self.btn_move, self.btn_my]

        # init frame
        # self.track = Track(self.frame_track)
        self.charge = Charge(self.frame_charge)
        self.repair = Repair(self.frame_repair)
        self.move = Move(self.frame_move)
        self.my = My(self.frame_my)
        #
        self.show_frame_charge()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def reset_btn_bg(self):
        for btn in self.btns:
            btn.configure(bg='SystemButtonFace')

    def show_frame_track(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_track.configure(bg='red')
        self.frame_track.pack()

    def show_frame_charge(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_charge.configure(bg='red')
        self.frame_charge.pack()

    def show_frame_repair(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_repair.configure(bg='red')
        self.frame_repair.pack()

    def show_frame_move(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_move.configure(bg='red')
        self.frame_move.pack()

    def show_frame_my(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_my.configure(bg='red')
        self.frame_my.pack()

    def show(self):
        self.master.mainloop()


if __name__ == '__main__':
    c = OperatorUI()
    c.show()
