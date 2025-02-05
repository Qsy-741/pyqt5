# -*- coding: utf-8 -*-
import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from Basedir import basedir
from SerialController import serialController
from ui.light import Ui_light_Form


class LightCore(QWidget, Ui_light_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        serialController.rotary_data_received.connect(self.update_light)
        serialController.start_listening()

    def update_light(self,dict):
        value = dict['data']
        if value > 5:
            self.ImageLabel.setImage(os.path.join(basedir, 'resource', "on_light.png"))
        else:
            self.ImageLabel.setImage(os.path.join(basedir, 'resource', "off_light.png"))
        self.ImageLabel.update()
        self.ImageLabel.repaint()

    def closeEvent(self, event):
        start_cmd = {"name": "ultrasonic", "state": 2}
        serialController.send_data(json.dumps(start_cmd))
        serialController.stop_listening()
        super().closeEvent(event)
