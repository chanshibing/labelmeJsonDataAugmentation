from data_aug.data_aug import *
from data_aug.bbox_util import *
from data_aug.json2numpy import *
import cv2
import glob
import pickle as pkl
import numpy as np
import json
import matplotlib.pyplot as plt

labelme_json = glob.glob('H:/yjs614/data/2/*.json')
outSubName = "FlipAndRandomScaleAndRandomHSV."

for jsonName in labelme_json :
    imgName = jsonName.split('.')[0] + ".jpg"
    img = cv2.imread(imgName)[:, :, ::-1]  # OpenCV uses BGR channels
    bboxes = getBboxes(jsonName)  # 获取boxes
    #plt.imshow(draw_rect(img, bboxes))
    #plt.show()
    # img = cv2.imread("messi.jpg")[:,:,::-1] #OpenCV uses BGR channels
    # bboxes = pkl.load(open("messi_ann.pkl", "rb"))

    # [RandomHorizontalFlip(1),RandomHSV(1,2,3),Resize(500),RandomShear(), RandomScale(0.2, diff = True), RandomRotate(10)]
    transforms = Sequence([RandomHorizontalFlip(1),RandomScale(0.4, diff = True),RandomHSV(5,1,50)])
    rBoxes = bboxes
    img, bboxes = transforms(img, bboxes)

    #plt.imshow(draw_rect(img, bboxes))
    #plt.axis('on')  # 关掉坐标轴为 off
    #plt.title('imageO')  # 图像题目
    #plt.show()
    outName = ""
    for ss in imgName.split('/')[:-1]:
        outName += ss + '/'
    filePath = outName + imgName.split('/')[-1].split('\\')[0] + '/'
    outName = filePath  + 'dataAug/' + imgName.split('/')[-1].split('\\')[-1].split('.')[0] + outSubName + imgName.split('/')[-1].split('.')[1]
    plt.imsave(outName, img)
    save2json(filePath, imgName.split('/')[-1].split('\\')[-1].split('.')[0], outSubName, bboxes, rBoxes)
    a = 0
