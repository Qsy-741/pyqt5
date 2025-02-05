# -*- coding: utf-8 -*-
import json
import os
import random

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget
from Basedir import basedir
from PlayMusic import play_sound
from SerialController import serialController
from ui.screen import Ui_Screen_Form


class ScreenCore(QWidget, Ui_Screen_Form):
    def __init__(self):
        super().__init__()
        self.body = ""
        self.y = 0
        self.x = 0
        self.cover = True
        self.font_size = 1
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

        validator = QIntValidator()
        # 限制输入范围为 0 到 100
        validator.setRange(0, 99)

        self.sizeBox.addItem("字号--小号")
        self.sizeBox.addItem("字号--正常")
        self.sizeBox.addItem("字号--大号")
        self.sizeBox.setCurrentIndex(1)
        self.edit_x.setText("0")
        self.edit_y.setText("0")
        self.edit_x.setValidator(validator)
        self.edit_y.setValidator(validator)

        self.PushButton.clicked.connect(self.send_str)
        self.scrollButton.checkedChanged.connect(self.scroll_font)

        self.animation_timer = QtCore.QTimer(self)
        self.animation_timer.timeout.connect(self.update_cursor)

    def send_str(self):
        self.font_size = self.sizeBox.currentIndex() + 1
        self.cover = self.coverButton.checked
        if self.edit_x.text() or self.edit_y.text():
            self.x = int(self.edit_x.text())
            self.y = int(self.edit_y.text())
        self.body = self.bodyLineEdit.text()
        data = {"name": "screen",
                "data": {"cursor": [int(self.x), int(self.y)], "size": self.font_size, "cover": self.cover,
                         "text": self.body}}
        serialController.send_data(json.dumps(data))

    def scroll_font(self):
        state = self.scrollButton.checked
        if state and self.body != "":
            self.animation_timer.start(15)  # 每 20 毫秒更新一次
        else:
            self.animation_timer.stop()

    def update_cursor(self):
        if self.x >= 128:
            self.x = 0
        self.x = int(self.x) + 1
        data = {"name": "screen",
                "data": {"cursor": [int(self.x), int(self.y)], "size": self.font_size, "cover": self.cover,
                         "text": self.body}}
        serialController.send_data(json.dumps(data))

    def closeEvent(self, event):
        start_cmd = {"name": "screen", "state": 2}
        if self.animation_timer:
            self.animation_timer.stop()  # 停止定时器
        serialController.send_data(json.dumps(start_cmd))
        super().closeEvent(event)

