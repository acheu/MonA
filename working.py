import numpy as np
import cv2
import imutils
import argparse
import time

#Monitoring Always - MonA

while(True): #main body loop function 

    cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    # folder = '/home/chewie/Videos/webcamFeed-Dragon/' #location of output files 
    folder = '/mona/readyshare/webcamFeed/' #Mounted NAS 
    framePrev = 0
    firstFrame = []
    movementFlag = False
    min_area = 100
    holdTime = 20 #Seconds
    triggerTime = 0

    while(cap.isOpened()):    
        ret, frame = cap.read()
        if ret==True:
            
            # Convert to grayscale and smooth
            frameR = imutils.resize(frame, width=500)
	    gray = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray,(21,21),0)

            if firstFrame == []:
                firstFrame = gray
                continue

            # Computer difference between first frame and current
            frameDelta = cv2.absdiff(firstFrame,gray)
            thresh = cv2.threshold(frameDelta,127,255,cv2.THRESH_BINARY)[1]

            # Dilate the threshold image to fill in holes then find contors?
            thresh = cv2.dilate(thresh, None, iterations=2)
            (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if triggerTime == 0:
                for c in cnts:
                    if cv2.contourArea(c) > min_area and movementFlag == False:
                        movementFlag = True
                        outFile = folder + str(int(time.time())) + '.avi'
                        out = cv2.VideoWriter(outFile,fourcc, 5.0, (640,480))
                        triggerTime = time.time()
                        break
                    else:
                        movementFlag = False
            else:
                x = 10
                y = 20
                text_color = (0, 0, 0)             
                
                cv2.putText(frame, time.strftime('%X %x %Z'), (x,y), cv2.FONT_HERSHEY_PLAIN, 1.0, text_color, thickness=1)
                out.write(frame)
                #cv2.imshow('frame',frame)
                #cv2.startWindowThread()
                if time.time() > triggerTime + holdTime:
                    out.release()
                    cap.release()
                    break
                    movementFlag = False #toggle movement flag off
                    triggerTime = 0 #reset trier

        else:
            continue
