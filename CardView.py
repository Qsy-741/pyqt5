import json
import os
import time
from Basedir import basedir
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QSizePolicy, QDialog
from qfluentwidgets import ElevatedCardWidget, ImageLabel, CaptionLabel, FlowLayout, ScrollArea
from LightCore import LightCore
from Mp3Core import MP3
from ScreenCore import ScreenCore
from TouchCore import TouchCore
from UltrasonicCore import UltrasonicCore
from ninestripcore import NineStripCore
from ui.LedExample import Ui_LedExample
from jisuanqicore import Jisuanqi
from ui.buzzer import Buzzer_Form
from ui.car_game import Ui_Car_Form
from SerialController import serialController


class CardView(ElevatedCardWidget):
    pressEvent_signal = pyqtSignal()

    def __init__(self, iconPath: str, width=0, height=0, name="", parent=None):
        super().__init__(parent)
        self.setContentsMargins(0,0,0,0)
        self.iconWidget = ImageLabel(iconPath, self)
        self.label = CaptionLabel(name, self)

        self.iconWidget.scaledToHeight(height)
        self.iconWidget.scaledToWidth(width)

        self.iconWidget.setBorderRadius(8,8,8,8)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0,0,0,10)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignTop)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(
            self.label, 0, Qt.AlignHCenter | Qt.AlignBottom)

        self.setFixedSize(220, 260)

    def mousePressEvent(self, e):
        super(ElevatedCardWidget, self).mousePressEvent(e)  # 调用基类的mousePressEvent方法
        self.pressEvent_signal.emit()


class Widget(ScrollArea):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.ui5 = None
        self.ui3 = None
        self.ui2 = None
        self.ui4 = None
        self.ui1 = None
        self.view = QWidget(self)
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 设置尺寸策略为扩展
        # 设置背景色为透明
        palette = self.view.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0, 0))
        self.view.setPalette(palette)

        self.flowLayout = FlowLayout(self.view)
        self.flowLayout.setSpacing(6)
        self.flowLayout.setContentsMargins(10, 10, 10, 10)
        self.flowLayout.setAlignment(Qt.AlignVCenter)
        self.setWidget(self.view)  # 设置滚动区域的视口
        self.setWidgetResizable(True)

        self.led_card = CardView(os.path.join(basedir, 'resource', "台灯.jpg"),210,200,"台灯实验", self)
        self.keyboard_card = CardView(os.path.join(basedir, 'resource', "计算器.png"),150,150, "触摸键盘实验", self)
        self.rotary_potentiometer_card = CardView(os.path.join(basedir, 'resource', "car_game_bg.png"), 190, 190, "旋转电位器实验", self)
        self.led_strip_card = CardView(os.path.join(basedir, 'resource', "井字棋2.png"), 180, 180,
                                                  "灯板模拟井字棋实验", self)
        self.mp3_card = CardView(os.path.join(basedir, 'resource', "MP3_2.png"), 210, 200, "音乐播放器实验", self)
        self.ultrasonic_card = CardView(os.path.join(basedir, 'resource', "超声波.png"), 210, 200, "超声波测距实验", self)
        self.buzzer_card = CardView(os.path.join(basedir, 'resource', "钢琴键盘.png"), 180, 170, "电子琴实验", self)
        self.light_card = CardView(os.path.join(basedir, 'resource', "light.png"), 210, 200, "光敏开关实验", self)
        self.touch_card = CardView(os.path.join(basedir, 'resource', "按门铃.png"), 140, 140, "电子门铃实验", self)
        self.screen_card = CardView(os.path.join(basedir, 'resource', "显示器.png"), 210, 200, "显示屏实验", self)
        self.b_card = CardView(os.path.join(basedir, 'resource', "井字棋.png"), 210, 200, "实验", self)
        self.c_card = CardView(os.path.join(basedir, 'resource', "井字棋.png"), 210, 200, "实验", self)
        self.d_card = CardView(os.path.join(basedir, 'resource', "井字棋.png"), 210, 200, "实验", self)
        self.e_card = CardView(os.path.join(basedir, 'resource', "井字棋.png"), 210, 200, "实验", self)
        self.f_card = CardView(os.path.join(basedir, 'resource', "井字棋.png"), 210, 200, "实验", self)
        self.g_card = CardView(os.path.join(basedir, 'resource', "井字棋.png"), 210, 200, "实验", self)

        self.led_card.pressEvent_signal.connect(self.show_led_example_dialog)
        self.keyboard_card.pressEvent_signal.connect(self.show_key_board_dialog)
        self.led_strip_card.pressEvent_signal.connect(self.show_led_strip_dialog)
        self.rotary_potentiometer_card.pressEvent_signal.connect(self.show_rotary_potentiometer_dialog)
        self.mp3_card.pressEvent_signal.connect(self.show_mp3_dialog)
        self.ultrasonic_card.pressEvent_signal.connect(self.show_ultrasonic_dialog)
        self.buzzer_card.pressEvent_signal.connect(self.show_buzzer_dialog)
        self.light_card.pressEvent_signal.connect(self.show_light_dialog)
        self.touch_card.pressEvent_signal.connect(self.show_touch_dialog)
        self.screen_card.pressEvent_signal.connect(self.show_screen_dialog)

        self.flowLayout.addWidget(self.led_card)
        self.flowLayout.addWidget(self.keyboard_card)
        self.flowLayout.addWidget(self.rotary_potentiometer_card)
        self.flowLayout.addWidget(self.led_strip_card)
        self.flowLayout.addWidget(self.mp3_card)
        self.flowLayout.addWidget(self.ultrasonic_card)
        self.flowLayout.addWidget(self.buzzer_card)
        self.flowLayout.addWidget(self.light_card)
        self.flowLayout.addWidget(self.touch_card)
        self.flowLayout.addWidget(self.screen_card)
        self.flowLayout.addWidget(self.b_card)
        self.flowLayout.addWidget(self.c_card)
        self.flowLayout.addWidget(self.d_card)
        self.flowLayout.addWidget(self.e_card)
        self.flowLayout.addWidget(self.f_card)
        self.flowLayout.addWidget(self.g_card)

        self.view.setLayout(self.flowLayout)  # 设置视口的布局为FlowLayout
        self.setObjectName(text.replace(' ', '-'))
        with open(os.path.join(basedir, 'resource/qss/dark', "home_interface.qss")) as f:
            self.setStyleSheet(f.read())

    def show_led_example_dialog(self):
        self.ui1 = Ui_LedExample()
        start_cmd = {"name": "LED", "state": 1}
        serialController.send_data(json.dumps(start_cmd))
        self.led_dialog = QDialog(self)
        self.ui1.setupUi(self.led_dialog)
        self.led_dialog.closeEvent = self.led_example_dialog_close
        self.led_dialog.setWindowTitle("台灯实验")
        self.led_dialog.setWindowIcon(QIcon(os.path.join(basedir, 'resource', "logo.png")))
        self.led_dialog.exec_()

    def led_example_dialog_close(self, event):
        event.accept()  # 允许窗口关闭
        start_cmd = {"name": "LED", "state": 2}
        serialController.send_data(json.dumps(start_cmd))

    def show_key_board_dialog(self):
        start_cmd = {"name": "keyBoard", "state": 1}
        serialController.send_data(json.dumps(start_cmd))
        self.ui2 = Jisuanqi()
        self.ui2.show()

    def show_led_strip_dialog(self):
        self.ui3 = NineStripCore()
        start_cmd = {"name": "ninestrip", 'state': 1}
        serialController.send_data(json.dumps(start_cmd))
        self.led_strip_dialog = QDialog(self)
        self.ui3.setupUi(self.led_strip_dialog)
        self.ui3.initialize()
        self.led_strip_dialog.closeEvent = self.led_strip_dialog_close
        self.led_strip_dialog.setWindowTitle("灯板模拟井字棋实验")
        self.led_strip_dialog.setWindowIcon(QIcon(os.path.join(basedir, 'resource', "logo.png")))
        self.led_strip_dialog.exec_()

    def led_strip_dialog_close(self, event):
        event.accept()  # 允许窗口关闭
        start_cmd = {"name": "ninestrip", 'state': 2}
        serialController.send_data(json.dumps(start_cmd))

    def show_rotary_potentiometer_dialog(self):
        start_cmd = {"name": "analog", "state": 1}
        serialController.send_data(json.dumps(start_cmd))
        time.sleep(0.01)
        start_cmd = {"name": "switch", "state": 1}
        serialController.send_data(json.dumps(start_cmd))
        self.rotary_dialog = QDialog(self)
        self.rotary_dialog.closeEvent = self.rotary_dialog_close
        self.rotary = Ui_Car_Form()
        self.rotary.setupUi(self.rotary_dialog)
        self.rotary_dialog.setWindowTitle("选择电位器实验")
        self.rotary_dialog.setWindowIcon(QIcon(os.path.join(basedir, 'resource', "logo.png")))
        self.rotary_dialog.exec_()
        # 连接对话框的 closeEvent 信号到自定义槽函数

    def rotary_dialog_close(self, event):
        """处理旋转电位器对话框关闭事件"""
        if self.rotary.animation_timer:
            self.rotary.animation_timer.stop()  # 停止定时器
        event.accept()  # 允许窗口关闭
        start_cmd = {"name": "analog", "state": 2}       # 关闭主控电位器
        serialController.send_data(json.dumps(start_cmd))
        time.sleep(0.01)
        start_cmd = {"name": "switch", "state": 2}
        serialController.send_data(json.dumps(start_cmd))
        serialController.stop_listening()
    
    def show_mp3_dialog(self):
        start_cmd = {"name": "MP3", "state": 1}
        serialController.send_data(json.dumps(start_cmd))
        self.ui4 = MP3()
        self.ui4.show()

    def show_ultrasonic_dialog(self):
        start_cmd = {"name": "ultrasonic", "state": 1}
        serialController.send_data(json.dumps(start_cmd))
        self.ui5 = UltrasonicCore()
        self.ui5.show()

    def show_buzzer_dialog(self):
        self.ui6 = Buzzer_Form()
        start_cmd = {"name": "Buzzer", "state": 1}
        serialController.send_data(json.dumps(start_cmd))
        self.buzzer_dialog = QDialog(self)
        self.ui6.setupUi(self.buzzer_dialog)
        self.buzzer_dialog.setWindowTitle("电子琴实验")
        self.buzzer_dialog.setWindowIcon(QIcon(os.path.join(basedir, 'resource', "logo.png")))
        self.buzzer_dialog.closeEvent = self.buzzer_dialog_close
        self.buzzer_dialog.exec_()

    def buzzer_dialog_close(self, event):
        event.accept()
        start_cmd = {"name": "Buzzer", "state": 2}
        serialController.send_data(json.dumps(start_cmd))

    def show_light_dialog(self):
        start_cmd = {"name": "analog", "state": 1}
        serialController.send_data(json.dumps(start_cmd))
        self.ui7 = LightCore()
        self.ui7.show()

    def show_touch_dialog(self):
        start_cmd = {"name": "switch", "state": 1}
        serialController.send_data(json.dumps(start_cmd))
        self.ui8 = TouchCore()
        self.ui8.show()

    def show_screen_dialog(self):
        start_cmd = {"name": "screen", "state": 1}
        serialController.send_data(json.dumps(start_cmd))
        self.ui9 = ScreenCore()
        self.ui9.show()

