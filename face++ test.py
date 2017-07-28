import urllib.parse
import urllib.request
import json
import cv2
import numpy as np
import handle_frame
import Global_Variables
import os

URL = 'https://api-cn.faceplusplus.com/humanbodypp/beta/detect'  # fance++调用身体监测的地址
API_KEY = 'iJZuow0cOQez62sxfNdjzjwXkaX9y0rB'  # 申请的api的key
API_SECRET = 'gz_PVjfT8V7DrMxfAOpOreAwMN1L2dGY'  # 申请的api的secret

'''
暂时使用的base64将图片进行编码传输
还可以使用图片url、图片二进制进行传输，具体请参考官方文档
https://console.faceplusplus.com.cn/documents/7774430
'''
DATA = {
    'api_key': API_KEY,
    'api_secret': API_SECRET,
    'image_base64': ''
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


def find_human_body(frame):
    image_base64 = handle_frame.image_to_base64(frame)
    DATA['image_base64'] = image_base64
    urldata = urllib.parse.urlencode(DATA)
    urldata = urldata.encode('utf8')
    with urllib.request.urlopen(URL, urldata) as f:
        decodejson = json.load(f)
        # print(len(decodejson['humanbodies']))
        if (len(decodejson['humanbodies']) > 0):
            return decodejson['humanbodies'], len(decodejson['humanbodies'])
        else:
            return '', 0


def draw_image(human_info, paint_frame):
    # shape=image.shape
    # print(shape)
    # img1 = np.zeros(shape, np.uint8)
    for humanrectangle in human_info:
        x1 = humanrectangle['humanbody_rectangle']['left']
        y1 = humanrectangle['humanbody_rectangle']['top']
        x2 = humanrectangle['humanbody_rectangle']['left'] + humanrectangle['humanbody_rectangle']['width']
        y2 = humanrectangle['humanbody_rectangle']['top'] + humanrectangle['humanbody_rectangle']['height']
        cv2.rectangle(paint_frame, (x1, y1), (x2, y2), (0, 255, 0), -1)
    return paint_frame


def cal_area(human_info, frame, paint_frame):
    paint_image = draw_image(human_info, paint_frame)
    ratio = handle_frame.cal_area_with_classify_pixel(frame, paint_image)
    return ratio


def generate_video_image(frame, mode):
    shape = frame.shape
    width = 1024
    proportion = float(shape[0]) / float(shape[1])
    height = width * proportion
    size = (int(width), int(height))
    frame = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    cv2.imwrite('middle.jpg', frame,
                [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    frame = cv2.imread('middle.jpg')
    paint_frame = cv2.imread('middle.jpg')
    frame_binary = open('middle.jpg', 'rb')
    frame_binary = frame_binary.read()
    human_info, length = find_human_body(frame_binary)
    if length == 0:
        return Global_Variables.shots[9], 0
    if mode == 1:
        if length > 1:
            max_area = 0
            index = human_info[0]
            for humanrectangle in human_info:
                current_area = humanrectangle['humanbody_rectangle']['width'] * humanrectangle['humanbody_rectangle'][
                    'height']
                if max_area < current_area:
                    max_area = current_area
                    index = humanrectangle
            human_info = [index]
            length=1
            height, width, channel = frame.shape
            height_ratio=index['humanbody_rectangle']['height']/height
            if height_ratio<0.25:
                return Global_Variables.shots[8],cal_area(human_info, frame, paint_frame)
            elif height_ratio<0.5:
                return Global_Variables.shots[7],cal_area(human_info, frame, paint_frame)
            elif height_ratio<0.75:
                return Global_Variables.shots[6],cal_area(human_info,frame,paint_frame)
    # print(human_info)
    ratio = cal_area(human_info, frame, paint_frame)
    # print(ratio)
    if length == 1:
        if ratio > 0.9:
            return Global_Variables.shots[0], ratio
        elif ratio > 0.3:
            return Global_Variables.shots[1], ratio
        elif ratio > 0.2:
            return Global_Variables.shots[2], ratio
        elif ratio > 0.12:
            return Global_Variables.shots[3], ratio
        elif ratio > 0.08:
            return Global_Variables.shots[4], ratio
        elif ratio > 0.05:
            return Global_Variables.shots[5], ratio
        elif ratio > 0.03:
            return Global_Variables.shots[6], ratio
        elif ratio > 0.018:
            return Global_Variables.shots[7], ratio
        else:
            return Global_Variables.shots[8], ratio
    if length == 2:
        if ratio > 0.95:
            return Global_Variables.shots[0], ratio
        elif ratio > 0.75:
            return Global_Variables.shots[1], ratio
        elif ratio > 0.37:
            return Global_Variables.shots[2], ratio
        elif ratio > 0.15:
            return Global_Variables.shots[3], ratio
        elif ratio > 0.1:
            return Global_Variables.shots[4], ratio
        elif ratio > 0.05:
            return Global_Variables.shots[5], ratio
        elif ratio > 0.025:
            return Global_Variables.shots[6], ratio
        elif ratio > 0.015:
            return Global_Variables.shots[7], ratio
        else:
            return Global_Variables.shots[8], ratio
    if length == 3:
        if ratio > 0.97:
            return Global_Variables.shots[0], ratio
        elif ratio > 0.9:
            return Global_Variables.shots[1], ratio
        elif ratio > 0.8:
            return Global_Variables.shots[2], ratio
        elif ratio > 0.55:
            return Global_Variables.shots[3], ratio
        elif ratio > 0.12:
            return Global_Variables.shots[4], ratio
        elif ratio > 0.04:
            return Global_Variables.shots[5], ratio
        elif ratio > 0.02:
            return Global_Variables.shots[6], ratio
        elif ratio > 0.01:
            return Global_Variables.shots[7], ratio
        else:
            return Global_Variables.shots[8], ratio
    else:
        if ratio > 0.97:
            return Global_Variables.shots[0], ratio
        elif ratio > 0.92:
            return Global_Variables.shots[1], ratio
        elif ratio > 0.85:
            return Global_Variables.shots[2], ratio
        elif ratio > 0.48:
            return Global_Variables.shots[3], ratio
        elif ratio > 0.1:
            return Global_Variables.shots[4], ratio
        elif ratio > 0.037:
            return Global_Variables.shots[5], ratio
        elif ratio > 0.022:
            return Global_Variables.shots[6], ratio
        elif ratio > 0.015:
            return Global_Variables.shots[7], ratio
        else:
            return Global_Variables.shots[8], ratio


def read_cut_video(filename, filepath, count, mode=0):
    image_count = count
    capture = cv2.VideoCapture(filename)
    if not capture.isOpened():
        print('文件打开失败')
        return image_count
    success, frame = capture.read()
    rate_count = 1
    rate = capture.get(cv2.CAP_PROP_FPS)
    # print("帧率为:" + str(rate))
    if rate > 1000 or rate <= 0:
        rate = 24
    totalFrameNumber = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    generate_frame = []
    for i in range(1, 4):
        generate_frame.append(int(totalFrameNumber / 4 * i))
    while success:
        # cal_frame_hist(frame)
        success, frame = capture.read()
        # 读取失败,退出循环
        if not success:
            break
        rate_count += 1
        # 在剪裁视频中,当读取到对应切割点的frame时分析颜色
        if rate_count in generate_frame:
            try:
                result, ratio = generate_video_image(frame, mode)
            except:
                continue
            path = "E:\shots"
            if not os.path.exists(path):
                os.mkdir(path)
            dirname=filepath.split('\\')[len(filepath.split('\\'))-1]
            if not os.path.exists(path+'\\'+dirname):
                os.mkdir(path+'\\'+dirname)
            if not os.path.exists(path+'\\'+dirname+'\\'+ result):
                os.mkdir(path+'\\'+dirname+'\\'+ result)
                cv2.imencode(".jpg", frame)[1].tofile(path + '\\' + dirname + '\\' + result + '\\' + str(image_count) + '_' + str(ratio) + '.jpg')
            image_count += 1
    return image_count


def read_video_list(filepath, mode=0):
    """
    读取剪裁文件夹下的所有文件，并依次对其进行分析
    :param mode:
    0、对横坐标切割10份，分析每一份中的最主题颜色
    1、对图像整体分析颜色，取前10个主题颜色。
    :return:
    """
    count = 0
    list = os.listdir(filepath)
    for file in list:
        file = os.path.join(filepath, file)
        if not os.path.isdir(file):
            print('读取' + file)
            count = read_cut_video(file, filepath, count, mode=mode)


# image=cv2.imread('d:\\2.jpg')
# print(generate_video_image(image))
# generate_video_image(image)
read_video_list('D:\文件与资料\Onedrive\文档\PycharmProjects\internship_working\cut\S.W.A.T.2003.720p.BluRay.DTS.x264-CtrlHD',mode=1)
# read_cut_video(
#     'D:\文件与资料\Onedrive\文档\PycharmProjects\internship_working\cut\S.W.A.T.2003.720p.BluRay.DTS.x264-CtrlHD\S.W.A.T.2003.720p.BluRay.DTS.x264-CtrlHD_126.avi',
#     'D:\文件与资料\Onedrive\文档\PycharmProjects\internship_working\cut\S.W.A.T.2003.720p.BluRay.DTS.x264-CtrlHD', 0, mode=1)
