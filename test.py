import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('井字棋')
        self.setGeometry(100, 100, 300, 300)

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # 创建横线
        self.horizontal_line1 = QFrame()
        self.horizontal_line1.setFrameShape(QFrame.HLine)
        self.horizontal_line1.setFrameShadow(QFrame.Sunken)
        self.grid_layout.addWidget(self.horizontal_line1, 1, 0, 1, 3)

        self.horizontal_line2 = QFrame()
        self.horizontal_line2.setFrameShape(QFrame.HLine)
        self.horizontal_line2.setFrameShadow(QFrame.Sunken)
        self.grid_layout.addWidget(self.horizontal_line2, 2, 0, 1, 3)

        # 创建竖线
        self.vertical_line1 = QFrame()
        self.vertical_line1.setFrameShape(QFrame.VLine)
        self.vertical_line1.setFrameShadow(QFrame.Sunken)
        self.grid_layout.addWidget(self.vertical_line1, 0, 1, 3, 1)

        self.vertical_line2 = QFrame()
        self.vertical_line2.setFrameShape(QFrame.VLine)
        self.vertical_line2.setFrameShadow(QFrame.Sunken)
        self.grid_layout.addWidget(self.vertical_line2, 0, 2, 3, 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ttt = TicTacToe()
    ttt.show()
    sys.exit(app.exec_())