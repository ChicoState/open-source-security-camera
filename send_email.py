#!/usr/bin/python
import os
import sys
import environ
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
from sqlite3 import Error

def send_email(times):
    mail_content = "Hello,\n" + \
    "This is a test email sent using Python SMTP library.\n"

    for entry in times:
        mail_content = mail_content + str(entry) + "\n"

    # Read in the private email settings
    env = environ.Env()
    environ.Env.read_env()

    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_PORT = 587
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    RECIPIENT_ADDRESS = env('RECIPIENT_ADDRESS')

    #Setup the MIME (From, to, subject)
    message = MIMEMultipart()
    message['From'] = EMAIL_HOST_USER
    message['To'] = RECIPIENT_ADDRESS
    message['Subject'] = 'Security Camera Notifications'

    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))

    #Create SMTP session, login, and then send email
    session = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)

    #Enable Security and send the email
    session.starttls()
    session.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    text = message.as_string()
    session.sendmail(EMAIL_HOST_USER, RECIPIENT_ADDRESS, text)
    session.quit()
    print('Mail Sent')

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

def insert_recording(connection, file_name, file_path, length, camera_id_id):

    querey = ''' INSERT INTO core_recording(recordingLength, fileName, filePath, cameraId_id)
                VALUES(?,?,?,?) '''
    new_recording = (length, file_name, file_path, camera_id_id)
    cur = connection.cursor()
    cur.execute(querey, new_recording)
    connection.commit()


def select_all_times(connection, file_name):
    cur = connection.cursor()

    #Additional SQLite query statements to choose which column to format the email with
    cur.execute('SELECT * FROM core_recording ORDER BY ID DESC LIMIT 1')
    #cur.execute('SELECT name from sqlite_master where type= "table"')

    rows = cur.fetchall()
    for row in rows:
        print(row)

    return rows


def main():

    file_name = sys.argv[1]
    file_path = sys.argv[2]
    length = sys.argv[3]
    camera_id_id = sys.argv[4]

    database = r"osCam/db.sqlite3"
    connection = create_connection(database)
    
    with connection:
        insert_recording(connection, file_name, file_path, length, camera_id_id)
        times = select_all_times(connection, file_name)
        send_email(times)

    connection.close()


if __name__ == '__main__':
    main()
