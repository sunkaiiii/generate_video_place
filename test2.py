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

a=[1,2,3]
b=[2,3,4]
c=[1,2,3]

print(a.any(b))
print(a.any(c))
print(a.all(b))
print(a.all(c))