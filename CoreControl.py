import subprocess

from PyQt5.QtCore import pyqtSignal, QThread


class CoreControl(QThread):

    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)  # 新增一个信号来传递返回码

    def __init__(self, code):
        super(CoreControl, self).__init__()
        self.code = code

    def run(self):
        process = subprocess.Popen(
            ['python', '-c', self.code],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True,
            encoding='utf-8'  # 显式指定编码
        )
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.output_signal.emit(output)
        rc = process.poll()
        self.finished_signal.emit(rc)  # 发送进程的返回码

