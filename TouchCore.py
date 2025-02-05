# -*- coding: utf-8 -*-
import json
import os
import random

from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtWidgets import QWidget
from Basedir import basedir
from PlayMusic import play_sound
from SerialController import serialController
from ui.touch import Ui_touch_Form


class TouchCore(QWidget, Ui_touch_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

        self.animation = QPropertyAnimation(self.ImageLabel, b"pos")
        self.animation.setDuration(1000)  # 动画持续时间 (毫秒)
        self.animation.setEasingCurve(QEasingCurve.InOutSine)  # 动画曲线
        serialController.switch_data_received.connect(self.pressEvent)
        serialController.start_listening()

    def pressEvent(self, press):
        if not press:
            self.start_shaking()
            music = random.choice(['叮咚长音', '叮咚叮咚'])
            play_sound(music+'.wav')

    def start_shaking(self):
        original_pos = self.ImageLabel.pos()
        self.animation.setStartValue(original_pos)
        self.animation.setKeyValueAt(0.25, original_pos + QPoint(10, 0))  # 右摇
        self.animation.setKeyValueAt(0.5, original_pos)
        self.animation.setKeyValueAt(0.75, original_pos + QPoint(-10, 0))  # 左摇
        self.animation.setEndValue(original_pos)
        self.animation.start()

    def closeEvent(self, event):
        start_cmd = {"name": "switch", "state": 2}
        serialController.send_data(json.dumps(start_cmd))
        serialController.stop_listening()
        super().closeEvent(event)
