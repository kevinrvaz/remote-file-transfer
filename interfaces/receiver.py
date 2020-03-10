from concurrent.futures import ProcessPoolExecutor, wait
from interfaces.client import Client
from multiprocessing import Manager
from shutil import rmtree
import socket
import math
import os

TEMP_LOCATION = ".asdkjasdkasdhlsadhsajdhlas"


def server_ports():
    return list(range(30000, 30010))


def receive_data_thread(server, ip, location):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, server))
    file_name = client.recv(10).decode("utf-8").strip()

    data = client.recv(4096)
    if data:
        with open(os.path.join(os.path.sep.join(location.split(os.path.sep)[:-1]),
                               TEMP_LOCATION, file_name), "wb") as file:
            file.write(data)

    print(f"Received data filename {file_name} of size {len(data)}")
    return len(data)


class ReceivedData:
    def __init__(self):
        self.data = 0


class Receiver(Client):
    received_data = 0

    def __init__(self, ip, save_file_path):
        super().__init__(ip, save_file_path)
        self.__received = False

    def set_received(self, val):
        self.__received = val

    def get_received(self):
        return self.__received

    def get_file_name(self):
        _, file_name = os.path.split(self.save_file_location)
        return file_name

    def fetch_data(self, ui_element):
        IP = ui_element.ui.lineEditIP.text()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, self.get_port()))

        header = client.recv(200)
        vals = header.split()
        size = int(vals[0])
        file_name = " ".join([vals[i].decode("utf-8") for i in range(1, len(vals))])
        save_location = os.path.join(self.save_file_location, file_name)

        futures = []
        ports = server_ports()
        os.makedirs(os.path.join(os.path.sep.join(save_location.split(os.path.sep)[:-1]),
                                 TEMP_LOCATION), exist_ok=True)

        r = ReceivedData()
        lock = Manager().Lock()

        def update_hook(future):
            res = future.result()
            if res:
                with lock:
                    r.data += res
                    ui_element.ui.progressBar.setValue((r.data / size) * 100)

        with ProcessPoolExecutor(max_workers=10) as executor:
            for i in range(int(math.ceil(size / 4096))):
                futures.append(executor.submit(receive_data_thread, ports[i % 10], IP, save_location))
                futures[-1].add_done_callback(update_hook)

        wait(futures)

        self.write_data(save_location)
        self.set_received(True)

    def write_data(self, save_location):
        with open(save_location, "wb") as file:
            path = os.path.join(os.path.sep.join(save_location.split(os.path.sep)[:-1]),
                                TEMP_LOCATION)

            files = [i for i in os.listdir(path) if i.isnumeric()]

            for temp_file in sorted(files, key=int):
                with open(os.path.join(path, temp_file), "rb") as temp:
                    print(f"writing {temp_file}")
                    file.write(temp.read())

        rmtree(path)
