import json
from functools import partial

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidgetItem, QWidget
from SerialController import serialController
from ui.jisuanqi import Ui_Form3


class Jisuanqi(QWidget, Ui_Form3):
    def __init__(self):
        super().__init__()
        self.expression = ""
        self.num_list = []
        self.history_list = []
        serialController.start_listening()
        serialController.keyboard_data_received.connect(self.analyze_data)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

        self.PushButton_0.clicked.connect(partial(self.add_num, 0))
        self.PushButton_1.clicked.connect(partial(self.add_num, 1))
        self.PushButton_2.clicked.connect(partial(self.add_num, 2))
        self.PushButton_3.clicked.connect(partial(self.add_num, 3))
        self.PushButton_4.clicked.connect(partial(self.add_num, 4))
        self.PushButton_5.clicked.connect(partial(self.add_num, 5))
        self.PushButton_6.clicked.connect(partial(self.add_num, 6))
        self.PushButton_7.clicked.connect(partial(self.add_num, 7))
        self.PushButton_8.clicked.connect(partial(self.add_num, 8))
        self.PushButton_9.clicked.connect(partial(self.add_num, 9))
        self.PushButton_dec.clicked.connect(partial(self.add_num, '.'))
        self.PushButton_add.clicked.connect(partial(self.add_symbol, '+'))
        self.PushButton_sub.clicked.connect(partial(self.add_symbol, '-'))
        self.PushButton_multi.clicked.connect(partial(self.add_symbol, '×'))
        self.PushButton_divi.clicked.connect(partial(self.add_symbol, '÷'))
        self.PushButton_back.clicked.connect(self.back_num)
        self.PrimaryPushButton.clicked.connect(self.sum_result)
        self.PushButton_AC.clicked.connect(self.clear_body)

    def add_num(self, arg):
        _translate = QCoreApplication.translate
        tmp = self.BodyLabel.text()
        if '=' in tmp:
            item = QListWidgetItem()
            item.setTextAlignment(Qt.AlignTrailing | Qt.AlignBottom)
            font = QFont()
            font.setPointSize(20)
            item.setFont(font)
            item.setText(_translate("history", tmp))
            self.ListWidget.addItem(item)
            self.ListWidget.scrollToBottom()
            self.BodyLabel.setText(str(arg))
        elif tmp == '0':  # 开始阶段 框显示 0
            if arg == '.':
                tmp = tmp + str(arg)
                self.BodyLabel.setText(tmp)
            else:
                self.BodyLabel.setText(str(arg))
        elif tmp[-1] in ['+', '-', 'x', '÷', '.'] and arg == '.':
            print(tmp[-1])
            return
        else:  # 有了数字之后 框里追加数字
            if arg == '.' and '.' in tmp:  # 判断小数点，小数点只能加一次
                try:
                    next_num = float(tmp.replace(self.expression, ""))
                    tmp = tmp + str(arg)
                    next_num = float(tmp.replace(self.expression, ""))
                    tmp = tmp[:-1]
                except Exception as e:
                    print(e)
                    return
            tmp = tmp + str(arg)
            self.BodyLabel.setText(tmp)

    def back_num(self):
        context = self.BodyLabel.text()
        if len(context) == 1:
            self.BodyLabel.setText('0')
            return
        if context != "0" and context != "":
            if context[-1] in ['+', '-', 'x', '÷']:
                try:
                    self.num_list.pop()
                except Exception as e:
                    self.num_list.clear()
                    print(e)
            context = context[:-1]
            self.BodyLabel.setText(context)

    def clear_body(self):
        self.BodyLabel.setText('0')

    def add_symbol(self, arg):
        tmp = self.BodyLabel.text()
        if '=' in tmp:
            self.add_history()
            index = tmp.find('=')
            self.BodyLabel.setText(tmp[index+1:]+str(arg))
            self.expression = tmp[index+1:] + str(arg)
            self.num_list.clear()
            self.num_list.append(float(tmp[index+1:]))
            print("expression:", tmp)
            return 0
        if tmp[-1] == '.':  # 输入框最后一位是 . 表示还没有输入完，不能添加符号
            return 0
        if tmp[-1] in ['+', '-', '×', '÷']:
            tmp = list(tmp)
            tmp[-1] = arg
            tmp = "".join(tmp)
            self.BodyLabel.setText(tmp)
            return 0
        elif not self.num_list:     # 添加首个数字
            self.num_list.append(float(tmp))
            tmp = tmp + str(arg)
            self.BodyLabel.setText(tmp)
        else:                               # 添加第二个数字同时计算出结果
            self.calculation()
            tmp = tmp + str(arg)
            self.BodyLabel.setText(tmp)
        self.expression = tmp               # 记住当前的表达式的样子，待会儿用于去除
        print("expression:", tmp)

    def calculation(self):
        result = 0
        tmp = self.BodyLabel.text()
        next_num = float(tmp.replace(self.expression, ""))
        if self.expression[-1] in ['+', '-', '×', '÷']:
            if self.expression[-1] == '+':
                result = self.num_list[0] + next_num
            elif self.expression[-1] == '-':
                result = self.num_list[0] - next_num
            elif self.expression[-1] == '×':
                result = self.num_list[0] * next_num
            elif self.expression[-1] == '÷':
                result = self.num_list[0] / next_num
            self.num_list[0] = result
            print(result)
            return result
        else:
            return -1

    def sum_result(self):
        tmp = self.BodyLabel.text()
        if tmp == "" or self.expression == "" or self.num_list == [] or tmp.replace(self.expression, "") == "":
            return
        result = self.calculation()
        tmp = tmp + "=" + str(result)
        self.BodyLabel.setText(tmp)
        self.history_list.append(tmp)
        self.num_list.clear()
        # tmp = tmp[:-1]
        # self.num_list = self.num_list.append(float(tmp))
        # print(self.num_list)

    def add_history(self):
        context = self.BodyLabel.text()
        _translate = QCoreApplication.translate
        item = QListWidgetItem()
        item.setTextAlignment(Qt.AlignTrailing | Qt.AlignBottom)
        font = QFont()
        font.setPointSize(20)
        item.setFont(font)
        item.setText(_translate("history", context))
        self.ListWidget.addItem(item)
        self.ListWidget.scrollToBottom()

    def analyze_data(self, data):
        key = data['data']['key']
        key = chr(int(key))
        if key in ['1','2','3','4','5','6','7','8','9','0','*']:
            self.add_num(key)
        elif key in ['A', 'B', 'C', 'D', '#']:
            if key == 'A':
                self.add_symbol('÷')
            elif key == 'B':
                self.add_symbol('×')
            elif key == 'C':
                self.add_symbol('-')
            elif key == 'D':
                self.add_symbol('+')
            elif key == '#':
                self.back_num()

    def closeEvent(self, event):
        start_cmd = {"name": "keyBoard", "state": 2}
        serialController.send_data(json.dumps(start_cmd))
        serialController.stop_listening()
        super().closeEvent(event)

