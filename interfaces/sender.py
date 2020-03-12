from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from interfaces.server import Server
from multiprocessing import Manager
import aiofiles
import asyncio
import socket
import os
import gc


PROCESS_WORKERS = 10
THREAD_WORKERS = 10
BUFFER_SIZE = 65536
USED_PORTS = 200


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


def send_data_thread(file_name, server, data):
    client, address = server.accept()
    client.send(bytes(f"{file_name:<{10}}", "utf-8"))
    client.send(data)
    return len(data)


async def send_data_process_async(file_name, servers, start, fn, event_loop):
    completed_bytes = SentData()

    async def update_hook(future_list):
        for val in future_list:
            if type(val) == int:
                res = val
            else:
                res = await val
            if res:
                completed_bytes.data += res

    futures = []

    with ThreadPoolExecutor(max_workers=THREAD_WORKERS) as thread_pool:
        index = file_name

        async for data in fn(start):
            futures.append(await event_loop.run_in_executor(thread_pool, send_data_thread,
                                                            index, servers[index % THREAD_WORKERS], data))
            index += 1
            del data

    await update_hook(futures)

    del thread_pool

    return completed_bytes.data


def send_data_process(file_name, servers, start, fn):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    return loop.run_until_complete(send_data_process_async(file_name, servers, start, fn, loop))


class SentData:
    def __init__(self, pipe=None):
        self.pipe = pipe
        self.data = 0


class Sender(Server):
    def __init__(self, ip, file_location):
        super().__init__(ip, file_location)
        self.data = 0

    def get_file_name(self):
        _, tail = os.path.split(self.file_location)
        return tail

    def get_file_size(self):
        file_size = os.path.getsize(self.file_location)
        return file_size

    async def read_data(self, start):
        async with aiofiles.open(self.file_location, mode="rb") as file:
            await file.seek(start)
            sent_data = 0
            while True:
                if sent_data >= (BUFFER_SIZE * THREAD_WORKERS):
                    break
                data = await file.read(BUFFER_SIZE)
                sent_data += len(data)
                if not data or len(data) <= 0:
                    break
                yield data

    async def send_data_async(self, connection_pipe, process_loop):
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

        s = SentData(connection_pipe)
        process_lock = Manager().Lock()

        servers = [create_server(i, self.ip) for i in range(USED_PORTS)]

        def update_hook(value):
            res = value
            if res:
                with process_lock:
                    s.data += res
                    s.pipe.send((s.data / file_size) * 100)

        with ProcessPoolExecutor(max_workers=PROCESS_WORKERS) as executor:
            start = 0
            for file_name, chunk_start in enumerate(range(0, file_size, BUFFER_SIZE * THREAD_WORKERS)):
                end = start + THREAD_WORKERS
                future = await process_loop.run_in_executor(executor, send_data_process, file_name * THREAD_WORKERS,
                                                            servers[start:end], chunk_start, self.read_data)
                update_hook(future)
                start = end
                if end == USED_PORTS:
                    start = 0

        del executor
        del process_lock
        del servers

        gc.collect()

    def send_data(self, pipe):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.send_data_async(pipe, loop))
