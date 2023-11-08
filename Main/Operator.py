from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime

import tkintermapview
from PIL import Image, ImageTk

from ManipulateDatabase import CusOpenDatabase, OperatorDatabase

FONT = ('Arial', 20)  # text size

FONT_TOP = ('Arial', 20, 'bold')  # top botton size

FONT_TITLE = ('Arial', 50, 'bold')  # title size

# entry size
HEIGHT = 50
WIDTH = 300


# OPERATOR
class Track:
    def __init__(self, master) -> None:
        self.l_map = None
        self.parkingtable = None
        self.ridingtable = None
        self.master = master
        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()

        # create frames
        self.frame_track_main = Frame(self.master, width=S_W, height=S_H)
        # self.frames = [self.frame_track_main]

        self.init_frame()
        self.show_frame_track_main()

    def show_frame_track_main(self):
        self.frame_track_main.pack()

    def init_frame(self):
        self.ftrack_main()

    def show_riding_tabel(self):
        self.btn_riding.configure(bg='lightpink')
        self.btn_parking.configure(bg='SystemButtonFace')
        self.btn_map.configure(bg='SystemButtonFace')
        num = 1
        self.show_table(num)

    def show_parking_tabel(self):
        self.btn_parking.configure(bg='lightpink')
        self.btn_riding.configure(bg='SystemButtonFace')
        self.btn_map.configure(bg='SystemButtonFace')
        num = 0
        self.show_table(num)

    def show_map(self):
        self.btn_map.configure(bg='lightpink')
        self.btn_riding.configure(bg='SystemButtonFace')
        self.btn_parking.configure(bg='SystemButtonFace')
        num = 2
        self.show_table(num)

    def getRidingData(self):
        DB = OperatorDatabase()
        BikeData = DB.get_riding_location()
        return BikeData

    def getParkingData(self):
        DB = OperatorDatabase()
        ParkData = DB.get_parking_location()
        return ParkData

    def show_table(self, num):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        if hasattr(self, 'ridingtable') and self.ridingtable is not None:
            self.ridingtable.destroy()
        if hasattr(self, 'parkingtable') and self.parkingtable is not None:
            self.parkingtable.destroy()
        if hasattr(self, 'l_map') and self.l_map is not None:
            self.l_map.destroy()

        if num == 0:
            self.data = self.getParkingData()
            columns = ['No.', 'Bike ID', 'Bike Type', 'Location', 'Battery']
            self.parkingtable = TrackParkingTable(self.frame_track_main, columns=columns,
                                                  data=self.data)
            self.parkingtable.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)
        if num == 1:
            self.data = self.getRidingData()
            columns = ['No.', 'Bike ID', 'Bike Type', 'Location', 'Start Time', 'Battery']
            self.ridingtable = TrackRidingTable(self.frame_track_main, columns=columns,
                                                data=self.data)
            self.ridingtable.place(x=S_W / 1440 * 60, y=S_H / 900 * 300)
        if num == 2:
            self.l_map = LabelFrame(self.frame_track_main)
            self.l_map.place(x=S_W / 1440 * 20, y=S_H / 900 * 250, width=1400, height=550)

            map_widget = tkintermapview.TkinterMapView(self.l_map, width=1400, height=550, corner_radius=0)
            map_widget.set_position(55.87180409870281, -4.288428799073684)
            map_widget.set_zoom(15)
            map_widget.grid()

            conn = sqlite3.connect('RIDENOW.db')
            print("Database connecting successfully")
            c = conn.cursor()
            c.execute("""
                SELECT address FROM Parking_lot
                """)
            address = c.fetchall()
            print(address)

            c.execute("""
                SELECT name FROM Parking_lot
                """)
            parking_lot_name = c.fetchall()
            print(parking_lot_name)
            names = [item[0] for item in parking_lot_name]
            # Loop through each tuple and extract the values
            latitude = []
            longitude = []
            for item in address:
                # Extract the string from the tuple
                coord_string = item[0]

                # Remove the brackets and split the string into latitude and longitude
                coord_string = coord_string.strip('[]')
                lat, long = map(float, coord_string.split(', '))
                latitude.append(lat)
                longitude.append(long)
                # set a position marker
                for x, y, z in zip(latitude, longitude, names):
                    markers = map_widget.set_marker(x, y, text="{}".format(z))

    def ftrack_main(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.btn_riding = Button(self.frame_track_main, text='On Riding',
                                 command=self.show_riding_tabel, font=FONT)
        self.btn_riding.place(x=S_W / 1440 * 200, y=S_H / 900 * 150, height=50, width=300)

        self.btn_parking = Button(self.frame_track_main, text='In Parking Lot',
                                  command=self.show_parking_tabel, font=FONT)
        self.btn_parking.place(x=S_W / 1440 * 570, y=S_H / 900 * 150, height=50, width=300)

        self.btn_map = Button(self.frame_track_main, text='Location Map',
                              command=self.show_map, font=FONT)
        self.btn_map.place(x=S_W / 1440 * 930, y=S_H / 900 * 150, height=50, width=300)

    def ftrack_main(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.btn_riding = Button(self.frame_track_main, text='On Riding',
                                 command=self.show_riding_tabel, font=FONT)
        self.btn_riding.place(x=S_W / 1440 * 200, y=S_H / 900 * 150, height=50, width=300)

        self.btn_parking = Button(self.frame_track_main, text='In Parking Lot',
                                  command=self.show_parking_tabel, font=FONT)
        self.btn_parking.place(x=S_W / 1440 * 570, y=S_H / 900 * 150, height=50, width=300)

        self.btn_map = Button(self.frame_track_main, text='Location Map',
                              command=self.show_map, font=FONT)
        self.btn_map.place(x=S_W / 1440 * 930, y=S_H / 900 * 150, height=50, width=300)


class TrackRidingTable(ttk.Treeview, Track):
    # def __init__(self, master, columns) -> None:
    def __init__(self, master, columns,
                 data) -> None:
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

        # self.bind("<Double-1>", self.show_window)

        self.datas = self.add_row(data)

    def add_row(self, datas):
        self.datalist = []
        count = 1
        for data in datas:
            row_data = [count] + list(data)
            self.insert("", END, values=row_data)
            self.datalist.append(row_data)
            count += 1
        return self.datalist


class TrackParkingTable(ttk.Treeview, Track):
    # def __init__(self, master, columns) -> None:
    def __init__(self, master, columns,
                 data) -> None:
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

        self.datas = self.add_row(data)

    def add_row(self, datas):
        self.datalist = []
        count = 1
        for data in datas:
            row_data = [count] + list(data)
            self.insert("", END, values=row_data)
            self.datalist.append(row_data)
            count += 1
        return self.datalist


class Charge:
    def __init__(self, master) -> None:

        self.master = master
        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()

        # create frames
        self.frame_charge_main = Frame(self.master, width=S_W, height=S_H)
        self.frame_charge_history = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_charge_main, self.frame_charge_history]

        self.init_frame()
        self.show_frame_charge_main()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def show_frame_charge_main(self):
        self.forget_all()
        self.frame_charge_main.pack()

    def show_frame_charge_history(self):
        self.forget_all()
        self.frame_charge_history.pack()

    def init_frame(self):
        self.fcharge_main()
        self.fcharge_history()

    # get Location for combobox
    def select_location(self):
        location_data = CusOpenDatabase()
        locationData = location_data.select_parking_location()
        return locationData

    # get bike type for combobox
    def select_type(self):
        type_data = OperatorDatabase()
        typeData = type_data.bikeType()
        return typeData

    def getChargeData(self):
        DB = OperatorDatabase()
        if self.selected_location.get() != "Choose Location" and \
                self.selected_type1.get() != "Choose Type":
            chargeData = DB.get_chargeData(self.selected_location.get(),
                                           self.selected_type1.get())  # two parameters
        elif self.selected_location.get() == "Choose Location" and \
                self.selected_type1.get() != "Choose Type":
            chargeData = DB.get_chargeData_t(self.selected_type1.get())  # use type
        elif self.selected_location.get() != "Choose Location" and \
                self.selected_type1.get() == "Choose Type":
            chargeData = DB.get_chargeData_l(self.selected_location.get())  # use location
        else:
            chargeData = DB.get_chargeData_no()
        return chargeData

    def getChargeHistoryData(self):
        DB = OperatorDatabase()
        Oid = DB.get_loginData()[2]

        day = self.selected_day.get()
        month = self.selected_month.get()
        year = self.selected_year.get()
        date = "{}-{}-{}".format(year, month, day)
        type2 = self.selected_type2.get()

        if day != "Day" and month != "Month" and year != "Year" and type2 != "Choose Type":
            chargeHistoryData = DB.get_chargeHistory(date, type2, Oid)
        elif (day == "Day" or month == "Month" or year == "Year") and type2 != "Choose Type":
            chargeHistoryData = DB.get_chargeHistory_t(type2, Oid)
        elif day != "Day" and month != "Month" and year != "Year" and type2 == "Choose Type":
            chargeHistoryData = DB.get_chargeHistory_d(date, Oid)
        else:
            chargeHistoryData = DB.get_chargeHistory_no(Oid)
        return chargeHistoryData

    def show_charge_tabel(self, event):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.data = self.getChargeData()
        columns = ['No.', 'Bike ID', 'Bike Type', 'Battery', 'Location']
        self.table = ChargeTable(self.frame_charge_main, columns=columns,
                                 data=self.data)
        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

    def show_charge_history_tabel(self, event):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        columns = ['No.', 'Bike ID', 'Bike Type', 'Charge Date', 'Operator ID']

        self.data = self.getChargeHistoryData()
        self.table = ChargeHistoryTable(self.frame_charge_history, columns=columns,
                                        data=self.data)
        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

    def fcharge_main(self):

        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.selected_location = StringVar()
        self.l_location = Label(self.frame_charge_main, text='Location:', font=FONT)
        self.l_location.place(x=S_W / 1440 * 150, y=S_H / 900 * 150)
        self.comb_location = ttk.Combobox(self.frame_charge_main, values=self.select_location(),
                                          textvariable=self.selected_location, font=FONT)
        self.comb_location.set("Choose Location")
        self.comb_location.place(x=S_W / 1440 * (150 + 150), y=S_H / 900 * 150, width=WIDTH, height=HEIGHT)
        self.comb_location.bind("<<ComboboxSelected>>", self.show_charge_tabel)

        self.selected_type1 = StringVar()
        self.l_type = Label(self.frame_charge_main, text='Bike Type:', font=FONT)
        self.l_type.place(x=S_W / 1440 * (300 + WIDTH + 150), y=S_H / 900 * 150)
        self.comb_t = ttk.Combobox(self.frame_charge_main, values=self.select_type(),
                                   textvariable=self.selected_type1, font=FONT)
        self.comb_t.set("Choose Type")
        self.comb_t.place(x=S_W / 1440 * (300 + WIDTH + 300), y=S_H / 900 * 150, width=WIDTH, height=HEIGHT)
        self.comb_t.bind("<<ComboboxSelected>>", self.show_charge_tabel)

        self.l_box = Label(self.frame_charge_main, text='List of Information:', font=FONT)
        self.l_box.place(x=S_W / 1440 * 150, y=S_H / 900 * 250)

        self.btn_history = Button(self.frame_charge_main, text="History", font=FONT,
                                  command=self.show_frame_charge_history)
        self.btn_history.place(x=S_W / 1440 * 1120, y=S_H / 900 * 60, width=WIDTH, height=HEIGHT)

        columns = ['No.', 'Bike ID', 'Bike Type', 'Battery', 'Location']

        self.intidata = self.getChargeData()
        self.table = ChargeTable(self.frame_charge_main, columns=columns,
                                 data=self.intidata)
        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

    def fcharge_history(self):

        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_title = Label(self.frame_charge_history, text='CHARGE HISTORY', font=FONT_TITLE)
        self.l_title.place(x=S_W / 1440 * 400, y=S_H / 900 * 100)

        self.current_datetime = datetime.now()
        self.current_date = self.current_datetime.date()
        self.year = list(range(2021, self.current_date.year + 1))
        self.month = list(range(1, 13))
        day1 = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
        self.day = day1+(list(range(10, 32)))

        self.selected_day = StringVar()
        self.selected_month = StringVar()
        self.selected_year = StringVar()
        self.selected_type2 = StringVar()

        self.l_date = Label(self.frame_charge_history, text='Date:', font=FONT)
        self.l_date.place(x=S_W / 1440 * 150, y=S_H / 900 * 200)
        self.comb_day = ttk.Combobox(self.frame_charge_history, values=self.day,
                                     textvariable=self.selected_day, font=FONT)
        self.comb_day.insert(0, "Day")
        self.comb_day.place(x=S_W / 1440 * (150 + 150), y=S_H / 900 * 200, width=WIDTH / 3, height=HEIGHT)
        self.comb_month = ttk.Combobox(self.frame_charge_history, values=self.month,
                                       textvariable=self.selected_month, font=FONT)
        self.comb_month.insert(0, "Month")
        self.comb_month.place(x=S_W / 1440 * (150 + 150) + WIDTH / 3, y=S_H / 900 * 200, width=WIDTH / 3, height=HEIGHT)
        self.comb_year = ttk.Combobox(self.frame_charge_history, values=self.year,
                                      textvariable=self.selected_year, font=FONT)
        self.comb_year.insert(0, "Year")
        self.comb_year.place(x=S_W / 1440 * (150 + 150) + 2 * WIDTH / 3, y=S_H / 900 * 200, width=WIDTH / 3,
                             height=HEIGHT)
        self.comb_day.bind("<<ComboboxSelected>>", self.show_charge_history_tabel)
        self.comb_month.bind("<<ComboboxSelected>>", self.show_charge_history_tabel)
        self.comb_year.bind("<<ComboboxSelected>>", self.show_charge_history_tabel)

        self.l_type = Label(self.frame_charge_history, text='Bike Type:', font=FONT)
        self.l_type.place(x=S_W / 1440 * (300 + WIDTH + 150), y=S_H / 900 * 200)
        self.comb_type = ttk.Combobox(self.frame_charge_history, values=self.select_type(),
                                      textvariable=self.selected_type2, font=FONT)
        self.comb_type.insert(0, "Choose Type")
        self.comb_type.place(x=S_W / 1440 * (300 + WIDTH + 300), y=S_H / 900 * 200, width=WIDTH, height=HEIGHT)
        self.comb_type.bind("<<ComboboxSelected>>", self.show_charge_history_tabel)

        self.l_box = Label(self.frame_charge_history, text='List of Information:', font=FONT)
        self.l_box.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

        self.btn_return = Button(self.frame_charge_history, text="Return", font=FONT,
                                 command=self.show_frame_charge_main)
        self.btn_return.place(x=S_W / 1440 * 150, y=S_H / 900 * 760, width=WIDTH, height=HEIGHT)

        self.data = self.getChargeHistoryData()
        columns = ['No.', 'Bike ID', 'Bike Type', 'Charge Date', 'Operator ID']
        self.table = ChargeHistoryTable(self.frame_charge_history, columns=columns,
                                        data=self.data)
        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)


class ChargeTable(ttk.Treeview, Charge):
    # def __init__(self, master, columns) -> None:
    def __init__(self, master, columns,
                 data) -> None:
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

        self.datas = self.add_row(data)

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
        # get Treeview institution
        tree = event.widget
        # get current ID
        selected_item_id = tree.focus()
        # get index
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
    # charge detail interface

    def __init__(self, record: ChargeDetail) -> None:
        self.record = record

    def confim_charge(self):
        result = messagebox.askyesno("Confirm", "Confirm Charge？")
        if result:  # if confim charge
            O_DB = OperatorDatabase()
            OData = O_DB.get_loginData()
            OID = OData[2]
            currentime = datetime.now()
            Time = str(currentime.time()).split('.')[0]
            Date = str(currentime.date())

            O_DB.insertChargeHistory(
                self.record.BID, self.record.BType, OID, self.record.Battery, Time, self.record.Location, Date
            )
            O_DB.modifybattery(self.record.BID)

            messagebox.showinfo("success window", "Charge Successful !")

            self.master.destroy()

    def __init__(self, record: ChargeDetail) -> None:
        self.record = record

        self.master = Tk()
        self.master.title('Charge Detail')
        self.master.geometry('600x400+400+200')

        self.init_ui()

    def init_ui(self):
        font = ('Arial', 16)
        # create widget
        self.l_title = Label(self.master, text='CHARGE DETAIL', font=FONT)
        self.l_title.place(x=200, y=20)

        self.l_bike_id = Label(self.master, text='Bike ID:', font=font)
        self.l_bike_id.place(x=80, y=70)
        self.e_bike_id = Entry(self.master, font=font)
        self.e_bike_id.insert(0, self.record.BID)
        self.e_bike_id.configure(state='readonly')
        self.e_bike_id.place(x=200, y=70, width=300)
        self.e_bike_id["justify"] = "center"

        self.l_bike_type = Label(self.master, text='Bike type:', font=font)
        self.l_bike_type.place(x=80, y=120)
        self.e_bike_type = Entry(self.master, font=font)
        self.e_bike_type.insert(0, self.record.BType)
        self.e_bike_type.configure(state='readonly')
        self.e_bike_type.place(x=200, y=120, width=300)
        self.e_bike_type["justify"] = "center"

        self.l_battery = Label(self.master, text='Battery:', font=font)
        self.l_battery.place(x=80, y=170)
        self.e_battery = Entry(self.master, font=font)
        self.e_battery.insert(0, self.record.Battery)
        self.e_battery.configure(state='readonly')
        self.e_battery.place(x=200, y=170, width=300)
        self.e_battery["justify"] = "center"

        self.l_location = Label(self.master, text='Location:', font=font)
        self.l_location.place(x=80, y=220)
        self.e_location = Entry(self.master, font=font)
        self.e_location.insert(0, self.record.Location)
        self.e_location.configure(state='readonly')
        self.e_location.place(x=200, y=220, width=300)
        self.e_location["justify"] = "center"

        currenttime = str(datetime.now()).split(".")[0]
        self.l_time = Label(self.master, text='time:', font=font)
        self.l_time.place(x=80, y=270)
        self.e_time = Entry(self.master, font=font)
        self.e_time.insert(0, currenttime)
        self.e_time.configure(state='readonly')
        self.e_time.place(x=200, y=270, width=300)
        self.e_time["justify"] = "center"

        self.btn_return = Button(self.master, text='Return', font=font,
                                 command=self.master.destroy)
        self.btn_return.place(x=100, y=330, height=50, width=150)

        self.btn_charge = Button(self.master, text='Charge', font=font,
                                 command=self.confim_charge)
        self.btn_charge.place(x=350, y=330, height=50, width=150)

    def show(self):
        self.master.mainloop()


class ChargeHistoryTable(ttk.Treeview):
    def __init__(self, master, columns,
                 data) -> None:
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

        self.datas = self.add_row(data)

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
            record = ChargeHistoryDetail(*self.datas[row_index])
            record_ui = ChargeHistoryDetails(record)
            record_ui.show()


class ChargeHistoryDetail:

    def __init__(self, no=None, BID=None, Btype=None, ChargeDate=None,
                 Operator=None, battery=None, ChargeTime=None) -> None:
        self.no = no
        self.BID = BID
        self.BType = Btype
        self.ChargeDate = ChargeDate
        self.ChargeTime = ChargeTime
        self.Operator = Operator
        self.battery = battery

        self.Time = "{} {}".format(self.ChargeDate, self.ChargeTime)


class ChargeHistoryDetails:
    # show charge history record detail

    def __init__(self, record: ChargeHistoryDetail) -> None:
        self.record = record

        self.master = Tk()
        self.master.title('Charge History Detail')
        self.master.geometry('600x400+400+200')

        self.init_ui()

    def init_ui(self):
        font = ('Arial', 16)
        # create widget
        self.l_title = Label(self.master, text='CHARGE RECORD', font=FONT)
        self.l_title.place(x=200, y=20)

        self.l_bike_id = Label(self.master, text='Bike ID:', font=font)
        self.l_bike_id.place(x=80, y=70)
        self.e_bike_id = Entry(self.master, font=font)
        self.e_bike_id.insert(0, self.record.BID)
        self.e_bike_id.configure(state='readonly')
        self.e_bike_id.place(x=250, y=70, width=250)
        self.e_bike_id["justify"] = "center"

        self.l_bike_type = Label(self.master, text='Bike type:', font=font)
        self.l_bike_type.place(x=80, y=120)
        self.e_bike_type = Entry(self.master, font=font)
        self.e_bike_type.insert(0, self.record.BType)
        self.e_bike_type.configure(state='readonly')
        self.e_bike_type.place(x=250, y=120, width=250)
        self.e_bike_type["justify"] = "center"

        self.l_battery = Label(self.master, text='Charge Time:', font=font)
        self.l_battery.place(x=80, y=170)
        self.e_battery = Entry(self.master, font=font)
        self.e_battery.insert(0, self.record.Time)
        self.e_battery.configure(state='readonly')
        self.e_battery.place(x=250, y=170, width=250)
        self.e_battery["justify"] = "center"

        self.l_location = Label(self.master, text='Oringinal Battery:', font=font)
        self.l_location.place(x=80, y=220)
        self.e_location = Entry(self.master, font=font)
        self.e_location.insert(0, self.record.battery)
        self.e_location.configure(state='readonly')
        self.e_location.place(x=250, y=220, width=250)
        self.e_location["justify"] = "center"

        self.l_time = Label(self.master, text='Operator ID:', font=font)
        self.l_time.place(x=80, y=270)
        self.e_time = Entry(self.master, font=font)
        self.e_time.insert(0, self.record.Operator)
        self.e_time.configure(state='readonly')
        self.e_time.place(x=250, y=270, width=250)
        self.e_time["justify"] = "center"

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

    def select_errortype(self):
        type_data = OperatorDatabase()
        typeData = type_data.errorType()
        return typeData

    def getRepairData(self):
        DB = OperatorDatabase()
        Rlocation = self.comb_location.get()
        Rtype = self.comb_typee.get()
        if Rlocation != "Choose Location" and Rtype != "Choose Type":
            repairData = DB.get_repairData(Rlocation, Rtype)
        elif Rlocation == "Choose Location" and Rtype != "Choose Type":
            repairData = DB.get_repairData_t(Rtype)
        elif Rlocation != "Choose Location" and Rtype == "Choose Type":
            repairData = DB.get_repairData_l(Rlocation)
        else:
            repairData = DB.get_repairData_no()

        return repairData

    def getRepairHistoryData(self):
        DB = OperatorDatabase()
        OData = DB.get_loginData()
        OID = OData[2]

        day = self.selected_day.get()
        month = self.selected_month.get()
        year = self.selected_year.get()
        date = "{}-{}-{}".format(year, month, day)
        type = self.selected_type.get()
        if day != "Day" and month != "Month" and year != "Year" and type != "Error Type":
            repair_Hist_Data = DB.get_repairHistory(date, type, OID)
        elif day != "Day" and month != "Month" and year != "Year" and type == "Error Type":
            repair_Hist_Data = DB.get_repairHistory_d(date, OID)
        elif (day == "Day" or month == "Month" or year == "Year") and type != "Error Type":
            repair_Hist_Data = DB.get_repairHistory_t(type, OID)
        else:
            repair_Hist_Data = DB.get_repairHistory_no(OID)
        return repair_Hist_Data

    def show_repair_tabel(self, event):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        columns = ['No.', 'Bike ID', 'Bike Type', 'Error Type', 'Location']

        self.mydata = self.getRepairData()
        self.table = RepairTable(self.frame_repair_main, columns=columns,
                                 data=self.mydata)
        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

    def show_repair_history_tabel(self, event):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        columns = ['No.', 'Bike ID', 'Bike Type', 'Error Type', 'Repair Date']

        self.dataa = self.getRepairHistoryData()
        self.table = RepairHistoryTable(self.frame_repair_history, columns=columns,
                                        data=self.dataa)
        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

    def frepair_main(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.selected_location = StringVar()
        self.l_location = Label(self.frame_repair_main, text='Location:', font=FONT)
        self.l_location.place(x=S_W / 1440 * 150, y=S_H / 900 * 150)
        self.comb_location = ttk.Combobox(self.frame_repair_main, values=list(self.select_location()),
                                          textvariable=self.selected_location, state="readonly", font=FONT)
        self.comb_location.set("Choose Location")
        self.comb_location.place(x=S_W / 1440 * (150 + 150), y=S_H / 900 * 150, width=WIDTH, height=HEIGHT)
        self.comb_location.bind("<<ComboboxSelected>>", self.show_repair_tabel)

        self.selected_type3 = StringVar()
        self.l_type = Label(self.frame_repair_main, text='Error Type:', font=FONT)
        self.l_type.place(x=S_W / 1440 * (300 + WIDTH + 150), y=S_H / 900 * 150)
        self.comb_typee = ttk.Combobox(self.frame_repair_main, values=list(self.select_errortype()),
                                       textvariable=self.selected_type3, state="readonly", font=FONT)
        self.comb_typee.set("Choose Type")
        self.comb_typee.place(x=S_W / 1440 * (300 + WIDTH + 300), y=S_H / 900 * 150, width=WIDTH, height=HEIGHT)
        self.comb_typee.bind("<<ComboboxSelected>>", self.show_repair_tabel)

        self.l_box = Label(self.frame_repair_main, text='List of Information:', font=FONT)
        self.l_box.place(x=S_W / 1440 * 150, y=S_H / 900 * 250)

        self.btn_history = Button(self.frame_repair_main, text="History", font=FONT,
                                  command=self.show_frame_repair_history)
        self.btn_history.place(x=S_W / 1440 * 1120, y=S_H / 900 * 60, width=WIDTH, height=HEIGHT)

        self.idata = self.getRepairData()
        columns = ['No.', 'Bike ID', 'Bike Type', 'Error Type', 'Location']
        self.table = RepairTable(self.frame_repair_main, columns=columns,
                                 data=self.idata)
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
        day1 = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
        self.day = day1 + (list(range(10, 32)))

        self.selected_day = StringVar()
        self.selected_month = StringVar()
        self.selected_year = StringVar()
        self.selected_type = StringVar()
        self.l_date = Label(self.frame_repair_history, text='Date:', font=FONT)
        self.l_date.place(x=S_W / 1440 * 150, y=S_H / 900 * 200)
        self.comb_day = ttk.Combobox(self.frame_repair_history, values=self.day,
                                     textvariable=self.selected_day, font=FONT)
        self.comb_day.insert(0, "Day")
        self.comb_day.place(x=S_W / 1440 * (150 + 150), y=S_H / 900 * 200, width=WIDTH / 3, height=HEIGHT)
        self.comb_month = ttk.Combobox(self.frame_repair_history, values=self.month,
                                       textvariable=self.selected_month, font=FONT)
        self.comb_month.insert(0, "Month")
        self.comb_month.place(x=S_W / 1440 * ((150 + 150) + WIDTH / 3), y=S_H / 900 * 200, width=WIDTH / 3,
                              height=HEIGHT)
        self.comb_year = ttk.Combobox(self.frame_repair_history, values=self.year,
                                      textvariable=self.selected_year, font=FONT)
        self.comb_year.insert(0, "Year")
        self.comb_year.place(x=S_W / 1440 * ((150 + 150) + 2 * WIDTH / 3), y=S_H / 900 * 200, width=WIDTH / 3,
                             height=HEIGHT)
        self.comb_day.bind("<<ComboboxSelected>>", self.show_repair_history_tabel)
        self.comb_month.bind("<<ComboboxSelected>>", self.show_repair_history_tabel)
        self.comb_year.bind("<<ComboboxSelected>>", self.show_repair_history_tabel)

        self.l_type = Label(self.frame_repair_history, text='Error Type:', font=FONT)
        self.l_type.place(x=S_W / 1440 * (300 + WIDTH + 150), y=S_H / 900 * 200)
        self.comb_type = ttk.Combobox(self.frame_repair_history, values=self.select_errortype(),
                                      textvariable=self.selected_type, state="readonly", font=FONT)
        self.comb_type.set("Error Type")
        self.comb_type.place(x=S_W / 1440 * (300 + WIDTH + 300), y=S_H / 900 * 200, width=WIDTH, height=HEIGHT)
        self.comb_type.bind("<<ComboboxSelected>>", self.show_repair_history_tabel)

        self.l_box = Label(self.frame_repair_history, text='List of Information:', font=FONT)
        self.l_box.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

        self.btn_return = Button(self.frame_repair_history, text="Return", font=FONT,
                                 command=self.show_frame_repair_main)
        self.btn_return.place(x=S_W / 1440 * 150, y=S_H / 900 * 760, width=WIDTH, height=HEIGHT)

        self.data0 = self.getRepairHistoryData()
        columns = ['No.', 'Bike ID', 'Bike Type', 'Error Type', 'Repair Date']
        self.table = RepairHistoryTable(self.frame_repair_history, columns=columns,
                                        data=self.data0)
        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)


class RepairTable(ttk.Treeview, Repair):

    def __init__(self, master, columns, data) -> None:
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

        self.datas = self.add_row(data)

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

    def __init__(self, no=None, BID=None, BType=None, Errortype=None,
                 Location=None, date=None,
                 pic=None, description=None) -> None:
        self.no = no
        self.BID = BID
        self.BType = BType
        self.Errortype = Errortype
        self.Location = Location
        self.date = date
        self.pic = pic
        self.description = description

        self.Time = self.date


class RepairDetails:
    # show repair record detail

    def __init__(self, record: RepairDetail) -> None:
        self.record = record

        self.master = Tk()
        self.master.title('Repair Detail')
        self.master.geometry('600x400+400+200')

        self.master.lift()
        self.master.focus_force()

        self.init_ui()

    def confim_repair(self):
        result = messagebox.askyesno("Confirm", "Confirm Repair？")
        if result:
            O_DB = OperatorDatabase()
            OData = O_DB.get_loginData()
            OID = OData[2]
            currentime = datetime.now()
            Time = str(currentime.time()).split(".")[0]
            Date = str(currentime.date())
            Sta = "Completed"
            bid = self.record.BID

            O_DB.modifyrepair(OID, Sta, Time, Date, bid)
            O_DB.modifystate(bid)

            messagebox.showinfo("success window", "Repair Successful !")

            self.master.destroy()

    def init_ui(self):
        font = ('Arial', 16)
        # create widget

        self.l_title = Label(self.master, text='REPAIR DETAIL', font=FONT)
        self.l_title.place(x=220, y=20)

        self.l_bikeid = Label(self.master, text="Bike ID: ", font=font)
        self.l_bikeid.place(x=70, y=70)
        self.e_bikeid = Entry(self.master, font=font)
        self.e_bikeid.insert(0, self.record.BID)
        self.e_bikeid.configure(state='readonly')
        self.e_bikeid.place(x=230, y=70, width=280, height=30)
        self.e_bikeid["justify"] = "center"

        self.l_biketype = Label(self.master, text='Bike Type:', font=font)
        self.l_biketype.place(x=70, y=110)
        self.e_biketype = Entry(self.master, font=font)
        self.e_biketype.insert(0, self.record.BType)
        self.e_biketype.configure(state='readonly')
        self.e_biketype.place(x=230, y=110, width=280, height=30)
        self.e_biketype["justify"] = "center"

        self.l_errortype = Label(self.master, text='Error Type:', font=font)
        self.l_errortype.place(x=70, y=150)
        self.e_errortype = Entry(self.master, font=font)
        self.e_errortype.insert(0, self.record.Errortype)
        self.e_errortype.configure(state='readonly')
        self.e_errortype.place(x=230, y=150, width=280, height=30)
        self.e_errortype["justify"] = "center"

        self.l_Location = Label(self.master, text='Location:', font=font)
        self.l_Location.place(x=70, y=190)
        self.e_Location = Entry(self.master, font=font)
        self.e_Location.insert(0, self.record.Location)
        self.e_Location.configure(state='readonly')
        self.e_Location.place(x=230, y=190, width=280, height=30)
        self.e_Location["justify"] = "center"

        self.l_stime = Label(self.master, text='Report Time:', font=font)
        self.l_stime.place(x=70, y=230)
        self.e_stime = Entry(self.master, font=font)
        self.e_stime.insert(0, self.record.Time)
        self.e_stime.configure(state='readonly')
        self.e_stime.place(x=230, y=230, width=280, height=30)
        self.e_stime["justify"] = "center"

        self.l_description = Label(self.master, text='Description:', font=font)
        self.l_description.place(x=70, y=270)
        self.m_description = Message(self.master, text=self.record.description, font=font, width=300)
        self.m_description.place(x=230, y=270)

        self.btn_return = Button(self.master, text="Return", font=font,
                                 command=self.master.destroy)
        self.btn_return.place(x=70, y=360, width=200, height=30)

        self.btn_charge = Button(self.master, text='Repair', font=font,
                                 command=self.confim_repair)
        self.btn_charge.place(x=330, y=360, width=200, height=30)

    def show(self):
        self.master.mainloop()


class RepairHistoryTable(ttk.Treeview, Repair):

    def __init__(self, master, columns,
                 data) -> None:
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
        self.datas = self.add_row(data)

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
            record = RepairHistoryDetail(*self.datas[row_index])
            record_ui = RepairHistoryDetails(record)
            record_ui.show()


class RepairHistoryDetail:
    def __init__(self, no=None, BID=None, BType=None, Errortype=None,
                 date=None, Location=None, time=None,
                 starting_date=None, operator_id=None, pic=None, description=None) -> None:
        self.no = no
        self.BID = BID
        self.BType = BType
        self.Errortype = Errortype
        self.Location = Location
        self.time = time
        self.date = date
        self.starting_date = starting_date
        self.operator_id = operator_id
        self.pic = pic
        self.description = description

        self.Time = "{} {}".format(self.date, self.time)
        self.sTime = starting_date


class RepairHistoryDetails:
    # show repair history record detail

    def __init__(self, record: RepairHistoryDetail) -> None:
        self.record = record

        self.master = Tk()
        self.master.title('Repair Detail')
        self.master.geometry('600x400+400+200')

        self.init_ui()

    def init_ui(self):
        # create widget
        font = ('Arial', 15)

        self.l_title = Label(self.master, text='REPAIR DETAIL', font=FONT)
        self.l_title.place(x=220, y=20)

        self.l_biketype = Label(self.master, text='Bike Type:', font=font)
        self.l_biketype.place(x=40, y=70)
        self.e_biketype = Entry(self.master, font=font)
        self.e_biketype.insert(0, self.record.BType)
        self.e_biketype.configure(state='readonly')
        self.e_biketype.place(x=170, y=70, width=150, height=30)
        self.e_biketype["justify"] = "center"

        self.l_bikeid = Label(self.master, text="Bike ID: ", font=font)
        self.l_bikeid.place(x=335, y=70)
        self.e_bikeid = Entry(self.master, font=font)
        self.e_bikeid.insert(0, self.record.BID)
        self.e_bikeid.configure(state='readonly')
        self.e_bikeid.place(x=460, y=70, width=90, height=30)
        self.e_bikeid["justify"] = "center"

        self.l_errortype = Label(self.master, text='Error Type:', font=font)
        self.l_errortype.place(x=40, y=110)
        self.e_errortype = Entry(self.master, font=font)
        self.e_errortype.insert(0, self.record.Errortype)
        self.e_errortype.configure(state='readonly')
        self.e_errortype.place(x=170, y=110, width=150, height=30)
        self.e_errortype["justify"] = "center"

        self.l_oid = Label(self.master, text='Operator ID:', font=font)
        self.l_oid.place(x=335, y=110)
        self.e_oid = Entry(self.master, font=font)
        self.e_oid.insert(0, self.record.operator_id)
        self.e_oid.configure(state='readonly')
        self.e_oid.place(x=460, y=110, width=90, height=30)
        self.e_oid["justify"] = "center"

        self.l_Location = Label(self.master, text='Location:', font=font)
        self.l_Location.place(x=40, y=150)
        self.e_Location = Entry(self.master, font=font)
        self.e_Location.insert(0, self.record.Location)
        self.e_Location.configure(state='readonly')
        self.e_Location.place(x=170, y=150, width=380, height=30)
        self.e_Location["justify"] = "center"

        self.l_stime = Label(self.master, text='Report Time:', font=font)
        self.l_stime.place(x=40, y=190)
        self.e_stime = Entry(self.master, font=font)
        self.e_stime.insert(0, self.record.sTime)
        self.e_stime.configure(state='readonly')
        self.e_stime.place(x=170, y=190, width=380, height=30)
        self.e_stime["justify"] = "center"

        self.l_etime = Label(self.master, text='Repair Time:', font=font)
        self.l_etime.place(x=40, y=230)
        self.e_etime = Entry(self.master, font=font)
        self.e_etime.insert(0, self.record.Time)
        self.e_etime.configure(state='readonly')
        self.e_etime.place(x=170, y=230, width=380, height=30)
        self.e_etime["justify"] = "center"

        self.l_description = Label(self.master, text='Description:', font=font)
        self.l_description.place(x=40, y=270)
        text = "111111111111111111111111111111111111111111111111"
        self.m_description = Message(self.master, text=self.record.description, font=font, width=380)
        self.m_description.place(x=170, y=270, width=380)

        self.btn_return = Button(self.master, text="Return", font=font,
                                 command=self.master.destroy)
        self.btn_return.place(x=260, y=360, width=100, height=30)

    def show(self):
        self.master.mainloop()


class Move:
    def __init__(self, master) -> None:
        self.master = master

        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()

        # create frames
        self.frame_move_main = Frame(self.master, width=S_W, height=S_H)
        self.frame_move_history = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_move_main, self.frame_move_history]

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

    def show_frame_move_history(self):
        self.forget_all()
        self.frame_move_history.pack()

    def init_frame(self):
        self.fmove_main()
        self.fmove_history()

    def open_database(self):
        conn = sqlite3.connect("RIDENOW.db")
        self.c = conn.cursor()

    def select_location(self):
        self.open_database()
        self.c.execute("""SELECT name FROM Parking_lot""")
        parking_location = self.c.fetchall()
        return parking_location

    def select_type(self):
        type_data = OperatorDatabase()
        typeData = type_data.bikeType()
        return typeData

    def getMoveHistoryData(self):
        DB = OperatorDatabase()

        day = self.selected_day.get()
        month = self.selected_month.get()
        year = self.selected_year.get()
        date = "{}-{}-{}".format(year, month, day)
        type2 = self.selected_typem.get()

        if day != "Day" and month != "Month" and year != "Year" and type2 != "Choose Type":
            moveHistoryData = DB.get_moveHistory(date, type2)
            print("a")
        elif (day == "Day" or month == "Month" or year == "Year") and type2 != "Choose Type":
            moveHistoryData = DB.get_moveHistory_t(type2)
            print("b")
        elif day != "Day" and month != "Month" and year != "Year" and type2 == "Choose Type":
            moveHistoryData = DB.get_moveHistory_d(date)
            print("c")
        else:
            moveHistoryData = DB.get_moveHistory_no()
            print("d")

        print(moveHistoryData)
        return moveHistoryData

    def show_move_history_tabel(self, event):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        columns = ['No.', 'Bike ID', 'Bike Type', 'current location', 'original location']

        self.data = self.getMoveHistoryData()
        self.table = MoveHistoryTable(self.frame_move_history, columns=columns,
                                      data=self.data)
        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

    def fmove_main(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.l_box = Label(self.frame_move_main, text='List of Information:', font=FONT)
        self.l_box.place(x=S_W / 1440 * 200, y=S_H / 900 * 250)

        self.btn_history = Button(self.frame_move_main, text="History", font=FONT,
                                  command=self.show_frame_move_history)
        self.btn_history.place(x=S_W / 1440 * 1120, y=S_H / 900 * 60, width=WIDTH, height=HEIGHT)

        self.show_move_tabel()

    def show_move_tabel(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        columns = ['No.', 'Location', 'Total Number', 'electric_bike', 'electric_scooter']

        self.table = MoveTable(self.frame_move_main, columns=columns)

        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

    def fmove_history(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.current_datetime = datetime.now()
        self.current_date = self.current_datetime.date()
        self.year = list(range(2021, self.current_date.year + 1))
        self.month = list(range(1, 13))
        day1 = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
        self.day = day1 + (list(range(10, 32)))

        self.selected_day = StringVar()
        self.selected_month = StringVar()
        self.selected_year = StringVar()
        self.selected_typem = StringVar()

        self.l_title = Label(self.frame_move_history, text='MOVE HISTORY', font=FONT_TITLE)
        self.l_title.place(x=S_W / 1440 * 400, y=S_H / 900 * 100)

        self.l_date = Label(self.frame_move_history, text='Date:', font=FONT)
        self.l_date.place(x=S_W / 1440 * 150, y=S_H / 900 * 200)
        self.comb_day = ttk.Combobox(self.frame_move_history, values=self.day,
                                     textvariable=self.selected_day, font=FONT)
        self.comb_day.insert(0, "Day")
        self.comb_day.place(x=S_W / 1440 * (150 + 150), y=S_H / 900 * 200, width=WIDTH / 3, height=HEIGHT)
        self.comb_month = ttk.Combobox(self.frame_move_history, values=self.month,
                                       textvariable=self.selected_month, font=FONT)
        self.comb_month.insert(0, "Month")
        self.comb_month.place(x=S_W / 1440 * (150 + 150) + WIDTH / 3, y=S_H / 900 * 200, width=WIDTH / 3, height=HEIGHT)
        self.comb_year = ttk.Combobox(self.frame_move_history, values=self.year,
                                      textvariable=self.selected_year, font=FONT)
        self.comb_year.insert(0, "Year")
        self.comb_year.place(x=S_W / 1440 * (150 + 150) + 2 * WIDTH / 3, y=S_H / 900 * 200, width=WIDTH / 3,
                             height=HEIGHT)
        self.comb_day.bind("<<ComboboxSelected>>", self.show_move_history_tabel)
        self.comb_month.bind("<<ComboboxSelected>>", self.show_move_history_tabel)
        self.comb_year.bind("<<ComboboxSelected>>", self.show_move_history_tabel)

        self.l_typem = Label(self.frame_move_history, text='Bike Type:', font=FONT)
        self.l_typem.place(x=S_W / 1440 * 300 + WIDTH + 120, y=S_H / 900 * 200)
        self.comb_typem = ttk.Combobox(self.frame_move_history, values=self.select_type(),
                                       textvariable=self.selected_typem, font=FONT)
        self.comb_typem.place(x=S_W / 1440 * 300 + WIDTH + 300, y=S_H / 900 * 200, width=WIDTH, height=HEIGHT)

        self.comb_typem.insert(0, "Choose Type")
        self.comb_typem.bind("<<ComboboxSelected>>", self.show_move_history_tabel)

        self.l_box = Label(self.frame_move_history, text='List of Information:', font=FONT)
        self.l_box.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)

        self.btn_return = Button(self.frame_move_history, text="Return", font=FONT,
                                 command=self.show_frame_move_main)
        self.btn_return.place(x=S_W / 1440 * 150, y=S_H / 900 * 760, width=WIDTH, height=HEIGHT)

        self.data = self.getMoveHistoryData()
        columns = ['No.', 'Bike ID', 'Bike Type', 'current location', 'original location']
        self.table = MoveHistoryTable(self.frame_move_history, columns=columns,
                                      data=self.data)
        self.table.place(x=S_W / 1440 * 150, y=S_H / 900 * 300)


class MoveTable(ttk.Treeview, Move):

    def __init__(self, master, columns) -> None:
        super().__init__(
            master=master,
            columns=columns,
            show='headings',
            style='Treeview',
        )

        self.getdata = self.getMoveData()

        style = ttk.Style(master)
        style.configure('Treeview', font=('Arial', 14), rowheight=30)
        style.configure('Treeview.Heading', font=('Arial', 20))

        for column in columns:
            self.heading(column, text=column, anchor=CENTER)
            self.column(column, width=220, anchor=CENTER)

        self.bind("<Double-1>", self.show_window)
        self.datas = self.add_row(self.getdata)

    def getMoveData(self):
        moveList = OperatorDatabase()
        moveData = moveList.get_MoveData()
        return moveData

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
            record = MoveDetail(*self.datas[row_index])
            record_ui = MoveLocations(record)
            record_ui.show()


class MoveDetail:

    def __init__(self, no=None, location=None, num=None,
                 eletype=None, electric_scooter=None) -> None:
        self.no = no
        self.location = location
        self.num = num
        self.eletype = eletype
        # self.eletype = eletype


class MoveDetails:
    # show move detail

    def confim_move(self):
        self.moveto = self.movetolocation.get()
        result = messagebox.askyesno("Confirm", "Confirm Move？")
        if result:
            messagebox.showinfo("success window", "Move Successful !")
        self.master.destroy()

    def __init__(self, record: MoveDetail) -> None:
        self.record = record

        self.master = Tk()
        self.master.title('Move Detail')
        self.master.geometry('600x400+400+200')

        self.init_ui()

    def get_location(self):
        DB = CusOpenDatabase()
        parking_location = DB.select_parking_location()
        return parking_location

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

        self.l_location = Label(self.master, text='Location:', font=font)
        self.l_location.place(x=80, y=170)
        self.e_location = Entry(self.master, font=font)
        self.e_location.insert(0, self.record.Location)
        self.e_location.configure(state='readonly')
        self.e_location.place(x=200, y=170, width=300)

        self.movetolocation = StringVar()
        self.l_moveto = Label(self.master, text='Move To:', font=font)
        self.l_moveto.place(x=80, y=220)
        self.c_moveto = ttk.Combobox(self.master, font=font, values=self.get_location(),
                                     textvariable=self.movetolocation)
        self.c_moveto.set("Choose Location")
        self.c_moveto.place(x=200, y=220, width=300)

        time = str(datetime.now()).split('.')[0]
        self.l_time = Label(self.master, text='time:', font=font)
        self.l_time.place(x=80, y=270)
        self.e_time = Entry(self.master, font=font)
        self.e_time.insert(0, time)
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


class MoveLoTable(ttk.Treeview):

    def __init__(self, master, columns, data) -> None:
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

        # save data in table
        self.datas = self.add_row(data)

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
            record = MoveLocation(*self.datas[row_index])
            record_ui = MoveDetails(record)
            record_ui.show()


class MoveLocation:

    def __init__(self, no=None, BID=None, Btype=None,
                 Location=None, Time=None) -> None:
        self.no = no
        self.BID = BID
        self.BType = Btype
        self.Location = Location
        self.Time = Time


class MoveLocations:
    # show move location detail

    def __init__(self, record: MoveDetail) -> None:
        self.record = record

        self.master = Tk()
        self.master.title('Move Locations')
        self.master.geometry('1440x900')

        self.master.lift()
        self.master.focus_force()

        self.init_ui()

    def show_frame_move_location(self):
        self.frame_move_location.pack()

    def getMoveLocationData(self):
        DB = OperatorDatabase()
        MoveLocationData = DB.get_LocationData(self.record.location)
        return MoveLocationData

    def returnlast(self):
        self.master.destroy()

    def init_ui(self):
        font = ('Arial', 16)
        # create widget

        self.l_title = Label(self.master, text='Move Locations', font=FONT_TITLE)
        self.l_title.place(x=450, y=70)

        location = self.record.location
        self.l_location = Label(self.master, text="Location: ", font=FONT)
        self.l_location.place(x=230, y=200)
        self.l_lo = Label(self.master, text=location, font=FONT)
        self.l_lo.place(x=400, y=200)

        num = self.record.num
        self.l_num = Label(self.master, text='Bike Number:', font=FONT)
        self.l_num.place(x=900, y=200)
        self.l_num1 = Label(self.master, text=num, font=FONT)
        self.l_num1.place(x=1100, y=200)

        self.l_table = Label(self.master, text="List of Infomation: ", font=FONT)
        self.l_table.place(x=200, y=310)
        self.data = self.getMoveLocationData()
        columns = ['No.', 'Bike ID', 'Bike Type', 'location']
        self.table = MoveLoTable(self.master, columns=columns, data=self.data)
        self.table.place(x=200, y=350)
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=250)

        self.btn_return = Button(self.master, text="Return", font=FONT, command=self.returnlast)
        self.btn_return.place(x=200, y=730, width=300, height=50)

    def show(self):
        self.master.mainloop()


class MoveHistoryTable(ttk.Treeview):
    def __init__(self, master, columns, data) -> None:
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

        self.datas = self.add_row(data)

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
    # show move history detail

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
        self.conn = sqlite3.connect('RIDENOW.db')
        self.cursor = self.conn.cursor()
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
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.entry_username = Entry(self.frame_my_main, font=FONT)
        self.entry_username.place(x=S_W / 1440 * (400 + 200), y=S_H / 900 * 400, width=WIDTH, height=HEIGHT)

        self.entry_username.focus()

    def edit_password(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.entry_password = Entry(self.frame_my_main, show="*", font=FONT)
        self.entry_password.place(x=S_W / 1440 * (400 + 200), y=S_H / 900 * 500, width=WIDTH, height=HEIGHT)

        self.entry_password.focus()

    def edit_email(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.entry_email = Entry(self.frame_my_main, font=FONT)
        self.entry_email.place(x=S_W / 1440 * (400 + 200), y=S_H / 900 * 600, width=WIDTH, height=HEIGHT)

        self.entry_email.focus()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def get_operatorlogin(self):
        logindata = OperatorDatabase()
        latest_user = logindata.get_loginData()
        return latest_user

    def confirm_username(self):
        new_username = self.entry_username.get()
        # insert new username to database
        self.update_username_in_database(new_username)
        self.btn_confirm_username.pack_forget()
        messagebox.showinfo("success window", "Edit Username Successful !")
        self.entry_username.destroy()
        self.ll_username["text"] = new_username

    def confirm_password(self):
        new_password = self.entry_password.get()
        # insert new password to database
        self.update_password_in_database(new_password)
        self.btn_confirm_password.pack_forget()
        messagebox.showinfo("success window", "Edit Password Successful !")
        self.entry_password.destroy()
        self.ll_password["text"] = "**********"

    def confirm_email(self):
        new_email = self.entry_email.get()
        # insert new email to database
        self.update_email_in_database(new_email)
        self.btn_confirm_email.pack_forget()
        messagebox.showinfo("success window", "Edit Email Successful !")
        self.entry_email.destroy()
        self.ll_email["text"] = new_email

    def update_username_in_database(self, new_username):
        operator_id = self.get_operatorlogin()[2]
        try:
            self.cursor.execute("UPDATE Operator SET username = ? WHERE operator_id = ?",
                                (new_username, operator_id))
            self.conn.commit()
            print("Username updated successfully!")
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

    def update_password_in_database(self, new_password):
        operator_id = self.get_operatorlogin()[2]
        try:
            self.cursor.execute("UPDATE Operator SET password = ? WHERE operator_id = ?",
                                (new_password, operator_id))
            self.conn.commit()
            print("Password updated successfully!")
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

    def update_email_in_database(self, new_email):
        operator_id = self.get_operatorlogin()[2]
        try:
            self.cursor.execute("UPDATE Operator SET email = ? WHERE operator_id = ?",
                                (new_email, operator_id))
            self.conn.commit()
            print("Email updated successfully!")
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

    def fmy_main(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.l_title = Label(self.frame_my_main, text='MY ACCOUNT', font=FONT_TITLE)
        self.l_title.place(x=S_W / 1440 * 500, y=S_H / 900 * 100)

        # get logindata
        logindata = self.get_operatorlogin()
        self.l_operatorid = Label(self.frame_my_main, text='Operator ID:', font=FONT)
        self.l_operatorid.place(x=S_W / 1440 * 400, y=S_H / 900 * 300)
        self.l_oid = Label(self.frame_my_main, text="{}".format(logindata[2]), font=FONT)
        self.l_oid.place(x=S_W / 1440 * (400 + 200), y=S_H / 900 * 300, width=WIDTH, height=HEIGHT)
        # get login information
        logindata = self.get_operatorlogin()

        self.l_username = Label(self.frame_my_main, text='Username:', font=FONT)
        self.l_username.place(x=S_W / 1440 * 400, y=S_H / 900 * 400)
        self.ll_username = Label(self.frame_my_main, text="{}".format(logindata[3]), font=FONT)
        self.ll_username.place(x=S_W / 1440 * (400 + 200), y=S_H / 900 * 400, width=WIDTH, height=HEIGHT)

        self.l_password = Label(self.frame_my_main, text='Password:', font=FONT)
        self.l_password.place(x=S_W / 1440 * 400, y=S_H / 900 * 500)
        self.ll_password = Label(self.frame_my_main, text="**********", font=FONT)
        self.ll_password.place(x=S_W / 1440 * (400 + 200), y=S_H / 900 * 500, width=WIDTH, height=HEIGHT)

        self.l_email = Label(self.frame_my_main, text='Email:', font=FONT)
        self.l_email.place(x=S_W / 1440 * 400, y=S_H / 900 * 600)
        self.ll_email = Label(self.frame_my_main, text="{}".format(logindata[4]), font=FONT)
        self.ll_email.place(x=S_W / 1440 * (400 + 200), y=S_H / 900 * 600, width=WIDTH, height=HEIGHT)

        self.btn_edit_username = Button(self.frame_my_main, text="Edit", font=FONT,
                                        command=self.edit_username)
        self.btn_edit_username.place(x=S_W / 1440 * 950, y=S_H / 900 * 400, width=100, height=50)

        self.btn_edit_password = Button(self.frame_my_main, text="Edit", font=FONT,
                                        command=self.edit_password)
        self.btn_edit_password.place(x=S_W / 1440 * 950, y=S_H / 900 * 500, width=100, height=50)

        self.btn_edit_email = Button(self.frame_my_main, text="Edit", font=FONT,
                                     command=self.edit_email)
        self.btn_edit_email.place(x=S_W / 1440 * 950, y=S_H / 900 * 600, width=100, height=50)

        # add 3 confim button in fmy_main
        self.btn_confirm_username = Button(self.frame_my_main, text="Confirm", font=FONT, command=self.confirm_username)
        self.btn_confirm_username.place(x=S_W / 1440 * 1070, y=S_H / 900 * 400, width=100, height=50)
        self.btn_confirm_username.pack_forget()

        self.btn_confirm_password = Button(self.frame_my_main, text="Confirm", font=FONT, command=self.confirm_password)
        self.btn_confirm_password.place(x=S_W / 1440 * 1070, y=S_H / 900 * 500, width=100, height=50)
        self.btn_confirm_password.pack_forget()

        self.btn_confirm_email = Button(self.frame_my_main, text="Confirm", font=FONT, command=self.confirm_email)
        self.btn_confirm_email.place(x=S_W / 1440 * 1070, y=S_H / 900 * 600, width=100, height=50)
        self.btn_confirm_email.pack_forget()


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

        original_image = Image.open("logo.png")
        resized_image = original_image.resize((250, 62), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(resized_image)
        self.logo_label = Label(self.master, image=self.logo)
        self.logo_label.photo = self.logo
        self.logo_label.place(x=10, y=60)

        # init frame
        self.track = Track(self.frame_track)
        self.charge = Charge(self.frame_charge)
        self.repair = Repair(self.frame_repair)
        self.move = Move(self.frame_move)
        self.my = My(self.frame_my)
        self.show_frame_track()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def reset_btn_bg(self):
        for btn in self.btns:
            btn.configure(bg='SystemButtonFace')

    def show_frame_track(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_track.configure(bg='lightpink')
        self.frame_track.pack()

    def show_frame_charge(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_charge.configure(bg='lightpink')
        self.frame_charge.pack()

    def show_frame_repair(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_repair.configure(bg='lightpink')
        self.frame_repair.pack()

    def show_frame_move(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_move.configure(bg='lightpink')
        self.frame_move.pack()

    def show_frame_my(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_my.configure(bg='lightpink')
        self.frame_my.pack()

    def show(self):
        self.master.mainloop()


if __name__ == '__main__':
    c = OperatorUI()
    c.show()
