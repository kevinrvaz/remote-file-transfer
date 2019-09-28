import abc


class Server(abc.ABC):
    def __init__(self, ip, file_location):
        self.ip = ip
        self.__port = 5000
        self.file_location = file_location

    def get_port(self):
        return self.__port

    @abc.abstractmethod
    def get_file_name(self):
        pass

    @abc.abstractmethod
    def get_file_size(self):
        pass

    @abc.abstractmethod
    def send_data(self, ui_element):
        pass
