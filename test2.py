import numpy as np
import cv2

cap=cv2.VideoCapture('E:\电影\\Little.Forest.Natsu.Aki.2014.1080p.BluRay.x264.DTS-Yukosu.mkv')
fgbg=cv2.createBackgroundSubtractorMOG2(75,25,True)

success=True
while(success):
    success,frame=cap.read()
    fgmask=fgbg.apply(frame)
    cv2.imshow('frame',fgmask)
    cv2.waitKey(30)
cap.release()
cv2.destroyAllWindows()