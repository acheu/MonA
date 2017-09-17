import numpy as np
import cv2
import imutils
import argparse
import time
import filehandler  # Mona Resource
import notificationbuddy as email  # Mona Resource
import pi_pins  # Mona Resource

#Monitoring Always - MonA

def main():
    emailobj = email.notificationbuddy()
    pi = pi_pins.pi1_pins()
    face_switch = False  # Face Switch - video records when TRUE
    while(True): #main body loop function
        
        face_switch = face_switch_buffer()
        if face_switch:
            cap = cv2.VideoCapture(0)
            if not cap or not cap.isOpened():
                print('Error at capture')
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')

        #folder = '/home/chewie/Videos/webcamFeed-Dragon/' #location of output files 
        folder = '/home/chewie/Downloads/'
        framePrev = 0
        firstFrame = []
        movementFlag = False
        min_area = 100
        holdTime = 10 #Seconds
        triggerTime = 0
        housekeeping(folder)  # Call function that deletes any old files
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
                            out = cv2.VideoWriter(outFile,fourcc, 30.0, (640,480))
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
                        emailobj.send_email('Motion detected')
                        break
                        movementFlag = False #toggle movement flag off
                        triggerTime = 0 #reset trigger

            else:
                continue
    emailobj.quit_server()


def face_switch_buffer():
    # This function defines when the recording will turn on after it's detected the face switch has been turned on
    zero_min = time.time()  # time to compare against
    five_min = first + 60*5  # 5 minutes later to 0min
    __ping = pi.mona_switch.ping()
    while time.time() > five_min and __ping:
        __ping = pi.mona_switch.ping()
        time.sleep(1)
    return __ping  # if there's been 5 minutes of the switch being on, then return true


def housekeeping(floc):
    flist = filehandler.GetFileList(floc)  # returns list of all files in the folder
    # Now need to iterate through all files. Files are named with their epoch time of creation
    rm_list = []
    file_lasts = time.time() - 60*60*24*7  # last time stamp in unix time that will be kept
    for i in flist:
        time_file = i.split('.')  # split apart the appended file name ie .avi
        time_file = time_file[0]  # take the string part of the name ie the unix time of recording
        u_time_file = float(time_file)  # convert to float to compare against unix time
        if u_time_file < file_lasts:
            rm_list.append(i)
    filehandler.RMFileFromList(floc, rm_list)


if __name__== "__main__":
    main()
