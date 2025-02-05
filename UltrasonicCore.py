import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget
from Basedir import basedir
from SerialController import serialController
from ui.ultrasonic import Ui_Us_Form


class UltrasonicCore(QWidget, Ui_Us_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

        self.movie = QMovie(os.path.join(basedir, 'resource', "us_animation.gif"))
        self.label.setMovie(self.movie)
        self.movie.start()

        self.movie_2 = QMovie(os.path.join(basedir, 'resource', "us_animation2.gif"))
        self.label_2.setMovie(self.movie_2)
        self.movie_2.start()

        self.ultrasonic_value.setReadOnly(True)
        self.BodyLabel.setText("        Avatarmind超声波模块是一款超声波测距模块。特别应用于玩具超声测距，机器人等应用。采用自研超声波测距解调芯片，单总线，外围更加简洁，芯片内置高精度振荡器，无需额外晶振。驱动采用扫频技术，减少探头本身一致性对模块灵敏度的影响。")
        self.BodyLabel.setWordWrap(True)
        self.BodyLabel_2.setText("        外部 MCU 初始设置为输出，给模块 I/O 脚一个大于 10us 的高电平脉冲；输出脉冲信号后，MCU 设置 为输入模式，等待模块给出的一个与距离等比的高电平脉冲信号；测量结束后 MCU 设置为输出模式，进行下次测量。声速可根据脉宽时间“T”算出：\n        距离=T(从发送信号至接收到信号的时间)*340/2 ( 340m/s是声音在空气中的传播速度)")
        self.BodyLabel_2.setWordWrap(True)

        serialController.start_listening()
        serialController.ultrasonic_data_received.connect(self.update_value)

    def update_value(self, value):
        value = value['data']
        value = round(value, 2)
        self.ultrasonic_value.setText("{:.2f}".format(value))

    def closeEvent(self, event):
        start_cmd = {"name": "ultrasonic", "state": 2}
        serialController.send_data(json.dumps(start_cmd))
        serialController.stop_listening()
        super().closeEvent(event)
