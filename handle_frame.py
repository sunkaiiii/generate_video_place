#coding=utf-8
import cv2
import base64
from PIL import Image

"""
 -------------compare_frame-------------
提供了直方图、平均哈希、感知哈希三种方式判断场景
可以根据需要选择不同的方法来判断场景来剪裁视频
"""

def calculate(img1,img2):
    """
    计算直方图的相关性
    :return: 返回值dgree为相关性系数，一般认为>0.7的时候即为相似场景
    """
    hist1 = cv2.calcHist([img1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0.0, 255.0])
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


def classify_hist_with_split(img1,img2):
    """
    将传入的图标通道分离，分别计算三个通道的直方图相关性系数
    :return: 当返回值<0.7（默认值）的时候，认为场景发生了改变
    """
    sub_img1=cv2.split(img1)
    sub_img2=cv2.split(img2)
    sub_data=0
    for im1,im2 in zip(sub_img1,sub_img2):
        sub_data+=calculate(im1,im2)
    sub_data=sub_data/3
    return sub_data

def cal_area_with_classify_pixel(img1,img2):
    count=0
    height,width,channel=img1.shape
    # print(height,width)
    for h in range(height):
        for w in range(width):
            if img1[h,w].tolist() != img2[h,w].tolist():
                # print(img1[h, w],img2[h,w])
                count += 1
    # print(count)

    return count/(height*width)

def image_to_base64(frame):
    # frame = Image.fromarray(img1, 'RGB').tobytes()
    # frame=frame.tobytes()
    image_base64=base64.b64encode(frame)
    return image_base64

def merge_tow_and_cal_area(rect1,rect2):
    class point:
        def __init__(self):
            self.x = 0
            self.y = 0

    p1=point()
    p2=point()

    p1.x=max(rect1['left'],rect2['left'])
    p1.y=max(rect1['top'],rect2['top'])
    p2.x=max((rect1['left']+rect1['width']),(rect2['left']+rect2['width']))
    p2.y=max((rect1['top']+rect1['height']),(rect2['top']+rect2['height']))
    Ajoin=0
    if(p2.x>p1.x and p2.y>p1.y):
        Ajoin=(p2.x-p1.x)*(p2.y-p1.y)
    A1=rect1['width']*rect1['height']
    A2=rect2['width']*rect2['height']
    AUnion=(A1+A2-Ajoin)
    if(AUnion>0):
        return Ajoin
    else:
        return A1+A2

if __name__ == "__main__":
    img1=cv2.imread('d:\\1.jpg')
    img2=open('d:\\1.jpg','rb')
    img2=img2.read()
    # print(img2)
    frame = Image.fromarray(img1, 'RGB').tobytes()
    print(frame)
    # img2=base64.b64encode(img2)
    # print(img2)
    # # img2=cv2.imread('d:\\3.jpg')
    # # print(cal_area_with_classify_pixel(img1,img2))
    # print(image_to_base64(img1))