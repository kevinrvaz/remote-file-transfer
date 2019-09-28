from PyQt5.QtWidgets import QMessageBox
from interfaces.server import Server

import socket
import os


class Sender(Server):
    def __init__(self, ip, file_location):
        super().__init__(ip, file_location)

    def get_file_name(self):
        _, tail = os.path.split(self.file_location)
        return tail

    def get_file_size(self):
        file_size = os.path.getsize(self.file_location)
        return file_size

    def contruct_header(self, size, file_name):
        HEADER_SIZE = 200
        msg = f"{size} {file_name}"
        header = f"{msg:<{HEADER_SIZE}}"
        return header

    def send_data(self, ui_element):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, self.get_port()))
        server.listen(10)

        with open(self.file_location, "rb") as file:
            bytes_data = file.readlines()

        file_size = int(self.get_file_size())
        file_name = self.get_file_name()

        print(file_name, file_size)

        client, address = server.accept()
        print(f"connection established with {address}")

        client.send(bytes(self.contruct_header(file_size, file_name), "utf-8"))

        sent_data = 0
        for data in bytes_data:
            client.send(data)
            sent_data += len(data)
            ui_element.ui.progressBar.setValue((sent_data/file_size) * 100)
        client.close()

        message = QMessageBox()
        ui_element.windows.append(message)
        message.setText("Transfer completed")
        message.show()
        ui_element.windows.pop()
