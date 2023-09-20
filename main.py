# encoding=utf-8
from collections import namedtuple
from time import sleep
from re import search, match
from json import dump
import tkinter
from tkinter import *
import json
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pydirectinput
import webbrowser


class Macro(object):
    def __init__(self, macro, listener, icon1, bg1):
        self.macro = macro
        self.listener = listener
        self.icon1 = icon1
        self.bg1 = bg1

    def main_gui(self):

        def open_file(file):
            webbrowser.open(file)

        def on_press(s):
            global listener
            print(s)
            #if s == Key.esc:
            #    listener.stop()  # stop listener

            try:
                k = s.char  # single-char keys
            except:
                k = s.name  # other keys

            canvas1.itemconfigure(text3, text=k)
            if k in macro:  # keys of interest
                print_macro(k)

        def print_macro(k):
            keyboard = Controller()
            keyboard.type('c') #chat
            sleep(1.0)
            keyboard.type(macro[k])
            sleep(0.8)
            pydirectinput.press('enter')

        def on_start():
            button2["state"] = NORMAL
            button2.config(bg='white')
            button1["state"] = DISABLED
            button1.config(bg='gray80')
            global listener

            if not listener:
                canvas1.itemconfigure(text1, text="Start listener...")
                print("Start listener...")
                listener = keyboard.Listener(on_press=on_press)
                listener.start()  # start thread
            else:
                print("listener already running")

        def on_stop():
            button1["state"] = NORMAL
            button1.config(bg='white')
            button2["state"] = DISABLED
            button2.config(bg='gray80')
            canvas1.itemconfigure(text3, text="")
            global listener

            if listener:
                canvas1.itemconfigure(text1, text="Stop listener...")
                print("Stop listener...")
                listener.stop()  # stop thread
                listener.join()  # wait till thread really ends its job
                listener = None  # to inform that listener doesn't exist
            else:
                print("listener not running")

        # Create object
        root = Tk()
        # Title
        root.title("ACC Shortcuts")
        # Adjust size
        root.geometry("500x300")
        # No resize
        root.resizable(False, False)
        # Icon
        try:
            root.iconbitmap("icon.ico")
        except:
            root.iconbitmap(icon1)

        # Create Canvas
        canvas1 = Canvas(root, width=500, height=300)
        canvas1.pack(fill="both", expand=True)

        # Display image
        try:
            with open('bg.png') as f:
                # Add image file
                bg = PhotoImage(file="bg.png")
                canvas1.create_image(0, 0, image=bg, anchor="nw")
        except FileNotFoundError:
            bg = PhotoImage(data=bg1)
            canvas1.create_image(0, 0, image=bg, anchor="nw")

        canvas1.create_rectangle(10, 290, 90, 270, fill='black')

        # Add Text
        text1 = canvas1.create_text(440, 280, font=("Arial", 10), text="Waiting to start", fill = 'white')
        text2 = canvas1.create_text(410, 36, font=("Purisa", 12), text="ACC Shortcuts", fill = 'white')
        text3 = canvas1.create_text(15, 280, font=("Arial", 10), text="", fill = 'white', anchor='w')

        # Create Buttons
        button1 = Button(root, text="START", bg='white', fg='black', command=on_start)
        button2 = Button(root, text="STOP", bg='gray80', fg='black', command=on_stop, state = DISABLED)
        button3 = Button(root, text="Config", bg='white', command= lambda: open_file("macro.json"))
        button4 = Button(root, text="Help", bg='white', command= lambda: open_file("help.txt"))

        # Display Buttons
        button1_canvas = canvas1.create_window(150, 120,
                                               anchor="nw",
                                               height=50,
                                               width=200,
                                               window=button1)

        button2_canvas = canvas1.create_window(150, 170,
                                               anchor="nw",
                                               height=50,
                                               width=200,
                                               window=button2)

        button3_canvas = canvas1.create_window(150, 220,
                                               anchor="nw",
                                               height=50,
                                               width=100,
                                               window=button3)

        button4_canvas = canvas1.create_window(250, 220,
                                               anchor="nw",
                                               height=50,
                                               width=100,
                                               window=button4)

        root.mainloop()


listener = None  # to keep listener
# stop listener if it was created
if listener:  # if listener is not None:
    print("Stop listener...")
    listener.stop()  # stop thread
    listener.join()  # wait till thread really ends its job
try:
    with open('macro.json') as json_file:
        macro = json.load(json_file)
except FileNotFoundError:
        base = '{"4": "Sorry","5": "Good race","6": "Thanks!"}'
        file = open("macro.json", "w")
        file.write(base)
        file.close()
        macro = json.loads(base)


icon1 = ""
bg1 = ""

ins_bill = Macro(macro, listener, icon1, bg1)
ins_bill.main_gui()
