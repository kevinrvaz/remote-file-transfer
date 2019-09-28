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
        # file_name = self.get_file_name()
        # save_location = os.path.join(self.save_file_location, file_name)

        IP = ui_element.ui.lineEditIP.text()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, self.get_port()))

        transferred_file_bytes = []

        while True:
            server_data = client.recv(4096)
            if len(server_data) <= 0:
                break
            transferred_file_bytes.append(server_data)

        self.write_data(transferred_file_bytes, self.save_file_location)
        message = QMessageBox()
        message.setText("Download complete")
        message.show()

    def write_data(self, data, save_location):
        with open(save_location, "wb") as file:
            for file_data in data:
                file.write(file_data)
