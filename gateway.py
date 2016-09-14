#! /usr/bin/python3

import subprocess
import tkinter as Tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk as zz
import tkinter.filedialog

import sys
import time
import struct
import _thread as thread
from datetime import datetime
from PyLaz.PyLaz import *

# Initializing Parameter
LOGO = 'lazurite_mini_b.gif'
BLUE = '#99CCFF'
YELLOW = '#FFCC00'
RED = '#FF00FF'
WHITE = '#000000'
XSCALL = 180
YSCALL = 30

## quit event handler
start_flag = False

mac_menu =("Serial Monitor","Binary Monitor")
mac_combobox = zz.Combobox
mac_mode  = 0
separator =" "
on_cloud = False
def on_closing():
    if start_flag == False:
        if messagebox.askokcancel("Quit", "Do you want to quit??"):
            root.destroy()
    else:
        print("please stop gateway")
    
## Gateway Process
class Gateway():
    lazurite = PyLaz()

    def __init__(self):
        result = self.lazurite.open()
    def mac802154_unsupported_format(self,raw,size):
        print(datetime.today(),"unsupported format::",raw)

    def mac802154_SM(self,raw,size):
        global separator
        print(datetime.today(),"0x%04x"%raw["header"],"0x%02x"%raw["seq_num"],"0x%04x"%raw["rx_panid"],"0x%04x"%raw["rx_addr"],"0x%04x"%raw["tx_addr"],"%03d "%raw["rx_rssi"],raw["payload"].decode('utf-8'),sep=separator)

        return
    
    def mac802154_BM(self,raw,size):
        global separator
        header = struct.unpack_from('H',raw,0)[0]
        if header == 0xa821:
            seq = struct.unpack_from('B',raw,2)[0]
            rxPanid = struct.unpack_from('H',raw,3)[0]
            rxAddr = struct.unpack_from('H',raw,5)[0]
            txAddr = struct.unpack_from('H',raw,7)[0]
            rssi = struct.unpack_from('B',raw,size-1)[0]
            msg = ""
            print(datetime.today(),"0x%04x"%header,"0x%02x"%seq,"0x%04x"%rxPanid,"0x%04x"%rxAddr,"0x%04x"%txAddr,"%03d "%rssi,sep=separator,end=separator)
            for i in range(9,size-1):
                print(str("%02x"%struct.unpack_from('B',raw,i)[0]),sep="",end=separator)
            print("")
            return
        elif header == 0xa802:
            seq = struct.unpack_from('B',raw,2)[0]
            rxPanid = struct.unpack_from('H',raw,3)[0]
            rxAddr = struct.unpack_from('H',raw,5)[0]
            txAddr = struct.unpack_from('H',raw,7)[0]
            rssi = struct.unpack_from('B',raw,size-1)[0]
            print(datetime.today(),"0x%04x"%header,"0x%02x"%seq,"0x%04x"%rxPanid,"0x%04x"%rxAddr,"0x%04x"%txAddr,"%03d "%rssi,"(ACK)",sep=separator)
            return
        else:
            self.mac802154_unsupported_format(raw,size)
            
    
    def loop(self):
        global start_flag
        global mac_combobox
        print("      date/time            headr  seq  rxPan  rxAddr txAddr rssi data b\'(text)\'")
        print("--------------------------|------|----|------|------|------|----|----------------")
        while start_flag:
            size=self.lazurite.available()
            if size > 0 :
                data=self.lazurite.read()
                dispMode = mac_combobox.current()
                self.mac802154_SM(data,size)
            time.sleep(0.001)

    def start_receive(self,ch,panid,rate,pwr):
        self.lazurite.begin(ch,panid,rate,pwr)
        self.lazurite.rxEnable()

        thread.start_new_thread(self.loop,())
    
    def close_driver(self):
        self.lazurite.rxDisable()
        self.lazurite.close()

###### Frame Process
class Frame(Tk.Frame):
    def __init__(self, master=None):
        global start_flag
        Tk.Frame.__init__(self, master)


        
        self.gw = Gateway()

#### COMMAND DISPLAY
        self.panid= Tk.IntVar()
        self.panid=0xABCD
        self.PanidDisp= Tk.StringVar()
        self.PanidDisp.set(hex(self.panid))
        self.master.title('Lazurite Gateway')

        self.row_offset = 0

# DISPLAY LOGO
#        f_command = Tk.Frame(self, relief=Tk.RIDGE, bd=4)
        f_command = Tk.Frame(self,  bd=4)
        self.image= Tk.PhotoImage(file=LOGO)
        self.logoBackGround=Tk.Label(f_command, image=self.image, bg='gray', relief=Tk.RIDGE, anchor=Tk.W)
        f_cb = Tk.Frame(self,bd=4)
# DISPLAY Channel
        self.ch =36
        self.chNumberDisp = Tk.IntVar()
        self.chNumberDisp.set(self.ch)

        self.l_ch = Tk.Label(f_command,text="Ch", relief=Tk.RIDGE, anchor=Tk.W)
        self.t_ch = Tk.Entry(f_command,textvariable=self.chNumberDisp,width=10, relief=Tk.SUNKEN, bd=2, state=Tk.NORMAL)
        
        self.b_chIncButton = Tk.Button(f_command, font=('Helvetica', '6'), text='+', command=self.chInc)
        self.b_chDecButton = Tk.Button(f_command, font=('Helvetica', '6'), text='-', command=self.chDec)

# DISPLAY Power
        self.pwr = (1,20)
        
        self.l_pwr = Tk.Label(f_command,text="Pwr", relief=Tk.RIDGE, anchor=Tk.W)
        self.b_pwr = zz.Combobox(f_command,value=self.pwr, width=10,state="readonly")
        self.b_pwr.current(1)
        
# DISPLAY Rate
        self.rate = (50,100)

        self.l_rate = Tk.Label(f_command,text="Rate", relief=Tk.RIDGE, anchor=Tk.W)
        self.b_rate = zz.Combobox(f_command,value=self.rate, width=10,state="readonly")
        self.b_rate.current(1)



# DISPLAY PANID
        self.l_panid = Tk.Label(f_command,text="PANID", relief=Tk.RIDGE, anchor=Tk.W)
        self.t_panid = Tk.Entry(f_command,textvariable=self.PanidDisp,width=10, relief=Tk.SUNKEN, bd=2, state=Tk.NORMAL)

# DISPLAY Start/Stop Button         
        self.b_start = Tk.Button(f_command, text='Start', command=self.Start)
        self.b_stop = Tk.Button(f_command, text='Stop', command=self.Stop, state=Tk.DISABLED)


## Option check buttom
        self.ign = Tk.BooleanVar()
        self.c_ign = Tk.Checkbutton(f_command,text="Ignore address",variable=self.ign)

# DISPLAY display mode
        global mac_menu
        global mac_combobox
        global mac_mode

        mac_combobox=zz.Combobox(f_command,value=mac_menu,width=20,state="readonly")
        mac_combobox.current(mac_mode)

## InfoCorpus
#        self.InfoCorpus= Tk.PhotoImage(file='InfoCorpusLogo.gif')
#        self.ImageInforcopus = Tk.Label(f_command, image=self.InfoCorpus, bg='gray', relief=Tk.RIDGE)

        
# DISPLAY save log buttom
        self.b_savelog=Tk.Button(f_command, text='SAVE', command=self.Save, state=Tk.NORMAL)
        self.b_clearlog=Tk.Button(f_command, text='CLEAR LOG', command=self.Clear, state=Tk.NORMAL)

## Command Frame Location
        self.logoBackGround.grid(row=0,column=0)
        self.b_start.grid(row=0, column=4)
        self.b_stop.grid(row=0, column=5)

        self.l_ch.grid(row=2,column=0,sticky=Tk.W + Tk.E,pady=10)
        self.t_ch.grid(row=2,column=1,padx=20,sticky=Tk.W)
        self.b_chIncButton.grid(row=2, column=4, sticky=Tk.W + Tk.E + Tk.S)
        self.b_chDecButton.grid(row=2, column=5, sticky=Tk.W + Tk.E + Tk.S)

        self.l_pwr.grid(row=4,column=0,sticky=Tk.W + Tk.E,pady=10)
        self.b_pwr.grid(row=4,column=1,padx=20,sticky=Tk.W)

        self.l_rate.grid(row=5,column=0,sticky=Tk.W + Tk.E,pady=10)
        self.b_rate.grid(row=5,column=1,padx=20,sticky=Tk.W)

        self.l_panid.grid(row=6,column=0,sticky=Tk.W + Tk.E,pady=10)
        self.t_panid.grid(row=6,column=1,padx=20,sticky=Tk.W)

        '''self.c_ign.grid(row=0,column=6,sticky=Tk.W + Tk.E,padx=20)
        mac_combobox.grid(row=5,column=6,padx=20)
        '''
        self.b_savelog.grid(row=6,column=6,padx=20)
        self.b_clearlog.grid(row=6,column=7,padx=20)

#        self.ImageInforcopus.grid(row=0, column=8)

## LOG WINDOW
        global XSCALL
        global YSCALL
        f_log = Tk.Frame(self)
#        self.logText = Tk.StringVar()
#        self.logText.set("")
        self.s_logtext=ScrolledText(f_log,width=XSCALL, height=YSCALL)
        self.s_logtext.grid(sticky=Tk.W+Tk.E)
        self.s_logtext.write = self.write
        sys.stdout = self.s_logtext

## FRAME Location
        f_command.pack()
        f_log.pack()

    def write(self,str):
        self.s_logtext.insert(Tk.END,str)
        time.sleep(0.001)
        self.s_logtext.yview_scroll(str.count("\n") + 1, "units")

    def Start(self):
        global start_flag

        ## update parameters
        self.ch = self.chNumberDisp.get()
        self.pwr = int(self.b_pwr.get())
        self.rate = int(self.b_rate.get())
        self.panid = int(self.PanidDisp.get(),0)

        ## parameter check
        if self.ch < 24 or self.ch > 61:
            print("ch number error")
            return

        if self.pwr != 1 and self.pwr != 20:
            print("power error =",self.pwr)
            return

        if self.rate != 50 and self.rate != 100:
            print("rate error=",self.rate)
            return

        if self.panid <= 0 or self.panid > 0xffff:
            print("PANID error")
            return
        
        ## Start Gateway
        self.b_start.configure(state=Tk.DISABLED)
        self.b_stop.configure(state=Tk.NORMAL)
        self.b_chIncButton.configure(state=Tk.DISABLED)
        self.b_chIncButton.configure(state=Tk.DISABLED)
        self.logoBackGround.configure(bg=BLUE)
        self.b_savelog.configure(state=Tk.DISABLED)
        start_flag = True
        self.init_gateway()

        
    def Stop(self):
        global start_flag
        self.b_start.configure(state=Tk.NORMAL)
        self.b_stop.configure(state=Tk.DISABLED)
        self.b_chIncButton.configure(state=Tk.NORMAL)
        self.b_chIncButton.configure(state=Tk.NORMAL)
        self.logoBackGround.configure(bg='gray')
        self.b_savelog.configure(state=Tk.NORMAL)

        start_flag = False
        self.gw.close_driver()

        
    def chInc(self):
        self.ch = self.chNumberDisp.get()
        if self.ch < 61 and self.ch >= 24:
            self.ch += 1
        elif self.ch < 24:
            self.ch = 24
        else:
            self.ch = 61
        self.chSet()
            
    def chDec(self):
        self.ch = self.chNumberDisp.get()
        if self.ch <= 61 and self.ch > 24:
            self.ch -= 1
        elif self.ch > 61:
            self.ch = 61
        else:
            self.ch = 24
        self.chSet()
        
    def chSet(self):
        self.chNumberDisp.set(self.ch)

    def Clear(self):
        self.s_logtext.delete(1.0,Tk.END)

    def Save(self):
        filename = Tk.filedialog.asksaveasfile(filetypes = [('Log Files', ('.log'))])
        if filename != "":
            logfile = open(filename.name,mode = 'w')
            log_data = self.s_logtext.get(1.0,Tk.END)
            logfile.write(log_data)
            logfile.close()
        return
        
    def init_gateway(self):
        if self.ign.get():
            self.mode = 1
        else:
            self.mode = 0
        self.gw.start_receive(self.ch,self.panid,self.rate,self.pwr)

    def close(self):
        if self.dvice_open:
            self.gw.close_driver()

##### Main Process

if __name__ == '__main__':
    root = Tk.Tk()
    f = Frame(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    f.pack()
    f.mainloop()
