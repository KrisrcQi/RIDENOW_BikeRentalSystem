from tkinter import *

FONT = ('Arial', 20)



class window:
    def __init__(self) -> None:
        self.master = Tk()

        self.master.title("Customer")
        S_W = self.master.winfo_screenwidth()
        S_H = self.master.winfo_screenheight()
        self.master.geometry("{}x{}".format(S_W, S_H))

        # create label:
        self.l_bike_id = Label(self.master, text="Bike ID: ", font=FONT)
        self.l_bike_id_show = Label(self.master, text="", font=FONT)
        self.l_bike_type = Label(self.master, text="Bike Type: ", font=FONT)
        self.l_bike_type_show = Label(self.master, text="", font=FONT)
        self.l_start_location = Label(self.master, text="Start Location: ", font=FONT)
        self.l_start_location_show = Label(self.master, text="", font=FONT)
        self.l_end_location = Label(self.master, text="End Location: ", font=FONT)
        self.l_end_location_show = Label(self.master, text="", font=FONT)
        self.l_start_time = Label(self.master, text="Start Time: ", font=FONT)
        self.l_start_time_show = Label(self.master, text="", font=FONT)
        self.l_end_time = Label(self.master, text="End time: ", font=FONT)
        self.l_end_time_show = Label(self.master, text="", font=FONT)
        self.l_price = Label(self.master, text="Price: ", font=FONT)
        self.l_price_show = Label(self.master, text="", font=FONT)

        ## create buttons:
        self.btn_go_back_4 = Button(self.master, text="Return", font=FONT)

        # place components

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

    def show (self):
        self.master.mainloop()


window().show()