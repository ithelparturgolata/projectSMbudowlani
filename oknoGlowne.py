from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview
# -*- coding: utf-8 -*-
import mysql.connector
from tkinter import messagebox
from smsapi.client import SmsApiPlClient
from smsapi.exception import SmsApiException
import os
from oknoBudynek import *

def open_window():
    top = Toplevel()
    # top.title("top window")
    # top.geometry("300x300+120+120")
    # button1 = Button(top, text="close", command=top.destroy)
    # button1.pack()


root = Tk()
button = Button(root, text="open window", command=open_window)
button.pack()

root.geometry("300x300+120+120")
root.mainloop()