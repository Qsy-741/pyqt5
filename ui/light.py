# -*- coding: utf-8 -*-
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from Basedir import basedir
from ui.car_game import ResizableImageLabel


class Ui_light_Form(object):
    def setupUi(self, light_Form):
        light_Form.setObjectName("light_Form")
        light_Form.resize(640, 480)
        light_Form.setWindowIcon(QIcon(os.path.join(basedir, 'resource', "logo.png")))
        self.verticalLayout = QtWidgets.QVBoxLayout(light_Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ImageLabel = ResizableImageLabel(light_Form)
        self.ImageLabel.setMaximumSize(QtCore.QSize(9999, 9999))
        self.ImageLabel.setMinimumSize(640, 480)
        self.ImageLabel.setObjectName("ImageLabel")
        self.ImageLabel.setImage(os.path.join(basedir, 'resource', "off_light.png"))
        self.verticalLayout.addWidget(self.ImageLabel)

        self.retranslateUi(light_Form)
        QtCore.QMetaObject.connectSlotsByName(light_Form)

    def retranslateUi(self, light_Form):
        _translate = QtCore.QCoreApplication.translate
        light_Form.setWindowTitle(_translate("light_Form", "光敏开关试验"))
