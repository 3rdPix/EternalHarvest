from PyQt5.QtCore import QObject
from os.path import join, exists
from socket import socket, AF_INET, SOCK_STREAM
from bk.window_signals import WindowSignals
from bk.router import Router
from bk.requests import Requests
import json
import threading


class WindowLogic(WindowSignals):

    def __init__(self, paths: dict, **kwargs) -> None:
        super().__init__(**kwargs)
        self.paths = paths.get('back')
        self.init_connection()

    """
    Conection
    """
    def init_connection(self) -> None:
        with open('net_info.json', 'r') as file:
            net_info = json.load(file)
            host = net_info.get('host')
            port = net_info.get('port')
        self.t_socket: socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.t_socket.connect((host, port))
            self.start_listen_thread()
        except ConnectionError: pass
    
    def start_listen_thread(self) -> None:
        thread = threading.Thread(target=self.listen_server, daemon=True)
        thread.start()

    def listen_server(self) -> None:
        try:
            while True:
                len_in_bytes = self.t_socket.recv(4)
                len_content = int.from_bytes(len_in_bytes, byteorder='big')
                msg = Router.receive_bytes(len_content, self.t_socket)
                self.read_cmd(msg)
        except ConnectionError: pass

    # To send requests
    def starken(self, object) -> None:
        msg = Router.codify_bytes(object)
        self.t_socket.sendall(msg)

    # Identify commands from server
    def read_cmd(self, cmd) -> None:
        pass

    """
    Tasks
    """
    def log_to_server(self) -> None:
        if not exists('user_info.json'):
            return self.sg_show_sign_up_window.emit()
        with open('user_info.json', 'r') as file:
            user_info = json.load(file)
        self.starken(Requests.log_in(user_info))

    def create_user(self, user_info: dict) -> None:
        self.starken(Requests.log_in(user_info))