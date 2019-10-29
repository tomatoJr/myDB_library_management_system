#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Date    : 2019-10-27 14:23:07
# @Author  : Dong (dongwei@tamu.edu)
# @Link    : https://github.com/tomatoJr
# @Version : 1.0.0

from tkinter import *
import pymysql
import os
import xlrd
import random


def drop_all_tables(cursor):
    # drop all tables
    cursor.execute("drop table if exists Student_Rent_Books")
    cursor.execute("drop table if exists Faculty_Rent_Books")
    cursor.execute("drop table if exists Student_Fine_History")
    cursor.execute("drop table if exists Faculty_Fine_History")
    cursor.execute("drop table if exists Student")
    cursor.execute("drop table if exists Faculty")
    cursor.execute("drop table if exists Book")


def create_all_tables(cursor):
    # create tables
    cursor.execute("create table Student(Student_id int, name varchar(255) not null, Dept varchar(255) not null, gender varchar(1) not null, email varchar(255) not null, check(gender='F' or gender='M'), primary key(Student_id))")
    cursor.execute("create table Faculty(Faculty_id int, name varchar(255) not null, Dept varchar(255) not null, gender varchar(1) not null,email varchar(255) not null,check(gender='F' or gender='M'),primary key(Faculty_id))")
    cursor.execute("create table Book(Book_id int,isbn long not null,title varchar(255) not null,author varchar(255) not null, status varchar(255) not null,primary key(Book_id))")
    cursor.execute("create table Student_Rent_Books(Student_id int,Book_id int,borrow_date timestamp not null,due_date timestamp,return_date timestamp,primary key(Student_id, Book_id, borrow_date),foreign key(Student_id) references Student(Student_id)  ON DELETE CASCADE ON UPDATE CASCADE,foreign key(Book_id) references Book(Book_id) on delete cascade on update cascade)")
    cursor.execute("create table Faculty_Rent_Books(Faculty_id int, Book_id int, borrow_date timestamp not null, due_date timestamp ,  return_date timestamp, primary key(Faculty_id, Book_id, borrow_date), foreign key(Faculty_id) references Faculty(Faculty_id)  ON DELETE CASCADE ON UPDATE CASCADE, foreign key(Book_id) references Book(Book_id) on delete cascade on update cascade)")
    cursor.execute("create table Student_Fine_History(Fine_id int NOT NULL auto_increment,Student_id int,Book_id int,due_date timestamp not null,return_date timestamp not null,amount int not null,status varchar(255) not null,primary key(Fine_id),foreign key(Student_id) references Student(Student_id) on delete cascade on update cascade,foreign key(Book_id) references Book(Book_id) on delete cascade on update cascade)")
    cursor.execute("create table Faculty_Fine_History(Fine_id int NOT NULL auto_increment,Faculty_id int,Book_id int,due_date timestamp not null,return_date timestamp not null,amount int not null,status varchar(255) not null,primary key(Fine_id),foreign key(Faculty_id) references Faculty(Faculty_id) on delete cascade on update cascade,foreign key(Book_id) references Book(Book_id) on delete cascade on update cascade)")


def insert_data_from_open_file(db, cursor, file_path, sheet_names):
    # read data from open file
    workbook = xlrd.open_workbook(file_path)  # open workbook
    # grab all sheets by name
    sheets = workbook.sheet_names()
    # get certain worksheet from workbook
    for sheet_name in sheet_names:
        # print(sheet_name)
        worksheet = workbook.sheet_by_name(sheet_name)
        for i in range(1, worksheet.nrows):
            dept_list = []
            for j in range(0, worksheet.ncols):
                if type(worksheet.cell_value(i, j)) is float:
                    dept_list.append(int(worksheet.cell_value(i, j)))
                else:
                    dept_list.append(worksheet.cell_value(i, j))

            sql = "insert into "+str(sheet_name)+" values ("
            for i in dept_list:
                if type(i) is str:
                    sql = sql+"'"+str(i)+"'"+', '
                else:
                    sql = sql+str(i)+', '
            sql = sql[:-2:] + ")"
            # print(sql)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()


def count_records(cursor, table_name):
    # sql = "select Book_id from "+str (table_name)
    sql = "select count(*) from "+str(table_name)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    except:
        print('error')


def db_configuration():
    db = pymysql.connect('localhost', 'root', 'password', 'myDB')
    cursor = db.cursor()
    drop_all_tables(cursor)
    create_all_tables(cursor)
    file_path = os.path.dirname(os.path.abspath(__file__))+'/data.xlsx'
    tables = ['Student', 'Faculty', 'Book']
    insert_data_from_open_file(db, cursor, file_path, tables)
    db.close()


if __name__ == "__main__":
    db_configuration()
