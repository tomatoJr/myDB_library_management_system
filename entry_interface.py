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

from db import *
from main_window import *
from fine_interface import *
from return_interface import *
from user_interface import *


def entry_interface(master, db):

    style = ttk.Style()
    style.configure('TButton', foreground='black', background='blue')

    entry_interface_frame = Frame(master)
    entry_interface_frame.pack(expand=YES, fill=BOTH)

    cursor = db.cursor()

    Label(entry_interface_frame,
          text='Howdy! \n Welcome to TAMU library management system.\n').pack()

    id_frm = Frame(entry_interface_frame)
    id_frm.pack()
    Label(id_frm, text="Please input your ID:").pack(side=LEFT)
    id_entry = Entry(id_frm, show=None)
    id_entry.pack(side=RIGHT)

    pwd_frm = Frame(entry_interface_frame)
    pwd_frm.pack()
    Label(pwd_frm, text="Please input your password:").pack(side=LEFT)
    pwd_entry = Entry(pwd_frm, show='*')
    pwd_entry.pack(side=RIGHT)

    def click_to_login(identification):
        id_input = id_entry.get()
        pwd_input = pwd_entry.get()
        if (id_input == pwd_input):
            sql = "select name from "+identification + \
                " where "+identification + "_id="+str(id_input)
            try:
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    messagebox.showinfo(title='Successfully Login',
                                        message='Successfully Login!')
                    entry_interface_frame.destroy()
                    user_mani_interface(master, db, id_input, identification)
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

    bt_frm = Frame(entry_interface_frame)
    bt_frm.pack()

    # student login
    # Label(bt_frm, text='Login as student').pack(side=LEFT)
    student_login_button = ttk.Button(
        bt_frm, text='Login as student',  command=click_student_login)
    student_login_button.pack(side=LEFT)
    # faculty login

    faculty_login_button = ttk.Button(
        bt_frm, text='Login as faculty', command=click_faculty_login)
    faculty_login_button.pack(side=RIGHT)
    # Label(bt_frm, text='Login as faculty').pack(side=RIGHT)

    # quit button
    quit_frm = Frame(entry_interface_frame)
    quit_frm.pack()
    Label(quit_frm, text='Quit').pack(side=LEFT)
    ttk.Button(quit_frm, text='Quit',
               command=master.quit).pack(side=RIGHT)
