import cv2 as cv
from cv2 import imshow
from cv2 import VideoWriter
from datetime import datetime
import time
#recoding setup
def setRecording(fileName, frame):
    #type of codec (os dependent, currently working for ubunto 20.4)
    codec = cv.VideoWriter_fourcc(*'XVID')
    #where to save files
    filePath = "videos/{}.avi".format(fileName)
    #set frame rate for recording
    fps = 15
    #read from frame
    isTrue, frame = capture.read()
    width, height, channels = frame.shape
    #return output object
    return cv.VideoWriter(filePath, codec, fps, (height, width))

#works for images, recordings, live video 
def rescaleFrame(frame, scale):
    #scale the width and height, (cast to int)
    width = int(frame.shape[1] * scale)
    height =int(frame.shape[0] * scale)
    dimensions = (width, height)
    #return resize frame to particular dimension
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

#convert frame to grey, compute Gaussian blur for noise reduction, update ave,
#compute weighted averages, compute difference between wieghted ave and grayscale frame to get delta (background bodel - grayscale frame)
def imgProcess(frame, avg):
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
        print("something went wrong, exiting program :(")
        exit()
    return avg, cnts
#innitial video capture: source ov vid or file path/name for usb cam
capture = cv.VideoCapture(0)
if not capture.isOpened():
    print("camera could not be opened")
    exit()
#initialize video capture: source PiCam:
avg = None
#label videos based on date/time
date_time = datetime.now().strftime("%Y_%m_%d, %H:%M:%S")
#get first frame
isTrue, frame = capture.read()
out = setRecording(date_time, frame)
#number of frames to record per video
numframes = 0
#infinate loop and capture video until 'd' is pressed
while True:
    text = "searching..."
    #read video, gets a bool and frame
    isTrue, frame = capture.read()
    if not isTrue:
        print("could not receive image frame: shutting down")
        break
    #update average frame and countour frame
    avg, cnts = imgProcess(frame, avg)
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
    #display the image
    cv.imshow('Video', frame)
    #if motion detected record:
    if text == "Motion!":
        numframes+=1
        out.write(frame)
        cv.imshow('recording', frame)
    #if number of frames in recording is greater than 500 save recording and start new recording file
    if numframes > 100:
        numframes = 0
        out.release()
        date_time = datetime.now().strftime("%Y_%m_%d, %H:%M:%S")
        out= setRecording(date_time, frame)
    #check for interupt
    if cv.waitKey(28) & 0xFF==ord('d'):
        break
#if escaped, releas video and destroy windows.
out.release()
capture.release()
cv.destroyAllWindows()
cv.waitKey(0)