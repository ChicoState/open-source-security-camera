import cv2 as cv
from cv2 import imshow

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
    gray = cv.GaussianBlur(gray, (11,11),0)
    #if first loop, need to set avg
    if avg is None:
        avg = gray.copy().astype("float")
    #get weighted average of prev frame
    cv.accumulateWeighted(gray, avg, 0.5)
    #compute difference between first frame and cur frame
    frameDelta = cv.absdiff(gray, cv.convertScaleAbs(avg))
    thresh = cv.threshold(frameDelta, 5, 255, cv.THRESH_BINARY)[1]
    #dilate the threshold image to fill in holes
    thresh = cv.dilate(thresh, None, iterations=2)
    #get contours
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(cnts) == 2:
        cnts = cnts[0]
    elif len(cnts) == 3:
        cnts = cnts[1]
    else:
        print("something went wrong, exiting program :(")
    return avg, cnts
#get background subtraction with k nearest neighbor
backSubknn = cv.createBackgroundSubtractorKNN()
#innitial video capture: source ov vid or file path/name
capture = cv.VideoCapture(0)
#initially the average frame is 0, set in loop from grayscale image
avg = None
#infinate loop and capture video until 'd' is pressed
while True:
    text = "searching..."
    #read video, gets a bool and frame
    isTrue, frame = capture.read()
    #resize frame
    frame_resized =rescaleFrame(frame, 1)
    #convert to grayscale image
    avg, cnts = imgProcess(frame_resized, avg)
    for c in cnts:
        #if contours are less than desired area cont
        if cv.contourArea(c) < 7000:
            continue
        #set boundaries for motion box from contours
        (x,y,w,h) = cv.boundingRect(c)
        #set motion box on frame
        cv.rectangle(frame_resized, (x,y), (x+w, y+h), (0, 0, 255), 2)
        #change notification text
        text = "Motion!"
    #add text to frame
    cv.putText(frame_resized, "Status: {}".format(text), (15,15), cv.FONT_HERSHEY_SIMPLEX, .5, (0,0,255), 1)
    #display the image
    cv.imshow('Video', frame_resized)
    #check for interupt
    if cv.waitKey(28) & 0xFF==ord('d'):
        break
#if escaped, releas video and destroy windows.
capture.release()
cv.destroyAllWindows()
cv.waitKey(0)