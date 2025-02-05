# -*- coding: utf-8 -*-
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from qfluentwidgets import TransparentPushButton
from Basedir import basedir
from ui.car_game import ResizableImageLabel


class Ui_MP3_Form(object):
    def setupUi(self, MP3_Form):
        MP3_Form.setObjectName("MP3_Form")
        MP3_Form.setFixedSize(640, 555)
        self.setWindowIcon(QIcon(os.path.join(basedir, 'resource', "logo.png")))
        self.mp3_background = ResizableImageLabel(MP3_Form)
        self.mp3_background.setImage(os.path.join(basedir, 'resource', "MP3_bg.png"))
        self.mp3_background.setGeometry(QtCore.QRect(0, 20, 640, 555))

        self.add_volume = TransparentPushButton(MP3_Form)
        self.add_volume.setGeometry(QtCore.QRect(276, 90, 100, 50))
        self.add_volume.setObjectName("add_volume")
        self.add_volume.setIcon(os.path.join(basedir, 'resource', "加音.png"))
        self.add_volume.setIconSize(QtCore.QSize(50, 50))

        self.reduce_volume = TransparentPushButton(MP3_Form)
        self.reduce_volume.setGeometry(QtCore.QRect(279, 420, 100, 50))
        self.reduce_volume.setObjectName("reduce_volume")
        self.reduce_volume.setIcon(os.path.join(basedir, 'resource', "减音.png"))
        self.reduce_volume.setIconSize(QtCore.QSize(50, 50))

        self.play_pause = TransparentPushButton(MP3_Form)
        self.play_pause.setGeometry(QtCore.QRect(295, 240, 80, 80))
        self.play_pause.setObjectName("play_pause")
        self.play_pause.setIcon(os.path.join(basedir, 'resource', "播放.png"))
        self.play_pause.setIconSize(QtCore.QSize(50, 50))

        self.next_song = TransparentPushButton(MP3_Form)
        self.next_song.setGeometry(QtCore.QRect(445, 250, 100, 50))
        self.next_song.setObjectName("next_song")
        self.next_song.setIcon(os.path.join(basedir, 'resource', "下一曲.png"))
        self.next_song.setIconSize(QtCore.QSize(70, 40))

        self.previous_song = TransparentPushButton(MP3_Form)
        self.previous_song.setGeometry(QtCore.QRect(100, 250, 100, 50))
        self.previous_song.setObjectName("previous_song")
        self.previous_song.setIcon(os.path.join(basedir, 'resource', "上一曲.png"))
        self.previous_song.setIconSize(QtCore.QSize(70, 40))

        self.retranslateUi(MP3_Form)
        QtCore.QMetaObject.connectSlotsByName(MP3_Form)

    def retranslateUi(self, MP3_Form):
        _translate = QtCore.QCoreApplication.translate
        MP3_Form.setWindowTitle(_translate("MP3_Form", "MP3音乐播放器实验"))
