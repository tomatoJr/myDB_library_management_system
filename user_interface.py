#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Date    : 2019-10-28 11:52:14
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
import fine_interface
import return_interface
from main_window import *


def user_mani_interface(master, db, user_id, identification):

    style = ttk.Style()
    style.configure('TButton', foreground='black', background='blue')

    user_interface_frame = Frame(master)
    user_interface_frame.pack(expand=YES, fill=BOTH)

    cursor = db.cursor()

    # welcome user
    sql = "select name from "+identification + \
        " where "+identification + "_id="+str(user_id)
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        Label(user_interface_frame, text="Welcome! " +
              identification+" "+str(result[0])).pack()
    except:
        print('error')

    def borrow_book():
        # get bid
        bid = bid_entry.get()
        if not bid:
            btitle = bt_entry.get()
            sql = "select * from Book where title='"+str(btitle)+"'"
            cursor.execute(sql)
            result = cursor.fetchone()
            bid = str(result[0])

        # check for status in case of duplicate rent record
        sql = "select status from Book where Book_id="+str(bid)
        cursor.execute(sql)
        status = cursor.fetchone()[0]

        if status == 'available':
            if identification == 'Student':
                messagebox.showinfo(title="Successfully borrowed!",
                                    message=identification+' can borrow book up to 4 months.\n You should return this book before '+str((datetime.datetime.now()+datetime.timedelta(days=120)).date()))
            else:
                messagebox.showinfo(title="Successfully borrowed!",
                                    message=identification+' can borrow book up to 1 year.\n You should return this book before '+str((datetime.datetime.now()+datetime.timedelta(days=365)).date()))

            sql = "insert into "+identification+"_Rent_Books ("+identification+"_id, Book_id, borrow_date) values(" + str(
                user_id)+","+str(bid) + ",CURRENT_TIMESTAMP()" + ")"
            cursor.execute(sql)
            db.commit()

            sql = "(select max(borrow_date) from "+identification+"_Rent_Books where "+identification+"_id="+str(
                user_id)+" and Book_id = "+str(bid)+")"
            cursor.execute(sql)
            result = cursor.fetchone()
            borrow_date = result[0]

            if identification == 'Student':
                due_time = borrow_date+datetime.timedelta(days=120)
            else:
                due_time = borrow_date+datetime.timedelta(days=365)

            sql = "update "+identification+"_Rent_Books set due_date='"+str(due_time)+"' where "+identification+"_id="+str(
                user_id)+" and Book_id="+str(bid) + " and borrow_date = '"+str(borrow_date)+"'"
            cursor.execute(sql)
            db.commit()

        else:
            messagebox.showwarning(title="Book Unavailable!",
                                   message='This book is unavailable now.')

        # set unavailable status
        sql = "update Book set status='unavailable' where Book_id="+str(bid)
        cursor.execute(sql)
        db.commit()

    def check_for_book_id():
        bid = bid_entry.get()
        sql = "select * from Book where Book_id="+str(bid)
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            book_name = str(result[2])
            book_author = str(result[3])
            book_status = str(result[4])
            info = "title: "+book_name+"\nauthor: "+book_author+"\n"+book_status+" now"
            if book_status == 'available':
                messagebox.showinfo(title='Book Info', message=info)

                borrow_frm = Frame(user_interface_frame)
                borrow_frm.pack()
                Label(borrow_frm, text="You can borrow "+book_name+" now:").pack(
                    side=LEFT)
                button = ttk.Button(
                    borrow_frm, text='borrow', command=borrow_book)
                button.pack(side=RIGHT)
            else:
                messagebox.showwarning(title='Book Info', message=info)
        except:
            print('error')

    # inquiry for book id
    inquiry_frm = Frame(user_interface_frame)
    inquiry_frm.pack()
    Label(inquiry_frm, text="You can search for book by input book id here:").pack(
        side=LEFT)
    button = ttk.Button(inquiry_frm, text='check', command=check_for_book_id)
    button.pack(side=RIGHT)
    bid_entry = Entry(inquiry_frm, show=None)
    bid_entry.pack(side=RIGHT)

    def check_for_book_title():
        btitle = bt_entry.get()

        sql = "select * from Book where title='"+str(btitle)+"'"
        print(sql)
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            book_id = str(result[0])
            book_name = str(result[2])
            book_author = str(result[3])
            book_status = str(result[4])
            info = "title: "+book_name+"\nauthor: "+book_author+"\n"+book_status+" now"
            # Label(user_interface_frame, text=info).pack()
            if book_status == 'available':
                messagebox.showinfo(title='Book Info', message=info)

                borrow_frm = Frame(user_interface_frame)
                borrow_frm.pack()
                Label(borrow_frm, text="You can borrow "+book_name+" now:").pack(
                    side=LEFT)
                button = ttk.Button(borrow_frm, text='borrow',
                                    command=borrow_book)
                button.pack(side=RIGHT)
            else:
                messagebox.showwarning(title='Book Info', message=info)
        except:
            print('error')

    # inquiry for book title
    # The Hunger Games
    inquiry_by_t_frm = Frame(user_interface_frame)
    inquiry_by_t_frm.pack()
    Label(inquiry_by_t_frm, text="You can search for book by input book title here:").pack(
        side=LEFT)
    button = ttk.Button(inquiry_by_t_frm, text='check',
                        command=check_for_book_title)
    button.pack(side=RIGHT)
    bt_entry = Entry(inquiry_by_t_frm, show=None)
    bt_entry.pack(side=RIGHT)

    def return_book_func():
        user_interface_frame.destroy()
        return_interface.return_book_interface(
            master, db, user_id, identification)

    # return book
    return_frm = Frame(user_interface_frame)
    return_frm.pack()
    Label(return_frm, text="Return borrowed book here:").pack(
        side=LEFT)
    button = ttk.Button(return_frm, text='return',
                        command=return_book_func)
    button.pack(side=RIGHT)

    def fine_button_func():
        user_interface_frame.destroy()
        fine_interface.fine_mani_interface(master, db, user_id, identification)

    # check fine ticket
    fine_frm = Frame(user_interface_frame)
    fine_frm.pack()
    Label(fine_frm, text="Check for fine tickets here:").pack(
        side=LEFT)
    button = ttk.Button(fine_frm, text='check',
                        command=fine_button_func)
    button.pack(side=RIGHT)

    # quit button
    quit_frm = Frame(user_interface_frame)
    quit_frm.pack()
    Label(quit_frm, text='Quit').pack(side=LEFT)
    ttk.Button(quit_frm, text='Quit', command=master.quit).pack(side=RIGHT)
