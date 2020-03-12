from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
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
PROCESS_WORKERS = 10
THREAD_WORKERS = 10
BUFFER_SIZE = 65536
USED_PORTS = 200


async def write_file_thread(location, data):
    async with aiofiles.open(location, mode="wb") as file:
        await file.write(data)


async def receive_data_thread(port, ip, location):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        file_name = client.recv(10).decode("utf-8").strip()
    except (ConnectionResetError, ConnectionRefusedError):
        return 0

    received_bytes = []

    while True:
        temp = client.recv(BUFFER_SIZE)
        if temp:
            received_bytes.append(temp)
        else:
            break

    client.close()

    data = b"".join(received_bytes)

    if data:
        location = os.path.join(os.path.sep.join(location.split(os.path.sep)[:-1]),
                                TEMP_LOCATION, file_name)
        await write_file_thread(location, data)

    return len(data)


async def receive_data_process_async(ports, ip, location, event_loop):
    completed_bytes = ReceivedData()

    async def update_hook(future_list):
        for val in future_list:
            res = await val
            if res:
                completed_bytes.data += res

    futures = []

    with ThreadPoolExecutor(max_workers=THREAD_WORKERS) as thread_pool:
        for port in ports:
            futures.append(await event_loop.run_in_executor(thread_pool, receive_data_thread,
                                                            port, ip, location))

    await update_hook(futures)

    del thread_pool

    return completed_bytes.data


def receive_data_process(ports, ip, location):
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    return event_loop.run_until_complete(receive_data_process_async(ports, ip, location, event_loop))


class ReceivedData:
    def __init__(self, pipe=None):
        self.pipe = pipe
        self.data = 0


class Receiver(Client):
    def __init__(self, ip, save_file_path):
        super().__init__(ip, save_file_path)
        self.save_location = ""
        self.ip = ip

    def get_file_name(self):
        _, file_name = os.path.split(self.save_file_location)
        return file_name

    async def fetch_data_async(self, ip, connection_pipe, process_loop):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, self.get_port()))

        header = client.recv(200)
        val = header.split()
        size = int(val[0])
        file_name = " ".join([val[i].decode("utf-8") for i in range(1, len(val))])
        save_location = os.path.join(self.save_file_location, file_name)

        ports = list(range(30000, 30000 + USED_PORTS))

        os.makedirs(os.path.join(os.path.sep.join(save_location.split(os.path.sep)[:-1]),
                                 TEMP_LOCATION), exist_ok=True)

        r = ReceivedData(connection_pipe)
        process_lock = Manager().Lock()

        def update_hook(value):
            res = value
            if res:
                with process_lock:
                    r.data += res
                    r.pipe.send((r.data / size) * 100)

        with ProcessPoolExecutor(max_workers=PROCESS_WORKERS) as executor:
            start = 0
            for i in range(int(math.ceil(size / (BUFFER_SIZE * THREAD_WORKERS)))):
                end = start + THREAD_WORKERS
                future = await process_loop.run_in_executor(executor, receive_data_process,
                                                            ports[start:end], ip, save_location)
                update_hook(future)
                start = end
                if end == USED_PORTS:
                    start = 0

        del executor
        del ports
        del process_lock

        gc.collect()

        self.save_location = save_location
        r.pipe.send(save_location)

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

    def fetch_data(self, pipe):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.fetch_data_async(self.ip, pipe, loop))
