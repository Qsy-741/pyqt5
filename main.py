# coding:utf-8
import logging
import os
import sys
import warnings
from Basedir import basedir
from FirmwareDownload import EsptoolThread

# 忽略所有 DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# 标准输入输出导致内存泄漏
# 创建一个日志记录器
logger = logging.getLogger('stdout_logger')
logger.setLevel(logging.INFO)

# 创建一个文件处理器，并指定日志文件路径
file_handler = logging.FileHandler(os.path.join(basedir, 'resource', "Log.log"))
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


# 重定向标准输出到 空
class LoggerWriter:
    def __init__(self, logger, level, enable=False):
        self.logger = logger
        self.level = level
        self.enable = enable

    def write(self, message):
        if self.enable:
            if message.strip():  # 仅处理非空和非空白字符的消息
                self.logger.log(self.level, message.strip())
        else:
            pass

    def flush(self):
        pass

original_stdout = sys.stdout  # 保存原始的标准输出
original_stderr = sys.stderr  # 保存原始的标准错误
try:
    sys.stdout = LoggerWriter(logger, logging.INFO)
    sys.stderr = LoggerWriter(logger, logging.ERROR)
except Exception as e:
    print(f"Error in redirecting standard output: {e}")
    pass

from PyQt5.QtCore import Qt, QUrl, QPoint, pyqtSlot
from PyQt5.QtGui import QIcon, QDesktopServices, QColor, QTextCursor
from PyQt5.QtWidgets import QHBoxLayout, QApplication, QFrame, QStackedWidget, QFileDialog, QVBoxLayout

from qfluentwidgets import (NavigationItemPosition, MessageBox, MSFluentTitleBar, MSFluentWindow,
                            TabBar, SubtitleLabel, setFont, TabCloseButtonDisplayMode, isDarkTheme,
                            Action, DropDownPushButton, RoundMenu, TransparentToolButton, setTheme, Theme, toggleTheme,
                            IconWidget)
from qfluentwidgets import FluentIcon as FIF
from ui.fram_main import Ui_Main
from CardView import Widget
from CoreControl import CoreControl
from SerialController import SerialController, serialController


class TabInterface(QFrame, Ui_Main):
    """ Tab interface """
    def __init__(self, text: str, icon, objectName, parent=None):
        super().__init__(parent=parent)
        # self.iconWidget = IconWidget(icon, self)
        # self.label = SubtitleLabel(text, self)
        # self.iconWidget.setFixedSize(120, 120)
        # self.vBoxLayout = QVBoxLayout(self)
        # self.vBoxLayout.setAlignment(Qt.AlignCenter)
        # self.vBoxLayout.setSpacing(30)
        # self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)
        # self.vBoxLayout.addWidget(self.label, 0, Qt.AlignCenter)
        # setFont(self.label, 24)
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self.ui.PushButton.clicked.connect(self.code_analysis)
        serialController.deBug_data_received.connect(self.append_output)
        self.setObjectName(objectName)

    def code_analysis(self):
        code = self.ui.CodeEdit.toPlainText()
        self.core = CoreControl(code)
        self.core.output_signal.connect(self.append_output)
        self.core.finished_signal.connect(self.on_core_finished)
        self.core.start()
        # print(text)

    def append_output(self, text):
        # self.ui.Code_stdio.moveCursor(QTextCursor.End)
        # self.ui.Code_stdio.insertPlainText(text)
        cursor = self.ui.Code_stdio.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.ui.Code_stdio.setTextCursor(cursor)
        self.ui.Code_stdio.ensureCursorVisible()

    def on_core_finished(self, return_code):
        self.ui.Code_stdio.append("")
        # 处理返回码
        print(f"Execution finished with return code: {return_code}")


class CustomTitleBar(MSFluentTitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)

        # 串口用变量
        self.ser = None
        self.selected_port = None
        self.ports = []

        # add buttons
        self.toolButtonLayout = QHBoxLayout()
        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        self.darkModeButton = TransparentToolButton(FIF.CONSTRACT, self)
        # self.searchButton = TransparentToolButton(FIF.SEARCH_MIRROR.icon(color=color), self)
        # self.forwardButton = TransparentToolButton(FIF.RIGHT_ARROW.icon(color=color), self)
        # self.backButton = TransparentToolButton(FIF.LEFT_ARROW.icon(color=color), self)
        self.menu = RoundMenu(parent=self)
        # self.menu.addAction(Action(FIF.BASKETBALL, 'Basketball'))
        # self.menu.addAction(Action(FIF.ALBUM, 'Sing'))
        # self.menu.addAction(Action(FIF.MUSIC, 'Music'))
        self.menu.addAction(Action(QIcon(os.path.join(basedir, "resource", "chuankou.svg")), '串口连接断开'))

        self.dropDownPushButton = DropDownPushButton(QIcon(os.path.join(basedir, "resource", "chuankou.svg")),
                                                     '串口连接断开')
        self.dropDownPushButton.setMenu(self.menu)

        self.dropDownPushButton.clicked.connect(self.scanf_serial)

        # self.forwardButton.setDisabled(True)
        self.toolButtonLayout.setContentsMargins(20, 0, 20, 0)
        self.toolButtonLayout.setSpacing(15)
        self.toolButtonLayout.addWidget(self.darkModeButton)
        # self.toolButtonLayout.addWidget(self.searchButton)
        # self.toolButtonLayout.addWidget(self.backButton)
        # self.toolButtonLayout.addWidget(self.forwardButton)
        self.toolButtonLayout.addWidget(self.dropDownPushButton)
        self.hBoxLayout.insertLayout(4, self.toolButtonLayout)
        self.menu.triggered.connect(self.menuItemSelected)
        self.darkModeButton.clicked.connect(self.darkSwitch)
        # add tab bar
        self.tabBar = TabBar(self)

        self.tabBar.setMovable(True)
        self.tabBar.setTabMaximumWidth(220)
        self.tabBar.setTabShadowEnabled(True)
        self.tabBar.setTabSelectedBackgroundColor(QColor(255, 255, 255, 125), QColor(255, 255, 255, 50))
        # self.tabBar.setScrollable(True)
        self.tabBar.addButton.hide()    # 屏蔽关闭按钮
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.NEVER)  # 屏蔽关闭按钮

        self.tabBar.tabCloseRequested.connect(self.tabBar.removeTab)
        self.tabBar.currentChanged.connect(lambda i: print(self.tabBar.tabText(i)))

        self.hBoxLayout.insertWidget(5, self.tabBar, 1)
        self.hBoxLayout.setStretch(6, 0)

        # add avatar
        # self.avatar = TransparentDropDownToolButton('resource/shoko.png', self)
        # self.avatar.setIconSize(QSize(26, 26))
        # self.avatar.setFixedHeight(30)
        # self.hBoxLayout.insertWidget(7, self.avatar, 0, Qt.AlignRight)
        # self.hBoxLayout.insertSpacing(8, 20)

    def darkSwitch(self):
        toggleTheme(True, True)

    def canDrag(self, pos: QPoint):
        if not super().canDrag(pos):
            return False

        pos.setX(pos.x() - self.tabBar.x())
        return not self.tabBar.tabRegion().contains(pos)

    def menuItemSelected(self, action):
        # 更新按钮文本
        self.dropDownPushButton.setText(action.text())
        if 'COM' in action.text():
            self.open_port()
        else:
            serialController.close_ser_port()

    def scanf_serial(self):
        self.menu.clear()
        self.ports = list(serialController.scanf_ser_port())
        for port in self.ports:
            if "CH" in port.description:
                # 将串口名添加到列表控件
                self.menu.addAction(Action(QIcon(os.path.join(basedir, "resource", "chuankou.svg")), port.description))
        self.menu.addAction(Action(QIcon(os.path.join(basedir, "resource", "chuankou.svg")), '串口连接断开'))

    def open_port(self):
        """打开指定串口"""
        serialController.close_ser_port()
        tmp = self.dropDownPushButton.text()
        for port in self.ports:
            if tmp == port.description:
                self.selected_port = port.device
                break
        if not serialController.open_ser_port(self.selected_port):
                self.dropDownPushButton.setText("串口访问被拒")


class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()
        self.esptool_thread = None
        self.headBar = CustomTitleBar(self)
        self.mainBody = None
        self.setTitleBar(self.headBar)
        self.tabBar = self.titleBar.tabBar  # type: TabBar

        # create sub interface
        self.homeInterface = QStackedWidget(self, objectName='homeInterface')
        # self.appInterface = Widget('Application Interface', self)
        # self.videoInterface = Widget('Video Interface', self)
        self.libraryInterface = Widget('library Interface', self)

        # self.libraryInterface.card.ui.led_example_signal.connect(CustomTitleBar.send_command)

        self.initNavigation()
        self.initWindow()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.updateFrameless()


    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页', FIF.HOME_FILL)
        # self.addSubInterface(self.appInterface, FIF.APPLICATION, '应用')
        # self.addSubInterface(self.videoInterface, FIF.VIDEO, '示例')

        # self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF,
        #                      '库', FIF.LIBRARY_FILL, NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF,
                             '模块实验', FIF.LIBRARY_FILL)
        self.navigationInterface.addItem(
            routeKey='firmware download',
            icon=FIF.DOWNLOAD,
            text='固件下载',
            onClick=self.downloadFirmware,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text='帮助',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(
            self.homeInterface.objectName())

        # add tab
        self.addTab('Heart', '首页', icon=os.path.join(basedir, "resource", "ip.png"))

        self.tabBar.currentChanged.connect(self.onTabChanged)
        self.tabBar.tabAddRequested.connect(self.onTabAddRequested)

    def initWindow(self):
        self.resize(1100, 750)
        self.setWindowIcon(QIcon(os.path.join(basedir, "resource", "logo.png")))
        self.setWindowTitle('Avatar-Code+')
        self.updateFrameless()
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def downloadFirmware(self):
        serialController.close_ser_port()
        fileDialog = QFileDialog()
        path = fileDialog.getOpenFileName(filter='*bin', initialFilter='*bin')
        print(path)
        print(self.headBar.selected_port)
        self.esptool_thread = EsptoolThread(self.headBar.selected_port, path[0])
        self.esptool_thread.output_updated.connect(self.updateDebugText)
        self.esptool_thread.finished.connect(self.downloadFinish)
        self.esptool_thread.start()

    def updateDebugText(self, output):
        self.mainBody.append_output(output)

    def downloadFinish(self):
        if not serialController.open_ser_port(self.headBar.selected_port):
            self.headBar.dropDownPushButton.setText("串口访问被拒")

    def showMessageBox(self):
        w = MessageBox(
            '支持作者🥰',
            '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水🥤。您的支持就是作者开发和维护项目的动力🚀',
            self
        )
        w.yesButton.setText('来啦老弟')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://www.baidu.com/s?wd=%E6%94%AF%E4%BB%98%E5%AE%9D"))

    def onTabChanged(self, index: int):
        objectName = self.tabBar.currentTab().routeKey()
        self.homeInterface.setCurrentWidget(self.findChild(TabInterface, objectName))
        self.stackedWidget.setCurrentWidget(self.homeInterface)
        pass

    def onTabAddRequested(self):
        text = f'编程页×{self.tabBar.count()}'
        self.addTab(text, text, os.path.join(basedir, "resource", "logo.png"))

    def addTab(self, routeKey, text, icon):
        self.tabBar.addTab(routeKey, text, icon)
        self.mainBody = TabInterface(text, icon, routeKey, self)
        self.homeInterface.addWidget(self.mainBody)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # setTheme(Theme.DARK)
    app = QApplication(sys.argv)
    sys.stderr.enable = True
    sys.stdout.enable = True
    w = Window()
    w.setWindowFlag(Qt.FramelessWindowHint)
    w.setMicaEffectEnabled(False)
    # setTheme(Theme.LIGHT)
    w.updateFrameless()
    w.show()
    app.exec_()
