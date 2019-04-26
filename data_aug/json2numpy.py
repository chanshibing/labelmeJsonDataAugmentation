import json
import numpy as np

class json2Numpy(object):
    def __init__(self, labelmeJson, imgRName = "", fileS = "", boxes1 = [], boxes2 = []):
        '''
        :param labelmeJson: one json file
        '''
        self.labelmeJson = labelmeJson
        self.imgRName = imgRName
        self.fileS = fileS
        self.boxes1 = boxes1
        self.boxes2 = boxes2

    def data_transfer(self):
        with open(self.labelmeJson, 'r') as fp:
            data = json.load(fp)  # 加载json文件
            point = []
            data['imagePath'] = data['imagePath'].split('\\')[-1]
            for shapes in data['shapes']:
                points = shapes['points']
                point.append([float(points[0][0]), float(points[0][1]), float(points[1][0]), float(points[1][1]), 0.])
            boxes = np.array(point)
        fp.close()
        with open(self.labelmeJson, 'w') as out:
            json.dump(data, out)
        out.close()
        return boxes
    def saveJson(self):
        with open(self.labelmeJson + self.imgRName + ".json", 'r') as fp:
            data = json.load(fp)  # 加载json文件
            outData = data
            point = []
            num1 = 0
            num2 = 0
            a = []
            fileName = outData['imagePath'].split('\\')
            outData['imagePath'] = fileName[-1].split('.')[0] + self.fileS + fileName[-1].split('.')[1]
            boxes2Length = len(self.boxes1)
            for shapes in outData['shapes']:
                points = shapes['points']
                if self.boxes2[num2][0] < 2048 and self.boxes2[num2][1] < 2048 and self.boxes2[num2][2] < 2048 and self.boxes2[num2][3] < 2048:
                    points[0][0] = self.boxes1[num1][0]
                    points[0][1] = self.boxes1[num1][1]
                    points[1][0] = self.boxes1[num1][2]
                    points[1][1] = self.boxes1[num1][3]
                    num1 += 1
                    num2 += 1
                else:
                    points[0][0] = 0
                    points[0][1] = 0
                    points[1][0] = 0
                    points[1][1] = 0
                    num2 += 1
                    if num1 < boxes2Length:
                        if self.boxes1[num1][0] >= 2048 or self.boxes1[num1][1] >= 2048 or self.boxes1[num1][2] >= 2048 or self.boxes1[num1][3] >= 2048:
                            num1 += 1
        fp.close()
        outS = self.labelmeJson + "dataAug/" + self.imgRName + self.fileS + "json"
        with open(outS, 'w') as out:
            json.dump(outData, out)
        out.close()

def getBboxes(labelmeJson):
    cl = json2Numpy(labelmeJson)
    return cl.data_transfer()

def save2json(labelmeJson, imgRName, fileS, boxes1, boxes2):
    cl = json2Numpy(labelmeJson, imgRName, fileS, boxes1, boxes2)
    return cl.saveJson()