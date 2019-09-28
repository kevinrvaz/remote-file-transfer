from PyQt5.QtWidgets import QMessageBox
from interfaces.client import Client

import socket
import os


class Receiver(Client):
    def __init__(self, ip, save_file_path):
        super().__init__(ip, save_file_path)

    def get_file_name(self):
        _, file_name = os.path.split(self.save_file_location)
        return file_name

    def fetch_data(self, ui_element):

        IP = ui_element.ui.lineEditIP.text()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, self.get_port()))

        header = client.recv(200)
        size, file_name = header.split()
        size = int(size)
        file_name = file_name.decode("utf-8")
        save_location = os.path.join(self.save_file_location, file_name)

        transferred_file_bytes = []
        received_data = 0
        while True:
            server_data = client.recv(4096)
            received_data += len(server_data)
            if len(server_data) <= 0:
                break
            ui_element.ui.progressBar.setValue((received_data/size) * 100)
            transferred_file_bytes.append(server_data)

        self.write_data(transferred_file_bytes, save_location)
        message = QMessageBox()
        ui_element.windows.append(message)
        message.setText("Download complete")
        message.show()
        ui_element.windows.pop()

    def write_data(self, data, save_location):
        with open(save_location, "wb") as file:
            for file_data in data:
                file.write(file_data)
