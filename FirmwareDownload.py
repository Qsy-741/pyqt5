import io
import sys

import esptool
from PyQt5.QtCore import QThread, pyqtSignal


class EmittingStringIO(io.StringIO):
    def __init__(self, signal):
        super().__init__()
        self.signal = signal

    def write(self, s):
        super().write(s)
        self.signal.emit(s)


class EsptoolThread(QThread):
    output_updated = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, port, ol_path):
        super().__init__()
        self.port = port
        self.ol_path = ol_path

    def run(self):
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = EmittingStringIO(self.output_updated)
        sys.stderr = EmittingStringIO(self.output_updated)
        try:
            print(f"Starting esptool with port: {self.port} and ol_path: {self.ol_path}")
            # logging.info(f"Starting esptool with port: {self.port} and ol_path: {self.ol_path}")
            esptool.main(['--chip', 'auto', '--port', self.port, '--baud', '115200', '--before', 'default_reset', '--after', 'hard_reset', 'write_flash', '-z', '--flash_mode', 'dio', '--flash_freq', '40m', '--flash_size', '4MB', '0x0', self.ol_path])
        except Exception as e:
            # logging.error(f"Error running esptool: {e}")
            print(e)
        finally:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        self.finished.emit()

