import json
import threading
import time

import serial
import serial.tools.list_ports
from PyQt5.QtCore import pyqtSignal, QObject


class SerialController(QObject):
    # 定义一个信号，它将携带接收到的数据
    data_received = pyqtSignal(dict)
    keyboard_data_received = pyqtSignal(dict)
    rotary_data_received = pyqtSignal(dict)
    deBug_data_received = pyqtSignal(str)
    switch_data_received = pyqtSignal(bool)
    ultrasonic_data_received = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.ser = None
        self.listening_thread = None
        self.stop_listening_flag = False  # 控制监听线程的标志

    def scanf_ser_port(self):
        return serial.tools.list_ports.comports()

    def open_ser_port(self, selected_port):
        # self.close_ser_port()
        try:
            self.ser = serial.Serial(selected_port, 115200)
            self.ser.timeout = 0  # 设置为非阻塞模式
            self.ser.write(b"connect ok")
            self.ser.flush()  # 确保所有数据都被发送出去
            return True
        except serial.SerialException as e:
            print(e)
            return False

    def close_ser_port(self):
        if self.ser:
            self.ser.close()

    def send_data(self, command):
        # command = str(command).strip()  # 确保命令是字符串，并移除两端的空白字符
        try:
            self.ser.write(command.encode())  # 将命令转换为字节，并通过串行端口发送
            self.ser.flush()  # 确保所有数据都被发送出去
            print(command.encode())
        except Exception as e:
            print(e)

    def start_listening(self):
        self.stop_listening_flag = False  # 重置停止标志
        self.listening_thread = threading.Thread(target=self.listen_for_data)
        self.listening_thread.start()

    def listen_for_data(self):
        buffer = ""
        decoder = json.JSONDecoder()
        try:
            while self.ser.is_open and not self.stop_listening_flag:
                if self.ser.in_waiting > 0:  # 检查是否有数据可读
                    try:
                        # 读取数据
                        data = self.ser.read(self.ser.in_waiting).decode()
                        buffer += data
                        # 尝试解析缓冲区中的 JSON 对象
                        while buffer:
                            try:
                                obj, index = decoder.raw_decode(buffer)
                                print("RX:", obj)
                                if obj['name'] == "keyBoard":
                                    self.keyboard_data_received.emit(obj)
                                elif obj['name'] == "debug":
                                    self.deBug_data_received.emit(obj['data'])
                                elif obj['name'] == "analog":
                                    self.rotary_data_received.emit(obj)
                                elif obj['name'] == "switch":
                                    self.switch_data_received.emit(obj['data'])
                                elif obj['name'] == "ultrasonic":
                                    self.ultrasonic_data_received.emit(obj)

                                # 处理解析后的 JSON 数据
                                self.data_received.emit(obj)
                                # 移除已解析的部分
                                buffer = buffer[index:].lstrip()
                                break
                            except json.JSONDecodeError:
                                # 如果解析失败，说明数据可能不完整，跳出循环继续读取
                                break
                    except serial.SerialException as e:
                        print("没有串口打开")
                        print(e)
                        break
                else:
                    time.sleep(0.01)  # 避免 CPU 占用过高
        except Exception as e:
            print("串口外圈try")
            print(e)
        finally:
            print("结束串口接收")
            self.listening_thread = None

    def stop_listening(self):
        self.stop_listening_flag = True  # 设置停止标志
        if self.listening_thread:
            self.listening_thread.join()  # 等待线程结束
            self.listening_thread = None  # 线程结束后清空


serialController = SerialController()
