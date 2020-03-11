from concurrent.futures import ProcessPoolExecutor, wait, ThreadPoolExecutor
from interfaces.client import Client
from multiprocessing import Manager
from threading import Lock
import aiofiles
import asyncio
import socket
import math
import os
import gc

TEMP_LOCATION = ".asdkjasdkasdhlsadhsajdhlas"
PROCESS_WORKERS = 5
THREAD_WORKERS = 10
BUFFER_SIZE = 32768
USED_PORTS = 100


async def write_file_thread(location, data):
    async with aiofiles.open(location, mode="wb") as file:
        await file.write(data)


def receive_data_thread(port, ip, location, loop):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))

    try:
        file_name = client.recv(10).decode("utf-8").strip()
    except ConnectionResetError:
        return

    received_bytes = []

    while True:
        temp = client.recv(8192)
        if temp:
            received_bytes.append(temp)
        else:
            break

    data = b"".join(received_bytes)

    task = None

    if data:
        location = os.path.join(os.path.sep.join(location.split(os.path.sep)[:-1]),
                                TEMP_LOCATION, file_name)
        task = asyncio.ensure_future(write_file_thread(location, data), loop=loop)

    return len(data), task


def receive_data_process(ports, ip, location):
    threads = []
    thread_lock = Lock()

    completed_bytes = ReceivedData()

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    file_tasks = []

    def update_hook(future):
        res = future.result()
        if res:
            with thread_lock:
                completed_bytes.data += res[0]
                if res[1]:
                    file_tasks.append(res[1])

    with ThreadPoolExecutor(max_workers=THREAD_WORKERS) as thread_pool:
        for port in ports:
            threads.append(thread_pool.submit(receive_data_thread, port, ip, location, event_loop))
            threads[-1].add_done_callback(update_hook)

    wait(threads)

    if file_tasks:
        event_loop.run_until_complete(asyncio.wait(file_tasks))

    del event_loop
    del file_tasks
    del threads
    del thread_pool
    del thread_lock

    return completed_bytes.data


class ReceivedData:
    def __init__(self):
        self.data = 0


class Receiver(Client):
    def __init__(self, ip, save_file_path):
        super().__init__(ip, save_file_path)
        self.__received = False
        self.save_location = ""

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
        ports = list(range(30000, 30000 + USED_PORTS))

        os.makedirs(os.path.join(os.path.sep.join(save_location.split(os.path.sep)[:-1]),
                                 TEMP_LOCATION), exist_ok=True)

        r = ReceivedData()
        process_lock = Manager().Lock()

        def update_hook(future):
            res = future.result()
            if res:
                with process_lock:
                    r.data += res
                    ui_element.ui.progressBar.setValue((r.data / size) * 100)

        with ProcessPoolExecutor(max_workers=PROCESS_WORKERS) as executor:
            for i in range(int(math.ceil(size / (BUFFER_SIZE * THREAD_WORKERS)))):
                futures.append(executor.submit(receive_data_process,
                                               ports[(i % THREAD_WORKERS) * THREAD_WORKERS:(i % THREAD_WORKERS)
                                                     * THREAD_WORKERS + THREAD_WORKERS], IP, save_location))
                futures[-1].add_done_callback(update_hook)

        wait(futures)
        del executor
        del ports
        del process_lock
        del futures
        gc.collect()

        self.save_location = save_location
        self.set_received(True)

    async def write_data(self, save_location, ui_element):
        async with aiofiles.open(save_location, mode="wb") as file:
            path = os.path.join(os.path.sep.join(save_location.split(os.path.sep)[:-1]),
                                TEMP_LOCATION)

            files = [i for i in os.listdir(path) if i.isnumeric()]
            for index, temp_file in enumerate(sorted(files, key=int)):
                async with aiofiles.open(os.path.join(path, temp_file), mode="rb") as temp:
                    contents = await temp.read()
                    ui_element.ui.progressBar.setValue(((index + 1) / len(files)) * 100)
                    await file.write(contents)

        return path
