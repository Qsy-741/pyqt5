# -*- coding: utf-8 -*-
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from Basedir import basedir
from ui.car_game import ResizableImageLabel


class Ui_touch_Form(object):
    def setupUi(self, touch_Form):
        touch_Form.setObjectName("touch_Form")
        touch_Form.setFixedSize(500, 450)
        touch_Form.setWindowIcon(QIcon(os.path.join(basedir, 'resource', "logo.png")))
        self.verticalLayout = QtWidgets.QVBoxLayout(touch_Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ImageLabel = ResizableImageLabel(touch_Form)
        self.ImageLabel.setMaximumSize(QtCore.QSize(9999, 9999))
        self.ImageLabel.setMinimumSize(450, 300)
        self.ImageLabel.setMaximumSize(500, 440)
        self.ImageLabel.setImage(os.path.join(basedir, 'resource', "门铃.png"))
        self.ImageLabel.setObjectName("ImageLabel")
        self.verticalLayout.addWidget(self.ImageLabel, alignment=Qt.AlignHCenter)

        self.retranslateUi(touch_Form)
        QtCore.QMetaObject.connectSlotsByName(touch_Form)

    def retranslateUi(self, touch_Form):
        _translate = QtCore.QCoreApplication.translate
        touch_Form.setWindowTitle(_translate("touch_Form", "电子门铃实验"))
