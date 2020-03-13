import abc


class Client(abc.ABC):
    def __init__(self, ip, save_file_path):
        self.ip = ip
        self.__port = 5000
        self.save_file_location = save_file_path

    def get_port(self):
        return self.__port

    @abc.abstractmethod
    def fetch_data(self, pipe1, pipe2):
        pass

    @abc.abstractmethod
    def write_data(self, save_location, ui_element):
        pass

    @abc.abstractmethod
    def get_file_name(self):
        pass
