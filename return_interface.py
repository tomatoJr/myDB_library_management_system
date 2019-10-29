#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Date    : 2019-10-28 16:28:03
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
from fine_interface import *
from main_window import *
from user_interface import *


def return_book_interface(master, db, user_id, identification):
    return_book_interface_frame = Frame(master)
    return_book_interface_frame.pack(expand=YES, fill=BOTH)

    style = ttk.Style()
    style.configure('TButton', foreground='black', background='blue')

    # create cursor
    cursor = db.cursor()

    # return book
    return_frm = Frame(return_book_interface_frame)
    return_frm.pack()
    Label(return_frm, text="Select and return borrowed book here:").pack(side=LEFT)

    sql = 'select * from '+str(identification)+'_Rent_Books where ' + \
        identification+"_id="+str(user_id)+' and return_date is NULL'
    cursor.execute(sql)
    result = cursor.fetchall()
    book_ids = []
    book_names = []
    for item in result:
        book_ids.append(item[1])

    for book_id in book_ids:
        sql = 'select title from Book where Book_id='+str(book_id)
        cursor.execute(sql)
        result = cursor.fetchone()
        book_names.append(result[0])

    def return_to_lib():
        # get bid
        book_name = lb.get(lb.curselection())
        bid = (book_ids[book_names.index(book_name)])

        # get the newest_borrow_date to find the corresponding record
        sql = "(select max(borrow_date) from "+identification+"_Rent_Books where "+identification+"_id="+str(
            user_id)+" and Book_id = "+str(bid)+")"
        cursor.execute(sql)
        result = cursor.fetchone()
        newest_borrow_date = result[0]

        # get due_date to discern if expired
        sql = "select due_date from "+identification+"_Rent_Books where "+identification+"_id ="+str(
            user_id)+" and Book_id = "+str(bid)+" and borrow_date='"+str(newest_borrow_date)+"'"
        cursor.execute(sql)
        due_date = cursor.fetchone()[0]

        # update return time
        return_date = datetime.datetime.now()
        sql = 'update '+identification + \
            "_Rent_Books set return_date='" + \
            str(return_date) + \
            "' where "+identification+"_id=" + \
            str(user_id)+" and Book_id="+str(bid) + \
            " and borrow_date='"+str(newest_borrow_date)+"'"
        cursor.execute(sql)
        db.commit()

        # update book status
        sql = "update Book set status='available' where Book_id="+str(bid)
        cursor.execute(sql)
        db.commit()

        # warning if book expired
        if(return_date > due_date):
            delta = return_date-due_date
            pattern = re.compile(r'\d+ day')
            result = pattern.match(str(delta))
            amount = 0
            if(result):
                days = re.sub(' day', '', str(result.group(0)))
                amount = int(days)*0.1
                print(amount)

            if amount == 0:
                pass
            else:
                sql = "insert into "+identification + \
                    "_Fine_History  ("+identification + "_id,Book_id, due_date, return_date, amount, status) values(" + \
                    str(user_id)+","+str(bid)+",'"+str(return_date)+"','" + \
                    str(due_date)+"'," + str(amount)+", 'unpaid'"+")"
                print(sql)

                messagebox.showinfo(title='Book Expired!',
                                    message='Book '+book_name+' has been returned but you already missed the due date.\nPlease check your Fine Ticket.')
        else:
            messagebox.showinfo(title='Successfully returned!',
                                message='Book '+book_name+' has been returned.')

    return_button = ttk.Button(
        return_frm, text='return', command=return_to_lib)
    return_button.pack(side=RIGHT)

    # show book listbox
    lb = Listbox(return_frm)
    for item in book_names:
        lb.insert('end', item)
    lb.pack(side=RIGHT)

    def back_to_user_interface():
        return_book_interface_frame.destroy()
        user_mani_interface(master, db, user_id, identification)

    back_frm = Frame(return_book_interface_frame)
    back_frm.pack()
    Label(back_frm, text='Go back to the user interface:').pack(side=LEFT)
    back_to_user_interface_button = ttk.Button(
        back_frm, text='back', command=back_to_user_interface)
    back_to_user_interface_button.pack(side=RIGHT)
