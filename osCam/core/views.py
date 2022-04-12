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
        self.video = cv.VideoCapture(0)
        self.BoxColor = (0,0,255)
        self.searchTextColor = (0,0,255)
        self.motionTextColor = (0,0,255)
        self.searchText = ["searching   ", "searching.  ", "searching.. ", "searching..."]
        self.motionText = ["Motion   ","Motion!  ","Motion!! ","Motion!!!"]
        self.avg = None
        self.out = None
        self.flip = False
        self.showBoxes = True
        self.detected = False
    
    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if(not success):
            print("did not read from camera")
            time.sleep(2)
        if self.flip:
            frame = cv.flip(frame,0)
        frame = MotionDetect.rescaleFrame(frame, .75)
        text = self.searchText[int(time.time())%4]
        self.detected = False
        cnts = MotionDetect.imgProcess(frame, self)
        for c in cnts:
            #if contours are less than desired area cont
            if cv.contourArea(c) < 5000:
                continue
            #set boundaries for motion box from contours
            if self.showBoxes:
                (x,y,w,h) = cv.boundingRect(c)
                #set color to draw box:
                color = self.BoxColor
                #motion box line thickness
                thickness = 2
                #set motion box on frame
                cv.rectangle(frame, (x,y), (x+w, y+h), color, thickness)
            #change notification text
            text = self.motionText[int(time.time())%4]
            self.detected = True
        #add text to frame
        if self.detected:
            status_color = self.motionTextColor 
        else:
            status_color= self.searchTextColor
        cv.putText(frame, "Status: {}".format(text), (15,15), cv.FONT_HERSHEY_SIMPLEX, .5, status_color, 1)
        #current date/time
        date_time = datetime.now()
        cv.putText(frame, "Date/Time: {}".format(date_time.strftime("%Y/%m/%d, %H:%M:%S")), (200,15), cv.FONT_HERSHEY_SIMPLEX, .5, status_color, 1)
        ret, jpeg = cv.imencode('.jpg', frame)
        return jpeg.tobytes()

    #convert frame to grey, compute Gaussian blur for noise reduction, update ave,
    #compute weighted averages, compute difference between wieghted ave and grayscale frame to get delta (background bodel - grayscale frame)
    def imgProcess(frame, self):
        #convert to grayscale image
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        #blur image to reduce noise (filter size 21X21)
        kernel_size=(7,7) #can differ but both must be positive and odd
        gray = cv.GaussianBlur(gray, kernel_size,0)
        #if first loop, need to set avg
        if self.avg is None:
            self.avg = gray.copy().astype("float")
        alpha = 0.5
        #get weighted average of prev frame
        cv.accumulateWeighted(gray, self.avg, alpha=alpha)
        #compute difference between first frame and cur frame
        frameDelta = cv.absdiff(gray, cv.convertScaleAbs(self.avg))
        thresh = cv.threshold(frameDelta, 2, 255, cv.THRESH_BINARY)[1]
        #dilate the threshold image to fill in holes
        dil = cv.dilate(thresh, None, iterations=2)
        #get contours
        cnts = cv.findContours(dil.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if len(cnts) == 2:
            cnts = cnts[0]
        elif len(cnts) == 3:
            cnts = cnts[1]
        else:
            print("something went wrong with contours:(")
        return cnts

    def rescaleFrame(frame, scale):
        #scale the width and height, (cast to int)
        width = int(frame.shape[1] * scale)
        height =int(frame.shape[0] * scale)
        dimensions = (width, height)
        #return resize frame to particular dimension
        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

@login_required
def home(request):
    return render(request, 'core/home.html')

def gen(camera):
	while True:
		# frame = camera.get_frame()
		frame = b'test'
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def feed(request):
	return StreamingHttpResponse(gen(None),
					content_type='multipart/x-mixed-replace; boundary=frame')

