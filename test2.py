# coding: utf-8
from typing import List, Union
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt, QRectF, pyqtSignal, QPoint, QTimer, QEvent, QAbstractItemModel, pyqtProperty
from PyQt5.QtGui import QPainter, QPainterPath, QIcon, QCursor, QTextCursor
from PyQt5.QtWidgets import (QApplication, QAction, QHBoxLayout, QLineEdit, QToolButton, QTextEdit,
                             QPlainTextEdit, QCompleter, QStyle, QWidget)
from qfluentwidgets import FluentIconBase, FluentStyleSheet, isDarkTheme, drawIcon, setFont, FluentIcon as FIF, \
    LineEditMenu, themeColor, RoundMenu, IndicatorMenuItemDelegate, MenuAnimationType, SmoothScrollDelegate
from qfluentwidgets.components.widgets.menu import TextEditMenu
import warnings

# Ignore DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)


class EditLayer(QWidget):
    """ Edit layer """

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        parent.installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.parent() and e.type() == QEvent.Resize:
            self.resize(e.size())

        return super().eventFilter(obj, e)

    def paintEvent(self, e):
        if not self.parent().hasFocus():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        m = self.contentsMargins()
        path = QPainterPath()
        w, h = self.width() - m.left() - m.right(), self.height()
        path.addRoundedRect(QRectF(m.left(), h - 10, w, 10), 5, 5)

        rectPath = QPainterPath()
        rectPath.addRect(m.left(), h - 10, w, 7.5)
        path = path.subtracted(rectPath)

        painter.fillPath(path, themeColor())


class TextEdit(QTextEdit):
    """ Text edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._completerMenu = None
        self._completer = None
        self.showTip = False
        self.space_bit = " "
        self.layer = EditLayer(self)
        self.scrollDelegate = SmoothScrollDelegate(self)
        FluentStyleSheet.LINE_EDIT.apply(self)
        setFont(self)

        self.textChanged.connect(self.__onTextEdited)

    def contextMenuEvent(self, e):
        menu = TextEditMenu(self)
        menu.exec_(e.globalPos())

    def setCompleter(self, completer: QCompleter):
        self._completer = completer

    def completer(self):
        return self._completer

    def keyPressEvent(self, event):
        if self.showTip:
            # 如果不允许，则拦截上下键事件
            if event.key() in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Return):
                return
        # 调用基类的keyPressEvent方法处理其他按键
        super().keyPressEvent(event)

    def __onTextEdited(self):
        if not self.completer():
            return
        cursor = self.textCursor()
        # 获取光标位置
        position = cursor.position()
        temp_cursor = QTextCursor(cursor.document())
        temp_cursor.setPosition(position - 2)
        temp_cursor.setPosition(position, QTextCursor.KeepAnchor)
        tmp = temp_cursor.selectedText()
        self.space_bit = " "
        if(len(tmp) > 1):
            self.text_before_cursor = tmp[1]
            self.space_bit = tmp[0]
        else:
            self.text_before_cursor = tmp
        # if " " == self.text_before_cursor[0]:
        #     return
        print(f"光标前的1个字符是：{self.text_before_cursor}")
        if self.text_before_cursor:
            QTimer.singleShot(50, self._showCompleterMenu)
        if self._completerMenu:
            self._completerMenu.close()

    def setCompleterMenu(self, menu):
        """ set completer menu

        Parameters
        ----------
        menu: CompleterMenu
            completer menu
        """
        menu.activated.connect(self._completer.activated)
        menu.statu.connect(self.update_showTip_flag)
        self._completerMenu = menu

    def update_showTip_flag(self):
        self.showTip = False

    def _showCompleterMenu(self):
        if not self.completer() or not self.text_before_cursor or not (self.space_bit == " "):
            return

        # create menu
        if not self._completerMenu:
            self.setCompleterMenu(CompleterMenu(self))
        # add menu items
        self.completer().setCompletionPrefix(self.text_before_cursor)
        changed = self._completerMenu.setCompletion(self.completer().completionModel())
        self._completerMenu.setMaxVisibleItems(self.completer().maxVisibleItems())

        # show menu
        if changed:
            self.showTip = True
            self._completerMenu.popup()

    def paintEvent(self, e):
        super().paintEvent(e)
        if not self.hasFocus():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        m = self.contentsMargins()
        path = QPainterPath()
        w, h = self.width() - m.left() - m.right(), self.height()
        path.addRoundedRect(QRectF(m.left(), h - 10, w, 10), 5, 5)

        rectPath = QPainterPath()
        rectPath.addRect(m.left(), h - 10, w, 8)
        path = path.subtracted(rectPath)

        painter.fillPath(path, themeColor())


class CompleterMenu(RoundMenu):
    """ Completer menu """

    activated = pyqtSignal(str)
    statu = pyqtSignal(str)

    def __init__(self, textEdit: TextEdit):
        super().__init__()
        self.items = []
        self.lineEdit = textEdit

        self.view.setViewportMargins(0, 2, 0, 6)
        self.view.setObjectName('completerListWidget')
        self.view.setItemDelegate(IndicatorMenuItemDelegate())
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.installEventFilter(self)
        self.setItemHeight(33)

    def setCompletion(self, model: QAbstractItemModel):
        """ set the completion model """
        items = []
        for i in range(model.rowCount()):
            for j in range(model.columnCount()):
                items.append(model.data(model.index(i, j)))

        if self.items == items and self.isVisible():
            return False

        self.setItems(items)
        return True

    def setItems(self, items: List[str]):
        """ set completion items """
        self.view.clear()

        self.items = items
        self.view.addItems(items)

        for i in range(self.view.count()):
            item = self.view.item(i)
            item.setSizeHint(QSize(1, self.itemHeight))

    def _onItemClicked(self, item):
        self._hideMenu(False)
        self.__onItemSelected(item.text())

    def eventFilter(self, obj, e: QEvent):
        if e.type() != QEvent.KeyPress:
            return super().eventFilter(obj, e)

        # redirect input to line edit
        self.lineEdit.event(e)
        self.view.event(e)

        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() in [Qt.Key_Enter, Qt.Key_Return] and self.view.currentRow() >= 0:
            self.__onItemSelected(self.view.currentItem().text())
            self.close()

        return super().eventFilter(obj, e)

    def __onItemSelected(self, text):
        # current_text = self.lineEdit.toPlainText()
        # self.lineEdit.setText(current_text + text[1:])
        self.lineEdit.insertPlainText(text[1:])
        self.activated.emit(text)

    def popup(self):
        """ show menu """
        if not self.items:
            return self.close()
        # adjust menu size
        p = self.lineEdit
        # 获取光标矩形
        cursor_rect = p.cursorRect()
        # 这里我们使用光标矩形的中心点作为x坐标，底部作为y坐标
        x = cursor_rect.center().x()
        y = cursor_rect.bottom()

        # 如果self.view的宽度小于p的宽度，则设置最小宽度
        if self.view.width() < p.width():
            self.view.setMinimumWidth(p.width())
            self.adjustSize()

        # 你可以根据需要计算self.view的高度，这里假设heightForAnimation是一个自定义方法
        # 用于计算动画时self.view的高度
        pd = p.mapToGlobal(QPoint(x - 25, y))
        hd = self.view.heightForAnimation(pd, MenuAnimationType.FADE_IN_DROP_DOWN)

        pu = p.mapToGlobal(QPoint(x, y - 7))  # 减去7像素，使菜单稍微向上移动
        hu = self.view.heightForAnimation(pu, MenuAnimationType.FADE_IN_PULL_UP)

        if hd >= hu:
            pos = pd
            aniType = MenuAnimationType.FADE_IN_DROP_DOWN
        else:
            pos = pu
            aniType = MenuAnimationType.FADE_IN_PULL_UP

        self.view.adjustSize(pos, aniType)

        # update border style
        self.view.setProperty('dropDown', aniType == MenuAnimationType.FADE_IN_DROP_DOWN)
        self.view.setStyle(QApplication.style())
        self.view.update()

        self.adjustSize()
        self.exec(pos, aniType=aniType)

        # remove the focus of menu
        self.view.setFocusPolicy(Qt.NoFocus)
        self.setFocusPolicy(Qt.NoFocus)
        p.setFocus()

    def closeEvent(self, e):
        self.statu.emit("关闭")


# coding:utf-8
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.hBoxLayout = QHBoxLayout(self)
        self.lineEdit = TextEdit(self)

        # add completer
        stands = [
            "and", "as", "assert", "break", "class", "continue", "def",
            "del", "elif", "else", "except", "False", "finally", "for",
            "from", "global", "if", "import", "in", "is", "lambda",
            "None", "nonlocal", "not", "or", "pass", "raise", "return",
            "True", "try", "while", "with", "yield"
        ]
        self.completer = QCompleter(stands, self.lineEdit)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setMaxVisibleItems(10)
        self.lineEdit.setCompleter(self.completer)

        self.resize(400, 400)
        self.hBoxLayout.addWidget(self.lineEdit, 0, Qt.AlignCenter)


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()


