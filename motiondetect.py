#!/usr/bin/python
import cv2 as cv
from cv2 import imshow
from cv2 import VideoWriter
from datetime import datetime
import time
import os
from cv2 import erode
import numpy as np

class MotionDetect():
    def __init__(self):
        self.capture = cv.VideoCapture(0)
        self.codec = cv.VideoWriter_fourcc(*'XVID')
        self.date_time = None
        self.BoxColor = (0,0,255)
        self.searchTextColor = (0,0,255)
        self.motionTextColor = (0,0,255)
        self.fps = 30
        # number of frames recorded
        self.numFrames = 0
        # max number of frames to record
        self.maxFrames = 100
        # display tests
        self.searchText = ["searching   ", "searching.  ", "searching.. ", "searching..."]
        self.motionText = ["Motion   ","Motion!  ","Motion!! ","Motion!!!"]
        # rolling average of grayscale images
        self.avg = None
        # output file
        self.out = None
        self.fileName = None
        self.filePath = None
        # has motion been detected?
        self.detected = False
        # should record
        self.record = True
        self.flip = False
        self.mirror = False
        # should send email?
        self.notify = False
        self.showBox = True
    def cleanUp(self):
        if self.out != None:
            self.out.release()
        self.capture.release()
        cv.destroyAllWindows()
        cv.waitKey(0)
    #recoding setup
    def setRecording(self, fileName, frame):
        #type of codec (os dependent, currently working for ubunto 20.4)
        #where to save files
        filePath = "osCam/videos/{}.avi".format(fileName)
        #set frame rate for recording
        width, height, channels = frame.shape
        #return output object
        return fileName, filePath, cv.VideoWriter(filePath, self.codec, self.fps, (height, width))
    
    def rescaleFrame(self, frame, scale):
        #scale the width and height, (cast to int)
        width = int(frame.shape[1] * scale)
        height =int(frame.shape[0] * scale)
        dimensions = (width, height)
        #return resize frame to particular dimension
        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)
    
    def actions(self, frame):
        if self.detected:
                if self.record:
                    self.numFrames+=1
                    self.out.write(frame)
                    #if number of recorded frames is greater than max frames to record save recording and start new recording file
                    if self.numFrames > self.maxFrames:
                        self.numFrames = 0
                        self.out.release()
                        camID = 1
                        #pass database info to subProcess
                        self.fileName += '.avi'
                        if self.notify:
                            os.system('python send_email.py {} {} {} {}'.format(self.fileName, self.filePath, self.numFrames, camID))
                        date_time = datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
                        self.fileName, self.filePath, self.out= MotionDetect.setRecording(self, date_time, frame)

    #convert frame to grey, compute Gaussian blur for noise reduction, update ave,
    #compute weighted averages, compute difference between wieghted ave and grayscale frame to get delta (background bodel - grayscale frame)
    def imgProcess(self, frame, avg):
        #convert to grayscale image
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        #blur image to reduce noise (filter size 21X21)
        gray = cv.GaussianBlur(gray, (7,7),0)
        #if first loop, need to set avg
        if avg is None:
            avg = gray.copy().astype("float")
        #get weighted average of prev frame
        cv.accumulateWeighted(gray, avg, 0.5)
        #compute difference between first frame and cur frame
        frameDelta = cv.absdiff(gray, cv.convertScaleAbs(avg))
        thresh = cv.threshold(frameDelta, 5, 255, cv.THRESH_BINARY)[1]
        #dilate the threshold image to fill in holes
        dil = cv.dilate(thresh, None, iterations=2)
        #get contours
        cnts = cv.findContours(dil.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)    
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
            return cv.flip(frame,0)
        else:
            return frame
    def mirrorFrame(self, frame):
        if self.mirror:
            return cv.flip(frame,1)
        else:
            return frame
    def Detect(self):
        isTrue, frame = self.capture.read()
        frame = MotionDetect.flipFrame(self, frame)
        frame = MotionDetect.mirrorFrame(self, frame)
        if self.record:
            #label videos based on date/time
            date_time = datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
            #initialize file recoding
            self.fileName, self.filePath, self.out = MotionDetect.setRecording(self, date_time, frame)
            #write first frame
            self.out.write(frame)
            self.numFrames+=1
        #infinate loop and capture video until 'd' is pressed
        while not (cv.waitKey(28) & 0xFF==ord('d')):
            # image text if motion not found
            text = self.searchText[int(time.time())%4]
            #read video, gets a bool and frame
            isTrue, frame = self.capture.read()
            frame = MotionDetect.flipFrame(self, frame)
            frame = MotionDetect.mirrorFrame(self, frame)
            #process image
            self.avg, cnts = MotionDetect.imgProcess(self, frame, self.avg)
            for c in cnts:
                #if contours are less than desired area cont
                if cv.contourArea(c) < 5000:
                    continue
                #set boundaries for motion box from contours
                (x,y,w,h) = cv.boundingRect(c)
                #set color to draw box:
                color = (0,0,255)
                #motion box line thickness
                thickness = 2
                #set motion box on frame
                cv.rectangle(frame, (x,y), (x+w, y+h), color, thickness)
                #change notification text
                text = self.motionText[int(time.time())%4]
                self.detected = True
            #add text to frame
            status_color = MotionDetect.setStatusColor(self)
            cv.putText(frame, "Status: {}".format(text), (15,15), cv.FONT_HERSHEY_SIMPLEX, .5, status_color, 1)
            #current date/time
            date_time = datetime.now()
            cv.putText(frame, "{}".format(date_time.strftime("%d/%m/%Y, %H:%M:%S")), (450,15), cv.FONT_HERSHEY_SIMPLEX, .5, status_color, 1)
            #display the image
            cv.imshow('Video', frame)
            # if record, record, if notify, notify, etc.
            MotionDetect.actions(self, frame)
        MotionDetect.cleanUp(self)

if __name__=="__main__":
    detect=MotionDetect()
    detect.Detect()
