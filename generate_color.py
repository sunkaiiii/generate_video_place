#coding=gbk
import os
import cv2 as cv2
import numpy as np
import colorsys
from PIL import Image
import k_mean_class

"""
 -------------generate_color---------------
���ܣ�������кõ���Ƶ��·�����������ÿ����Ƶ֡�е�������ɫ
��������ͼ������ָ��·������
"""



def handle_main_color(colors,frame,filename,pathname,image_count,num=10):
    """
    �������õ���ɫ����ͼƬ�У������÷�������ͼƬ
    :param colors:�����õ���ɫlist
    :param frame:����֡
    :param filename:�ļ���
    :param pathname:·����
    :param image_count:�����ļ�������
    :param num:��ʾ��ɫ������
    """
    shape = frame.shape
    width = 800
    ratio = float(shape[0]) / float(shape[1])
    height = width * ratio
    size = (int(width), int(height))
    frame = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    count=0
    rec_width=width / num
    rec_height=rec_width*0.75
    width_add=width/200
    height_add=width/200
    cv2.rectangle(frame,(0,int(height-rec_height)),(int(width),int(height)),(220,220,220),-1)
    for i in colors:
        bgr=(i[2],i[1],i[0])
        # print(bgr)
        cv2.rectangle(frame,
                      (int(rec_width* count+width_add), int(height - rec_height+height_add)),
                      (int(rec_width * (count+1)-width_add),int(height-height_add)),
                      bgr, -1)
        count+=1
    # cv2.imshow('21',frame)
    # cv2.waitKey(0)
    save_file(pathname,filename,frame,image_count)

def find_main_color(frame,filename,pathname,image_count,max_iterations=10, min_distance=0.5, k=10):
    """
    mode=0ʱ���õķ�����ʹ�þ���kֵ�������ж�ͼ��������ɫ
    :param frame: Ҫ������֡
    :param filename: �ļ���
    :param pathname: Ŀ¼
    :param image_count: ����
    :param max_iterations:������ȣ�ֵԽ�������Խ����Խ��ȷ���ٶ�Խ��
    :param min_distance:������ɫ���룬��ֵԽС������ɫ����̶�Խ��
    :param k:�����ʼ��������ͬʱҲ�������color��list�ĳ���
    """
    k_image = k_mean_class.Kmeans(max_iterations=max_iterations, min_distance=min_distance, k=k)
    image = Image.fromarray(frame, 'RGB')
    try:
        color = k_image.run(image)
    except:
        print(pathname + filename + '����ʧ��')
        return None
    hsv_color = []
    for i in color:
        hsv_color.append(list(colorsys.rgb_to_hsv(i[0], i[1], i[2])))
    hsv_color = sorted(hsv_color, key=lambda x: x[2], reverse=True)
    # print(hsv_color)
    for i in range(0, len(hsv_color)):
        r, g, b = colorsys.hsv_to_rgb(hsv_color[i][0], hsv_color[i][1], hsv_color[i][2])
        color[i] = (b, g, r)
        # print(color[i])
    handle_main_color(color, frame,filename,pathname,image_count)
    return True

def save_file(pathname,filename,firstframe,image_count):
    """
    �����õģ�����������ɫɫ���ͼƬ����
    :param pathname:·����
    :param filename:�ļ���
    :param firstframe:��Ƶ֡
    :param image_count:����
    """
    pathname = pathname.split('\\')[len(pathname.split('\\')) - 1]
    if not os.path.exists(os.getcwd()+'\cut_main_color'):
        os.mkdir(os.getcwd()+"\cut_main_color")
    path = 'cut_main_color\\' + pathname + '\\'
    if not os.path.exists(path):
        os.mkdir(path)
    filename = filename.split('\\')[len(filename.split('\\')) - 1]
    # cv2.imwrite('cut_main_color\\123\\'+ filename + '_' + str(image_count) + '.jpg', frame)
    cv2.imencode('.jpg', firstframe)[1].tofile(path + filename + '_' + str(image_count) + '.jpg')
    print(os.getcwd() + '\\' + path + filename + '_' + str(image_count) + '.jpg' + '����ɹ�')

def find_main_color_by_vertical_cut(frame,filename,image_count,pathname,firstframe):
    """
    ���������и�Ϊ10�ݣ�����β���ÿһ�ݵ��е�������ɫ
    :param frame: ��ǰ֡
    :param filename: �ļ���
    :param image_count: ����
    """

    #���µ���ͼƬ��С
    shape=frame.shape
    width=1024
    ratio = float(shape[0]) / float(shape[1])
    height = width * ratio
    size = (int(width), int(height))
    frame = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    firstframe=cv2.resize(firstframe, size, interpolation=cv2.INTER_AREA)
    try:
         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    except:
        return None
    image = Image.fromarray(image, 'RGB')
    image = image.convert('RGBA')
    width=image.width
    height=image.height
    for i in range(0,10):
        # �и���Ƶ����������ѡ��ͼ���3/10��7/10��λ�ã��ų�һЩ��Ե����
        cut_image = image.crop((image.width / 10 * i, image.height/20*6, image.width / 10 * (i + 1), image.height/20*14))
        # cut_image.show()
        max_score=0
        colors=[]
        dominant_color=()
        for count,(r,g,b,a) in cut_image.getcolors(cut_image.size[0]*cut_image.size[1]):
            if a==0:
                continue
            # print(r,g,b)
            saturation=colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)[1]
            y=min(abs(r*2104+g*4130+b*802+4096+131072)>>13,235)
            y=(y-16.0)/(235-16)
            # print(y)

            # ���˵��߹����Ӱ
            if y>0.95:
                continue
            if y<0.05:
                continue

            score=(saturation+0.1)*count
            if score>max_score:
                if (b,g,r) in colors: #����Ѱ�Ҳ�һ������ɫ
                    continue
                max_score=score
                dominant_color=(b,g,r)

        try:
            colors.append(dominant_color)
            # ��ԭͼ����ʾɫ��
            cv2.rectangle(firstframe,
                          (int(width/10*i),height-64),
                          (int(width/10*(i+1)),height),
                          dominant_color,
                          -1)
        except:
            continue
    save_file(pathname,filename,firstframe,image_count)
def read_cut_video(filename,pathname,mode=0,max_iterations=10, min_distance=0.5, k=10):
    """
    ��ȡ����������ļ�֡����������ط������з���
    :return:
    """
    # ����Ƶ�ļ�
    capture = cv2.VideoCapture(filename)
    if not capture.isOpened():
        print('�ļ���ʧ��')
        return
    success, frame = capture.read()
    rate_count=1
    rate = capture.get(cv2.CAP_PROP_FPS)
    print("֡��Ϊ:" + str(rate))
    # ʹ��opencv��ȡ��Ƶ֡������Ϊinfinity,����ʱʹ��24֡
    # ��Ƶ���õ�Ĭ��֡��Ϊ24
    if rate>1000 or rate<=0:
        rate=24
    totalFrameNumber = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    generate_frame=[]
    for i in range(1,4):
        generate_frame.append(int(totalFrameNumber/4*i))
    image_count=0 #����ͼƬ��������
    while success:
        # cal_frame_hist(frame)
        success, frame = capture.read()
        #��ȡʧ��,�˳�ѭ��
        if not success:
            break
        rate_count += 1
        # �ڼ�����Ƶ��,����ȡ����Ӧ�и���frameʱ������ɫ
        if rate_count in generate_frame:
            firstframe=frame
            if mode==0:
                saturation = cv2.convertScaleAbs(frame, cv2.CV_8UC1, 1.2, -20) #����ͼ��Աȶȣ�����һ�����ȣ�ʹ��ɫ��������
                ok=0
                try:
                    for i in range(0,3):
                        if find_main_color(saturation,filename,pathname,image_count,max_iterations, min_distance, k) is True:##���û���ҵ���Ҫ��ɫ���߳���ִ�д���,���½���ѭ��:
                            ok=1
                            break
                        print('���е�'+str(i+1)+'������')
                    if ok==0:
                        success, frame = capture.read()
                        rate_count += 1
                        # ��ȡʧ��,�˳�ѭ��
                        if not success:
                            break
                        for i in range(3, 6):
                            if find_main_color(saturation, filename, pathname,
                                               image_count) is True:  ##���û���ҵ���Ҫ��ɫ���߳���ִ�д���,���½���ѭ��:
                                break
                            print('���е�' + str(i + 1) + '������')
                except:
                    return
                finally:
                    image_count += 1
            if mode==1:
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
                morph_close = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)  # ��ͼ���������㣬������ɫ���Ӷ�
                saturation = cv2.convertScaleAbs(morph_close, cv2.CV_8UC1, 1.2, -20)# ����ͼ��Աȶȣ�����һ�����ȣ�ʹ��ɫ��������
                find_main_color_by_vertical_cut(saturation,filename,image_count,pathname,firstframe)
                image_count += 1



def generate_cut_video_color(filepath='cut\\',mode=0,max_iterations=10, min_distance=0.5, k=10):
    """
    ��ȡ�����ļ����µ������ļ��������ζ�����з���
    :param mode:
    0���Ժ������и�10�ݣ�����ÿһ���е���������ɫ
    1����ͼ�����������ɫ��ȡǰ10��������ɫ��
    :return:
    """
    list=os.listdir(filepath)
    for file in list:
        file = os.path.join(filepath, file)
        if not os.path.isdir(file):
            print('��ȡ'+file)
            read_cut_video(file,filepath,mode,max_iterations, min_distance, k)



if __name__ == "__main__":
    generate_cut_video_color('D:\�ļ�������\Onedrive\�ĵ�\PycharmProjects\internship_working\cut\\����',mode=0)
    # filelist=os.listdir('E:\picture2')
    # count=0
    # for file in filelist:
    #     frame=cv2.imread('E:\picture2\\'+file)
    #     find_main_color(frame=frame,filename=file,image_count=count,pathname='E:\picture')
    #     count+=1







#
# def dict2list(dic: dict):
#         ''' ���ֵ�ת��Ϊ�б� '''
#         keys = dic.keys()
#         vals = dic.values()
#         lst = [(key, val) for key, val in zip(keys, vals)]
#         return lst


        # def find_main_color(frame):
#     '''
#     ������Ƶ֡,�ҵ�֡����Ҫ��ɫ������
#     :param frame:�������Ƶ֡
#     :return:��֡����Ҫ��ɫ
#     '''
#
#     # ��opencv��imageת��ΪImage��image
#     try:
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     except:
#         return None
#     image = Image.fromarray(image, 'RGB')
#     # print(max(image.getcolors(image.size[0] * image.size[1])))
#     image=image.convert('RGBA')
#     max_score=0
#     sort_socre={} #�����Ҫ��ɫ���ֵ�
#     for count,(r,g,b,a) in image.getcolors(image.size[0]*image.size[1]):
#         if a==0:
#             continue
#         # print(r,g,b)
#         saturation=colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)[1]
#         y=min(abs(r*2104+g*4130+b*802+4096+131072)>>13,235)
#         y=(y-16.0)/(235-16)
#         # print(y)
#
#         # ���˵��߹����Ӱ
#         if y>0.9:
#             continue
#         if y<0.1:
#             continue
#
#         score=(saturation+0.1)*count
#         if score>max_score:
#             max_score=score
#             dominant_color=(r,g,b)
#             sort_socre[str(dominant_color)]=max_score
#
#     # print(sort_socre)
#     sort_color=sorted(dict2list(sort_socre), key=lambda x: x[1], reverse=True)  # ����score��������)
#     # print(sort_color)
#     rowCount=0
#     main_colors=[]
#     for i in range(0,len(sort_color)):
#         main_colors.append(sort_color[i][0])
#         rowCount+=1
#         if rowCount==10:
#             return main_colors
#     return main_colors
#
# def rgb_str_to_rgb_tuple(rgb_str):
#     '''
#     ��find_main_color���ص��ֵ����������Ϊstr
#     ����ת��Ϊtuple
#     '''
#     rgb_str = rgb_str.strip("(")
#     rgb_str = rgb_str.strip(")")
#     rgb_str = rgb_str.strip('\'')
#     rgb_str = rgb_str.replace(', ', ',')
#     rgb_list = rgb_str.split(",")
#     # rgbת��Ϊbgr
#     return (int(rgb_list[2]),int(rgb_list[1]),int(rgb_list[0]))
#
# def save_frame_main_colors(frame_main_colors,filename,image_count,pathname,firstframe):
#     """
#     ����mode=1ʱ�����õ�ͼ��Ϊ�ļ�
#     :param frame_main_colors: ǰʮ��������ɫ
#     :param frame: ͼ��֡
#     :param image_count: ����
#     """
#     # ���ñ���ͼƬ�ķֱ���
#     shape=firstframe.shape
#     width=1024
#     ratio = float(shape[0]) / float(shape[1])
#     height = width * ratio
#     size = (int(width), int(height))
#     firstframe = cv2.resize(firstframe, size, interpolation=cv2.INTER_AREA)
#     # ��ԭʼͼƬ�ĵײ��Դ˷�����Ҫ��ɫ
#     # Ŀǰ�ݶ���ȡ��Ҫ��ɫ������Ϊ10
#     count=0
#     for i in frame_main_colors:
#         rgb = rgb_str_to_rgb_tuple(i)
#         # print(rgb)
#         cv2.rectangle(firstframe,
#                       (int(width / 10 * count), int(height - 64)),
#                       (int(width / 10 * (count + 1)),int(height)),
#                       rgb, -1)
#         count+=1
#     # cv2.imshow('image', img)
#     # Ϊ�µ�ͼƬ����
#     pathname=pathname.split('\\')[len(pathname.split('\\'))-1]
#     path='cut_main_color\\'+pathname+'\\'
#     if not os.path.exists(path):
#         os.mkdir(path)
#     filename = filename.split('\\')[len(filename.split('\\')) - 1]
#     # cv2.imwrite(os.getcwd()+'\\'+path + filename + '_' + str(image_count)+ '.jpg', img)
#     cv2.imencode('.jpg', firstframe)[1].tofile(path + filename + '_' + str(image_count) + '.jpg')
#     print(os.getcwd()+'\\'+path + filename + '_' + str(image_count)+ '.jpg'+ '����ɹ�')
#     # cv2.waitKey(0)