# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 20:06:27 2021

@author: Subhikshaa
"""

import mysql.connector

db_conn=mysql.connector.connect(host="localhost",user="root",password="Subu@2001",database="CN_DB")

db_cursor=db_conn.cursor()
db_cursor.execute("CREATE DATABASE IF NOT EXISTS CN_DB")
sql_query="CREATE TABLE history(port INT NOT NULL,command VARCHAR(50),cmd_time CHAR(10),cmd_date CHAR(10))"
#Uncomment below line if you have to create table for first time
#db_cursor.execute(sql_query)

print("Connected to mysql database.......")

def insert_record(cursor, port, command, cmd_time, cmd_date):
    sql = "INSERT INTO history (port, command, cmd_time, cmd_date) VALUES  (%s, %s, %s, %s)"
    val = (port, command, cmd_time, cmd_date)
    cursor.execute(sql, val)
    db_conn.commit()
    print("history table updated")
    
def print_history_table(cursor):
    cursor.execute("SELECT * FROM history")
    res = cursor.fetchall()

    s = ""
    for row in res:
        s += "Port: " + str(row[0]) + "\t" + "Command: " + str(row[1]) + "\t" + "Time: " + str(row[2]) + "\t" + "Date: " \
             + str(row[3]) + "\n"
    return s
