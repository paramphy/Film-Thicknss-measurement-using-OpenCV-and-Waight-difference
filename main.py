import cv2
import numpy as np
import utlis
from matplotlib import pyplot as plt
import tkinter as tk

#Defining Empty
def empty(a):
    pass

#Get Contour Function
def getContours(img,filter,minArea):
    #imgContour = img.copy()
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    arealist = []
    recarealist = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #cv2.drawContours(img,cnt,-1,(255,0,0),3)
        if area > minArea:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            area1 = cv2.contourArea(cnt)
            #print(peri)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            #print(len(approx))
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
            if objCor == filter:
                recarealist.append(area)
                objectType = 'Rectangle'
            elif objCor > filter:
                arealist.append(area)
                objectType = 'None'
            else:
                objectType = 'None'
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(imgContour, objectType, (x + w - 100, y + h - 100),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(imgContour, str(area), (x + w - 100, y + h - 200),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            print('area',arealist)
            print('rectangle_area',recarealist)

#Defining Trackbars
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
cv2.createTrackbar("Canny X","TrackBars",0,300,empty)
cv2.createTrackbar("Canny Y","TrackBars",0,300,empty)
cv2.createTrackbar("Karnel","TrackBars",5,10,empty)
cv2.createTrackbar("Threshold","TrackBars",50,255,empty)
cv2.createTrackbar("Minimum Area","TrackBars",1000,10000,empty)



while True:
    img = cv2.imread("2_film.jpg")
    imgContour = img.copy()
    cx = cv2.getTrackbarPos("Canny X", "TrackBars")
    cy = cv2.getTrackbarPos("Canny Y","TrackBars")
    k = cv2.getTrackbarPos("Karnel", "TrackBars")
    thres = cv2.getTrackbarPos("Threshold","TrackBars")
    minArea = cv2.getTrackbarPos("Minimum Area","TrackBars")


    kernel = np.ones((k, k), np.uint8)
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgblur = cv2.GaussianBlur(imgGrey, (k, k), 1)
    #imgThres1 = cv2.ADAPTIVE_THRESH_MEAN_C(imgblur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,1)
    _,imgThres = cv2.threshold(imgblur,thres,255,cv2.THRESH_BINARY_INV)
    imgCanny = cv2.Canny(imgThres, cx, cy)
    imgDialation = cv2.dilate(imgCanny, kernel, 1)
    imgErode = cv2.erode(imgDialation, kernel, 1)
    imageContour = getContours(imgErode,4,minArea)
    #print(imgContour)

    imgStack = utlis.stackImages(.15, ([img,imgThres, imgContour]))
    imgContour = cv2.resize(imgContour,(0,0),None,.5,.5)

    cv2.imshow("Image Stacks", imgStack)
    cv2.waitKey(1)

