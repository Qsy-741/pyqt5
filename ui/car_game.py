# -*- coding: utf-8 -*-
import os
import sys
import random
from typing import Union
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap, QImage, QImageReader, QMovie
from PyQt5.QtWidgets import QApplication, QWidget
from qfluentwidgets import ImageLabel, TitleLabel, CaptionLabel, PushButton
from Basedir import basedir
from qfluentwidgets import Dialog

from SerialController import serialController


class Ui_Car_Form(object):
    def __init__(self):
        self.main_car = None
        self.car = None
        self.end_game = True
        self.animation_speed = 1  # 默认速度
        self.animation_timer = None
        self.grade = 0

    def setupUi(self, Car_Form):
        Car_Form.setObjectName("Car_Form")
        Car_Form.setFixedSize(600, 800)
        self.car_background = ResizableImageLabel(Car_Form)
        self.car_background.setImage(os.path.join(basedir, 'resource', "malu.png"))
        self.car_background.setGeometry(QtCore.QRect(0, 0, 520, 660))
        # 获取父窗口的尺寸
        # 获取组件的尺寸
        widget_width = self.car_background.width()
        widget_height = self.car_background.height()
        # 计算组件的 x 和 y 坐标
        x = (600 - widget_width) // 2
        y = (800 - widget_height) // 2
        # 设置组件的位置
        self.car_background.move(x, y)
        self.car_background.setObjectName("car_background")
        self.TitleLabel = TitleLabel(Car_Form)
        self.TitleLabel.setGeometry(QtCore.QRect(180, 10, 240, 50))
        self.TitleLabel.setObjectName("TitleLabel")
        self.line_1 = Line(self.car_background, 170, 120, 18, 120)
        self.line_2 = Line(self.car_background, 170, 320, 18, 120)
        self.line_3 = Line(self.car_background, 170, 530, 18, 120)
        self.line_4 = Line(self.car_background, 350, 120, 18, 120)
        self.line_5 = Line(self.car_background, 350, 320, 18, 120)
        self.line_6 = Line(self.car_background, 350, 530, 18, 120)
        self.line_7 = Line(self.car_background, 170, -50, 18, 120)
        self.line_8 = Line(self.car_background, 170, 710, 18, 120)
        self.line_9 = Line(self.car_background, 350, -50, 18, 120)
        self.line_10 = Line(self.car_background, 350, 710, 18, 120)

        self.horizontalLayoutWidget = QtWidgets.QWidget(Car_Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 715, 580, 100))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CaptionLabel = CaptionLabel(Car_Form)
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.CaptionLabel.setText("分数：")
        self.horizontalLayout.addWidget(self.CaptionLabel)
        self.CaptionLabel_2 = CaptionLabel(Car_Form)
        self.CaptionLabel_2.setObjectName("CaptionLabel_2")
        self.CaptionLabel_2.setText("0")
        self.horizontalLayout.addWidget(self.CaptionLabel_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.PushButton = PushButton(Car_Form)
        self.PushButton.setObjectName("PushButton")
        self.PushButton.setText("开始 | 重玩")
        self.PushButton.clicked.connect(self.action_game)
        self.horizontalLayout.addWidget(self.PushButton)

        self.main_car = ResizableImageLabel(self.car_background)
        self.main_car.setImage(os.path.join(basedir, 'resource', "acar.png"))
        self.main_car.setGeometry(QtCore.QRect(210, 460, 100, 170))

        # 创建并启动动画定时器
        self.animation_timer = QtCore.QTimer(Car_Form)
        self.animation_timer.timeout.connect(self.update_line_positions)
        self.animation_timer.start(10)  # 每 20 毫秒更新一次

        self.main_car_bon = ResizableImageLabel(self.car_background)
        self.main_car_bon.setImage(os.path.join(basedir, 'resource', "carbon.png"))
        self.main_car_bon.setGeometry(QtCore.QRect(220, 430, 70, 70))
        self.main_car_bon.setVisible(False)

        self.random_refresh_car()
        self.car.setVisible(False)

        self.retranslateUi(Car_Form)
        QtCore.QMetaObject.connectSlotsByName(Car_Form)
        serialController.start_listening()
        serialController.rotary_data_received.connect(self.move_car)
        serialController.switch_data_received.connect(self.adjust_speed)

    def action_game(self):
        self.grade = 0
        self.end_game = False
        self.animation_speed = 1
        self.random_refresh_car()
        self.car.setVisible(True)
        self.main_car_bon.setVisible(False)
        self.CaptionLabel_2.setText(str(self.grade))
        self.animation_timer.start()

    def adjust_speed(self, switch):
        if switch:
            self.animation_speed += 1

    def move_car(self, data):
        if not self.end_game:
            place = data['data']
            x = int(346 * (place/100)) + 86
            self.main_car.move(x-self.main_car.width()//2, self.main_car.y())

    def update_line_positions(self):
        """更新线条的 y 坐标以实现动画效果"""
        for line in [self.line_1, self.line_2, self.line_3,
                     self.line_4, self.line_5, self.line_6,
                     self.line_7, self.line_8, self.line_9, self.line_10]:
            current_y = line.y() + line.height()//2
            if current_y > 720:
                new_y = -60
            else:
                new_y = current_y + self.animation_speed * 2
            line.set_y(new_y)
        if not self.end_game:
            current_y = self.car.y() + self.car.height()//2
            if current_y > 745:
                self.random_refresh_car()
                self.grade += 1
                self.CaptionLabel_2.setText(str(self.grade))
            else:
                new_y = current_y + self.animation_speed
                self.car.move(self.car.x(), new_y - self.car.height() // 2)
            if (self.car.y() + self.car.height()) > self.main_car.y() + 20 and \
                ((self.main_car.x()+30) < self.car.x() < (self.main_car.x() + self.main_car.width()-30) or
                (self.main_car.x()+30) < (self.car.x() + self.car.width()) < (self.main_car.x() + self.main_car.width()-30) or
                (self.main_car.x()+30) < (self.car.x() + self.car.width()//2) < (self.main_car.x() + self.main_car.width()-30)):
                # 判断到发生碰撞
                self.animation_timer.stop()
                self.end_game = True
                self.main_car_bon.move(self.car.x()+10, self.main_car_bon.y())
                self.main_car_bon.setVisible(True)
                self.main_car_bon.raise_()
                self.showDialog()

    def random_refresh_car(self):
        """随机刷新车辆"""
        car_list = ['acar.png', 'bcar.png', 'ccar.png', 'dcar.png']
        initial_position = [40, 210, 390]
        car = random.choice(car_list)
        car_start = random.choice(initial_position)
        if self.car is None:
            self.car = ResizableImageLabel(self.car_background)
        self.car.setImage(os.path.join(basedir, 'resource', str(car)))
        self.car.setGeometry(QtCore.QRect(int(car_start), -170, 100, 170))

    def set_animation_speed(self, speed):
        """设置动画速度

        Args:
            speed (int): 动画速度，正数表示向下移动，负数表示向上移动
        """
        self.animation_speed = speed

    def showDialog(self):
        title = '游戏结束！'
        content = """ 失败，出现碰撞！ """
        w = Dialog(title, content)
        w.setTitleBarVisible(False)
        w.setContentCopyable(True)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')

    def retranslateUi(self, Car_Form):
        _translate = QtCore.QCoreApplication.translate
        Car_Form.setWindowTitle(_translate("Car_Form", "Form"))
        self.TitleLabel.setText(_translate("Car_Form", "旋转电位器小游戏"))


class Line(QtWidgets.QFrame):
    def __init__(self, parent, x, y, width, height):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(x - width // 2, y - height // 2, width, height))
        self.setMinimumSize(QtCore.QSize(10, 0))
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setLineWidth(21)
        self.setMidLineWidth(8)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
        self.setPalette(palette)
        self.setFrameShape(QtWidgets.QFrame.VLine)

    def set_position(self, x, y):
        """设置线条中心点坐标

        Args:
            x (int):  目标中心点距离父组件左侧的 x 坐标
            y (int): 目标中心点距离父组件顶部的 y 坐标
        """
        width = self.width()
        height = self.height()
        new_x = x - width // 2
        new_y = y - height // 2
        self.move(new_x, new_y)

    def set_y(self, y):
        """设置线条中心点坐标

        Args:
            y (int): 要移动到新的y的坐标
        """
        height = self.height()
        new_y = y - height // 2
        self.move(self.x(), new_y)

    def set_stretch(self, horizontal_stretch, vertical_stretch):
        """设置线条拉伸

        Args:
            horizontal_stretch (int): 水平拉伸因子
            vertical_stretch (int): 垂直拉伸因子
        """
        policy = self.sizePolicy()
        policy.setHorizontalStretch(horizontal_stretch)
        policy.setVerticalStretch(vertical_stretch)
        self.setSizePolicy(policy)


class ResizableImageLabel(ImageLabel):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setScaledContents(False)  # 添加这行代码，允许 QLabel 缩放内容

    def setImage(self, image: Union[str, QPixmap, QImage] = None):
        """设置标签的图片，允许调整大小

        Args:
            image (Union[str, QPixmap, QImage], optional): 图片路径、QPixmap 或 QImage 对象. 默认为 None.
        """
        self.image = image or QImage()

        if isinstance(image, str):
            reader = QImageReader(image)
            if reader.supportsAnimation():
                self.setMovie(QMovie(image))
            else:
                self.image = reader.read()
        elif isinstance(image, QPixmap):
            self.image = image.toImage()

        #  不再固定大小，而是根据需要调整 QLabel 的大小
        self.adjustSize()
        self.update()


