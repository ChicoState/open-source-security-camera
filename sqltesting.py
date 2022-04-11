#!/usr/bin/python

import os
import sys
import environ
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    sqliteConnection = None
    try:
        sqliteConnection = sqlite3.connect(db_file)
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        print("SQLite Database Version is: ", record)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    return sqliteConnection
def select_all(connection, tableName, attributeName):
    cur = connection.cursor()
    #Additional SQLite query statements to choose which column to format the email with
    # cur.execute('SELECT {} FROM {} '.format(attributeName, tableName))
    cur.execute('SELECT name from sqlite_master where type= "table"')
    rows = cur.fetchall()
    for row in rows:
        print(row)
    return rows

def main():
    tableName = sys.argv[1]
    attributeName = sys.argv[2]
    database = r"osCam/db.sqlite3"
    connection = create_connection(database)    
    with connection:
        data = select_all(connection, tableName, attributeName)
    connection.close()

if __name__ == '__main__':
    main()
