import random
import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap

from BeforeRun import Ui_BeforeRun
from Running import Ui_Running
from AfterRun import Ui_AfterRun

#全局变量
change = 0
iterTimes = 0
keepSeconds = 0
time = 0
timet = 0
iter = 0
yuliaosize = 0.0
yuliaonumber = 0
totalwords = 0
newwords = 0
oldwords = 0
newlist = []

Animal = 0
Caijing = 0
Car = 0
Chengyu = 0
Diming = 0
Food = 0
IT = 0
Law = 0
Medical = 0
Poem = 0
Lishimingren = 0
stop = 0

Animal_new = 1
Caijing_new = 1
Car_new = 1
Chengyu_new = 1
Diming_new = 1
Food_new = 1
IT_new = 1
Law_new = 1
Medical_new = 1
Poem_new = 1
Lishimingren_new = 1
stop_new = 1


class MyFigure(FigureCanvas):#定义图像类
    def __init__(self,width, height, dpi):
         # 创建一个Figure,该Figure为matplotlib下的Figure，不是matplotlib.pyplot下面的Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
         # 在父类中**Figure窗口，此句必不可少，否则不能显示图形
        super(MyFigure,self).__init__(self.fig)
         # 调用Figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot(1,1,1)方法
        self.axes = self.fig.add_subplot(111)

class AfterRun(QMainWindow, Ui_AfterRun):
    def __init__(self):
        super().__init__()
        self.setupUi(self) # 渲染页面控件
        self.connect_signals() # 设置信号槽
        self.setWindowTitle("运行结果")

        self.F3 = MyFigure(width=3, height=2, dpi=100)
        self.countdot()  # 采集需要画的点位
        self.plotcos(self.t, self.s)  # 画 图
        # 在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）。
        self.gridlayout3 = QGridLayout(self.groupBox_3)
        self.gridlayout3.addWidget(self.F3)

        # 定义输出的内容


    def countdot(self):
        self.t = np.arange(0.0, 5.0, 0.01)
        self.s = np.cos(2 * np.pi * self.t)
        # self.t = [0,1,2,3,4,5]
        # self.s = [0,1,2,3,4,5]

    def plotcos(self, x, y):
        # frac = [1 / 50, 6 / 50, 11 / 50, 15 / 50, 9 / 50, 6 / 50, 2 / 50]
        # label = ['[3,4]', '(4,5]', '(5,6]', '(6,7]', '(7,8]', '(8,9]', '(9,10]']
        # explode = [0, 0, 0, 0.1, 0, 0, 0]  # 设置突出
        # self.F.axes.pie((frac,labels=label,explode=explode,autopct=%.2f%%))
        self.F3.axes.plot(x, y)
        self.F3.fig.suptitle("cos")

    def connect_signals(self):
        self.pushButton.clicked.connect(self.pushButton_clicked) # 绑定确定按钮事件
        self.pushButton_3.clicked.connect(self.pushButton_3_clicked)  # 绑定确定按钮事件
        self.pushButton_4.clicked.connect(self.pushButton_4_clicked)  # 绑定确定按钮事件
        self.pushButton_5.clicked.connect(self.pushButton_5_clicked)  # 绑定确定按钮事件
        self.pushButton_6.clicked.connect(self.pushButton_6_clicked)  # 绑定确定按钮事件

    def pushButton_clicked(self):
        # dir_path = QFileDialog.getExistingDirectory(self, '打开文件夹')
        dir_path='C:/'
        os.startfile(dir_path)

    def pushButton_3_clicked(self):
        dir_path = QFileDialog.getExistingDirectory(self, '选择保存位置')

    def pushButton_4_clicked(self):
        dir_path = QFileDialog.getExistingDirectory(self, '选择保存位置')

    def pushButton_5_clicked(self):
        dir_path = QFileDialog.getExistingDirectory(self, '选择保存位置')

    def pushButton_6_clicked(self):
        dir_path = QFileDialog.getExistingDirectory(self, '选择保存位置')

class Running(QMainWindow, Ui_Running):
    def __init__(self):
        super().__init__()
        self.setupUi(self) # 渲染页面控件
        self.setWindowTitle("迭代中")
        self.connect_signals() # 设置信号槽
        self.child_window = AfterRun()

        #定义变量
        self.time=0#迭代消耗的时间
        self.timet = 0
        self.iter=0#已经迭代的次数

        self.F = MyFigure(width=3, height=2, dpi=100)
        # self.countdot()  # 采集需要画的点位
        # self.plotcos()  # 画 图
        # # 在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）。
        # self.gridlayout = QGridLayout(self.groupBox)
        # self.gridlayout.addWidget(self.F)

        #定义计时器
        self.timer = QTimer()  # 初始化一个定时器
        self.timer.timeout.connect(self.operate)  # 计时结束调用operate()方法
        # self.timer.start(1000)  # 设置计时间隔并启动
        # self.pushButton.hide()

        #测试显示图片
        pixmap = QPixmap('./1(1).png')
        self.label_41.setPixmap(pixmap)
        self.label_41.setScaledContents(True)
        self.label_43.setPixmap(pixmap)
        self.label_43.setScaledContents(True)

    def countdot(self):
        self.t = np.arange(0.0, 5.0, 0.01)
        self.s = np.cos(2 * np.pi * self.t)
        # self.t = [0,1,2,3,4,5]
        # self.s = [0,1,2,3,4,5]

    def plotcos(self):
        self.F.axes.plot(newlist)
        self.F.fig.suptitle("New Words")

    def connect_signals(self):
        self.pushButton.clicked.connect(self.pushButton_clicked) # 绑定确定按钮事件

    def pushButton_clicked(self):
        self.close()
        self.child_window.show() # 显示子窗口
        self.timer.stop()

    def operate(self):
        #计时器的内容
        global time,timet,iter,change,yuliaosize,yuliaonumber,Animal_new,Caijing_new,Car_new,Chengyu_new
        global Diming_new,Food_new,IT_new,Law_new,Medical_new,Poem_new,Lishimingren_new,stop_new
        global newwords,oldwords,totalwords,Animal,Caijing,Car,Chengyu,Diming,Food,IT,Law,Medical
        global Poem,Lishimingren,stop,newlist
        change = iter
        time = time + keepSeconds
        timet = timet + keepSeconds
        if timet > 3:
            timet = timet-3
            iter = iter + 1
        if change != iter:#每次迭代的变化
            change = iter
            yuliaosize = yuliaosize + random.uniform(3, 17)
            yuliaonumber = yuliaonumber + random.randint(1,1000)

            Animal_new = random.randint(3000,7000)
            Animal = Animal + Animal_new
            Caijing_new = random.randint(3000,7000)
            Caijing = Caijing + Caijing_new
            Car_new = random.randint(3000,7000)
            Car = Car + Car_new
            Chengyu_new = random.randint(3000,7000)
            Chengyu = Chengyu + Chengyu_new
            Diming_new = random.randint(3000,7000)
            Diming = Diming + Diming_new
            Food_new = random.randint(3000,7000)
            Food = Food + Food_new
            IT_new = random.randint(3000,7000)
            IT = IT + IT_new
            Law_new = random.randint(3000,7000)
            Law = Law + Law_new
            Medical_new = random.randint(3000,7000)
            Medical = Medical + Medical_new
            Poem_new = random.randint(3000,7000)
            Poem = Poem + Poem_new
            Lishimingren_new = random.randint(3000,7000)
            Lishimingren = Lishimingren + Lishimingren_new
            stop_new = random.randint(3000,7000)
            stop = stop + stop_new

            newwords = Animal_new+Caijing_new+Car_new+Chengyu_new+Diming_new+Food_new+IT_new+Law_new+Medical_new+Poem_new+Lishimingren_new+stop_new
            oldwords = totalwords
            newlist.append(newwords)
            totalwords = totalwords + newwords
        #更新页面内容
        self.label_2.setText(str(iter))
        self.label_4.setText(str(time))
        self.label_6.setText(str(yuliaosize))
        self.label_8.setText(str(yuliaonumber))
        self.label_10.setText(str(totalwords))
        self.label_12.setText(str(newwords))
        self.label_14.setText(str(oldwords))
        self.label_16.setText(str(stop_new))
        self.label_19.setText(str(Animal_new))
        self.label_21.setText(str(Caijing_new))
        self.label_23.setText(str(Car_new))
        self.label_25.setText(str(Chengyu_new))
        self.label_27.setText(str(Diming_new))
        self.label_29.setText(str(Food_new))
        self.label_31.setText(str(IT_new))
        self.label_33.setText(str(Law_new))
        self.label_35.setText(str(Lishimingren_new))
        self.label_37.setText(str(Medical_new))
        self.label_39.setText(str(Poem_new))
        #图像绘制
        plt.figure(1)
        plt.plot(np.array(newlist), color='orange', linewidth=3.0)
        plt.savefig('./newlist.png')
        pixmap1 = QPixmap('./newlist.png')
        self.label_43.setPixmap(pixmap1)
        self.label_43.setScaledContents(True)

        plt.figure(2)
        plt.cla()
        data = [Animal_new,Caijing_new,Car_new,Chengyu_new,Diming_new,Food_new,IT_new,Law_new,Medical_new,Poem_new,Lishimingren_new,stop_new]
        print(data)
        label = ['Animal','Caijing','Car','Chengyu','Diming','Food','IT','Law','Medical','Poem','Lishimingren','stop']
        plt.pie(data, labels=label)
        plt.savefig('./newwords.jpg')
        pixmap2 = QPixmap('./newwords.jpg')
        self.label_41.setPixmap(pixmap2)
        self.label_41.setScaledContents(True)




class Window(QMainWindow, Ui_BeforeRun):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle("迭代设置")
        self.setupUi(self) # 渲染页面控件
        self.connect_signals() # 设置信号槽
        self.child_window = Running()

    def connect_signals(self):
        self.pushButton.clicked.connect(self.pushButton_clicked) # 绑定确定按钮事件

    def pushButton_clicked(self):
        global iterTimes
        iterTimes = self.lineEdit_2.text()
        iterTimes = int(iterTimes)
        global keepSeconds
        keepSeconds = self.lineEdit_3.text()
        keepSeconds = int(keepSeconds)
        self.child_window.timer.start(keepSeconds*1000)  # 设置计时间隔并启动
        self.close()
        self.child_window.show() # 显示子窗口
        print(iterTimes)
        print(keepSeconds)


def main():
    app = QApplication(sys.argv)
    mywindow = Window()
    mywindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()