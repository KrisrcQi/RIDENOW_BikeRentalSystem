from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage


FONT = ('Arial', 20)  #文本大小

FONT_TOP=('Arial', 20,'bold') #顶部框字体大小

FONT_TITLE=('Arial', 50,'bold')  #中部标题大小

# 每个entry/选项框大小
HEIGHT=50
WIDTH=300


#OPERATOR
class Track:
    def __init__(self) -> None:
        pass


class Charge:
    def __init__(self, master) -> None:

        self.master = master

        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()
        print("The current opening window size is: {}x{}".format(S_W, S_H))
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

    # 选择list的select all
    def select_all(self):
        return

    # 确认充电,充电成功小弹窗，自动跳转回charge界面
    def confim_charge(self):
        result = messagebox.askyesno("Confirm", "Confirm Charge？")
        if result:  # 如果用户点击了确认按钮
            self.ShowSuccess()

    def ShowSuccess(self):
        success_window = Tk()
        success_window.title("success window")
        label = Label(success_window, text="Charge Successful !",font=FONT)
        label.place(x=0, y=50)
        success_window.geometry("250x150+575+325")
        self.show_frame_charge_main()

    def fcharge_main(self):

        self.l_location = Label(self.frame_charge_main, text='Location:', font=FONT)
        self.l_location.place(x=150, y=150)
        self.comb_location = ttk.Combobox(self.frame_charge_main)
        self.comb_location.place(x=150+150, y=150, width=WIDTH, height=HEIGHT)

        self.l_type = Label(self.frame_charge_main, text='Bike Type:', font=FONT)
        self.l_type.place(x=300+WIDTH+150, y=150)
        self.comb_type = ttk.Combobox(self.frame_charge_main)
        self.comb_type.place(x=300+WIDTH+300, y=150, width=WIDTH, height=HEIGHT)

        self.l_box = Label(self.frame_charge_main, text='List of Information:',font=FONT)
        self.l_box.place(x=150, y=250)
        self.listbox = Listbox(self.frame_charge_main)
        self.listbox.place(x=150, y=300, width=1100, height=400)

        self.btn_selectall = Button(self.frame_charge_main, text="[]Select All", font=FONT,
                                    command=self.select_all)
        self.btn_selectall.place(x=150, y=700, width=WIDTH, height=HEIGHT)

        self.btn_charge = Button(self.frame_charge_main, text="Charge", font=FONT,
                                    command=self.show_frame_charge_confirm)
        self.btn_charge.place(x=950, y=700, width=WIDTH, height=HEIGHT)

        self.btn_history = Button(self.frame_charge_main, text="History", font=FONT,
                                 command=self.show_frame_charge_history)
        self.btn_history.place(x=1120, y=60, width=WIDTH, height=HEIGHT)

    def fcharge_confirm(self):
        self.l_title = Label(self.frame_charge_confirm, text='CONFIRM CHARGE', font=FONT_TITLE)
        self.l_title.place(x=400, y=100)

        self.l_operatorid = Label(self.frame_charge_confirm, text='Operator ID:', font=FONT)
        self.l_operatorid.place(x=500, y=300)
        self.l_oid = Label(self.frame_charge_confirm, text='XXXX', font=FONT)
        self.l_oid.place(x=500 + 200, y=300)

        self.l_location = Label(self.frame_charge_confirm, text='Location:', font=FONT)
        self.l_location.place(x=500, y=400)
        self.comb_location = ttk.Combobox(self.frame_charge_confirm)
        self.comb_location.place(x=500 + 200, y=400, width=WIDTH, height=HEIGHT)

        self.l_date = Label(self.frame_charge_confirm, text='Date:', font=FONT)
        self.l_date.place(x=500, y=500)
        self.entry_date = Entry(self.frame_charge_confirm)
        self.entry_date.place(x=500 + 200, y=500, width=WIDTH, height=HEIGHT)

        self.btn_return = Button(self.frame_charge_confirm, text="Return", font=FONT,
                                 command=self.show_frame_charge_main)
        self.btn_return.place(x=400, y=600, width=WIDTH, height=HEIGHT)

        self.btn_confirm = Button(self.frame_charge_confirm, text="Confirm", font=FONT,
                                  command=self.confim_charge)
        self.btn_confirm.place(x=750, y=600, width=WIDTH, height=HEIGHT)


    def fcharge_history(self):
        self.l_title = Label(self.frame_charge_history, text='CHARGE HISTORY', font=FONT_TITLE)
        self.l_title.place(x=400, y=100)

        self.l_date = Label(self.frame_charge_history, text='Date:', font=FONT)
        self.l_date.place(x=150, y=200)
        self.comb_date = ttk.Combobox(self.frame_charge_history)
        self.comb_date.place(x=150 + 150, y=200, width=WIDTH, height=HEIGHT)

        self.l_type = Label(self.frame_charge_history, text='Bike Type:', font=FONT)
        self.l_type.place(x=300 + WIDTH + 150, y=200)
        self.comb_type = ttk.Combobox(self.frame_charge_history)
        self.comb_type.place(x=300 + WIDTH + 300, y=200, width=WIDTH, height=HEIGHT)

        self.l_box = Label(self.frame_charge_history, text='List of Information:', font=FONT)
        self.l_box.place(x=150, y=300)
        self.listbox = Listbox(self.frame_charge_history)
        self.listbox.place(x=150, y=350, width=1100, height=400)

        self.btn_return = Button(self.frame_charge_history, text="Return", font=FONT,
                                  command=self.show_frame_charge_main)
        self.btn_return.place(x=150, y=760, width=WIDTH, height=HEIGHT)


class Repair:
    def __init__(self, master) -> None:
        self.master = master

        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()

        # create frames
        self.frame_repair_main = Frame(self.master, width=S_W, height=S_H)
        self.frame_repair_detail = Frame(self.master, width=S_W, height=S_H)
        self.frame_repair_detail_his = Frame(self.master, width=S_W, height=S_H)
        self.frame_repair_confirm = Frame(self.master, width=S_W, height=S_H)
        self.frame_repair_history = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_repair_main, self.frame_repair_detail, self.frame_repair_confirm,self.frame_repair_history,self.frame_repair_detail_his]

        self.init_frame()
        self.show_frame_repair_main()

    def forget_all(self):
        for frame in self.frames:
            frame.pack_forget()

    def show_frame_repair_main(self):
        self.forget_all()
        self.frame_repair_main.pack()

    def show_frame_repair_detail(self):
        self.forget_all()
        self.frame_repair_detail.pack()

    def show_frame_repair_detail_his(self):
        self.forget_all()
        self.frame_repair_detail_his.pack()

    def show_frame_repair_confirm(self):
        self.forget_all()
        self.frame_repair_confirm.pack()

    def show_frame_repair_history(self):
        self.forget_all()
        self.frame_repair_history.pack()

    def init_frame(self):
        self.frepair_main()
        self.frepair_detail()
        self.frepair_detail_his()
        self.frepair_confirm()
        self.frepair_history()




    def confim_repair(self):
        result = messagebox.askyesno("Confirm", "Confirm Repair？")
        if result:  # 如果用户点击了确认按钮
            self.ShowSuccess()

    def ShowSuccess(self):
        success_window = Tk()
        success_window.title("success window")
        label = Label(success_window, text="Repair Successful !",font=FONT)
        label.place(x=0, y=50)
        success_window.geometry("250x150+575+325")
        self.show_frame_repair_main()


    def frepair_main(self):

        self.l_location = Label(self.frame_repair_main, text='Location:', font=FONT)
        self.l_location.place(x=150, y=150)
        self.comb_location = ttk.Combobox(self.frame_repair_main)
        self.comb_location.place(x=150+150, y=150, width=WIDTH, height=HEIGHT)

        self.l_type = Label(self.frame_repair_main, text='Bike Type:', font=FONT)
        self.l_type.place(x=300+WIDTH+150, y=150)
        self.comb_type = ttk.Combobox(self.frame_repair_main)
        self.comb_type.place(x=300+WIDTH+300, y=150, width=WIDTH, height=HEIGHT)

        self.l_box = Label(self.frame_repair_main, text='List of Information:',font=FONT)
        self.l_box.place(x=150, y=250)
        self.listbox = Listbox(self.frame_repair_main)
        self.listbox.place(x=150, y=300, width=1100, height=400)

        # 现在先用button实现进入detail界面功能，以后通过每一条具体信息进入detail界面
        self.btn_detail = Button(self.frame_repair_main, text="Detail", font=FONT,
                                  command=self.show_frame_repair_detail)
        self.btn_detail.place(x=150, y=400, width=1100, height=HEIGHT)

        self.btn_history = Button(self.frame_repair_main, text="History", font=FONT,
                                 command=self.show_frame_repair_history)
        self.btn_history.place(x=1120, y=60, width=WIDTH, height=HEIGHT)

    def frepair_detail(self):
        self.l_title = Label(self.frame_repair_detail, text='REPAIR DETAIL', font=FONT_TITLE)
        self.l_title.place(x=450, y=100)

        self.l_bikeid = Label(self.frame_repair_detail, text='Bike ID:', font=FONT)
        self.l_bikeid.place(x=500, y=200)
        self.l_bid = Label(self.frame_repair_detail, text='XXXX', font=FONT)
        self.l_bid.place(x=500 + 200, y=200)

        self.l_biketype = Label(self.frame_repair_detail, text='Bike Type:', font=FONT)
        self.l_biketype.place(x=500, y=300)
        self.l_btype = Label(self.frame_repair_detail, text='type 1', font=FONT)
        self.l_btype.place(x=500 + 200, y=300)

        self.l_errortype = Label(self.frame_repair_detail, text='Error Type:', font=FONT)
        self.l_errortype.place(x=500, y=400)
        self.l_etype = Label(self.frame_repair_detail, text='type 11', font=FONT)
        self.l_etype.place(x=500 + 200, y=400)

        self.l_picture = Label(self.frame_repair_detail, text='Picture:', font=FONT)
        self.l_picture.place(x=500, y=500)

        self.test = PhotoImage(file="pic.png")
        self.lp = Label(self.frame_repair_detail, image=self.test)
        self.lp.place(x=500 + 200, y=500, width=200, height=150)

        self.btn_return = Button(self.frame_repair_detail, text="Return", font=FONT,
                                 command=self.show_frame_repair_main)
        self.btn_return.place(x=400, y=700, width=WIDTH, height=HEIGHT)

        self.btn_confirm = Button(self.frame_repair_detail, text="Confirm", font=FONT,
                                  command=self.show_frame_repair_confirm)
        self.btn_confirm.place(x=750, y=700, width=WIDTH, height=HEIGHT)

    def frepair_detail_his(self):
        self.l_title = Label(self.frame_repair_detail_his, text='REPAIR DETAIL', font=FONT_TITLE)
        self.l_title.place(x=450, y=100)

        self.l_bikeid = Label(self.frame_repair_detail_his, text='Bike ID:', font=FONT)
        self.l_bikeid.place(x=500, y=200)
        self.l_bid = Label(self.frame_repair_detail_his, text='XXXX', font=FONT)
        self.l_bid.place(x=500 + 200, y=200)

        self.l_biketype = Label(self.frame_repair_detail_his, text='Bike Type:', font=FONT)
        self.l_biketype.place(x=500, y=300)
        self.l_btype = Label(self.frame_repair_detail_his, text='type 1', font=FONT)
        self.l_btype.place(x=500 + 200, y=300)

        self.l_errortype = Label(self.frame_repair_detail_his, text='Error Type:', font=FONT)
        self.l_errortype.place(x=500, y=400)
        self.l_etype = Label(self.frame_repair_detail_his, text='type 11', font=FONT)
        self.l_etype.place(x=500 + 200, y=400)

        self.l_picture = Label(self.frame_repair_detail_his, text='Picture:', font=FONT)
        self.l_picture.place(x=500, y=500)
        self.test = PhotoImage(file="pic.png")
        self.lp = Label(self.frame_repair_detail_his, image=self.test)
        self.lp.place(x=500 + 200, y=500, width=200, height=150)

        self.btn_return = Button(self.frame_repair_detail_his, text="Return", font=FONT,
                                 command=self.show_frame_repair_history)
        self.btn_return.place(x=400, y=700, width=WIDTH, height=HEIGHT)


    def frepair_confirm(self):
        self.l_title = Label(self.frame_repair_confirm, text='CONFIRM REPAIR', font=FONT_TITLE)
        self.l_title.place(x=400, y=100)

        self.l_operatorid = Label(self.frame_repair_confirm, text='Operator ID:', font=FONT)
        self.l_operatorid.place(x=500, y=250)
        self.l_oid = Label(self.frame_repair_confirm, text='1111', font=FONT)
        self.l_oid.place(x=500 + 200, y=250)

        self.l_bikeid = Label(self.frame_repair_confirm, text='Bike ID:', font=FONT)
        self.l_bikeid.place(x=500, y=350)
        self.l_bid = Label(self.frame_repair_confirm, text='232', font=FONT)
        self.l_bid.place(x=500 + 200, y=350)

        self.l_location = Label(self.frame_repair_confirm, text='Location:', font=FONT)
        self.l_location.place(x=500, y=450)
        self.comb_location = ttk.Combobox(self.frame_repair_confirm)
        self.comb_location.place(x=500+200,y=450 , width=WIDTH, height=HEIGHT)

        self.l_date = Label(self.frame_repair_confirm, text='Date:', font=FONT)
        self.l_date.place(x=500, y=550)
        self.entry_date = Entry(self.frame_repair_confirm)
        self.entry_date.place(x=500+200, y=550, width=WIDTH, height=HEIGHT)

        # 现在先用button实现进入detail界面功能，以后通过每一条具体信息进入detail界面
        self.btn_return = Button(self.frame_repair_confirm, text="Return", font=FONT,
                                 command=self.show_frame_repair_detail)
        self.btn_return.place(x=400, y=700, width=WIDTH, height=HEIGHT)

        self.btn_return = Button(self.frame_repair_confirm, text="Confirm", font=FONT,
                                 command=self.confim_repair)
        self.btn_return.place(x=750, y=700, width=WIDTH, height=HEIGHT)

    def frepair_history(self):

        self.l_title = Label(self.frame_repair_history, text='REPAIR HISTORY', font=FONT_TITLE)
        self.l_title.place(x=400, y=100)

        self.l_date = Label(self.frame_repair_history, text='Date:', font=FONT)
        self.l_date.place(x=150, y=200)
        self.comb_date = ttk.Combobox(self.frame_repair_history)
        self.comb_date.place(x=150 + 150, y=200, width=WIDTH, height=HEIGHT)

        self.l_type = Label(self.frame_repair_history, text='Bike Type:', font=FONT)
        self.l_type.place(x=300 + WIDTH + 150, y=200)
        self.comb_type = ttk.Combobox(self.frame_repair_history)
        self.comb_type.place(x=300 + WIDTH + 300, y=200, width=WIDTH, height=HEIGHT)

        self.l_box = Label(self.frame_repair_history, text='List of Information:', font=FONT)
        self.l_box.place(x=150, y=300)
        self.listbox = Listbox(self.frame_repair_history)
        self.listbox.place(x=150, y=350, width=1100, height=400)

        # 现在先用button实现进入detail界面功能，以后通过每一条具体信息进入detail界面
        self.btn_detail = Button(self.frame_repair_history, text="Detail", font=FONT,
                                 command=self.show_frame_repair_detail_his)
        self.btn_detail.place(x=150, y=500, width=1100, height=HEIGHT)

        self.btn_return = Button(self.frame_repair_history, text="Return", font=FONT,
                                  command=self.show_frame_repair_main)
        self.btn_return.place(x=150, y=760, width=WIDTH, height=HEIGHT)


class Move:
    def __init__(self, master) -> None:
        self.master = master

        S_W = master.winfo_screenwidth()
        S_H = master.winfo_screenheight()

        # create frames
        self.frame_move_main = Frame(self.master, width=S_W, height=S_H)
        self.frame_move_detail = Frame(self.master, width=S_W, height=S_H)
        #self.frame_repair_detail_his = Frame(self.master, width=S_W, height=S_H)
        self.frame_move_confirm = Frame(self.master, width=S_W, height=S_H)
        self.frame_move_history = Frame(self.master, width=S_W, height=S_H)
        self.frames = [self.frame_move_main, self.frame_move_detail, self.frame_move_confirm,self.frame_move_history]

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

    def show_frame_move_detail(self):
        self.forget_all()
        self.frame_move_detail.pack()

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
        label = Label(success_window, text="Move Successful !",font=FONT)
        label.place(x=0, y=50)
        success_window.geometry("250x150+575+325")
        self.show_frame_move_main()

    def init_frame(self):
        self.fmove_main()
        self.fmove_detail()
        self.fmove_confirm()
        self.fmove_history()


    def fmove_main(self):

        self.l_location = Label(self.frame_move_main, text='Location:', font=FONT)
        self.l_location.place(x=150, y=150)
        self.comb_location = ttk.Combobox(self.frame_move_main)
        self.comb_location.place(x=150+150, y=150, width=WIDTH, height=HEIGHT)

        self.l_type = Label(self.frame_move_main, text='Bike Type:', font=FONT)
        self.l_type.place(x=300+WIDTH+150, y=150)
        self.comb_type = ttk.Combobox(self.frame_move_main)
        self.comb_type.place(x=300+WIDTH+300, y=150, width=WIDTH, height=HEIGHT)

        self.l_box = Label(self.frame_move_main, text='List of Information:',font=FONT)
        self.l_box.place(x=150, y=250)
        self.listbox = Listbox(self.frame_move_main)
        self.listbox.place(x=150, y=300, width=1100, height=400)

        # 现在先用button实现进入detail界面功能，以后通过每一条具体信息进入detail界面
        self.btn_detail = Button(self.frame_move_main, text="Detail", font=FONT,
                                  command=self.show_frame_move_detail)
        self.btn_detail.place(x=150, y=400, width=1100, height=HEIGHT)

        self.btn_history = Button(self.frame_move_main, text="History", font=FONT,
                                 command=self.show_frame_move_history)
        self.btn_history.place(x=1120, y=60, width=WIDTH, height=HEIGHT)

    def fmove_detail(self):
        self.l_title = Label(self.frame_move_detail, text='MOVE DETAIL', font=FONT_TITLE)
        self.l_title.place(x=450, y=100)

        self.l_type = Label(self.frame_move_detail, text='Bike Type:', font=FONT)
        self.l_type.place(x=400, y=220)
        self.comb_type = ttk.Combobox(self.frame_move_detail)
        self.comb_type.place(x=400+200, y=220, width=WIDTH, height=HEIGHT)

        self.l_locationid= Label(self.frame_move_detail, text='Location ID:', font=FONT)
        self.l_locationid.place(x=400, y=320)
        self.l_lid = Label(self.frame_move_detail, text='1111', font=FONT)
        self.l_lid.place(x=400 + 200, y=320)

        self.l_box = Label(self.frame_move_detail, text='List of Information:',font=FONT)
        self.l_box.place(x=150, y=350)
        self.listbox = Listbox(self.frame_move_detail)
        self.listbox.place(x=150, y=400, width=1100, height=300)

        self.btn_return = Button(self.frame_move_detail, text="Return", font=FONT,
                                 command=self.show_frame_move_main)
        self.btn_return.place(x=400, y=700, width=WIDTH, height=HEIGHT)

        self.btn_confirm = Button(self.frame_move_detail, text="Confirm", font=FONT,
                                  command=self.show_frame_move_confirm)
        self.btn_confirm.place(x=750, y=700, width=WIDTH, height=HEIGHT)

    def fmove_confirm(self):
        self.l_title = Label(self.frame_move_confirm, text='CONFIRM REPAIR', font=FONT_TITLE)
        self.l_title.place(x=400, y=100)

        self.l_operatorid = Label(self.frame_move_confirm, text='Operator ID:', font=FONT)
        self.l_operatorid.place(x=300, y=250)
        self.l_oid = Label(self.frame_move_confirm, text='11111', font=FONT)
        self.l_oid.place(x=300 + 200, y=250)

        self.l_from = Label(self.frame_move_confirm, text='From:', font=FONT)
        self.l_from.place(x=300, y=350)
        self.comb_from = ttk.Combobox(self.frame_move_confirm)
        self.comb_from.place(x=300+200,y=350 , width=WIDTH, height=HEIGHT)

        self.to = Label(self.frame_move_confirm, text='To:', font=FONT)
        self.to.place(x=850, y=350)
        self.to = ttk.Combobox(self.frame_move_confirm)
        self.to.place(x=850+120,y=350 , width=WIDTH, height=HEIGHT)


        self.l_date = Label(self.frame_move_confirm, text='Date:', font=FONT)
        self.l_date.place(x=300, y=450)
        self.entry_date = Entry(self.frame_move_confirm)
        self.entry_date.place(x=300+200, y=450, width=WIDTH, height=HEIGHT)

        # 现在先用button实现进入detail界面功能，以后通过每一条具体信息进入detail界面
        self.btn_return = Button(self.frame_move_confirm, text="Return", font=FONT,
                                 command=self.show_frame_move_detail)
        self.btn_return.place(x=400, y=600, width=WIDTH, height=HEIGHT)

        self.btn_return = Button(self.frame_move_confirm, text="Confirm", font=FONT,
                                 command=self.confim_move)
        self.btn_return.place(x=750, y=600, width=WIDTH, height=HEIGHT)

    def fmove_history(self):
        self.l_title = Label(self.frame_move_history, text='MOVE HISTORY', font=FONT_TITLE)
        self.l_title.place(x=400, y=100)

        self.l_date = Label(self.frame_move_history, text='Date:', font=FONT)
        self.l_date.place(x=150, y=200)
        self.comb_date = ttk.Combobox(self.frame_move_history)
        self.comb_date.place(x=150 + 150, y=200, width=WIDTH, height=HEIGHT)

        self.l_type = Label(self.frame_move_history, text='Bike Type:', font=FONT)
        self.l_type.place(x=300 + WIDTH + 150, y=200)
        self.comb_type = ttk.Combobox(self.frame_move_history)
        self.comb_type.place(x=300 + WIDTH + 300, y=200, width=WIDTH, height=HEIGHT)

        self.l_box = Label(self.frame_move_history, text='List of Information:', font=FONT)
        self.l_box.place(x=150, y=300)
        self.listbox = Listbox(self.frame_move_history)
        self.listbox.place(x=150, y=350, width=1100, height=400)

        self.btn_return = Button(self.frame_move_history, text="Return", font=FONT,
                                  command=self.show_frame_move_main)
        self.btn_return.place(x=150, y=760, width=WIDTH, height=HEIGHT)


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
        self.l_title = Label(self.frame_my_main, text='MY ACCOUNT', font=FONT_TITLE)
        self.l_title.place(x=400, y=100)

        self.l_operatorid = Label(self.frame_my_main, text='Operator ID:', font=FONT)
        self.l_operatorid.place(x=400, y=300)
        self.l_oid = Label(self.frame_my_main, text='XXXX', font=FONT)
        self.l_oid.place(x=400 + 200, y=300)

        self.l_username = Label(self.frame_my_main, text='Username:', font=FONT)
        self.l_username.place(x=400, y=400)
        self.entry_username = Entry(self.frame_my_main)
        self.entry_username.place(x=400 + 200, y=400, width=WIDTH, height=HEIGHT)

        self.l_password = Label(self.frame_my_main, text='Password:', font=FONT)
        self.l_password.place(x=400, y=500)
        self.entry_password = Entry(self.frame_my_main)
        self.entry_password.place(x=400 + 200, y=500, width=WIDTH, height=HEIGHT)

        self.l_email = Label(self.frame_my_main, text='Email:', font=FONT)
        self.l_email.place(x=400, y=600)
        self.entry_email = Entry(self.frame_my_main)
        self.entry_email.place(x=400 + 200, y=600, width=WIDTH, height=HEIGHT)

        self.btn_edit_username = Button(self.frame_my_main, text="Edit", font=FONT,
                                        command=self.edit_username)
        self.btn_edit_username.place(x=950, y=400, width = 100, height = 50)

        self.btn_edit_password = Button(self.frame_my_main, text="Edit", font=FONT,
                                        command=self.edit_password)
        self.btn_edit_password.place(x=950, y=500, width = 100, height = 50)

        self.btn_edit_email = Button(self.frame_my_main, text="Edit", font=FONT,
                                     command=self.edit_email)
        self.btn_edit_email.place(x=950, y=600, width = 100, height = 50)




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
        self.frames = [self.frame_track, self.frame_charge, self.frame_repair,self.frame_move,self.frame_my]

        self.btn_track = Button(self.master, text='Track',
                            command=self.show_frame_track, font=FONT_TOP)
        self.btn_track.place(x=0, y=0, width=S_W/5., height=HEIGHT)

        self.btn_charge = Button(self.master, text='Charge',
                            command=self.show_frame_charge, font=FONT_TOP)
        self.btn_charge.place(x=S_W/5, y=0, width=S_W/5., height=HEIGHT)
        self.btn_repair = Button(self.master, text='Repair',
                                 command=self.show_frame_repair, font=FONT_TOP)
        self.btn_repair.place(x=S_W/5*2, y=0, width=S_W / 5., height=HEIGHT)
        self.btn_move = Button(self.master, text='Move',
                                 command=self.show_frame_move, font=FONT_TOP)
        self.btn_move.place(x=S_W/5*3, y=0, width=S_W / 5., height=HEIGHT)
        self.btn_my = Button(self.master, text='My',
                            command=self.show_frame_my, font=FONT_TOP)
        self.btn_my.place(x=S_W/5*4, y=0, width=S_W/5., height=HEIGHT)
        self.btns = [self.btn_track, self.btn_charge, self.btn_repair,self.btn_move,self.btn_my]

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
