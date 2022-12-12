from socket import socket, AF_INET, SOCK_STREAM
import threading


class Servidor:

    def __init__(self, port: int, host: str) -> None:
        self.log(0, 'Inicializando Servidor...')
        self.host = host
        self.port = port
        self.sv_socket: socket = socket(AF_INET, SOCK_STREAM)
        self.link_and_listen()
        self.start_connection_thread()

    def link_and_listen(self) -> None:
        self.sv_socket.bind((self.host, self.port))
        self.sv_socket.listen()
        self.log(0, f'Servidor escuchando en {self.host}:{self.port}...')

    def start_connection_thread(self) -> None:
        thread = threading.Thread(target=self.accept_connections)
        thread.start()
        self.log(0, 'Hilo de conexiones iniciado.')

    def accept_connection(self) -> None:
        self.log(0, 'Servidor aceptando conexiones.')
        while True:
            client_socket, (client_addrs, client_port) = self.sv_socket.accept()
            self.log(1, f'Conectado a nuevo cliente en: {client_addrs}:{client_port}')
            listener = threading.Thread(target=self.client_listen_thread,
            args=(client_socket, ), daemon=True)
            listener.start()

    def client_listen_thread(self, client_socket: socket) -> None:
        try:
            while True:
                pass
        except ConnectionError:
            self.handle_disconnection(client_socket)

    def handle_disconnection(self, client_socket: socket) -> None:
        pass

    def log(self, format: int, msg: str) -> None:
        match format:
            case 0: print('[STATUS]', msg)
            case 1: print('[EVENT]', msg)
            case 2: print('[REQUEST]', msg)
