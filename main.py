from PyQt5.QtWidgets import QApplication, QDialog
from interfaces.receiver import Receiver
from interfaces.sender import Sender

import ui.receive_files
import ui.send_files
import ui.startup

import netifaces as ni
import threading
import platform
import sys


class StartUp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = ui.startup.Ui_Dialog()
        self.ui.setupUi(self)
        self.show()
        self.windows = list()
        self.ui.sendFiles.clicked.connect(self.open_send_files_ui)
        self.ui.receiveFiles.clicked.connect(self.open_receive_files_ui)

    def open_send_files_ui(self):
        self.setVisible(False)
        send_files_ui = SendFiles()
        self.windows.append(send_files_ui)
        send_files_ui.show()

    def open_receive_files_ui(self):
        self.setVisible(False)
        receive_files_ui = ReceiveFiles()
        self.windows.append(receive_files_ui)
        receive_files_ui.show()


class SendFiles(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = ui.send_files.Ui_Dialog()
        self.ui.setupUi(self)
        self.show()

        self.windows = list()
        self.ui.genIP.clicked.connect(self.generate_server_ip)
        self.ui.sendButton.clicked.connect(self.send_files)

    def generate_server_ip(self):
        ip = "127.0.0.1"
        if platform.system() == "Windows":
            for iface in ni.interfaces():
                iface_details = ni.ifaddresses(iface)
            if ni.AF_INET in iface_details:
                print(iface_details[ni.AF_INET])
                for ip_interfaces in iface_details[ni.AF_INET]:
                    for key, ip_add in ip_interfaces.items():
                        if key == 'addr' and ip_add != '127.0.0.1':
                            ip = ip_add
        else:
            ip = ni.ifaddresses("wlp2s0")[ni.AF_INET][0]["addr"]
        self.ui.ipLabel.setText(f"{ip}")

    def send_files(self):
        file_location = self.ui.lineEditFileLocation.text()
        ip = ni.ifaddresses("wlp2s0")[ni.AF_INET][0]["addr"]
        sender = Sender(ip, file_location)
        sender_thread = threading.Thread(target=sender.send_data, args=(self,))
        sender_thread.start()
        sender_thread.join()


class ReceiveFiles(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = ui.receive_files.Ui_Dialog()
        self.ui.setupUi(self)
        self.show()

        self.windows = list()
        self.ui.receiveButton.clicked.connect(self.receive_files)

    def receive_files(self):
        ip = self.ui.lineEditIP.text()
        save_location = self.ui.lineEditSavePath.text()
        receiver = Receiver(ip, save_location)
        receiver_thread = threading.Thread(target=receiver.fetch_data, args=(self,))
        receiver_thread.start()
        receiver_thread.join()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_up_ui = StartUp()
    start_up_ui.show()
    sys.exit(app.exec_())
