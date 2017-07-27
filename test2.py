import numpy as np
import cv2

# cap=cv2.VideoCapture('D:\文件与资料\Onedrive\文档\PycharmProjects\internship_working\cut\\1\\1_271.avi')
# fgbg=cv2.createBackgroundSubtractorMOG2(50,20,True)
#
# success=True
# while(success):
#     success,frame=cap.read()
#     fgmask=fgbg.apply(frame)
#     cv2.imshow('frame',fgmask)
#     cv2.waitKey(30)
# cap.release()
# cv2.destroyAllWindows()
# cv2.ocl.useOpenCL()
cv2.ocl.setUseOpenCL(flag=False)
img1=cv2.imread("d:\\1.jpg")
img2=cv2.imread('d:\\2.jpg')
sticher=cv2.createStitcher()
# cv2.cv2.createStitcher().
sticher.stitch(img1,img2)