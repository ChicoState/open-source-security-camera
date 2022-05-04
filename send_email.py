#!/usr/bin/python
import sys
import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText


def send_email(connection, times, video_file, file_name):
    mail_content = "Hello,\n\n" + \
        "The following entry was created in the database:.\n"

    for entry in times:
        mail_content = mail_content + str(entry) + "\n"

    #Assign vairables for smtplib functions
    django_email = str(get_email(connection))
    django_email_key = str(get_key(connection))

    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = django_email[2:(len(django_email)-3)]
    EMAIL_HOST_PASSWORD = django_email_key[2:(len(django_email_key)-3)]
    RECIPIENT_ADDRESS = django_email[2:(len(django_email)-3)]

    #Setup the MIME (From, to, subject)
    message = MIMEMultipart()
    message['From'] = EMAIL_HOST_USER
    message['To'] = RECIPIENT_ADDRESS
    message['Subject'] = 'Security Camera Notifications'

    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))

    attach_file = open(video_file, 'rb')    # Open the file as binary mode
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    attach_file.close()

    #Add payload header with filename
    encoders.encode_base64(payload)     # encode the attachment
    payload.add_header("Content-Disposition", "attachment", filename=file_name)
    message.attach(payload)

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

    querey = ''' INSERT INTO core_recording(recordingLength,
                fileName,
                filePath,
                cameraId_id)
                VALUES(?,?,?,?)
            '''
    new_recording = (length, file_name, file_path, camera_id_id)
    cur = connection.cursor()
    cur.execute(querey, new_recording)
    connection.commit()

def select_all_times(connection):
    cur = connection.cursor()
    cur.execute('SELECT * FROM core_recording ORDER BY ID DESC LIMIT 1')
    rows = cur.fetchall()
    return rows

def get_email(connection):
    cur = connection.cursor()
    cur.execute('SELECT email FROM user_customuser ORDER BY ID DESC LIMIT 1')
    rows = cur.fetchall()
    return rows[0]

def get_key(connection):
    cur = connection.cursor()
    cur.execute('SELECT emailKey FROM user_customuser ORDER BY ID DESC LIMIT 1')
    rows = cur.fetchall()
    return rows[0]

def main():

    file_name = sys.argv[1]
    file_path = sys.argv[2]
    length = sys.argv[3]
    camera_id_id = sys.argv[4]

    database = r"osCam/db.sqlite3"
    connection = create_connection(database)

    with connection:
        insert_recording(
            connection,
            file_name,
            file_path,
            length,
            camera_id_id
        )
        times = select_all_times(connection)
        send_email(
            connection,
            times,
            file_path,
            file_name
        )

    connection.close()


if __name__ == '__main__':
    main()
