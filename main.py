from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
from interfaces.receiver import Receiver
from interfaces.sender import Sender
from quamash import QEventLoop

import ui.receive_files
import ui.send_files
import ui.startup

import netifaces as ni
import platform
import asyncio
import sys


async def send_files(sender, self):
    sender.send_data(self)

    if sender.get_sent():
        message = QMessageBox()
        message.information(self, "Information", "Transfer complete")
        message.show()

    sender.set_sent(False)
    self.ui.sendButton.setEnabled(True)
    self.ui.labelProgress.setVisible(False)
    self.ui.progressBar.setVisible(False)

    def stopper(lp):
        lp.stop()


async def receive_files(receiver, self):
    receiver.fetch_data(self)

    if receiver.get_received():
        message = QMessageBox()
        message.information(self, "Information", "Download complete")
        message.show()

    receiver.set_received(False)

    self.ui.receiveButton.setEnabled(True)
    self.ui.label_4.setVisible(False)
    self.ui.progressBar.setVisible(False)

    def stopper(lp):
        lp.stop()


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
        self.ui.labelProgress.setVisible(False)
        self.ui.progressBar.setVisible(False)

        self.ui.genIP.clicked.connect(self.generate_server_ip)
        self.ui.sendButton.clicked.connect(self.send_files)
        self.ui.toolButton.clicked.connect(self.open_file_dialog)

        self.show()

    def open_file_dialog(self):
        if platform.system() == "Windows":
            file_explorer = QFileDialog.getOpenFileName(self, "Open File", "c:\\")
        else:
            file_explorer = QFileDialog.getOpenFileName(self, "Open File", "/home")
        self.ui.lineEditFileLocation.setText(file_explorer[0])

    def generate_server_ip(self):
        ip = self.get_ip()
        self.ui.ipLabel.setText(f"{ip}")

    def get_ip(self):
        if platform.system() == "Windows":
            for iface in ni.interfaces():
                iface_details = ni.ifaddresses(iface)
                if ni.AF_INET in iface_details:
                    print(iface_details[ni.AF_INET])
                    for ip_interfaces in iface_details[ni.AF_INET]:
                        for key, ip_add in ip_interfaces.items():
                            if key == 'addr' and ip_add != '127.0.0.1':
                                return ip_add
        return ni.ifaddresses("wlp2s0")[ni.AF_INET][0]["addr"]

    def send_files(self):
        self.ui.sendButton.setEnabled(False)
        self.ui.progressBar.setVisible(True)
        self.ui.labelProgress.setVisible(True)
        file_location = self.ui.lineEditFileLocation.text()
        ip = self.get_ip()

        sender = Sender(ip, file_location)
        asyncio.ensure_future(send_files(sender, self))


class ReceiveFiles(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = ui.receive_files.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.label_4.setVisible(False)
        self.ui.progressBar.setVisible(False)

        self.ui.receiveButton.clicked.connect(self.receive_files)
        self.ui.toolButton.clicked.connect(self.open_file_dialog)

        self.show()

    def open_file_dialog(self):
        if platform.system() == "Windows":
            file_viewer = QFileDialog.getExistingDirectory(self, "Open folder to save", "c:\\")
        else:
            file_viewer = QFileDialog.getExistingDirectory(self, "Open folder to save", "/home")
        self.ui.lineEditSavePath.setText(file_viewer)

    def receive_files(self):
        self.ui.receiveButton.setEnabled(False)
        self.ui.label_4.setVisible(True)
        self.ui.progressBar.setVisible(True)
        ip = self.ui.lineEditIP.text()
        save_location = self.ui.lineEditSavePath.text()

        receiver = Receiver(ip, save_location)
        asyncio.ensure_future(receive_files(receiver, self))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    start_up_ui = StartUp()
    start_up_ui.exec()
    with loop:
        loop.run_forever()
        loop.close()
    sys.exit(app.exec_())
