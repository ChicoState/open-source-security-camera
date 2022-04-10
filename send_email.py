import os
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


def select_all_times(connection):
    cur = connection.cursor()

    cur.execute('SELECT recorded_on FROM core_recording')

    #Additional SQlite query statements to choose which column to format the email with
    #cur.execute('SELECT * FROM core_recording')
    #cur.execute('SELECT id FROM core_recording')
    #cur.execute('SELECT recording_length FROM core_recording')
    #cur.execute('SELECT camera_id_id FROM core_recording')
    #cur.execute('SELECT name from sqlite_master where type= "table"')

    rows = cur.fetchall()
    for row in rows:
        print(row)

    return rows


def main():
    database = r"osCam/db.sqlite3"
    connection = create_connection(database)

    with connection:
        print("Listing All Times:")
        times = select_all_times(connection)
        send_email(times)

    connection.close()


if __name__ == '__main__':
    main()
