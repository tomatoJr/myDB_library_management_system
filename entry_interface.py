#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Date    : 2019-10-28 11:51:35
# @Author  : Dong (dongwei@tamu.edu)
# @Link    : https://github.com/tomatoJr
# @Version : 1.0.0

import os
from tkinter import *
from tkinter import ttk
import pymysql
import xlrd
import random
from tkinter import messagebox
import time
import datetime
import re

from main_window import *
from user_interface import *
from fine_interface import *
from return_interface import *


def entry_interface(db):
    # create master
    master = Tk()
    master.title('library management system')
    master.geometry('500x200')

    master_frame = Frame(master)
    master_frame.pack(expand=YES, fill=BOTH)

    Label(master_frame,
          text='Howdy! \n Welcome to TAMU library management system.\n').pack()

    id_frm = Frame(master_frame)
    id_frm.pack()
    Label(id_frm, text="Please input your ID:").pack(side=LEFT)
    id_entry = Entry(id_frm, show=None)
    id_entry.pack(side=RIGHT)

    pwd_frm = Frame(master_frame)
    pwd_frm.pack()
    Label(pwd_frm, text="Please input your password:").pack(side=LEFT)
    pwd_entry = Entry(pwd_frm, show='*')
    pwd_entry.pack(side=RIGHT)

    def click_to_login(identification):
        id_input = id_entry.get()
        pwd_input = pwd_entry.get()
        if (id_input == pwd_input):
            cursor = db.cursor()
            sql = "select name from "+identification + \
                " where "+identification + "_id="+str(id_input)
            # 230004501
            # 460042348
            try:
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    messagebox.showinfo(title='Successfully Login',
                                        message='Successfully Login!')
                    master.destroy()
                    user_mani_interface(db, id_input, identification)
                else:
                    messagebox.showwarning(title='Information Not Found',
                                           message='Information Not Found. Please try again.')
            except:
                print('error')
        else:
            messagebox.showwarning(title='Wrong Information',
                                   message='Wrong information. Please try again.')

    def click_student_login():
        click_to_login('Student')

    def click_faculty_login():
        click_to_login('Faculty')

    bt_frm = Frame(master_frame)
    bt_frm.pack()

    # student login
    Label(bt_frm, text='Login as student').pack(side=LEFT)
    student_login_button = ttk.Button(
        bt_frm, text='Login as student',  command=click_student_login)
    student_login_button.pack(side=LEFT)
    # faculty login

    style = ttk.Style()
    style.configure('TButton', foreground='black', background='blue')

    faculty_login_button = ttk.Button(
        bt_frm, text='Login as faculty', command=click_faculty_login)
    faculty_login_button.pack(side=RIGHT)
    Label(bt_frm, text='Login as faculty').pack(side=RIGHT)

    # quit button
    quit_frm = Frame(master_frame)
    quit_frm.pack()
    Label(quit_frm, text='Quit').pack(side=LEFT)
    ttk.Button(quit_frm, text='Quit', command=master.quit).pack(side=RIGHT)

    master.mainloop()


if __name__ == "__main__":
    # connect myDB
    db = pymysql.connect('localhost', 'root', 'password', 'myDB')

    entry_interface(db)
