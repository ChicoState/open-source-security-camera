from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse
from django.contrib.auth.decorators import login_required

# Open CV Motion Detect And Video Stream. Need to refactor and put this in app 'Streams' that already has architecture set .
import cv2 as cv
from cv2 import imshow
from cv2 import VideoWriter
from datetime import datetime
import time

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
    def setRecording(fileName, frame):
        #type of codec (os dependent, currently working for ubunto 20.4)
        codec = cv.VideoWriter_fourcc(*'XVID')
        #where to save files
        filePath = "videos/{}.avi".format(fileName)
        #set frame rate for recording
        fps = 15
        width, height, channels = frame.shape
        #return output object
        return cv.VideoWriter(filePath, codec, fps, (height, width))
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
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def feed(request):
	return StreamingHttpResponse(gen(MotionDetect()),
					content_type='multipart/x-mixed-replace; boundary=frame')

