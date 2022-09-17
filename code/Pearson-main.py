import csv
import sys

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QAction, QFileDialog
from PyQt5.QtGui import QIcon
import numpy as np


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
                    if id[:-1] not in TypeIdDict.keys():
                        TypeIdDict[id[:-1]] = row[0] + ' ' + row[1] + ' ' + row[-2]
                    else:
                        TypeIdDict[id[:-1]] += ';' + row[0] + ' ' + row[1] + ' ' + row[-2]
        self._signal.emit(TypeIdDict)


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.y = None
        self.x = None
        self.x2 = None
        self.pearsonSim = None
        self.TypeIdDict = None
        self.RR = None

        self.initData()

    def initUI(self):
        self.setWindowIcon(QIcon("../data/favicon.ico"))
        self.setWindowTitle("基于Pearson系数的跑鞋推荐系统")
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()
        self.resize(400, 400)
        openfile = QAction(QIcon(r'C:\Users\Administrator\PycharmProjects\QT\picture\文件.jpg'), 'open', self)
        # self.setStyleSheet("#MainWindow{border-image:url(background.jpg)}")
        self.setStyleSheet('''QWidget{background-color:#66ccff;}''')
        openfile.setShortcut("Ctrl + 0")
        openfile.setStatusTip('open new file')
        openfile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        filemune = menubar.addMenu('File')
        filemune.addAction(openfile)
        self.textEdit.setText("选择COROS运动数据后给出推荐")
        self.show()

    def initData(self):
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
        self.x = pace
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
        self.x2 = pace

    # 给出推荐并将决策树保存到本地的函数
    def giveRecommend(self):
        self.textEdit.setText("")
        uni = set()
        for shoe in self.TypeIdDict[self.RR].split(';'):
            if shoe not in uni:
                self.textEdit.append(shoe)
                uni.add(shoe)
                if self.TypeIdDict[self.RR].split(';')[-1] == shoe:
                    self.textEdit.append('...' + '\n')

    # 接收信息并typeIDDict赋值
    def signalTypeId(self, msg):
        self.TypeIdDict = msg

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'open file', '/')
        if fname[0]:
            self.getData(fname[0])
            if self.pearson(self.y, self.x) > self.pearson(self.y, self.x2):
                self.RR = '2'
            else:
                self.RR = '1'
            self.thread3 = TypeId()
            self.thread3._signal.connect(self.signalTypeId)  # 连接回调函数，接收结果
            self.thread3.start()
            self.thread3.finished.connect(self.giveRecommend)

    def pearson(self, x, y):
        pccs = np.corrcoef(x, y)
        pearsonSim = pccs.mean()
        return pearsonSim

    def getData(self, fileSource):

        with open(fileSource, 'r', encoding='utf-8-sig') as f:
            tmpPace4 = list(csv.reader(f))
        pace = []
        for row in tmpPace4[1:-1][:10]:
            tmpRow = []
            for single in row:
                if ':' in single:
                    tmpRow.append(float(single.split(':')[1]) * 60 + float(single.split(':')[2]))
                else:
                    tmpRow.append(float(single))
            pace.append(tmpRow)
        self.y = pace


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
