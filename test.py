import datetime as DT
import random
import threading
import time
import serial
from serial.tools import list_ports
from tkinter import *
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import messagebox
from collections import deque
from queue import Empty
from queue import Queue
from time import time as timer
from time import sleep
import numpy as np
from functools import partial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import date2num
from matplotlib.figure import Figure

root = tk.Tk()

def start_polling_loop(root, in_data_queue, delay):
    n = 500
        
    fig, ax = plt.subplots()   7
    
    line, = ax.step(x_data, y_data)    
    # second graph
    
    line2, = ax.step(x_data2, y_data2)
    line3, = ax.step(x_data3, y_data3)
    line4, = ax.step(x_data4, y_data4)
    line5, = ax.step(x_data5, y_data5)
    line6, = ax.step(x_data6, y_data6)
    line7, = ax.step(x_data7, y_data7)
    line8, = ax.step(x_data8, y_data8)
    

    # add to GUI
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.    
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # update in a loop
    def loop():
        timeout_millis = 45
        root.after(timeout_millis, loop)  # avoid drift
                
        try:
            in_data_queue.get(block=False)
        except Empty:
            return  # no new data
                
        # update plot      
        line.set_xdata(x_data)
        line.set_ydata(y_data)   
        
        # second graph
        
        line2.set_xdata(x_data2)
        line2.set_ydata(y_data2)  
        
        line3.set_xdata(x_data3)
        line3.set_ydata(y_data3)  
        
        line4.set_xdata(x_data4)
        line4.set_ydata(y_data4) 
        
        line5.set_xdata(x_data5)
        line5.set_ydata(y_data5) 
        
        line6.set_xdata(x_data6)
        line6.set_ydata(y_data6)  
        
        line7.set_xdata(x_data7)
        line7.set_ydata(y_data7)  
        
        line8.set_xdata(x_data8)
        line8.set_ydata(y_data8)    
        
        
        ax.relim()  # update axes limits
        ax.autoscale_view(True, True, True)
        canvas.draw()
        active_channel_color = 'Orange'
        off_channel_color = 'Black'
        print(break_ch[0])   
        
        if (break_ch[0] & 0b00000001) == 0b00000001:
            label['bg'] = off_channel_color
        else:
            label['bg'] = active_channel_color
        if (break_ch[0] & 0b00000010) == 0b00000010:
            label2['bg'] = off_channel_color
        else:
            label2['bg'] = active_channel_color 
        if (break_ch[0] & 0b00000100) == 0b00000100:
            label3['bg'] = off_channel_color 
        else:
            label3['bg'] = active_channel_color
        if (break_ch[0] & 0b00001000) == 0b00001000:
            label4['bg'] = off_channel_color
        else:
            label4['bg'] = active_channel_color
        if (break_ch[0] & 0b00010000) == 0b00010000:
            label5['bg'] = off_channel_color
        else:
            label5['bg'] = active_channel_color
        if (break_ch[0] & 0b00100000) == 0b00100000: 
            label6['bg'] = off_channel_color
        else: 
            label6['bg'] = active_channel_color
        if (break_ch[0] & 0b01000000) == 0b01000000:  
            label7['bg'] = off_channel_color 
        else:  
            label7['bg'] = active_channel_color
        if (break_ch[0] & 0b10000000) == 0b10000000:   
            label8['bg'] = off_channel_color 
        else:  
            label8['bg'] = active_channel_color
            
    root.after_idle(loop) 

def parser_payload(content, r):
    if content[0] == 0x06:
        if content[1] == 0x09:
            if len(content) >= 37:
                adc_parser(content, r) 
        else:
            print('Other command')
    else:
        print('Fail')
    return
    

def adc_parser(content, r):
    bytes_buff = bytearray(34)
    ch_data = bytearray(4)
    mult = 0
    ranges = 1200
    x = 0
    index_1 = 5
    index_2 = 9   
    break_ch[0] = 0b00000000
    while x != 8:
        ch_data.clear()
        
        tick = 0
        bytes_buff = content[index_1 :index_2]
        first = bytes_buff[0]
        first >>= 1
        second = bytes_buff[1]
        temp = second & 0b00000001
        temp <<= 7
        first |= temp
        second >>= 1
        
        ch_data.append(first)
        
        third = bytes_buff[2]
        temp = third & 0b00000001
        temp <<= 7   
        second |= temp
        third >>= 1
        ch_data.append(second)
        
        fourth_b = bytes_buff[3]
        temp = fourth_b & 0b00000010
        temp <<= 6
        third |= temp 
        
        ch_data.append(third)
    
        number = fourth_b & 0b00011100
        number >>= 2
        
        sign = fourth_b & 0b10000000
        sign >>= 7
        
        index_1 += 4
        index_2 += 4        
        
        ch1_data = int.from_bytes(ch_data[0:3], 'little')
        
        if 0 != (ch1_data & (1 << 23)):
            ch1_data |= ~(0xFFFFFF);   
            
        ch1 = ch1_data>>6 
        
        if number == 0:
            if sign == 1:
                break_ch[0] |= 0b00000001
            x_data.append(x_data[-1] + 1)
            y_data.append(ch1+ mult * ranges)
        elif number == 1:
            if sign == 1:
                break_ch[0] |= 0b00000010
            x_data2.append(x_data2[-1] + 1)
            y_data2.append(ch1+ mult * ranges)
        elif number == 2:
            if sign == 1:
                break_ch[0] |= 0b00000100
            x_data3.append(x_data3[-1] + 1)
            y_data3.append(ch1+ mult * ranges)
        elif number == 3:
            if sign == 1:
                break_ch[0] |= 0b00001000
            x_data4.append(x_data4[-1] + 1)
            y_data4.append(ch1+ mult * ranges)
        elif number == 4:
            if sign == 1:
                break_ch[0] |= 0b00010000
            x_data5.append(x_data5[-1] + 1)
            y_data5.append(ch1+ mult * ranges)
        elif number == 5:
            if sign == 1:
                break_ch[0] |= 0b00100000
            x_data6.append(x_data6[-1] + 1)
            y_data6.append(ch1+ mult * ranges)
        elif number == 6:
            if sign == 1:
                break_ch[0] |= 0b01000000
            x_data7.append(x_data7[-1] + 1)
            y_data7.append(ch1+ mult * ranges)
        else:
            if sign == 1:
                break_ch[0] |= 0b10000000
            x_data8.append(x_data8[-1] + 1)
            y_data8.append(ch1+ mult * ranges) 
        mult +=1
        x += 1
    in_data_queue.put(ch1_data>>2)
        
def main_parser(r):
    global ser
    global parser_stat
    LENGTH = 0
    reads = bytearray(100)
    content = bytearray(1000)
    read_buff = bytearray(100)
    while True:
        if parser_stat == 1:    #STX
                while ser.inWaiting() < 1:
                    sleep(0.001)
                read_buff = ser.read(1)
                if read_buff[0] != 0x03:
                    continue
                reads.clear()
                content.clear()
                reads += read_buff
                parser_stat += 1
            
            
        elif parser_stat == 2:  #LENGTH
                while ser.inWaiting() < 4:
                    if parser_stat == 1:
                        continue                    
                    sleep(0.001)
                read_buff = ser.read(4)
                LENGTH = int.from_bytes(read_buff[0:3], 'little')
                reads += read_buff
                parser_stat += 1  
                
        elif parser_stat == 3:
                while ser.inWaiting() < LENGTH:
                    if parser_stat == 1:
                        continue                    
                    sleep(0.001)
                read_buff = ser.read(LENGTH)
                content += read_buff
                reads += read_buff
                parser_stat += 1
                
        elif parser_stat == 4:
                while ser.inWaiting() < 4:
                    if parser_stat == 1:
                        continue                    
                    sleep(0.001)
                read_buff = ser.read(4)
                reads += read_buff
                parser_stat += 1     
                
        elif parser_stat == 5:         
                while ser.inWaiting() < 1:
                    if parser_stat == 1:
                        continue                    
                    sleep(0.001)
                read_buff = ser.read(1)
                if read_buff[0] != 0x04:
                    parser_stat = 1                    
                    continue
                reads += read_buff            
                parser_payload(content, r)
                parser_stat = 1
        
def start():
    try:   
        global ser
        global select_port
        global parser_stat
        
        if ser.isOpen():
            print("Comport ",select_port,": start")
            mess = bytearray([0x03, 0x02, 0x00, 0x00, 0x00, 0x09, 0x55, 0x11, 0x22, 0x33, 0x44, 0x04])    
            ser.write(mess)    
            parser_stat = 1
    except serial.SerialException as ex:
            print ('Port is unavailable: ', select_port)     
   
def stop():
    try:   
        global ser
        global select_port
        global parser_stat
        
        if ser.isOpen():        
            print("Comport ", select_port,": stop")
            mess = bytearray([0x03, 0x02, 0x00, 0x00, 0x00, 0x08, 0x55, 0x11, 0x22, 0x33, 0x44, 0x04])    
            ser.write(mess)        
            parser_stat = 1
            
    except:
            print ('Port is unavailable: ', select_port)  
    
    
def open_port():
    try:
        global ser
        global select_port
        global parser_stat
        ser = serial.Serial((combo.get().split())[0], baudrate=9600)
        if ser.isOpen():           
            select_port = (combo.get().split())[0]
            print("Comport",(combo.get().split())[0],"is open")
            
            if parser_thread.is_alive() == False:
                
                print("Start parser")
                parser_stat = 1
                parser_thread.start()
                     
    except:
            print ('Port is unavailable: ', (combo.get().split())[0])     


npoints = 1000

x_data = deque([0], maxlen=npoints)
x_data2 = deque([0], maxlen=npoints)
x_data3 = deque([0], maxlen=npoints)
x_data4 = deque([0], maxlen=npoints)
x_data5 = deque([0], maxlen=npoints)
x_data6 = deque([0], maxlen=npoints)
x_data7 = deque([0], maxlen=npoints)
x_data8 = deque([0], maxlen=npoints)

y_data = deque([0], maxlen=npoints)

y_data2 = deque([0], maxlen=npoints)
y_data3 = deque([0], maxlen=npoints)
y_data4 = deque([0], maxlen=npoints)
y_data5 = deque([0], maxlen=npoints)
y_data6 = deque([0], maxlen=npoints)
y_data7 = deque([0], maxlen=npoints)
y_data8 = deque([0], maxlen=npoints)


ser = serial

parser_stat = 1
select_port = "COM1"

in_data_queue = Queue()

break_ch = bytearray(1)

start_polling_loop(root, in_data_queue, delay=20)

btn = Button(root, text="Старт", command = start)  
btn.place(x ="10",y="1")  
btn2 = Button(root, text="Стоп", command = stop)  
btn2.place(x ="54",y="1")  
btn3 = Button(root, text="Открыть", command = open_port)  
btn3.place(x ="100",y="1")  

combo = Combobox(root)  
combo['values'] = list(list_ports.comports())
combo.current(0)
combo.place(x ="200",y="1")

label = Label(root,text = "№1",width=2, height=1)
label.place(x ="380",y="10")
label2 = Label(root,text = "№2",width=2, height=1)
label2.place(x ="400",y="10")
label3 = Label(root,text = "№3",width=2, height=1)
label3.place(x ="420",y="10")
label4 = Label(root,text = "№4",width=2, height=1)
label4.place(x ="440",y="10")
label5 = Label(root,text = "№5",width=2, height=1)
label5.place(x ="460",y="10")
label6 = Label(root,text = "№6",width=2, height=1)
label6.place(x ="480",y="10")
label7 = Label(root,text = "№7",width=2, height=1)
label7.place(x ="500",y="10")
label8 = Label(root,text = "№8",width=2, height=1)
label8.place(x ="520",y="10")

parser_thread = threading.Thread(target = main_parser,
     args=[root],
     daemon=True)

root.mainloop()