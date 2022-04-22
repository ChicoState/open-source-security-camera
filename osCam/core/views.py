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

import cv2 as cv
from cv2 import imshow
from cv2 import VideoWriter
from datetime import datetime
import time


class MotionDetect():
    def __init__(self):
        self.video = cv.VideoCapture(0)
        self.codec = cv.VideoWriter_fourcc(*'XVID')
        self.BoxColor = (0,0,255)
        self.searchTextColor = (0,0,255)
        self.motionTextColor = (0,0,255)
        self.searchText = ["searching   ", "searching.  ", "searching.. ", "searching..."]
        self.motionText = ["Motion   ","Motion!  ","Motion!! ","Motion!!!"]
        self.scale = .75
        self.avg = None
        self.out = None
        self.flip = False
        self.mirror = False
        self.showBoxes = True
        self.detected = False
    
    def __del__(self):
        self.video.release()
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
    def get_frame(self):
        success, frame = self.video.read()
        if(not success):
            print("did not read from camera")
            time.sleep(2)
        frame = MotionDetect.rescaleFrame(frame, self.scale)
        frame = MotionDetect.flipFrame(self, frame)
        frame = MotionDetect.mirrorFrame(self, frame)
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
        status_color = MotionDetect.setStatusColor(self)
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
	# path = None
	# cpath="/"
	pathDataDialog = PathDataDialog()
	this_user = User.objects.get(id=request.user.id)
	path_list = []
	print("REQUEST_post: ",request.POST)

	print("REQUEST_get: ",request.GET)

	if request.method == 'POST':
		if "$PATH" in request.POST:
			print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
			builder = request.POST.get("$PATH")
			print("\n\n%%%[MAIN__HOME.path-builder]: {}".format(builder))
			print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
			ui_context = displaySetStoragePath(request)
			return render(request, 'core/home.html', ui_context)
		else:
			print("[MAIN_HOME.request.isEMpty()]")
			
	elif request.method == 'GET':
		print("\n\nFound Path: {}".format(str(request.GET)))
		print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
		print("Request.GET")
		print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
		displayCurrentStorageView(request, this_user)
			
		next_path_list: list = []
		default_path_builder: Path = None
		storage_rule: StorageHandler = None
		if "$EDIT" in request.GET:
			print("\n\n$edit REQUEST: {}".format(request.GET))
			if Path.objects.get(user=this_user).exists():
				default_path_builder = Path.objects.get(user=this_user)
				# print(f"Most Recent Path: {default_path_builder.path} \n\n")
				default_path_builder.storage.objects.update_or_Create(
					update=True
				)
				next_path_list = getNextPathList(curUser=this_user, pathBuilder=default_path_builder)
				context = {"pathBuilder":default_path_builder, "nextPathList": next_path_list}
				print("path-builder: {}".format(default_path_builder))
				print("\n\tNextPath: {}".format(next_path_list))
				storage_rule=default_path_builder.storage.objects.get(id=default_path_builder.id)
				next_path_list = getNextPathList(curUser=this_user, pathBuilder=default_path_builder)
				# make sure to turn off after editing..
				storage_rule.update_or_create(
					update=False
				)
				return render(request, 'core/home.html', {
					"update_path_dialog":True,
					"path":default_path_builder.path, 
					"nextpaths":next_path_list
					})

		else: #no Request Query Params..
			if Path.objects.filter(user=this_user).exists():
				display = Path.objects.get(user=this_user)
				
				# display_storage_rule = storage_rule.objects.get(user=aUser)
				display_nextPathList = getNextPathList(this_user, display)
				return render(request, 'core/home.html', {
						"update_path_dialog":True,
						"path":display.path,
						"nextpaths":display_nextPathList
						})
			else:
				# display Default $Path info
				displayStorage = Path.objects.all()
				builder = {"fullpath":[]}
				stringifyBuilder = None
				for displayPath in displayStorage:
					builder["fullpath"].append(displayPath.path)
				stringifyBuilder = json.dumps(builder)
				display_storage_rule,created = StorageHandler.objects.get_or_create(user=this_user, 
					update=True,
					fullpath=stringifyBuilder,
				)
				return render(request, 'core/home.html', {
						"update_path_dialog":display_storage_rule.update,
						"path":PathDataDialog.DEFAULT_PATH,
						"nextpaths":getNextPathList(this_user, Path(PathDataDialog.DEFAULT_PATH))
						})

	# return render(request, 'core/home.html', {
	# 		"path_dialog":pathDataDialog.showDialog(),
	# 		"path":"$PAth is empty!", 
	# 		"nextpaths":["$EDIT"]
	# 		})



def gen(camera):
	while True:
		# frame = camera.get_frame()
		frame = b'test'
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def feed(request):
	return StreamingHttpResponse(gen(None),
					content_type='multipart/x-mixed-replace; boundary=frame')

	# return StreamingHttpResponse(gen(MotionDetect()),
	# 				content_type='multipart/x-mixed-replace; boundary=frame')
