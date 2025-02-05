from PyQt5.QtCore import Qt
from qfluentwidgets import (TabBar, qrouter, TextEdit)


class MyTabBar(TabBar):
    def __init__(self, parent):
        TabBar.__init__(self, parent)

    def removeTab(self, index: int):
        if not 0 <= index < len(self.items) or index == 0:
            # self.createCustomInfoBar()
            return

        # adjust current index
        if index < self.currentIndex():
            self._currentIndex -= 1
        elif index == self.currentIndex():
            if self.currentIndex() > 0:
                self.setCurrentIndex(self.currentIndex() - 1)
                self.currentChanged.emit(self.currentIndex())
            elif len(self.items) == 1:
                self._currentIndex = -1
            else:
                self.setCurrentIndex(1)
                self._currentIndex = 0
                self.currentChanged.emit(0)

        # remove tab
        item = self.items.pop(index)
        self.itemMap.pop(item.routeKey())
        self.hBoxLayout.removeWidget(item)
        qrouter.remove(item.routeKey())
        item.deleteLater()

        # remove shadow
        self.update()


class CustomTextEdit(TextEdit):
    def __init__(self, *args, **kwargs):
        super(CustomTextEdit, self).__init__(*args, **kwargs)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            # 插入四个空格代替制表符
            self.insertPlainText("    ")
        else:
            # 对于其他按键，调用默认处理
            super(CustomTextEdit, self).keyPressEvent(event)
