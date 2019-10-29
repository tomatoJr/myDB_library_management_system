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


from entry_interface import *
from main_window import *
from return_interface import *
from user_interface import *


def fine_mani_interface(db, user_id, identification):
        # create master
    master = Tk()
    master.title('library management system')
    master.geometry('400x200')

    style = ttk.Style()
    style.configure('TButton', foreground='black', background='blue')
    cursor = db.cursor()

    Label(master, text='Check your fine tickets here:').pack()

    sql = "select * from "+identification+"_Fine_History where " + \
        identification+"_id="+str(user_id)+" and status='unpaid'"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    amount = 0
    for item in result:
        amount += item[5]
    Label(master, text='Total fine is :$'+str(amount)+".").pack()

    def pay_fine():
        sql = "update "+identification+"_Fine_History set status='paid' where " + \
            identification+"_id="+str(user_id)
        print(sql)
        cursor.execute(sql)
        db.commit()

        messagebox.showinfo(title='Successfully Paid',
                            message="Your fine has been paid")
        master.destroy()
        fine_mani_interface(db, user_id, identification)

    button = ttk.Button(master, text='pay it now', command=pay_fine)
    button.pack()

    master.mainloop()


if __name__ == "__main__":
    db = pymysql.connect('localhost', 'root', 'password', 'myDB')

    fine_mani_interface(db, 230004501,  'Student')
    # fine_mani_interface(db, 460042348,  'Faculty')
