#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Date    : 2019-10-28 23:45:49
# @Author  : Dong (dongwei@tamu.edu)
# @Link    : https://github.com/tomatoJr
# @Version : 1.0.0

import os
from tkinter import *
import pymysql
import xlrd
import random
from tkinter import messagebox
import time
import datetime
import re


from db import *
from entry_interface import *
from main_window import *
from return_interface import *
from user_interface import *


def fine_mani_interface(master, db, user_id, identification):

    fine_mani_interface_frame = Frame(master)
    fine_mani_interface_frame.pack(expand=YES, fill=BOTH)

    style = ttk.Style()
    style.configure('TButton', foreground='black', background='blue')
    cursor = db.cursor()

    Label(fine_mani_interface_frame, text='Check your fine tickets here:').pack()

    sql = "select * from "+identification+"_Fine_History where " + \
        identification+"_id="+str(user_id)+" and status='unpaid'"
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result)
    amount = 0
    for item in result:
        amount += item[5]
    Label(fine_mani_interface_frame,
          text='Total fine is :$'+str(amount)+".").pack()

    def pay_fine():
        sql = "update "+identification+"_Fine_History set status='paid' where " + \
            identification+"_id="+str(user_id)
        # print(sql)
        cursor.execute(sql)
        db.commit()

        messagebox.showinfo(title='Successfully Paid',
                            message="Your fine has been paid")
        fine_mani_interface_frame.destroy()
        user_mani_interface(master, db, user_id, identification)

        # fine_mani_interface(db, user_id, identification)

    button = ttk.Button(fine_mani_interface_frame,
                        text='pay it now', command=pay_fine)
    button.pack()
