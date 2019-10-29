#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Date    : 2019-10-27 16:26:36
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
from return_interface import *
from user_interface import *


if __name__ == "__main__":
    db_configuration()

    # connect myDB
    db = pymysql.connect('localhost', 'root', 'password', 'myDB')

    entry_interface(db)
    # 230004501 is a student account
    # 460042348 is a faculty account
