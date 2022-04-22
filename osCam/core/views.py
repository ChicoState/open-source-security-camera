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
from .models import NextPath, Path, StorageHandler
from django.contrib.auth.models import User

class PathDataDialog(object):
	DEFAULT_PATH = "/"
	SENTINAL_PATH = "$PATH"
	SENTINAL_OPEN_PATH = "$OPEN_PATH"
	def __init__(self) -> None:
		self.show = False
		self.path = self.DEFAULT_PATH

<<<<<<< HEAD
	def updateVisibility(self, visible:Boolean) -> None:
		self.show = visible
	def updatePath(self, updatePath:Str) -> None:
		self.path=updatePath
=======
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
>>>>>>> f78c4c4 (Adding configuration page, added variables in models for Camera setup.)

	def displayPath(self)  -> None:
		print("[$Path]: {}".format(self.path))

	def showDialog(self) -> Boolean:
		return self.show




# Create your views here.
# import cv2 as cv
# from cv2 import imshow
# from cv2 import VideoWriter
# from datetime import datetime
# import time

# class MotionDetect():
#     def __init__(self):
#         #usb cam for testing, change for pi
#         self.video = cv.VideoCapture(0)
#         self.codec = cv.VideoWriter_fourcc(*'XVID')
#         #self.filePath = "videos/{}.avi".format(datetime.now().strftime("%Y_%m_%d, %H:%M:%S"))
#         self.avg = None
#         self.out = None
#         self.numframes = 0
#         self.record = False
#         self.rotate = False
#     def __del__(self):
#         self.video.release()
#     def get_frame(self):
#         success, frame = self.video.read()
#         if(not success):
#             print("did not read from camera")
#             time.sleep(2)
#         if self.rotate:
#             frame = cv.flip(frame,0)
#         frame = MotionDetect.rescaleFrame(frame, .75)
#         if not success:
#             print("could not get image from cammera")
#         text = "searching..."
#         cnts = MotionDetect.imgProcess(frame, self)
#         for c in cnts:
#             #if contours are less than desired area cont
#             if cv.contourArea(c) < 5000:
#                 continue
#             #set boundaries for motion box from contours
#             (x,y,w,h) = cv.boundingRect(c)
#             #set color to draw box:
#             color = (0,0,255)
#             #motion box line thickness
#             thickness = 2
#             #set motion box on frame
#             cv.rectangle(frame, (x,y), (x+w, y+h), color, thickness)
#             #change notification text
#             text = "Motion!"
#         #add text to frame
#         if text == "Motion!":
#             status_color = (0,0,255)
#         else:
#             status_color=(0,255,0)
#         cv.putText(frame, "Status: {}".format(text), (15,15), cv.FONT_HERSHEY_SIMPLEX, .5, status_color, 1)
#         #current date/time
#         date_time = datetime.now()
#         cv.putText(frame, "Date/Time: {}".format(date_time.strftime("%Y/%m/%d, %H:%M:%S")), (200,15), cv.FONT_HERSHEY_SIMPLEX, .5, status_color, 1)
#         ret, jpeg = cv.imencode('.jpg', frame)
#         if self.record:
#             if self.out == None:
#                 self.out = MotionDetect.setRecording(date_time.strftime("%Y/%m/%d, %H:%M:%S"), frame)
#             if text == "Motion!":
#                 self.numframes+=1
#                 self.out.write(frame)
#             #if number of frames in recording is greater than 500 save recording and start new recording file
#             if self.numframes > 250:
#                 self.numframes = 0
#                 self.out.release()
#                 date_time = datetime.now().strftime("%Y_%m_%d, %H:%M:%S")
#                 self.out= MotionDetect.setRecording(date_time, frame)
#         return jpeg.tobytes()

#     #convert frame to grey, compute Gaussian blur for noise reduction, update ave,
#     #compute weighted averages, compute difference between wieghted ave and grayscale frame to get delta (background bodel - grayscale frame)
#     def imgProcess(frame, self):
#         #convert to grayscale image
#         gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#         #blur image to reduce noise (filter size 21X21)
#         kernel_size=(7,7) #can differ but both must be positive and odd
#         gray = cv.GaussianBlur(gray, kernel_size,0)
#         #if first loop, need to set avg
#         if self.avg is None:
#             self.avg = gray.copy().astype("float")
#         alpha = 0.5
#         #get weighted average of prev frame
#         cv.accumulateWeighted(gray, self.avg, alpha=alpha)
#         #compute difference between first frame and cur frame
#         frameDelta = cv.absdiff(gray, cv.convertScaleAbs(self.avg))
#         thresh = cv.threshold(frameDelta, 2, 255, cv.THRESH_BINARY)[1]
#         #dilate the threshold image to fill in holes
#         dil = cv.dilate(thresh, None, iterations=2)
#         #get contours
#         cnts = cv.findContours(dil.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#         if len(cnts) == 2:
#             cnts = cnts[0]
#         elif len(cnts) == 3:
#             cnts = cnts[1]
#         else:
#             print("something went wrong with contours:(")
#         return cnts
#     def setRecording(fileName, frame):
#         #type of codec (os dependent, currently working for ubunto 20.4)
#         codec = cv.VideoWriter_fourcc(*'XVID')
#         #where to save files
#         filePath = "videos/{}.avi".format(fileName)
#         #set frame rate for recording
#         fps = 15
#         width, height, channels = frame.shape
#         #return output object
#         return cv.VideoWriter(filePath, codec, fps, (height, width))
#     def rescaleFrame(frame, scale):
#         #scale the width and height, (cast to int)
#         width = int(frame.shape[1] * scale)
#         height =int(frame.shape[0] * scale)
#         dimensions = (width, height)
#         #return resize frame to particular dimension
#         return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

def getNextPathList(curUser: User, pathBuilder: Path) -> list:
	# returns alist of children paths relative to our current Path in FileTree
	nextPaths = []
	print("Get Next Path List ??")
	for _name in os.listdir(pathBuilder.path):
		subdir = os.path.join(pathBuilder.path, _name)
		if os.path.isdir(subdir):
			print(_name)
			nextPaths.append(_name)

	return nextPaths	

def updatePathNext(pid: int, nextPaths: list) -> None:
	# Updates a Path's 'NEXT" entry, such that a path has a LIST of its children $paths
	print("Updating Path.next [it] {}".format(str(pid)))
	_curPath = Path.objects.get(id=pid)
	# it = _curPath.next
	print("Looking at [it] {}".format(str(_curPath.path)))
	for _next in nextPaths:
		# it:NextPath = NextPath.objects.create(
		# 	data=_next
		# )
		new_next = _curPath.next_set.create(
			data=_next
		)
		print("FOUND Data: ",new_next.data)
		print("Register: {} -- {}".format(_curPath.path,new_next.data))
		# _curPath.
		# _curPath.save()


def getFilePathContext(request) -> dict:
	# path = []
	# cur_path = None
	builder = request.POST.get("$PATH")
	print("Builder: {}".format(builder))
	# current_path
	this_user = User.objects.get(id=request.user.id)
	nextPaths:list = []
	# default_path:Path = None
	default_path_builder: Path = Path.objects.get(user=this_user)
	# print(f"Most Recent Path: {default_path.path} \n\n")
	nextPaths = getNextPathList(curUser=this_user, pathBuilder=default_path_builder)
	context = {"pathBuilder":default_path_builder, "nextPathList": nextPaths}
	
	# return (cur_path,nextPaths)
	return context
		# for record in default_path:
		# 	# cur_path += "/"+ record.path
		# 	print(f"record: {record}")
		# if default_path and default_path != '':
		# 	print()
		# 	print("cur path is: ".format(default_path))
		# 	print()
		# 	nextPaths = []
		# 	pth_main = []
		# 	# print(os.listdir(cur_path))
		# 	for sub in os.listdir(default_path.path):
		# 		subdir = os.path.join(default_path.path, sub)
		# 		if os.path.isdir(subdir):
		# 			print(sub)
		# 			nextPaths.append(sub)
					# p = Path(user=this_user, path=default_path.path)
					# for _path in pth_main:
					# nxtPath = NextPath(path=default_path.path, next=_path)
					# nxtPath.save()
					# pth_main.append(p)
					# p.save()

		
	# while True:
	# cur_path ='/'
		# choice = input("choose directory:") # this is same as waiting for request
		# if choice == 'back':
		# 	if len(path) == 0:
		# 		path.append('../')
		# 	else:
		# 		path.pop()
		# elif choice != 'back':
	# path.append(cur_path)
	# for el in path:
	# 	cur_path+= '/' + el
	# if default_path and default_path != '':
	# 	print()
	# 	print("cur path is: {}".format(default_path))
	# 	print()
	# 	nextPaths = []
	# 	# print(os.listdir(cur_path))
	# 	for sub in os.listdir(default_path):
	# 		subdir = os.path.join(default_path, sub)
	# 		if os.path.isdir(subdir):
	# 			print(sub)
	# 			nextPaths.append(sub)
	# 			Path(user=this_user, path=default_path, next=sub)

		# else:
		#     print("cur path is: .")
		#     print(os.listdir('.'))
	# context = {"pathBuilder":default_path, "nextPathList": nextPaths}
	# # return (cur_path,nextPaths)
	# return context

def displaySetStoragePath(request):

	# 	# =(1) get All 'next' paths set up in DB.model
	# 	# (2) Set Storage mode to UPDATE
	# 	# (3) append new Path
	# pathDataDialog = PathDataDialog()
	this_user = User.objects.get(id=request.user.id)
	next_path_list = []
	_full_path=Path.objects.filter(user=this_user)
	print("FULL_PATH {}".format(_full_path))
	full_path=""
	# for data in _full_path:
	# 	full_path+=data.path 

	full_path += "/"+request.POST.get("$PATH")
	cur_path_builder: Path = None 
	# if no Path objects exist yet for this user
	# - we create one and peek at its children
	if Path.objects.filter(user=this_user).exists():
	# 	# turn on Storate update permissions.
		cur_path_builder = Path( 
			user=this_user,
			path= "/" + request.POST.get("$PATH"),
		)
		
	# 	next_path_list=getNextPathList(this_user, this_path.path)
		for _data in next_path_list:
			cur_path_builder.next=NextPath.objects.create(
				data=_data
			)
		# cur_path_builder.storage=StorageHandler(user=this_user, update=True).save()

		storage_rule = StorageHandler.objects.get(user=this_user)
		storage_rule.user=this_user
		storage_rule.update = True 
		if storage_rule.fullpath is None:
			storage_rule.fullpath = ""
		else:
			storage_rule.fullpath += "/" + request.POST.get("$PATH")
		storage_rule.save()

		cur_path_builder.storage = storage_rule
		cur_path_builder.save()

		next_path_list = getNextPathList(this_user, cur_path_builder)
		# storage_rule:StorageHandler = cur_path_builder
		# StorageHandler.objects.get(id=cur_path_builder.id)
		# storage_rule=StorageHandler.objects.get(user=this_user)
		# storage_rule.update=False
		# full_path = storage_rule.fullpath
		# storage_rule.save()
		# return {
		# "update_path_dialog":storage_rule.update,
		# "path": full_path, 
		# "nextpaths":next_path_list,
		# }
	elif Path.objects.filter(user=this_user).none():

		storage_rule = StorageHandler.objects.create(
					user=this_user,
					update=True
				)
		cur_path_builder = Path.objects.create(
				user=this_user,
				path=PathDataDialog.DEFAULT_PATH,
				storage=storage_rule
		)

	# mypath = Path.objects.get(user=this_user)
	nextPaths = []
	print("Get Next Path List ??")
	pathBuilder = "/"+request.POST.get("$PATH")
	for _name in os.listdir():
		subdir = os.path.join(pathBuilder, _name)
		if os.path.isdir(subdir):
			print(_name)
			nextPaths.append(_name)
	# storage_rule:StorageHandler = cur_path_builder
	# StorageHandler.objects.get(id=cur_path_builder.id)
	storage_rule=StorageHandler.objects.get(user=this_user)
	storage_rule.update=True
	full_path = storage_rule.fullpath
	storage_rule.save()
		# Path.objects.get(user=this_user)

	print("\n[Created New FilePath for User [{}]]".format(this_user.username))
	return {
		"update_path_dialog":StorageHandler.objects.get(user=this_user).update,
		"path": storage_rule.fullpath, 
		"nextpaths":nextPaths,
		}


def displayCurrentStorageView(request, aUser:User):
	current_path_builder = request.GET
	print("\n\nREQUEST: {}".format(current_path_builder))
	next_path_list: list = []
	default_path_builder: Path = None
	storage_rule: StorageHandler = None
	if "$EDIT" in request.GET:
		print("\n\n$edit REQUEST: {}".format(current_path_builder))
		if Path.objects.get(user=aUser).exists():
			default_path_builder = Path.objects.get(user=aUser)
			# print(f"Most Recent Path: {default_path_builder.path} \n\n")
			default_path_builder.storage.objects.update_or_Create(
				update=True
			)
			next_path_list = getNextPathList(curUser=aUser, pathBuilder=default_path_builder)
			context = {"pathBuilder":default_path_builder, "nextPathList": next_path_list}
			print("path-builder: {}".format(default_path_builder))
			print("\n\tNextPath: {}".format(next_path_list))
			storage_rule=default_path_builder.storage.objects.get(id=default_path_builder.id)
			next_path_list = getNextPathList(curUser=aUser, pathBuilder=default_path_builder)
			# make sure to turn off after editing..
			storage_rule.update_or_create(
				update=False
			)
			return render(request, 'core/home.html', {
				"update_path_dialog":True,
				"path":default_path_builder.path, 
				"nextpaths":next_path_list
				})

	else:
		if Path.objects.filter(user=aUser).exists():
			display = Path.objects.get(user=aUser)
			
			# display_storage_rule = storage_rule.objects.get(user=aUser)
			display_nextPathList = getNextPathList(aUser, display)
			return render(request, 'core/home.html', {
					"update_path_dialog":True,
					"path":display.path,
					"nextpaths":display_nextPathList
					})
		else:
			# display Default $Path info
			# display_storage_rule = StorageHandler.objects.get(user=aUser)
			return render(request, 'core/home.html', {
					"update_path_dialog":False,
					"path":PathDataDialog.DEFAULT_PATH,
					"nextpaths":[PathDataDialog.SENTINAL_OPEN_PATH]
					})
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

<<<<<<< HEAD
	# return StreamingHttpResponse(gen(MotionDetect()),
	# 				content_type='multipart/x-mixed-replace; boundary=frame')
=======
>>>>>>> f78c4c4 (Adding configuration page, added variables in models for Camera setup.)
