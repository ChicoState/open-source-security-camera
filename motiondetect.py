#!/usr/bin/python
import cv2 as cv
from datetime import datetime
import time
import os
import sqlite3


class dataBase():
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

    def GetSettingsFromDB(connection):
        cur = connection.cursor()
        cur.execute('SELECT * FROM userconfig_storage')
        # get all rows from DB (there should be only 1)
        rows = cur.fetchall()
        attributeList = list()
        # loop through the rows
        for row in rows:
            # loop through all attributes in the row and store them in list
            for attribute in row:
                attributeList.append(attribute)
        # return list of attributes (user storage settings from DB
        return attributeList
class MotionDetect():
    def __init__(self):
        self.capture = cv.VideoCapture(0)
        self.codec = cv.VideoWriter_fourcc(*'XVID')
        self.date_time = None
        self.BoxColor = (0, 0, 255)
        self.searchTextColor = (0, 0, 255)
        self.motionTextColor = (0, 0, 255)
        self.fps = 30
        self.scale = 1
        self.numFrames = 0
        self.maxFrames = 100
        self.searchText = [
            "searching   ",
            "searching.  ",
            "searching.. ",
            "searching..."]
        self.motionText = [
            "Motion   ",
            "Motion!  ",
            "Motion!! ",
            "Motion!!!"]
        self.avg = None
        self.out = None
        self.fileName = None
        self.filePath = None
        self.detected = False
        self.record = False
        self.flip = False
        self.mirror = False
        self.notify = False
        self.showBox = True
        self.maxNumberVidoes = 10
        self.timeToLive = None  # need to implement time to live funciton
        self.showText = True

    def cleanUp(self):
        if self.out is not None:
            self.out.release()
        self.capture.release()
        cv.destroyAllWindows()
        cv.waitKey(0)

    def updateSettings(self, row):
        if len(row) > 0:
            self.record = row[1]
            self.showText = row[2]
            self.maxNumberVidoes = row[3]
            self.timeToLive = row[4]
            self.maxFrames = row[5]

    def setRecording(self, fileName, frame):
        # type of codec (os dependent, currently working for ubunto 20.4)
        # where to save files
        filePath = "osCam/videos/{}.avi".format(fileName)
        # set frame rate for recording
        width, height, channels = frame.shape
        # return output object
        return (
            fileName,
            filePath,
            cv.VideoWriter(filePath, self.codec, self.fps, (height, width))
            )

    def rescaleFrame(self, frame):
        # scale the width and height, (cast to int)
        width = int(frame.shape[1] * self.scale)
        height = int(frame.shape[0] * self.scale)
        dimensions = (width, height)
        # return resize frame to particular dimension
        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    def actions(self, frame):
        if self.detected:
            if self.record:
                if self.out is None:
                    date_time = datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
                    self.fileName,
                    self.filePath,
                    self.out = MotionDetect.setRecording(
                        self,
                        date_time,
                        frame
                    )
                self.numFrames += 1
                self.out.write(frame)
                # if number of recorded frames
                # is greater than max frames to record
                # then save recording and start new recording file
                if self.numFrames > self.maxFrames:
                    self.numFrames = 0
                    self.out.release()
                    camID = 1
                    # pass database info to subProcess
                    self.fileName += '.avi'
                    # only send email if recording and notifications are turned on
                    if self.notify and self.record:
                        os.system('python send_email.py {} {} {} {}'.format(
                            self.fileName,
                            self.filePath,
                            self.numFrames,
                            camID
                            )
                        )
                    date_time = datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
                    self.fileName,
                    self.filePath,
                    self.out = MotionDetect.setRecording(
                        self,
                        date_time,
                        frame
                    )

    # convert frame to grey,
    # compute Gaussian blur for noise reduction,
    # update ave,
    # compute weighted averages,
    # compute difference between wieghted ave and grayscale frame
    # to get delta (background bodel - grayscale frame)
    def imgProcess(self, frame, avg):
        # convert to grayscale image
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # blur image to reduce noise
        gray = cv.GaussianBlur(gray, (7, 7), 0)
        # if first loop, need to set avg
        if avg is None:
            avg = gray.copy().astype("float")
        # get weighted average of prev frame
        cv.accumulateWeighted(gray, avg, 0.5)
        # compute difference between first frame and cur frame
        frameDelta = cv.absdiff(gray, cv.convertScaleAbs(avg))
        thresh = cv.threshold(frameDelta, 5, 255, cv.THRESH_BINARY)[1]
        # dilate the threshold image to fill in holes
        dil = cv.dilate(thresh, None, iterations=2)
        # get contours
        cnts = cv.findContours(
            dil.copy(),
            cv.RETR_EXTERNAL,
            cv.CHAIN_APPROX_SIMPLE
        )
        if len(cnts) == 2:
            cnts = cnts[0]
        elif len(cnts) == 3:
            cnts = cnts[1]
        else:
            print("something went wrong, exiting program :(")
            exit()
        return avg, cnts

    def setStatusColor(self):
        if self.detected:
            return self.motionTextColor
        else:
            return self.searchTextColor

    def flipFrame(self, frame):
        if self.flip:
            return cv.flip(frame, 0)
        else:
            return frame

    def mirrorFrame(self, frame):
        if self.mirror:
            return cv.flip(frame, 1)
        else:
            return frame

    def setShowText(self, frame, text):
        if self.showText:
            status_color = MotionDetect.setStatusColor(self)
            cv.putText(
                frame,
                "Status: {}".format(text),
                (15, 15),
                cv.FONT_HERSHEY_SIMPLEX,
                .5,
                status_color,
                1
            )
            date_time = datetime.now()
            cv.putText(
                frame,
                "{}".format(date_time.strftime("%d/%m/%Y, %H:%M:%S")),
                (450, 15),
                cv.FONT_HERSHEY_SIMPLEX,
                .5,
                status_color,
                1
            )
        return frame

    def Detect(self):
        isTrue, frame = self.capture.read()
        frame = MotionDetect.rescaleFrame(self, frame)
        frame = MotionDetect.flipFrame(self, frame)
        frame = MotionDetect.mirrorFrame(self, frame)
        # set up database
        database = r"osCam/db.sqlite3"
        connection = dataBase.create_connection(database)
        # infinate loop and capture video until 'd' is pressed
        while not (cv.waitKey(28) & 0xFF == ord('d')):
            with connection:
                row = dataBase.GetSettingsFromDB(connection)
            MotionDetect.updateSettings(self, row)
            text = self.searchText[int(time.time()) % 4]
            isTrue, frame = self.capture.read()
            frame = MotionDetect.flipFrame(self, frame)
            frame = MotionDetect.mirrorFrame(self, frame)
            if isTrue:
                self.avg, cnts = MotionDetect.imgProcess(self, frame, self.avg)

            for c in cnts:
                # if contours are less than desired area cont
                if cv.contourArea(c) > 5000:
                    self.detected = True
                    if self.showBox:
                        (x, y, w, h) = cv.boundingRect(c)
                        color = (0, 0, 255)
                        thickness = 2
                        cv.rectangle(
                            frame,
                            (x, y),
                            (x+w, y+h),
                            color,
                            thickness
                        )
                        text = self.motionText[int(time.time()) % 4]
            frame = MotionDetect.setShowText(self, frame, text)
            cv.imshow('Video', frame)
            MotionDetect.actions(self, frame)
        connection.close()
        MotionDetect.cleanUp(self)


if __name__ == "__main__":
    detect = MotionDetect()
    detect.Detect()
