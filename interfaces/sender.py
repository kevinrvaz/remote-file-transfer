from concurrent.futures import ProcessPoolExecutor
from interfaces.server import Server
import aiofiles
import asyncio
import socket
import os
import gc

PROCESS_WORKERS = 4
ASYNC_POOL_SIZE = 50
BUFFER_SIZE = 65536
USED_PORTS = 40


def create_server(i, ip):
    return ip, i + 30000


def construct_header(size, file_name):
    HEADER_SIZE = 200
    msg = f"{size} {file_name}"
    header = f"{msg:<{HEADER_SIZE}}"
    return header


async def send_data_thread(reader, writer, file_name, start, fn):
    writer.write(bytes(f"{file_name:<{10}}", "utf-8"))
    await writer.drain()
    sent_data = 0

    async for data in fn(start):
        sent_data += len(data)
        writer.write(data)
        await writer.drain()
        del data

    writer.close()

    return sent_data


async def send_data_process_async(file_name, server, start, fn, event_loop):
    def update_hook(val):
        res = val.result()
        if res:
            completed_bytes.data += res
            completed_bytes.pipe.close()

    def add_hook(r, w, name, pos, callback):
        temp = send_data_thread(r, w, name, pos, callback)
        task = asyncio.create_task(temp)
        task.add_done_callback(update_hook)

    completed_bytes = SentData()

    ip, port = server

    coroutine = await asyncio.start_server(lambda r, w: add_hook(r, w, file_name, start, fn),
                                           ip, port, loop=event_loop, reuse_address=True)
    completed_bytes.pipe = coroutine

    async with coroutine:
        await coroutine.wait_closed()

    del coroutine

    return completed_bytes.data


def send_data_process(file_name, server, start, fn):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    return loop.run_until_complete(send_data_process_async(file_name, server, start, fn, loop))


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
                if sent_data >= (BUFFER_SIZE * ASYNC_POOL_SIZE):
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
        server.close()

        s = SentData(connection_pipe)

        servers = [create_server(i, self.ip) for i in range(USED_PORTS)]

        def update_hook(value):
            res = value
            if res:
                s.data += res
                s.pipe.send((s.data / file_size) * 100)

        with ProcessPoolExecutor(max_workers=PROCESS_WORKERS) as executor:
            for file_name, chunk_start in enumerate(range(0, file_size, BUFFER_SIZE * ASYNC_POOL_SIZE)):
                future = await process_loop.run_in_executor(executor, send_data_process, file_name * ASYNC_POOL_SIZE,
                                                            servers[file_name % USED_PORTS], chunk_start,
                                                            self.read_data)
                update_hook(future)

        del executor
        del servers

        gc.collect()

    def send_data(self, pipe):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.send_data_async(pipe, loop))
