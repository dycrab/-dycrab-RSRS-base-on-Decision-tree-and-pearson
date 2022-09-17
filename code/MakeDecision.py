# -*- coding: utf-8 -*-
# @Time : 2022/5/10 22:21
# @Author : Leviathan_Sei
# @File : MakeDecision.py
# @Python : 3.7

import csv
from DecisionTree import createTree
import decisionTreePlot as dtPlot



def getInfo():
    info = {'类型': '竞速', '预算': '≥1000元', '身体情况': '男＞60kg&＜80kg', '足弓': '正常'}
    return info


def getMyDate():
    with open('../data/跑鞋推荐datav2.csv','r',encoding='utf-8-sig') as f:
        f = list(csv.reader(f))
    return (f[1:], f[:1][0][:-1])
def makeTree():
    dataSet, labels = getMyDate()
    Tree = createTree(dataSet, labels)
    dtPlot.createPlot(Tree)
    print(Tree)
    return Tree

def classify(tree, info):
    nowKey = list(tree.keys())[0]
    ans = tree
    while True:
        ans = ans[nowKey]

        print(ans)
        tmpKey = info[nowKey]
        ans = ans[tmpKey]
        if type(ans) == type('1'):
            break
        nowKey = list(ans.keys())[0]
        print(nowKey)
    print(info, '推荐结果：', ans)
    
if __name__ == '__main__':
    tree = makeTree()
    info = getInfo()
    classify(tree, info)