# -*- coding: utf-8 -*-
# @Time : 2022/5/12 11:13
# @Author : Leviathan_Sei
# @File : Decision-Tree-main.py
# @Python : 3.7
import csv
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from DecisionTree import createTree
from decisionTreePlot import savePlot


class Info(QThread):
    _signal = pyqtSignal(dict)

    def __init__(self, decision=True):
        super(Info, self).__init__()
        self.decision_tree = decision
        self.info = {'类型': '', '预算': '', '身体情况': '', '足弓': ''}

    # 将选中的信息放入info_dict中并返回
    def run(self):
        if self.decision_tree.radioButton.isChecked():
            self.info['身体情况'] = '男' + self.decision_tree.radioButton.text().replace('&&', '&')
        if self.decision_tree.radioButton_2.isChecked():
            self.info['身体情况'] = '女' + self.decision_tree.radioButton_2.text().replace('&&', '&')
        if self.decision_tree.radioButton_3.isChecked():
            self.info['身体情况'] = '男' + self.decision_tree.radioButton_3.text().replace('&&', '&')
        if self.decision_tree.radioButton_4.isChecked():
            self.info['身体情况'] = '女' + self.decision_tree.radioButton_4.text().replace('&&', '&')
        if self.decision_tree.radioButton_5.isChecked():
            self.info['身体情况'] = '男' + self.decision_tree.radioButton_5.text().replace('&&', '&')
        if self.decision_tree.radioButton_6.isChecked():
            self.info['身体情况'] = '女' + self.decision_tree.radioButton_6.text().replace('&&', '&')

        if self.decision_tree.radioButton_7.isChecked():
            self.info['类型'] = self.decision_tree.radioButton_7.text()
        if self.decision_tree.radioButton_8.isChecked():
            self.info['类型'] = self.decision_tree.radioButton_8.text()

        if self.decision_tree.radioButton_9.isChecked():
            self.info['预算'] = self.decision_tree.radioButton_9.text().replace('&&', '&')
        if self.decision_tree.radioButton_10.isChecked():
            self.info['预算'] = self.decision_tree.radioButton_10.text().replace('&&', '&')
        if self.decision_tree.radioButton_11.isChecked():
            self.info['预算'] = self.decision_tree.radioButton_11.text().replace('&&', '&')

        if self.decision_tree.radioButton_12.isChecked():
            self.info['足弓'] = self.decision_tree.radioButton_12.text()
        if self.decision_tree.radioButton_13.isChecked():
            self.info['足弓'] = self.decision_tree.radioButton_13.text()
        if self.decision_tree.radioButton_14.isChecked():
            self.info['足弓'] = self.decision_tree.radioButton_14.text()
        self._signal.emit(self.info)


class Data(QThread):
    _signal = pyqtSignal(list)

    def __init__(self):
        super(Data, self).__init__()
        self.dataSet = None
        self.labels = None

    # 读取推荐数据
    def run(self):
        with open('../data/跑鞋推荐datav2.csv', 'r', encoding='utf-8-sig') as f:
            f = list(csv.reader(f))
        self.dataSet = f[1:]
        self.labels = f[:1][0][:-1]
        self._signal.emit([self.dataSet, self.labels])


class MakeDecisionTree(QThread):
    _signal = pyqtSignal(dict)

    def __init__(self, dataSet, labels):
        super(MakeDecisionTree, self).__init__()
        self.dataSet = dataSet
        self.labels = labels

    # 创建决策树
    def run(self):
        tree = createTree(dataSet=self.dataSet, labels=self.labels)
        self._signal.emit(tree)


class Classify(QThread):
    _signal = pyqtSignal(str)

    def __init__(self, tree, info):
        super(Classify, self).__init__()
        self.tree = tree
        self.info = info

    # 对用户数据进行分类
    def run(self):
        nowKey = list(self.tree.keys())[0]
        ans = self.tree
        while True:
            ans = ans[nowKey]
            tmpKey = self.info[nowKey]
            ans = ans[tmpKey]
            if type(ans) == type('1'):
                break
            nowKey = list(ans.keys())[0]
        self._signal.emit(ans)


class TypeId(QThread):
    _signal = pyqtSignal(dict)

    def __init__(self):
        super(TypeId, self).__init__()

    # 读取跑鞋数据并将每个类型ID的跑鞋都提取出来
    def run(self):
        TypeIdDict = {}
        with open('../data/shoes.csv', 'r', encoding='utf-8-sig') as f:
            file = list(csv.reader(f))
            for row in file:
                for id in row[-1].split(','):
                    if id not in TypeIdDict.keys():
                        TypeIdDict[id] = row[0] + ' ' + row[1] + ' ' + row[-2]
                    else:
                        TypeIdDict[id] += ';' + row[0] + ' ' + row[1] + ' ' + row[-2]
        self._signal.emit(TypeIdDict)


class DecisionPic(QThread):
    def __init__(self, tree):
        super(DecisionPic, self).__init__()
        self.tree = tree

    # 保存决策树
    def run(self):
        savePlot(self.tree)


class Decison(QtWidgets.QMainWindow):
    def __init__(self):
        super(Decison, self).__init__()
        loadUi('决策树.ui', self)
        self.setWindowIcon(QIcon("../data/favicon.ico"))
        self.setWindowTitle("基于决策树的跑鞋推荐系统")
        self.info = {'类型': '', '预算': '', '身体情况': '', '足弓': ''}
        self.pushButton.clicked.connect(self.makeDecison)
        self.pushButton.setStyleSheet('''QWidget{background-color:#FFFFFF;}''')
        self.groupBox_2.setStyleSheet('''QWidget{background-color:#87CEEB;}''')
        self.groupBox_3.setStyleSheet('''QWidget{background-color:#87CEEB;}''')
        self.groupBox_4.setStyleSheet('''QWidget{background-color:#87CEEB;}''')
        self.groupBox.setStyleSheet('''QWidget{background-color:#87CEEB;}''')
        self.textBrowser.setStyleSheet('''QWidget{background-color:#FFFFFF;}''')
        self.setStyleSheet('''QWidget{background-color:#66ccff;}''')
        self.dataSet = None
        self.labels = None
        self.tree = None
        self.thread = None
        self.thread1 = None
        self.thread2 = None
        self.thread3 = None
        self.thread4 = None
        self.thread5 = None
        self.RR = None
        self.TypeIdDict = None
        self.show()

    # 接收信号 并给info赋值
    def signalInfo(self, msg):
        self.info = msg
        self.pushButton.setEnabled(True)

    # 接收信号并给数据集和标签赋值
    def signalData(self, msg):
        self.dataSet = msg[0]
        self.labels = msg[1]

    # 接收信号并给tree赋值
    def signalTree(self, msg):
        self.tree = msg

    # 接收信息并给推荐结果赋值
    def signalRR(self, msg):
        self.RR = msg

    # 接收信息并typeIDDict赋值
    def signalTypeId(self, msg):
        self.TypeIdDict = msg

    # 使用线程类获取用户info的函数
    def getInfo(self):
        self.pushButton.setEnabled(False)
        self.thread = Info(self)
        self.thread._signal.connect(self.signalInfo)  # 连接回调函数，接收结果
        self.thread.start()  # 启动线程
        self.thread.finished.connect(self.getData)

    # 使用线程类获取data的函数
    def getData(self):
        self.thread1 = Data()
        self.thread1._signal.connect(self.signalData)  # 连接回调函数，接收结果
        self.thread1.start()
        self.thread1.finished.connect(self.makeTree)

    # 使用线程类获取树的函数
    def makeTree(self):
        self.thread2 = MakeDecisionTree(self.dataSet, self.labels)
        self.thread2._signal.connect(self.signalTree)  # 连接回调函数，接收结果
        self.thread2.start()
        self.thread2.finished.connect(self.classify)

    # 使用线程类进行分类的函数
    def classify(self):
        self.thread3 = Classify(self.tree, self.info)
        self.thread3._signal.connect(self.signalRR)  # 连接回调函数，接收结果
        self.thread3.start()
        self.thread3.finished.connect(self.getTypeId)

    # 使用线程类获取类型ID的字典的函数
    def getTypeId(self):
        self.thread3 = TypeId()
        self.thread3._signal.connect(self.signalTypeId)  # 连接回调函数，接收结果
        self.thread3.start()
        self.thread3.finished.connect(self.giveRecommend)

    # 给出推荐并将决策树保存到本地的函数
    def giveRecommend(self):
        for shoe in self.TypeIdDict[self.RR].split(';'):
            self.textBrowser.append(shoe)
            if self.TypeIdDict[self.RR].split(';')[-1] == shoe:
                self.textBrowser.append('...' + '\n')
        self.thread4 = DecisionPic(self.tree)
        self.thread4.start()

    def makeDecison(self):
        print("make decision")
        self.getInfo()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Decison()
    sys.exit(app.exec_())
