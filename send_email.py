import os
import environ
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
from sqlite3 import Error

def send_email():
    mail_content = "Hello,\n" + \
    "This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.\n" + \
    "Thank You"

    # Email Notification Settings
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
    message['Subject'] = 'A test mail sent by Python. It has an attachment.'

    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))

    #Create SMTP session, login, and then send email
    session = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)

    #enable security
    session.starttls()
    session.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    text = message.as_string()
    session.sendmail(EMAIL_HOST_USER, RECIPIENT_ADDRESS, text)
    session.quit()
    print('Mail Sent')

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Camera")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Camera WHERE priority=?", (priority,))

    rows = cur.fetchall()

    for row in rows:
        print(row)


def main():
    database = r"osCam/db.sqlite3"

    send_email()

    # create a database connection
    #conn = create_connection(database)
    #with conn:
    #    print("1. Query task by priority:")
    #    select_task_by_priority(conn, 1)

    #    print("2. Query all tasks")
    #    select_all_tasks(conn)


if __name__ == '__main__':
    main()
