# -*- coding: utf-8 -*-
import json
import os
import time
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor
from Basedir import basedir
from SerialController import serialController
from qfluentwidgets import FluentIcon as FIF, ToolButton, ColorDialog


class JsonData:
    def __init__(self, data):
        self.data = data

    def get_json(self):
        return json.dumps(self.data)

    def set_value(self, key, value):
        keys = key.split('.')
        current = self.data
        for k in keys[:-1]:
            current = current[k]
        current[keys[-1]] = value


data = {
    "name": "LED",
    "id": 1,
    "data": {
        "br": 0,
        "R": 255,
        "G": 255,
        "B": 255
    }
}
json_data = JsonData(data)


class Ui_LedExample(object):

    def __init__(self):
        self.led_example_signal = QtCore.pyqtSignal(str)
        self.led_states = {
            'led1': False,
            'led2': False,
            'led3': False,
            'led4': False
        }

    def setupUi(self, LedExample):
        LedExample.setObjectName("LedExample")
        # LedExample.resize(650, 650)
        LedExample.setWindowFlags(QtCore.Qt.Window)
        self.verticalLayout = QtWidgets.QVBoxLayout(LedExample)
        self.verticalLayout.setObjectName("verticalLayout")
        # self.led_Title = TitleLabel(LedExample)
        # self.led_Title.setObjectName("led_Title")
        # self.verticalLayout.addWidget(self.led_Title)
        self.led_image = ImageLabel(LedExample)
        self.led_image.setObjectName("led_image")
        self.led_image.setImage(os.path.join(basedir, 'resource', "台灯.jpg"))
        self.led_image.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # 设置最大尺寸和最小尺寸（可选）
        self.led_image.setMaximumSize(QtCore.QSize(6000, 6000))  # 如果您仍然希望限制最大尺寸
        self.led_image.setMinimumSize(QtCore.QSize(750, 650))  # 设置最小尺寸为 0x0
        self.verticalLayout.addWidget(self.led_image)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        # self.color_btn1 = PushButton(LedExample)
        # self.color_btn1.setObjectName("color_btn1")
        # self.horizontalLayout.addWidget(self.color_btn1)
        self.color_btn1 = ToolButton(FIF.PALETTE, LedExample)
        self.horizontalLayout.addWidget(self.color_btn1)
        self.color_btn1 .clicked.connect(lambda: self.__showColorDialog(LedExample,"color1"))##连接到槽函数
        self.led1_btn = PushButton(LedExample)
        self.led1_btn.setObjectName("led1_btn")
        self.horizontalLayout.addWidget(self.led1_btn)

        self.color_btn2 = ToolButton(FIF.PALETTE, LedExample)
        self.horizontalLayout.addWidget(self.color_btn2)
        self.color_btn2.clicked.connect(lambda: self.__showColorDialog(LedExample,"color2"))  ##连接到槽函数
        self.led2_btn = PushButton(LedExample)
        self.led2_btn.setObjectName("led2_btn")
        self.horizontalLayout.addWidget(self.led2_btn)

        self.color_btn3 = ToolButton(FIF.PALETTE, LedExample)
        self.horizontalLayout.addWidget(self.color_btn3)
        self.color_btn3.clicked.connect(lambda: self.__showColorDialog(LedExample,"color3"))  ##连接到槽函数
        self.led3_btn = PushButton(LedExample)
        self.led3_btn.setObjectName("led3_btn")
        self.horizontalLayout.addWidget(self.led3_btn)

        self.color_btn4 = ToolButton(FIF.PALETTE, LedExample)
        self.horizontalLayout.addWidget(self.color_btn4)
        self.color_btn4.clicked.connect(lambda: self.__showColorDialog(LedExample,"color4"))  ##连接到槽函数
        self.led4_btn = PushButton(LedExample)
        self.led4_btn.setObjectName("led4_btn")


        self.horizontalLayout.addWidget(self.led4_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.light_image = IconWidget(FIF.CONSTRACT, LedExample)
        self.light_image.setObjectName("light_image")
        self.light_image.setMinimumSize(20,20)
        self.light_image.setMaximumSize(20,20)
        # self.light_image.setIcon(FIF.CONSTRACT)
        self.horizontalLayout_2.addWidget(self.light_image)
        self.light_slider = Slider(LedExample)
        self.light_slider.setOrientation(QtCore.Qt.Horizontal)
        self.light_slider.setObjectName("light_slider")
        self.light_slider.setMinimum(0)
        self.light_slider.setMaximum(40)  # 设亮度范围是 0 到 100
        self.light_slider.valueChanged.connect(self.on_slider_value_changed)#连接信号到槽函数
        self.horizontalLayout_2.addWidget(self.light_slider)


        self.light_ComboBox = ComboBox(LedExample)
        self.light_ComboBox.setObjectName("light_ComboBox")
        # 添加选项到下拉列表，用于控制亮度
        self.light_ComboBox.addItem("LED1")
        self.light_ComboBox.addItem("LED2")
        self.light_ComboBox.addItem("LED3")
        self.light_ComboBox.addItem("LED4")
        self.light_ComboBox.addItem("ALL")
        self.horizontalLayout_2.addWidget(self.light_ComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(1, 3)

        self.led1_btn.clicked.connect(lambda: self.control_cmd("led1"))
        self.led2_btn.clicked.connect(lambda: self.control_cmd("led2"))
        self.led3_btn.clicked.connect(lambda: self.control_cmd("led3"))
        self.led4_btn.clicked.connect(lambda: self.control_cmd("led4"))

        self.retranslateUi(LedExample)
        QtCore.QMetaObject.connectSlotsByName(LedExample)
    def __showColorDialog(self,LedExample,colorID):
        self.w = ColorDialog(QColor("#ff1bfff0"), "选择颜色",LedExample,False)
        self.w.yesButton.clicked.connect(lambda:self.onYesClicked(colorID))
        self.w.yesButton.setText("确认")
        self.w.cancelButton.setText("取消")
        # w.colorChanged.connect(self.__onColorChanged)
        self.w.exec()
    def onYesClicked(self,colorID1):#当调试板的YES被按下，将当前的RGB值发送
        json_data.set_value('id', colorID1[-1])
        json_data.set_value('data.R', self.w.color.red())
        json_data.set_value('data.G', self.w.color.green())
        json_data.set_value('data.B', self.w.color.blue())
        try:
            serialController.send_data(json_data.get_json())
        except Exception as e:
            print(e)

    def on_slider_value_changed(self, value):
        # 当滑动条的值改变时，更新 data 字典中的 br 值
        if(self.light_ComboBox.currentIndex()+1==5):
            for i in range(1,5):
                json_data.set_value('id', i)
                json_data.set_value('data.br', value)
                time.sleep(0.01)
                try:
                    serialController.send_data(json_data.get_json())
                except Exception as e:
                    print(e)
        else:
            json_data.set_value('id', self.light_ComboBox.currentIndex()+1)
            json_data.set_value('data.br', value)
            try:
                serialController.send_data(json_data.get_json())
            except Exception as e:
                print(e)

    def retranslateUi(self, LedExample):
        _translate = QtCore.QCoreApplication.translate
        self.led1_btn.setText(_translate("LedExample", "开关1"))
        self.led2_btn.setText(_translate("LedExample", "开关2"))
        self.led3_btn.setText(_translate("LedExample", "开关3"))
        self.led4_btn.setText(_translate("LedExample", "开关4"))


    def control_cmd(self, led_id):
        self.led_states[led_id] = not self.led_states[led_id]  # 切换 LED 状态
        json_data.set_value("id", led_id[-1])
        self.light_ComboBox.setCurrentIndex(int(led_id[-1])-1)  # 将下拉框中的LED*切换为实际按下的开关*
        if self.led_states[led_id]:
            self.light_slider.setValue(40)  # 设置初始值
            json_data.set_value('data.br', 40)#开关按键只设置灯的亮度

        else:
            self.light_slider.setValue(0)  # 设置初始值
            json_data.set_value('data.br', 0)

        # print(json_data.get_json())
        try:
            serialController.send_data(json_data.get_json())
        except Exception as e:
            print(e)


from qfluentwidgets import ComboBox, IconWidget, ImageLabel, PushButton, Slider


