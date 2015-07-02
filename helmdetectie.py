#-------------------------------------------------------------------------------
# Name:        helmdetectie
# Purpose:     detecteren van de te volgen helm en commando's voor besturing doorgeven
#
# Author:      Cedric Liefhebber
#
# Created:     18-05-2015
# Copyright:   (c) Cedric Liefhebber 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cv2
import numpy as np
import time

cam = cv2.VideoCapture(0)

time.sleep(1)
retval, img = cam.read()
height, width = img.shape[:2]
print "hoogte, breedte:", height, width

#values for color filtering
#color_goal values for different colours:
#blue ~ 110
#yellow ~ ?
color_goal = 15
range_max = 15
color_min = np.array([color_goal-range_max,100,30],np.uint8)
color_max = np.array([color_goal+range_max,255,255],np.uint8)

#values for image processing
morphval = 6 #kernel size of morphological transformation
itercnt = 3 #amount of iterations
size_goal = 30 #pixel radius die de helm moet zijn
#kleiner betekend dat te drone te ver weg is, groter is te dichtbij

while True:
    retval,img = cam.read()
    if(retval == True ):
        img_hsv = cv2.cvtColor(img, cv2.cv.CV_BGR2HSV)
        img_treshold = cv2.inRange(img_hsv,color_min, color_max)
        img_closed = cv2.morphologyEx(img_treshold, cv2.MORPH_OPEN, np.ones((morphval,morphval),np.uint8), iterations = itercnt)
        img_mask = cv2.bitwise_and(img,img, mask = img_closed)
        img_final = img_mask

#tekenen van visualizatie
        cv2.line(img_final,(width/2,0),(width/2,height),(0,255,0),2,)
        cv2.line(img_final,(0,height/2),(width,height/2),(0,255,0),2,)
        cv2.circle(img_final,(width/2,height/2),size_goal,(0,255,0),2)
        cv2.putText(img_final,"Richting:",(0,height-15),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        cv2.imshow("beeld1",img_final)
        if(cv2.waitKey(10) == 27):
            cv2.destroyAllWindows()
            cam.release()
            break
