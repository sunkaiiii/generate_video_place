import urllib.parse
import urllib.request
import json
import cv2
import numpy as np
import handle_frame
import Global_Variables

URL='https://api-cn.faceplusplus.com/humanbodypp/beta/detect' #fance++调用身体监测的地址
API_KEY='**************************'  #申请的api的key
API_SECRET='**************************'   #申请的api的secret

'''
暂时使用的base64将图片进行编码传输
还可以使用图片url、图片二进制进行传输，具体请参考官方文档
https://console.faceplusplus.com.cn/documents/7774430
'''
DATA = {
    'api_key': API_KEY,
        'api_secret': API_SECRET,
        'image_base64':''
}

def merge_rectangle(json_rectangles):
    rectangles = []
    for rectangle in json_rectangles:
        x1 = rectangle['left']
        x2 = rectangle['left'] + rectangle['width']
        y1 = rectangle['top']
        y2 = rectangle['top'] + rectangle['height']
        rec = []
        rec.append(x1)
        rec.append(y1)
        rec.append(x2)
        rec.append(y2)
        rectangles.append(rec)
        # cv2.rectangle(img1, (x1, y1), (x2, y2), (255, 0, 0), 1)
    print(rectangles)
    rectlist, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
    print(rectlist)
    return rectlist

def find_human_body(filename):
    image_base64=handle_frame.image_to_base64(filename)
    DATA['image_base64']=image_base64
    urldata = urllib.parse.urlencode(DATA)
    urldata = urldata.encode('utf8')
    with urllib.request.urlopen(URL, urldata) as f:
        decodejson = json.load(f)
        # print(len(decodejson['humanbodies']))
        if(len(decodejson['humanbodies'])>0):
            return decodejson['humanbodies'],len(decodejson['humanbodies'])

def draw_image(human_info,filename):
    image=cv2.imread(filename)
    # shape=image.shape
    # print(shape)
    # img1 = np.zeros(shape, np.uint8)
    for humanrectangle in human_info:
        x1=humanrectangle['humanbody_rectangle']['left']
        y1=humanrectangle['humanbody_rectangle']['top']
        x2=humanrectangle['humanbody_rectangle']['left']+humanrectangle['humanbody_rectangle']['width']
        y2=humanrectangle['humanbody_rectangle']['top']+humanrectangle['humanbody_rectangle']['height']
        cv2.rectangle(image, (x1,y1), (x2, y2), (0, 255, 0), -1)
    # cv2.imshow('img1',image)
    # cv2.waitKey(0)
    return image


def cal_area(human_info,filename):
    paint_image=draw_image(human_info,filename)
    image=cv2.imread(filename)
    ratio=handle_frame.cal_area_with_classify_pixel(image, paint_image)
    return ratio


def generate_video_image(filename):
    human_info,length=find_human_body(filename)
    ratio=cal_area(human_info,filename)
    print(ratio)
    if length==1 or length==2:
        if ratio>0.6:
            return Global_Variables.shots[0]
        elif ratio>0.1:
            return Global_Variables.shots[1]
        else:
            return Global_Variables.shots[2]
    else:
        if ratio>0.75:
            return Global_Variables.shots[0]
        elif ratio>0.3:
            return Global_Variables.shots[1]
        else:
            return Global_Variables[2]

generate_video_image('d:\\1.jpg')