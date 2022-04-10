from ast import Str
from email.policy import default
import json
import pathlib
import re
from sys import path
from unittest.mock import DEFAULT
from xmlrpc.client import Boolean
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from requests import request
import os
from django.contrib.auth.models import User


class MotionDetect():
    def __init__(self):
        #usb cam for testing, change for pi
        self.video = cv.VideoCapture(0)
        self.codec = cv.VideoWriter_fourcc(*'XVID')
        #self.filePath = "videos/{}.avi".format(datetime.now().strftime("%Y_%m_%d, %H:%M:%S"))
        self.avg = None
        self.out = None
        self.numframes = 0
        self.record = False
    def __del__(self):
        self.video.release()
    def get_frame(self):
        success, frame = self.video.read()
        if(not success):
            print("did not read from camera")
            time.sleep(2)
        frame = cv.flip(frame,0)
        frame = MotionDetect.rescaleFrame(frame, .25)
        if not success:
            print("could not get image from cammera")
        text = "searching..."
        cnts = MotionDetect.imgProcess(frame, self)
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
            text = "Motion!"
        #add text to frame
        if text == "Motion!":
            status_color = (0,0,255)
        else:
            status_color=(0,255,0)
        cv.putText(frame, "Status: {}".format(text), (15,15), cv.FONT_HERSHEY_SIMPLEX, .5, status_color, 1)
        #current date/time
        date_time = datetime.now()
        cv.putText(frame, "Date/Time: {}".format(date_time.strftime("%Y/%m/%d, %H:%M:%S")), (200,15), cv.FONT_HERSHEY_SIMPLEX, .5, status_color, 1)
        ret, jpeg = cv.imencode('.jpg', frame)
        if self.record:
            if self.out == None:
                self.out = MotionDetect.setRecording(date_time.strftime("%Y/%m/%d, %H:%M:%S"), frame)
            if text == "Motion!":
                self.numframes+=1
                self.out.write(frame)
            #if number of frames in recording is greater than 500 save recording and start new recording file
            if self.numframes > 250:
                self.numframes = 0
                self.out.release()
                date_time = datetime.now().strftime("%Y_%m_%d, %H:%M:%S")
                self.out= MotionDetect.setRecording(date_time, frame)
        return jpeg.tobytes()






def gen(camera):
	while True:
		# frame = camera.get_frame()
		frame = b'test'
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def feed(request):
	return StreamingHttpResponse(gen(None),
					content_type='multipart/x-mixed-replace; boundary=frame')

