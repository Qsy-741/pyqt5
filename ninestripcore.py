import json

from PyQt5.QtWidgets import QDialog
from qfluentwidgets import Dialog

from ui.ninestrip import Ui_NineStrip
from SerialController import serialController


class NineStripCore(Ui_NineStrip):

    def __init__(self):
        self.btn_list = None
        self.press_num = None
        self.data = None
        self.axis = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 123,456,789,159,357,147,258,369 则 win
        self.stand = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [2, 4, 6], [0, 3, 6], [1, 4, 7], [2, 5, 8]]

    def initialize(self):
        self.data = {
            "name": "ninestrip",
            "id": -1,
            "data": {
                "br": 100,
                "R": 0,
                "G": 0,
                "B": 0
            }
        }
        self.press_num = 0  # 记录按下的次数
        self.btn11.clicked.connect(lambda: self.press_event(1, self.btn11))
        self.btn12.clicked.connect(lambda: self.press_event(2, self.btn12))
        self.btn13.clicked.connect(lambda: self.press_event(3, self.btn13))
        self.btn21.clicked.connect(lambda: self.press_event(4, self.btn21))
        self.btn22.clicked.connect(lambda: self.press_event(5, self.btn22))
        self.btn23.clicked.connect(lambda: self.press_event(6, self.btn23))
        self.btn31.clicked.connect(lambda: self.press_event(7, self.btn31))
        self.btn32.clicked.connect(lambda: self.press_event(8, self.btn32))
        self.btn33.clicked.connect(lambda: self.press_event(9, self.btn33))
        self.reset_btn.clicked.connect(self.reset)
        self.btn_list = [self.btn11, self.btn12, self.btn13, self.btn21, self.btn22, self.btn23, self.btn31, self.btn32,
                         self.btn33]

    def reset(self):
        self.press_num = 0
        self.data["id"] = -1  # 全息灭
        self.axis = [0, 0, 0, 0, 0, 0, 0, 0, 0]     # 清零标志位
        self.send_cmd()
        serialController.send_data(json.dumps(self.data))
        for btn in self.btn_list:
            self.inverse_btn(btn, "white")

    def press_event(self, id, btn):
        self.data["id"] = id
        if self.axis[id - 1] != 0:
            return
        self.press_num = self.press_num + 1
        if self.press_num % 2 == 0:  # 如果他是偶数
            self.data["data"]["R"] = 255
            self.inverse_btn(btn, "red")
            self.axis[id - 1] = 1
        else:
            self.data["data"]["B"] = 255
            self.inverse_btn(btn, "blue")
            self.axis[id - 1] = -1
        self.send_cmd()
        winer = self.judge_win()
        if winer == "red":
            self.showDialog("red")
        elif winer == "blue":
            self.showDialog("blue")
        elif self.press_num > 8:
            self.showDialog("平局")

    def send_cmd(self):
        serialController.send_data(json.dumps(self.data))
        self.data["id"] = -1  # 全息灭
        self.data["data"]["R"] = 0
        self.data["data"]["G"] = 0
        self.data["data"]["B"] = 0

    def judge_win(self):
        sum = 0
        for item in self.stand:
            for i in item:
                if self.axis[i] == 1:
                    sum += 1
            if sum == 3:
                return "red"
            else:
                sum = 0
        for item in self.stand:
            for i in item:
                if self.axis[i] == -1:
                    sum += 1
            if sum == 3:
                return "blue"
            else:
                sum = 0
        return ""

    def showDialog(self, str):
        title = '游戏结束！'
        if str == "red":
            content = """恭喜红色方获胜！"""
        elif str == "blue":
            content = """恭喜蓝色方获胜！"""
        else:
            content = """ 平局！ """
        w = Dialog(title, content)
        w.setTitleBarVisible(False)
        w.setContentCopyable(True)
        w.yesButton.setText("确定")
        w.cancelButton.setVisible(False)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')

    def inverse_btn(self, btn, color):
        if color == "red":
            btn.setStyleSheet(
                "QPushButton { color: black;background: rgba(255, 0, 0, 0.7);border: 1px solid rgba(0, 0, 0, 0.073);"
                "border-bottom: 1px solid rgba(0, 0, 0, 0.183);border-radius: 5px;"
                "padding: 5px 12px 6px 12px;outline: none;}")
        elif color == "blue":
            btn.setStyleSheet(
                "QPushButton { color: black;background: rgba(0, 0, 255, 0.7);border: 1px solid rgba(0, 0, 0, 0.073);"
                "border-bottom: 1px solid rgba(0, 0, 0, 0.183);border-radius: 5px;"
                "padding: 5px 12px 6px 12px;outline: none;}")
        elif color == "white":
            btn.setStyleSheet(
                "QPushButton { color: black;background: rgba(255, 255, 255, 0.7);border: 1px solid rgba(0, 0, 0, 0.073);"
                "border-bottom: 1px solid rgba(0, 0, 0, 0.183);border-radius: 5px;"
                "padding: 5px 12px 6px 12px;outline: none;}")
