# -*- coding: utf-8 -*-
# @Time : 2022/5/13 15:22
# @Author : Leviathan_Sei
# @File : pearson相似度计算.py
# @Python : 3.7

import csv
import numpy as np
import numpy



class CalPearson(object):
    def __init__(self):
        self.x = None
        self.y = None
        self.pearsonSim = None

    def dataTran(self):
        with open('../data/runing_data/pace 4/跑步20220403092631.csv', 'r', encoding='utf-8-sig') as f:
            tmpPace4 = list(csv.reader(f))
        pace = []
        for row in tmpPace4[1:-1]:
            tmpRow = []
            for single in row:
                if ':' in single:
                    tmpRow.append(float(single.split(':')[1]) * 60 + float(single.split(':')[2]))
                else:
                    tmpRow.append(float(single))
            pace.append(tmpRow)
        self.x = pace

    def dataTran2(self):
        with open('../data/runing_data/跑步20220430190342.csv', 'r', encoding='utf-8-sig') as f:
            tmpPace4 = list(csv.reader(f))
        pace = []
        for row in tmpPace4[1:-1]:
            tmpRow = []
            for single in row:
                if ':' in single:
                    tmpRow.append(float(single.split(':')[1]) * 60 + float(single.split(':')[2]))
                else:
                    tmpRow.append(float(single))
            pace.append(tmpRow)
        self.y = pace

    def pearson(self):
        self.dataTran()
        self.dataTran2()
        pccs = np.corrcoef(self.x, self.y)
        self.pearsonSim = pccs.mean()


if __name__ == '__main__':
    cal = CalPearson()
    cal.pearson()
    print(cal.pearsonSim)
