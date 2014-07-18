import sqlite3 as lite
from random import randint
import sys
import datetime

#run on the same level as database file
con = lite.connect('database.db')

f = open("somedata.txt","r")
item = "test"
count = 0


with con:
    cur = con.cursor()    

while item:
    item = ""
    item = f.readline().split("    ")[:-1]
    item.append(f.readline().split("        ")[1])
    dbentry = \
    "\' "+ item[0] + "\',"                +\
    " \' \' ,"                    +\
    "\'"+str(datetime.datetime.today())+"\',"  +\
    "1,"                         +\
    "\'\',"                    +\
    " 1,"                          +\
    "" + str(randint(1,10)) + ","         +\
    " " + str(randint(1,100)) + ","       +\
    "" + str(randint(5,120)) + ","         +\
    "\'drama\',"                      +\
    "\'\'"

    print 'INSERT INTO trackapp_trackitem (name,alt_names,item_type,cover_photo,progress,rating,amount,time,tags,notes) VALUES (' + dbentry + ")"
    cur.execute('INSERT INTO trackapp_trackitem (name,alt_names,created_at,item_type,cover_photo,progress,rating,amount,time,tags,notes) VALUES (' + dbentry + ")")
    con.commit()