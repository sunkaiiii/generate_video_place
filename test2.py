import pano
import cv2
import os

def read_video(filename):
    cap=cv2.VideoCapture(filename)
    rate = cap.get(cv2.CAP_PROP_FPS)
    count=0
    success, frame = cap.read()
    imageCount=0
    while success:
        success, frame = cap.read()
        count+=1
        if count>=rate:
            if not os.path.exists('stitchImage'):
                os.mkdir('stitchImage')
            (shotname, extension)=os.path.splitext(filename)
            shotname=shotname.split('\\')[len(shotname.split('\\'))-1]
            if not os.path.exists('stitchImage\\'+shotname):
                os.mkdir('stitchImage\\'+shotname)
            # frame=cv2.resize(frame,(960,544))
            cv2.imencode(".jpg", frame)[1].tofile(
                'stitchImage\\'+shotname+'\\'+str(imageCount)+'.jpg')
            imageCount+=1
            count=0

def read_file_list(path):
    if os.path.isdir(path):
        pathlist=os.listdir(path)
        for file in pathlist:
            read_video(path+'\\'+file)

# #
# img1=cv2.imread('E:\\test\\1.jpg')
# # cv2.resize(img1,(480, 320))
# img2=cv2.imread("E:\\test\\2.jpg")
# # cv2.resize(img2,(480, 320))
# img3=cv2.imread('E:\\test\\3.jpg')
# # cv2.resize(img3,(480, 320))
# stitch=pano.Stitch([img1,img2,img3],mode=1)

# read_file_list('D:\文件与资料\Onedrive\文档\PycharmProjects\internship_working\cut\\1')
read_video('E:\\2.mp4')
#
stitch=pano.Stitch('stitchImage\\2')
stitch.leftshift()
# # s.showImage('left')
stitch.rightshift()
print("done")
cv2.imwrite("test7-293.jpg", stitch.leftImage)
print("image written")
cv2.destroyAllWindows()