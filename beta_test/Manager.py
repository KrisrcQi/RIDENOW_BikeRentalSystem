from tkinter import *
from tkinter import Frame, Button
import sqlite3
import datetime
from dateutil.relativedelta import relativedelta
import math
from tkinter import ttk
from tkinter import Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

FONT = ('Arial', 15)
FONT_TOP = ('Arial', 20, 'bold')
FONT_TITLE = ('Arial', 50, 'bold')

HEIGHT = 50
WIDTH = 300

def gain_date():

    # generate date
    now = datetime.datetime.now()
    year = now.year
    dates = []
    for month in range(1, 13):
        for day in range(1, 32):
            try:
                date = datetime.datetime(year, month, day)
                dates.append(date.strftime("%Y-%m-%d"))
            except ValueError:
                pass
    return dates


class Rental:
    def __init__(self, master) -> None:
        self.master = master
        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()

        # create frames
        self.frame_rental_main = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_rental_main]

        self.init_frame()
        self.show_frame_rental_main()

    def init_frame(self):
        self.frental_main()

    def show_frame_rental_main(self):
        self.forget_all()
        self.frame_rental_main.pack()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def frental_main(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        # Create buttons with initial state set to "normal"
        self.btn_numofbike = Button(self.frame_rental_main, text="Number of bike rented by date", font=FONT,
                                    command=self.show_numofbike)
        self.btn_numofbike.state = "normal"  # Add a state attribute
        self.btn_income = Button(self.frame_rental_main, text="Income by date", font=FONT,
                                 command=self.Income_bar)
        self.btn_income.state = "normal"
        self.btn_cost = Button(self.frame_rental_main, text="Cost by date", font=FONT,
                               command=self.cost_bar)
        self.btn_cost.state = "normal"
        self.btn_profit = Button(self.frame_rental_main, text="Profit by date", font=FONT,
                                 command=self.btn_profit_line)
        self.btn_profit.state = "normal"
        # place buttons
        self.btn_numofbike.place(x=S_W / 1440 * 50, y=S_H / 900 * 250, width=300, height=50)
        self.btn_income.place(x=S_W / 1440 * 50, y=S_H / 900 * 350, width=300, height=50)
        self.btn_cost.place(x=S_W / 1440 * 50, y=S_H / 900 * 450, width=300, height=50)
        self.btn_profit.place(x=S_W / 1440 * 50, y=S_H / 900 * 550, width=300, height=50)

    def btn_profit_line(self):
        # after click button, clear all windows opened
        self.close_all()

        self.btn_numofbike.state = "normal"
        self.btn_numofbike.configure(bg='SystemButtonFace')
        self.btn_income.state = "normal"
        self.btn_income.configure(bg='SystemButtonFace')
        self.btn_cost.state = "normal"
        self.btn_cost.configure(bg='SystemButtonFace')
        self.btn_profit.state = "clicked"  # Set the state of the clicked button
        self.btn_profit.configure(bg='lightpink')

        # create labels, combobox
        self.numofbike_start_time = StringVar()
        self.numofbike_end_time = StringVar()
        all_date = gain_date()
        self.numofbike_start_select_l = Label(self.frame_rental_main, text="start time:", font=FONT)
        self.numofbike_end_select_l = Label(self.frame_rental_main, text="end time:", font=FONT)
        self.numofbike_start_select = ttk.Combobox(self.frame_rental_main, values=all_date,
                                                   textvariable=self.numofbike_start_time)
        self.numofbike_end_select = ttk.Combobox(self.frame_rental_main, values=all_date,
                                                 textvariable=self.numofbike_end_time)
        # create search bar buttons
        self.btn_numofbike_search = Button(self.frame_rental_main, text="Search", font=FONT,
                                           command=self.cost_bar_line)

        # place components
        self.numofbike_start_select.place(x=500, y=120, width=200, height=40)
        self.numofbike_end_select.place(x=900, y=120, width=200, height=40)
        self.numofbike_start_select_l.place(x=350, y=120, width=200, height=40)
        self.numofbike_end_select_l.place(x=750, y=120, width=200, height=40)
        self.btn_numofbike_search.place(x=1200, y=120, width=100, height=40)
        self.cost_bar_line()

    def cost_bar(self):
        # after click button, clear all windows opened
        self.close_all()

        self.btn_numofbike.state = "normal"
        self.btn_numofbike.configure(bg='SystemButtonFace')
        self.btn_income.state = "normal"
        self.btn_income.configure(bg='SystemButtonFace')
        self.btn_profit.state = "normal"
        self.btn_profit.configure(bg='SystemButtonFace')
        self.btn_cost.state = "clicked"  # Set the state of the clicked button
        self.btn_cost.configure(bg='lightpink')

        # create labels and combobox
        self.numofbike_start_time = StringVar()
        self.numofbike_end_time = StringVar()
        all_date = gain_date()
        self.numofbike_start_select_l = Label(self.frame_rental_main, text="start time:", font=FONT)
        self.numofbike_end_select_l = Label(self.frame_rental_main, text="end time:", font=FONT)
        self.numofbike_start_select = ttk.Combobox(self.frame_rental_main, values=all_date,
                                                   textvariable=self.numofbike_start_time)
        self.numofbike_end_select = ttk.Combobox(self.frame_rental_main, values=all_date,
                                                 textvariable=self.numofbike_end_time)
        # create search bar button:
        self.btn_numofbike_search = Button(self.frame_rental_main, text="Search", font=FONT,
                                           command=self.cost_bar_search)

        # place components:
        self.numofbike_start_select.place(x=500, y=120, width=200, height=40)
        self.numofbike_end_select.place(x=900, y=120, width=200, height=40)
        self.numofbike_start_select_l.place(x=350, y=120, width=200, height=40)
        self.numofbike_end_select_l.place(x=750, y=120, width=200, height=40)
        self.btn_numofbike_search.place(x=1200, y=120, width=100, height=40)
        self.cost_bar_search()

    def cost_bar_line(self):
        numofbike_start_time = self.numofbike_start_time.get()
        numofbike_end_time = self.numofbike_end_time.get()
        if not numofbike_end_time:
            numofbike_end_time = datetime.datetime.now().strftime("%Y-%m-%d")
        time_list = []
        for i in range(7):
            numofbike_end_time = datetime.datetime.strptime(numofbike_end_time, "%Y-%m-%d")
            time_list.append(numofbike_end_time.strftime("%Y-%m-%d"))
            numofbike_end_time += relativedelta(days=-1)
            numofbike_end_time = numofbike_end_time.strftime("%Y-%m-%d")
            if numofbike_end_time == numofbike_start_time:
                time_list.append(numofbike_start_time)
                break
        time_list.reverse()
        conn = sqlite3.connect('RIDENOW.db')
        c = conn.cursor()
        x = []
        y = []
        sql = "SELECT DISTINCT(type) FROM Bike_info"
        records = list(c.execute(sql))
        for i in records:
            y.append([])
        type_list = [i[0] for i in records]
        for _time in time_list:
            for idx, _type in enumerate(type_list):
                start = _time + " 00:00:00"
                end = _time + " 23:59:59"
                sql = "SELECT start_time, end_time FROM Tracking INNER JOIN Bike_info ON Bike_info.bike_id=Tracking.bike_id "
                sql += "WHERE start_time>=? and end_time<=? and type=?"
                c.execute(sql, (start, end, _type))
                records = c.fetchall()
                hour = 0
                for d in records:
                    s_time = datetime.datetime.strptime(d[0][:19], "%Y-%m-%d %H:%M:%S")
                    e_time = datetime.datetime.strptime(d[1][:19], "%Y-%m-%d %H:%M:%S")
                    seconds = (e_time - s_time).seconds
                    _hour = math.ceil(seconds / 3600)
                    hour += 1 * 2 + (_hour - 1) * 1.5
                sql = "SELECT count(1) FROM Charge_history WHERE charge_time>=? and charge_time<=? and bike_type=?"
                c.execute(sql, (start, end, _type))
                cost = int(c.fetchone()[0]) * 10
                sql = "SELECT error_type FROM Repair_history inner join Bike_info on Bike_info.bike_id=Repair_history.bike_id WHERE repair_time>=? and repair_time<=? and type=?"
                c.execute(sql, (start, end, _type))
                records = c.fetchall()
                for error_type in records:
                    if error_type[0] == "Wheels":
                        cost += 15
                    elif error_type[0] == "seats":
                        cost += 20
                    elif error_type[0] == "fronts":
                        cost += 15
                    else:
                        cost += 10
                y[idx].append(hour - cost)
            x.append(_time)
        totalWidth = 0.5
        labelNums = len(y)
        barWidth = totalWidth / labelNums
        seriesNums = len(time_list)
        fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
        fig.subplots_adjust(bottom=0.2)
        for idx, i in enumerate(y):
            ax.plot(x, i)
            for _y, v in enumerate(i):
                ax.text(_y, v + 0.01, "{:}".format(int(v)), ha='center', va='bottom')
        ax.set_xticks([x + barWidth / 2 * (labelNums - 1) for x in range(seriesNums)], x)
        ax.set_title('profits for two bike types')
        ax.set_xlabel('date')
        ax.set_ylabel('Profit(GBP)')
        ax.legend(type_list, loc='upper right', fancybox=True, shadow=True)
        ax.set_ylim(min(min(i) for i in y) - 100, max([max(i) for i in y]) + 150)
        ax.tick_params(axis='x', labelrotation=-30)

        # put canvas in the tkinter
        self.numofbike_canvas = FigureCanvasTkAgg(fig, master=self.frame_rental_main)
        self.numofbike_canvas.draw()
        self.numofbike_canvas.get_tk_widget().place(x=400, y=205)

    def cost_bar_search(self):
        numofbike_start_time = self.numofbike_start_time.get()
        numofbike_end_time = self.numofbike_end_time.get()
        if not numofbike_end_time:
            numofbike_end_time = datetime.datetime.now().strftime("%Y-%m-%d")
        time_list = []
        for i in range(7):
            numofbike_end_time = datetime.datetime.strptime(numofbike_end_time, "%Y-%m-%d")
            time_list.append(numofbike_end_time.strftime("%Y-%m-%d"))
            numofbike_end_time += relativedelta(days=-1)
            numofbike_end_time = numofbike_end_time.strftime("%Y-%m-%d")
            if numofbike_end_time == numofbike_start_time:
                time_list.append(numofbike_start_time)
                break
        time_list.reverse()
        conn = sqlite3.connect('RIDENOW.db')
        c = conn.cursor()
        x = []
        y = []
        sql = "select distinct(type) from Bike_info"
        records = list(c.execute(sql))
        for i in records:
            y.append([])
        type_list = [i[0] for i in records]
        for _time in time_list:
            for idx, _type in enumerate(type_list):
                start = _time
                end = _time
                sql = "select count(1) from Charge_history where charge_date>='{}' and charge_date<='{}' and bike_type='{}'".format(start, end, _type)
                c.execute(sql)
                cost = int(c.fetchone()[0]) * 10
                sql = "select error_type from Repair_history inner join Bike_info on Bike_info.bike_id=Repair_history.bike_id where repair_date>=? and repair_date<=? and type=?"
                c.execute(sql, (start, end, _type))
                records = c.fetchall()
                for error_type in records:
                    if error_type[0] == "Wheels":
                        cost += 15
                    elif error_type[0] == "seats":
                        cost += 20
                    elif error_type[0] == "fronts":
                        cost += 15
                    else:
                        cost += 10
                y[idx].append(cost)
            x.append(_time)
        totalWidth = 0.5
        labelNums = len(y)
        barWidth = totalWidth / labelNums
        seriesNums = len(time_list)
        fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
        fig.subplots_adjust(bottom=0.2)
        for idx, i in enumerate(y):
            ax.bar([x + barWidth * idx for x in range(seriesNums)], height=i, width=barWidth)
            for _y, v in enumerate(i):
                ax.text(_y + barWidth * idx + 0.05, v + 0.01, "{:}".format(int(v)), ha='center', va='bottom')
        ax.set_xticks([x + barWidth / 2 * (labelNums - 1) for x in range(seriesNums)], x)
        ax.set_title('costs for two bike types')
        ax.set_xlabel('date')
        ax.set_ylabel('cost(GBP)')
        ax.legend(type_list, loc='upper right', fancybox=True, shadow=True)
        ax.set_ylim(0, max([max(i) for i in y]) + 100)
        ax.tick_params(axis='x', labelrotation=-30)

        # put canvas in the tkinter
        self.numofbike_canvas = FigureCanvasTkAgg(fig, master=self.frame_rental_main)
        self.numofbike_canvas.draw()
        self.numofbike_canvas.get_tk_widget().place(x=400, y=205)

    def Income_bar_search(self):
        numofbike_start_time = self.numofbike_start_time.get()
        numofbike_end_time = self.numofbike_end_time.get()
        if not numofbike_end_time:
            numofbike_end_time = datetime.datetime.now().strftime("%Y-%m-%d")
        time_list = []
        for i in range(7):
            numofbike_end_time = datetime.datetime.strptime(numofbike_end_time, "%Y-%m-%d")
            time_list.append(numofbike_end_time.strftime("%Y-%m-%d"))
            numofbike_end_time += relativedelta(days=-1)
            numofbike_end_time = numofbike_end_time.strftime("%Y-%m-%d")
            if numofbike_end_time == numofbike_start_time:
                time_list.append(numofbike_start_time)
                break
        time_list.reverse()
        conn = sqlite3.connect('RIDENOW.db')
        c = conn.cursor()
        x = []
        y = []
        sql = "select distinct(type) from Bike_info"
        records = list(c.execute(sql))
        for i in records:
            y.append([])
        type_list = [i[0] for i in records]
        for _time in time_list:
            for idx, _type in enumerate(type_list):
                start = _time + " 00:00:00"
                end = _time + " 23:59:59"
                sql = "select start_time,end_time from Tracking inner join Bike_info on Bike_info.bike_id=Tracking.bike_id "
                sql += "where start_time>=? and end_time<=? and type=?"
                c.execute(sql, (start, end, _type))
                records = c.fetchall()
                hour = 0
                for d in records:
                    s_time = datetime.datetime.strptime(d[0][:19], "%Y-%m-%d %H:%M:%S")
                    e_time = datetime.datetime.strptime(d[1][:19], "%Y-%m-%d %H:%M:%S")
                    seconds = (e_time - s_time).seconds
                    first_10_second = 10
                    # Calculate the income with the price setting: first hour: 2 Pounds, later hour: 1.5 Pounds/hour
                    # Test price setting is first 10 seconds: 10 Pounds, later price: 0.2 Pounds/second
                    # # Define pricing
                    first_10s_price = 10
                    additional_price = 1
                    # Calculate rent cost:
                    if seconds <= first_10_second:
                        hour += first_10s_price
                    else:
                        hour += first_10s_price + (seconds - first_10_second) * additional_price

                y[idx].append(hour)
            x.append(_time)
        totalWidth = 0.5
        labelNums = len(y)
        barWidth = totalWidth / labelNums
        seriesNums = len(time_list)
        fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
        fig.subplots_adjust(bottom=0.2)
        for idx, i in enumerate(y):
            ax.bar([x + barWidth * idx for x in range(seriesNums)], height=i, width=barWidth)
            for _y, v in enumerate(i):
                ax.text(_y + barWidth * idx + 0.05, v + 0.01, "{:}".format(int(v)), ha='center', va='bottom')
        ax.set_xticks([x + barWidth / 2 * (labelNums - 1) for x in range(seriesNums)], x)
        ax.set_title('Income for two bike')
        ax.set_xlabel('date')
        ax.set_ylabel('income(GBP)')
        ax.legend(type_list, loc='upper right', fancybox=True, shadow=True)
        ax.set_ylim(0, max([max(i) for i in y]) + 300)
        ax.tick_params(axis='x', labelrotation=-30)

        # put canvas in the tkinter
        self.numofbike_canvas = FigureCanvasTkAgg(fig, master=self.frame_rental_main)
        self.numofbike_canvas.draw()
        self.numofbike_canvas.get_tk_widget().place(x=400, y=205)

    def close_all(self):
        try:
            self.numofbike_start_select_l.destroy()
            self.numofbike_end_select_l.destroy()
            self.numofbike_start_select.destroy()
            self.numofbike_end_select.destroy()
            self.btn_numofbike_search.destroy()
        except Exception as e:
            pass

    def Income_bar(self):

        self.close_all()

        self.btn_numofbike.state = "normal"
        self.btn_numofbike.configure(bg='SystemButtonFace')
        self.btn_profit.state = "normal"
        self.btn_profit.configure(bg='SystemButtonFace')
        self.btn_cost.state = "normal"
        self.btn_cost.configure(bg='SystemButtonFace')
        self.btn_income.state = "clicked"  # Set the state of the clicked button
        self.btn_income.configure(bg='lightpink')

        self.numofbike_start_time = StringVar()
        self.numofbike_end_time = StringVar()
        all_date = gain_date()
        self.numofbike_start_select_l = Label(self.frame_rental_main, text="start time:", font=FONT)
        self.numofbike_end_select_l = Label(self.frame_rental_main, text="end time:", font=FONT)
        self.numofbike_start_select = ttk.Combobox(self.frame_rental_main, values=all_date,
                                                   textvariable=self.numofbike_start_time)
        self.numofbike_end_select = ttk.Combobox(self.frame_rental_main, values=all_date,
                                                 textvariable=self.numofbike_end_time)
        self.btn_numofbike_search = Button(self.frame_rental_main, text="Search", font=FONT,
                                           command=self.Income_bar_search)

        self.numofbike_start_select.place(x=500, y=120, width=200, height=40)
        self.numofbike_end_select.place(x=900, y=120, width=200, height=40)
        self.numofbike_start_select_l.place(x=350, y=120, width=200, height=40)
        self.numofbike_end_select_l.place(x=750, y=120, width=200, height=40)
        self.btn_numofbike_search.place(x=1200, y=120, width=100, height=40)
        self.Income_bar_search()

    def numofbike_search(self):
        numofbike_start_time = self.numofbike_start_time.get()
        numofbike_end_time = self.numofbike_end_time.get()
        if not numofbike_end_time:
            numofbike_end_time = datetime.datetime.now().strftime("%Y-%m-%d")
        time_list = []
        for i in range(7):
            numofbike_end_time = datetime.datetime.strptime(numofbike_end_time, "%Y-%m-%d")
            time_list.append(numofbike_end_time.strftime("%Y-%m-%d"))
            numofbike_end_time += relativedelta(days=-1)
            numofbike_end_time = numofbike_end_time.strftime("%Y-%m-%d")
            if numofbike_end_time == numofbike_start_time:
                time_list.append(numofbike_start_time)
                break
        time_list.reverse()
        conn = sqlite3.connect('RIDENOW.db')
        c = conn.cursor()
        x = []
        y = []
        sql = "select distinct(type) from Bike_info"
        records = list(c.execute(sql))
        for i in records:
            y.append([])
        type_list = [i[0] for i in records]
        for _time in time_list:
            for idx, _type in enumerate(type_list):
                start = _time + " 00:00:00"
                end = _time + " 23:59:59"
                sql = "select count(1) from Tracking inner join Bike_info on Bike_info.bike_id=Tracking.bike_id  "
                sql += " where start_time>=? and end_time<=? and type=?"
                c.execute(sql, (start, end, _type))
                count = c.fetchone()[0]
                y[idx].append(count)
            x.append(_time)
        totalWidth = 0.5
        labelNums = len(y)
        barWidth = totalWidth / labelNums
        seriesNums = len(time_list)
        fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
        fig.subplots_adjust(bottom=0.2)
        for idx, i in enumerate(y):
            ax.bar([x + barWidth * idx for x in range(seriesNums)], height=i, width=barWidth)
            for _y, v in enumerate(i):
                ax.text(_y + barWidth * idx + 0.01, v + 0.01, "{:}".format(int(v)), ha='center', va='bottom')
        ax.set_xticks([x + barWidth / 2 * (labelNums - 1) for x in range(seriesNums)], x)
        ax.set_title('number of two bike types rented')
        ax.set_xlabel('date')
        ax.set_ylabel('number of bikes')
        ax.legend(type_list, loc='upper right', fancybox=True, shadow=True)
        ax.set_ylim(0, max([max(i) for i in y]) + 30)
        ax.tick_params(axis='x', labelrotation=-30)

        # put canvas in the tkinter
        self.numofbike_canvas = FigureCanvasTkAgg(fig, master=self.frame_rental_main)
        self.numofbike_canvas.draw()
        self.numofbike_canvas.get_tk_widget().place(x=400, y=205)

    def show_numofbike(self):

        self.btn_profit.state = "normal"
        self.btn_profit.configure(bg='SystemButtonFace')
        self.btn_income.state = "normal"
        self.btn_income.configure(bg='SystemButtonFace')
        self.btn_cost.state = "normal"
        self.btn_cost.configure(bg='SystemButtonFace')
        self.btn_numofbike.state = "clicked"  # Set the state of the clicked button)
        self.btn_numofbike.configure(bg='lightpink')

        self.numofbike_start_time = StringVar()
        self.numofbike_end_time = StringVar()
        all_date = gain_date()
        self.numofbike_start_select_l = Label(self.frame_rental_main, text="start time:", font=FONT)
        self.numofbike_end_select_l = Label(self.frame_rental_main, text="end time:", font=FONT)
        self.numofbike_start_select = ttk.Combobox(self.frame_rental_main, values=all_date,
                                                   textvariable=self.numofbike_start_time)
        self.numofbike_end_select = ttk.Combobox(self.frame_rental_main, values=all_date,
                                                 textvariable=self.numofbike_end_time)
        self.numofbike_start_select.place(x=500, y=120, width=200, height=40)
        self.numofbike_end_select.place(x=900, y=120, width=200, height=40)
        self.numofbike_start_select_l.place(x=350, y=120, width=200, height=40)
        self.numofbike_end_select_l.place(x=750, y=120, width=200, height=40)
        self.btn_numofbike_search = Button(self.frame_rental_main, text="Search", font=FONT,
                                           command=self.numofbike_search)
        self.btn_numofbike_search.place(x=1200, y=120, width=100, height=40)
        self.numofbike_search()



class Location:
    def __init__(self, master) -> None:
        self.master = master
        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()

        # create frames
        self.frame_location_main = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_location_main]

        self.init_frame()
        self.show_frame_location_main()

    def init_frame(self):
        self.flocation_main()

    def show_frame_location_main(self):
        self.forget_all()
        self.frame_location_main.pack()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def flocation_main(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        # create frequency plot
        self.plot_graph(S_W, S_H)

    def plot_graph(self, S_W, S_H):
        conn = sqlite3.connect('RIDENOW.db')
        c = conn.cursor()
        c.execute('SELECT name, num_bike, electric_bike, electric_scooter FROM Parking_lot')
        data = c.fetchall()
        data = sorted(data, key=lambda x: x[1])  # 可以根据你的需要修改排序依据
        names = [row[0] for row in data]
        num_bikes = [row[1] for row in data]
        electric_bikes = [row[2] for row in data]
        electric_scooters = [row[3] for row in data]

        fig, ax = plt.subplots(figsize=(12, 7))
        fig.subplots_adjust(left=0.3, right=0.9, bottom=0.1, top=0.9)
        barHeight = 0.25
        r1 = range(len(names))
        r2 = [x - barHeight for x in r1]
        r3 = [x - 2 * barHeight for x in r1]

        # 先绘制 num_bikes
        bars1 = ax.barh(r1, num_bikes, color='#fcbad3', height=barHeight, edgecolor='grey', label='num_bike')

        # 然后绘制 electric_bikes 和 electric_scooters
        bars2 = ax.barh(r2, electric_bikes, color='#aa96da', height=barHeight, edgecolor='grey', label='electric_bike')
        bars3 = ax.barh(r3, electric_scooters, color='#a8d8ea', height=barHeight, edgecolor='grey', label='electric_scooter')

        ax.set_title('Number of Bikes/Scooters in Each Location')
        ax.set_xlabel('Counts', fontweight='bold')
        ax.set_ylabel('Location', fontweight='bold')
        ax.set_yticks([r for r in range(len(num_bikes))])
        ax.set_yticklabels(names)
        ax.legend()


        canvas = FigureCanvasTkAgg(fig, master=self.frame_location_main)
        canvas.draw()
        canvas.get_tk_widget().place(x=100, y=150)


class Maintenance:
    def __init__(self, master) -> None:
        self.master = master
        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()

        # create frames
        self.frame_maintenance_main = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_maintenance_main]

        self.init_frame()
        self.show_frame_maintenance_main()

    def init_frame(self):
        self.fmaintenance_main()

    def show_frame_maintenance_main(self):
        self.forget_all()
        self.frame_maintenance_main.pack()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def fmaintenance_main(self):
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.show_percent_repaired(S_W, S_H)

    def show_percent_repaired(self, S_W=None, S_H=None):
        conn = sqlite3.connect('RIDENOW.db')
        c = conn.cursor()
        bike_types = ["electric_bike", "electric_scooter"]
        fig, axs = plt.subplots(1, 2, figsize=(12, 6))

        for i, bike_type in enumerate(bike_types):
            c.execute('''
                SELECT repair_message, COUNT(repair_message)
                FROM Error_journal
                WHERE bike_type = ?
                GROUP BY repair_message
            ''', (bike_type,))

            data = c.fetchall()
            messages = [row[0] for row in data]
            counts = [row[1] for row in data]

            axs[i].pie(counts, labels=messages, autopct='%1.1f%%', startangle=140)
            axs[i].set_title(f'Distribution of Repair Messages ({bike_type})')

        conn.close()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_maintenance_main)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=110, y=150)
        canvas.draw()

    def plot_graph(self, S_W, S_H):
        conn = sqlite3.connect('RIDENOW.db')
        c = conn.cursor()
        c.execute('SELECT name, num_bike, electric_bike, electric_scooter FROM Parking_lot')
        data = c.fetchall()
        data = sorted(data, key=lambda x: x[1])  # 可以根据你的需要修改排序依据
        names = [row[0] for row in data]
        num_bikes = [row[1] for row in data]
        electric_bikes = [row[2] for row in data]
        electric_scooters = [row[3] for row in data]

        fig, ax = plt.subplots(figsize=(12, 7))
        barWidth = 0.25
        r1 = range(len(names))
        r2 = [x + barWidth for x in r1]
        r3 = [x + barWidth for x in r2]

        bars1 = ax.bar(r1, num_bikes, color='b', width=barWidth, edgecolor='grey', label='num_bike')
        bars2 = ax.bar(r2, electric_bikes, color='r', width=barWidth, edgecolor='grey', label='electric_bike')
        bars3 = ax.bar(r3, electric_scooters, color='g', width=barWidth, edgecolor='grey', label='electric_scooter')

        ax.set_title('Number of Bikes/Scooters in Each Location')
        ax.set_xlabel('Location', fontweight='bold')
        ax.set_ylabel('Counts', fontweight='bold')
        ax.set_xticks([r + barWidth for r in range(len(num_bikes))])
        ax.set_xticklabels(names)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_location_main)
        canvas.draw()
        canvas.get_tk_widget().place(x=100, y=100)



class ManagerUI:

    def __init__(self) -> None:

        self.master = Tk()
        self.master.title("Manager")

        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()

        self.master.geometry(f"{S_W}x{S_H}")
        self.font = ('Arial', 14)

        # create frames
        self.frame_rental = Frame(self.master, width=S_W, height=S_H)
        self.frame_location = Frame(self.master, width=S_W, height=S_H)
        self.frame_maintenance = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_rental, self.frame_location, self.frame_maintenance]

        self.btn_rental = Button(self.master, text='Rental Data', font=FONT_TOP, command=self.show_frame_rental)
        # command=self.show_frame_track,
        self.btn_rental.place(x=0, y=0, width=S_W / 3., height=HEIGHT)
        # command = self.show_frame_track
        self.btn_location = Button(self.master, text='Location Management', font=FONT_TOP,
                                   command=self.show_frame_location)
        self.btn_location.place(x=S_W / 3, y=0, width=S_W / 3., height=HEIGHT)
        self.btn_maintenance = Button(self.master, text='Maintenance Data', font=FONT_TOP,
                                      command=self.show_frame_maintenance)
        self.btn_maintenance.place(x=S_W / 3 * 2, y=0, width=S_W / 3., height=HEIGHT)
        self.btns = [self.btn_rental, self.btn_location, self.btn_maintenance]

        original_image = Image.open("logo.png")
        resized_image = original_image.resize((250, 62), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(resized_image)
        self.logo_label = Label(self.master, image=self.logo)
        self.logo_label.photo = self.logo
        self.logo_label.place(x=10, y=60)

        self.my = Rental(self.frame_rental)
        self.my = Location(self.frame_location)
        self.my = Maintenance(self.frame_maintenance)
        #
        self.show_frame_rental()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def reset_btn_bg(self):
        for btn in self.btns:
            btn.configure(bg='SystemButtonFace')

    def show_frame_rental(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_rental.configure(bg='lightpink')
        self.frame_rental.pack()

    def show_frame_location(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_location.configure(bg='lightpink')
        self.frame_location.pack()

    def show_frame_maintenance(self):
        self.forget_all()
        self.reset_btn_bg()
        self.btn_maintenance.configure(bg='lightpink')
        self.frame_maintenance.pack()

    def show(self):
        self.master.mainloop()


if __name__ == '__main__':
    c = ManagerUI()
    c.show()
