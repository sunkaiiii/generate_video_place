import cv2
import os
"""
视频场景拼接
"""
stich_path="stichImage\\"

def read_video(filename):
    '''
    将视频每秒的内容提取出来
    :param filename: 视频文件路径
    :return: 视频文件名，用来拼接
    '''
    cap=cv2.VideoCapture(filename)
    rate = cap.get(cv2.CAP_PROP_FPS)
    count=0
    success, frame = cap.read()
    imageCount=0
    while success:
        success, frame = cap.read()
        count+=1
        if count>=rate:
            if not os.path.exists(stich_path):
                os.mkdir(stich_path)
            (shotname, extension)=os.path.splitext(filename)
            shotname=shotname.split('\\')[len(shotname.split('\\'))-1]
            if not os.path.exists(stich_path+shotname):
                os.mkdir(stich_path+shotname)
            # frame=cv2.resize(frame,(960,544))
            cv2.imencode(".jpg", frame)[1].tofile(
                stich_path+shotname+'\\'+str(imageCount)+'.jpg')
            imageCount+=1
            count=0
    stitcher_iamge(shotname)


def stitcher_iamge(shotname):
    """
    使用OpenCV的stitcher进行拼接
    ****需要OpenCV 3.3.0****
    OpenCV 3.3.0以下的版本stitcher不能正确的运行，详情参考 https://github.com/opencv/opencv/issues/6969#issuecomment-326430615
    :param shotname:
    """
    imgs=[]
    for file in os.listdir(stich_path+shotname):
        imgs.append(cv2.imread(stich_path+shotname+'\\'+file))
    stitcher = cv2.createStitcher(False)
    result = stitcher.stitch(imgs)
    cv2.imwrite(stich_path+shotname+'\\'+"stich_result.jpg", result[1])

def read_file_list(path):
    if os.path.isdir(path):
        pathlist=os.listdir(path)
        for file in pathlist:
            read_video(path+'\\'+file)



read_video('E:\\2.mp4')
