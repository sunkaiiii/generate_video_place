import numpy as np
import cv2
a=[{'width': 227, 'top': 340, 'height': 499, 'left': 147},
{'width': 171, 'top': 438, 'height': 401, 'left': 847},
{'width': 210, 'top': 386, 'height': 441, 'left': 527},
{'width': 184, 'top': 432, 'height': 405, 'left': 680},
{'width': 174, 'top': 412, 'height': 402, 'left': 319}]
# for i in a:
#     print(i)

class point:
    def __init__(self):
        self.x=0
        self.y=0

def merge_rect(rect1,rect2):
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

print(merge_rect({'width': 347, 'top': 376, 'height': 618, 'left': 388},
{'width': 300, 'top': 520, 'height': 561, 'left': 138}))
img1=np.zeros((1100,1100,3),np.uint8)
img2=np.zeros((1100,1100,3),np.uint8)
box=[]
rec=[]
for i in a:
    x1=i['left']
    x2=i['left']+i['width']
    y1=i['top']
    y2=i['top']+i['height']
    rec=[]
    rec.append(x1)
    rec.append(y1)
    rec.append(x2)
    rec.append(y2)
    box.append(rec)
    cv2.rectangle(img1,(x1,y1),(x2,y2),(255,0,0),1)

# print(non_max_suppression_fast(box,0))
#
print(box)
rectlist,weights=cv2.groupRectangles(box,groupThreshold=1,eps=0.5)
#
print(rectlist,weights)
for i in rectlist:
    cv2.rectangle(img2,(i[0],i[1]),(i[2],i[3]),(0,255,0),1)
cv2.imshow('img1',img1)
cv2.imshow('img2',img2)
cv2.waitKey(0)