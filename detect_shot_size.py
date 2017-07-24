# -*- coding: utf-8 -*""" Created on Thu Jan 30 11:06:23 2014
import numpy as np
import cv2
fontface = cv2.CascadeClassifier('data\haarcascades\haarcascade_frontalface_alt2.xml')
prontface=cv2.CascadeClassifier('data\haarcascades\haarcascade_profileface.xml')
fullbody=cv2.CascadeClassifier('data\haarcascades\haarcascade_fullbody.xml')
lowererbody=cv2.CascadeClassifier('data\haarcascades\haarcascade_lowerbody.xml')
uperbody=cv2.CascadeClassifier('data\haarcascades\haarcascade_upperbody.xml')
eyes=cv2.CascadeClassifier('data\haarcascades\haarcascade_eye.xml')
left_eyes=cv2.CascadeClassifier('data\haarcascades\haarcascade_lefteye_2splits.xml')
right_eyes=cv2.CascadeClassifier('data\haarcascades\haarcascade_righteye_2splits.xml')
eyewithglass=cv2.CascadeClassifier('data\haarcascades\haarcascade_eye_tree_eyeglasses.xml')
# eye_cascade = cv2.CascadeClassifier('C:\Users\sunkai\PycharmProjects\OpenCv\data\haarcascades_cuda\haarcascade_eye.xml')

# img = cv2.imread('1.jpg')
color = [(0, 0, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 0, 255)]
font = cv2.FONT_HERSHEY_SIMPLEX
def generate_frame(frame,scale=1.2):
    size=frame.shape[:2]
    image=np.zeros(size,dtype=np.float16)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image=cv2.equalizeHist(image)
    divisor=12
    h, w = size
    minSize=(int(w/divisor), int(h/divisor))
    faceRects = fontface.detectMultiScale(image, scale, 2, 0|cv2.CASCADE_SCALE_IMAGE,minSize)#人脸检测
    pronRects=prontface.detectMultiScale(image, scale, 2, 0|cv2.CASCADE_SCALE_IMAGE,minSize)
    fullbodyRects=fullbody.detectMultiScale(image, scale, 1, 0|cv2.CASCADE_SCALE_IMAGE,minSize)
    lowerbodyRects=lowererbody.detectMultiScale(image, scale, 1, 0|cv2.CASCADE_SCALE_IMAGE,minSize)
    uperbodyRects=uperbody.detectMultiScale(image, scale, 1, 0|cv2.CASCADE_SCALE_IMAGE,minSize)
    eyeRects=eyes.detectMultiScale(image, scale, 1, 0|cv2.CASCADE_SCALE_IMAGE,minSize)
    leftEyesRects=left_eyes.detectMultiScale(image, scale, 1, 0|cv2.CASCADE_SCALE_IMAGE,minSize)
    rightEyesRects=right_eyes.detectMultiScale(image, scale, 1, 0|cv2.CASCADE_SCALE_IMAGE,minSize)
    eyewithglassRects=eyewithglass.detectMultiScale(image, scale, 1, 0|cv2.CASCADE_SCALE_IMAGE,minSize)
    # print(faceRects,pronRects,fullbodyRects,lowerbodyRects,uperbodyRects,eyeRects)
    if len(fullbodyRects)>0:
        for faceRect in fullbodyRects: #对每一个人脸画矩形框
                x, y, w, h = faceRect
                cv2.rectangle(frame, (x, y), (x+w, y+h), color[0])
                cv2.putText(frame,'fullbody',(x,y),font,0.6,(255,255,255),1)
    elif len(uperbodyRects)>0:
        for faceRect in uperbodyRects:
            x, y, w, h = faceRect
            cv2.rectangle(frame, (x, y), (x + w, y + h), color[1])
            cv2.putText(frame, 'upbody', (x, y), font, 0.6, (255, 255, 255), 1)
    elif len(lowerbodyRects)>0:
        for faceRect in lowerbodyRects:
            x, y, w, h = faceRect
            cv2.rectangle(frame, (x, y), (x + w, y + h), color[2])
            cv2.putText(frame, 'lowerbody', (x, y), font, 0.6, (255, 255, 255), 1)
    if len(faceRects)>0:
        for faceRect in faceRects: #对每一个人脸画矩形框
                x, y, w, h = faceRect
                cv2.rectangle(frame, (x, y), (x+w, y+h), color[3])
                cv2.putText(frame, 'frontface', (x, y), font, 0.6, (255, 255, 255), 1)
    elif len(eyewithglassRects)>0:
        for faceRect in eyewithglassRects:  # 对每一个人脸画矩形框
            x, y, w, h = faceRect
            cv2.rectangle(frame, (x, y), (x + w, y + h), color[5])
            cv2.putText(frame, 'eyeswithglass', (x, y), font, 0.6, (255, 255, 255), 1)
    # elif len(leftEyesRects)>0:
    #     for faceRect in leftEyesRects: #对每一个人脸画矩形框
    #             x, y, w, h = faceRect
    #             cv2.rectangle(frame, (x, y), (x+w, y+h), color[5])
    #             cv2.putText(frame, 'eyes', (x, y), font, 0.6, (255, 255, 255), 1)
    # elif len(rightEyesRects)>0:
    #     for faceRect in rightEyesRects: #对每一个人脸画矩形框
    #             x, y, w, h = faceRect
    #             cv2.rectangle(frame, (x, y), (x+w, y+h), color[5])
    #             cv2.putText(frame, 'eyes', (x, y), font, 0.6, (255, 255, 255), 1)
    # elif len(eyeRects)>0:
    #     for faceRect in eyeRects: #对每一个人脸画矩形框
    #             x, y, w, h = faceRect
    #             cv2.rectangle(frame, (x, y), (x+w, y+h), color[5])
    #             cv2.putText(frame, 'eyes', (x, y), font, 0.6, (255, 255, 255), 1)
    if len(pronRects)>0 :#如果人脸数组长度大于0
        for faceRect in pronRects: #对每一个人脸画矩形框
                x, y, w, h = faceRect
                cv2.rectangle(frame, (x, y), (x+w, y+h), color[4])
                cv2.putText(frame, 'profileface', (x, y), font, 0.6, (255, 255, 255), 1)
    return frame

def read_and_generate_video(filename):
    cap = cv2.VideoCapture(filename)
    success, frame = cap.read()
    while success:
        success, frame = cap.read()
        frame = generate_frame(frame)
        cv2.imshow("test", frame)  # 显示图像
        key = cv2.waitKey(24)
        c = chr(key & 255)
        if c in ['q', 'Q', chr(27)]:
            break
    cv2.destroyWindow("test")

def read_and_generate_image(filename):
    image=cv2.imread(filename)
    image=generate_frame(image)
    cv2.imshow('test',image)
    cv2.waitKey(0)
    cv2.destroyWindow('test')

def read_video_by_camera():
    cap = cv2.VideoCapture(0)
    success, frame = cap.read()
    while success:
        success, frame = cap.read()
        frame = generate_frame(frame)
        cv2.imshow("test", frame)  # 显示图像
        key = cv2.waitKey(24)
        c = chr(key & 255)
        if c in ['q', 'Q', chr(27)]:
            break
    cv2.destroyWindow("test")

# read_and_generate_video('D:\文件与资料\Onedrive\图片\Camera Roll\\Note7,iPhone 7拍的\\20161021_091733000_iOS.MOV')
read_and_generate_image('D:\\1.jpg')
# read_and_generate_video('D:\\1.mp4')
# read_video_by_camera()

