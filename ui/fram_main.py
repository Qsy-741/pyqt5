# -*- coding: utf-8 -*-
import os
import sys

# Form implementation generated from reading ui file 'fram_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

from Basedir import basedir
from PythonHighlighter import PythonHighlighter
from MyWidgets import CustomTextEdit


class FramelessWebEngineView(QWebEngineView):
    """ Frameless web engine view """

    def __init__(self, parent):
        # if sys.platform == "win32" and isinstance(parent.window(), AcrylicWindow):
        parent.window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            # pass

        super().__init__(parent=parent)
        # # self.setHtml("")
        #
        # # if isinstance(self.window(), FramelessWindow):
        self.window().updateFrameless()


class Ui_Main(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(1246, 960)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.SingleDirectionScrollArea = SingleDirectionScrollArea(Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SingleDirectionScrollArea.sizePolicy().hasHeightForWidth())
        self.SingleDirectionScrollArea.setSizePolicy(sizePolicy)
        self.SingleDirectionScrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.SingleDirectionScrollArea.setWidgetResizable(True)
        self.SingleDirectionScrollArea.setObjectName("SingleDirectionScrollArea")
        with open(os.path.join(basedir, 'resource/qss/dark', "home_interface.qss")) as f:
            self.SingleDirectionScrollArea.setStyleSheet(f.read())
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 813, 1527))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setStyleSheet("background: transparent;")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        # self.webView = QWebEngineView(Frame)
        # self.webView = FramelessWebEngineView(Frame)
        # self.Path = QUrl("index.html")
        # self.Path.setUrl("file:///C:/Users/Admin/PycharmProjects/PYQT5_Project/resource/index.html")
        # self.webView.setUrl(QUrl("https://www.bing.com/?mkt=zh-CN&mkt=zh-CN"))
        self.BodyLabel = BodyLabel(self.scrollAreaWidgetContents)
        self.BodyLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.BodyLabel.setTextFormat(QtCore.Qt.RichText)
        # self.BodyLabel.setTextFormat(QtCore.Qt.MarkdownText)
        self.BodyLabel.setScaledContents(True)
        self.BodyLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.BodyLabel.setWordWrap(True)
        self.BodyLabel.setObjectName("BodyLabel")
        self.BodyLabel.setContentsMargins(5, 10, 10, 12)
        self.verticalLayout.addWidget(self.BodyLabel)
        # self.verticalLayout.addWidget(self.webView)
        self.SingleDirectionScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.SingleDirectionScrollArea)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.TitleLabel = TitleLabel(Frame)
        self.TitleLabel.setObjectName("TitleLabel")
        self.verticalLayout_2.addWidget(self.TitleLabel)
        self.CodeEdit = CustomTextEdit(Frame)
        self.CodeEdit.setMinimumSize(QtCore.QSize(0, 250))
        self.CodeEdit.setObjectName("CodeEdit")
        self.CodeEdit.setAcceptRichText(False)
        self.verticalLayout_2.addWidget(self.CodeEdit)
        self.PushButton = PushButton(Frame)
        self.PushButton.setObjectName("PushButton")
        self.verticalLayout_2.addWidget(self.PushButton)
        self.Code_stdio = CustomTextEdit(Frame)
        self.Code_stdio.setMinimumSize(QtCore.QSize(0, 150))
        self.Code_stdio.setMaximumHeight(300)
        self.Code_stdio.setAcceptRichText(False)
        self.Code_stdio.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.Code_stdio.setObjectName("Code_stdio")
        self.verticalLayout_2.addWidget(self.Code_stdio)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)

        self.CodeEdit.setPlaceholderText("# 代码编辑区域")
        self.Code_stdio.setPlaceholderText("# 代码输出区域")
        self.highlighter = PythonHighlighter(self.CodeEdit.document())

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.TitleLabel.setText(_translate("Frame", "Python 代码编辑"))
        self.PushButton.setText(_translate("Frame", "运行"))
        self.BodyLabel.setText(_translate("Frame", self.loadMarkdown(os.path.join(basedir, 'resource', "首页.html"))))

    def loadMarkdown(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                markdown_text = file.read()
                return markdown_text
        except UnicodeDecodeError as e:
            print(f"Error reading file {file_path}: {e}")

from qfluentwidgets import BodyLabel, PushButton, SingleDirectionScrollArea, TitleLabel
