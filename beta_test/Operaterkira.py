from tkinter import *
from tkinter import ttk
from tkinter import messagebox

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
    def __init__(self) -> None:
        pass

class Move:
    def __init__(self) -> None:
        pass

class My:
    def __init__(self) -> None:
        pass




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
        # self.repair = Repair(self.frame_repair)
        # self.move = Move(self.frame_move)
        # self.my = My(self.frame_my)
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
