from concurrent.futures import ProcessPoolExecutor, wait
from interfaces.server import Server
from multiprocessing import Manager
import socket
import os


def create_server(i, ip):
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    temp_socket.bind((ip, i + 30000))
    temp_socket.listen(10)

    return temp_socket


def construct_header(size, file_name):
    HEADER_SIZE = 200
    msg = f"{size} {file_name}"
    header = f"{msg:<{HEADER_SIZE}}"
    return header


def send_data_thread(data, server, file_name):
    client, address = server.accept()

    print(f"Accepted connection from {address} on {server}")

    client.send(bytes(f"{file_name:<{10}}", "utf-8"))
    client.send(data)
    client.close()
    return len(data)


class SentData:
    def __init__(self):
        self.data = 0


class Sender(Server):
    def __init__(self, ip, file_location):
        super().__init__(ip, file_location)
        self.__sent = False
        self.data = 0

    def set_sent(self, val):
        self.__sent = val

    def get_sent(self):
        return self.__sent

    def get_file_name(self):
        _, tail = os.path.split(self.file_location)
        return tail

    def get_file_size(self):
        file_size = os.path.getsize(self.file_location)
        return file_size

    def read_data(self):
        with open(self.file_location, "rb") as file:
            while True:
                data = file.read(4096)
                if not data or len(data) <= 0:
                    break
                yield data

    def send_data(self, ui_element):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.ip, self.get_port()))
        server.listen(10)

        file_size = int(self.get_file_size())
        file_name = self.get_file_name()

        print(file_name, file_size)

        client, address = server.accept()
        print(f"connection established with {address}")

        client.send(bytes(construct_header(file_size, file_name), "utf-8"))
        client.close()

        futures = []

        s = SentData()
        lock = Manager().Lock()

        def update_hook(future):
            res = future.result()
            if res:
                with lock:
                    s.data += res
                    ui_element.ui.progressBar.setValue((s.data / file_size) * 100)

        servers = {i: create_server(i, self.ip) for i in range(10)}

        with ProcessPoolExecutor(max_workers=10) as executor:
            for file_name, data in enumerate(self.read_data()):
                futures.append(executor.submit(send_data_thread, data, servers[file_name % 10], file_name))
                futures[-1].add_done_callback(update_hook)

        wait(futures)

        if s.data != 0:
            self.set_sent(True)
