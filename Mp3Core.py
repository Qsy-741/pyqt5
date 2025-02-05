import json
import os
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import InfoBar, InfoBarPosition

from Basedir import basedir
from SerialController import serialController
from ui.mp3 import Ui_MP3_Form


class MP3(QWidget, Ui_MP3_Form):
    def __init__(self):
        super().__init__()
        self.play_flag = False
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

        self.play_pause.clicked.connect(partial(self.mp3_send_cmd, 1))
        self.add_volume.clicked.connect(partial(self.mp3_send_cmd, 5))
        self.reduce_volume.clicked.connect(partial(self.mp3_send_cmd, 6))
        self.next_song.clicked.connect(partial(self.mp3_send_cmd, 3))
        self.previous_song.clicked.connect(partial(self.mp3_send_cmd, 4))

    def mp3_send_cmd(self, cmd):
        command = {"name": "MP3", "id": cmd}
        if cmd == 1:
            if not self.play_flag:
                self.play_flag = True
                command['id'] = 1
                self.play_pause.setIcon(os.path.join(basedir, 'resource', "暂停.png"))
            else:
                self.play_flag = False
                command['id'] = 2
                self.play_pause.setIcon(os.path.join(basedir, 'resource', "播放.png"))
        if cmd == 3 or cmd == 4:
            self.play_flag = True
            self.play_pause.setIcon(os.path.join(basedir, 'resource', "暂停.png"))
        if cmd == 5:
            self.createTopInfoBar("MP3模块音量增加 + ")
        elif cmd == 6:
            self.createTopInfoBar("MP3模块音量减小 - ")
        serialController.send_data(json.dumps(command))

    def createTopInfoBar(self, str):
        # convenient static mothod
        InfoBar.info(
            title=self.tr('提示'),
            content=str,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
        )

    def closeEvent(self, event):
        start_cmd = {"name": "MP3", "state": 2}
        serialController.send_data(json.dumps(start_cmd))
        serialController.stop_listening()
        super().closeEvent(event)
