from socket import socket, AF_INET, SOCK_STREAM
from router import Router
from os.path import exists, join
import threading
import sqlite3


class Servidor:

    def __init__(self, port: int, host: str) -> None:
        self.log(0, 'Inicializando Servidor...')
        self.host = host
        self.port = port
        self.sv_socket: socket = socket(AF_INET, SOCK_STREAM)
        self.init_db()
        self.init_connection()
        
    def log(self, format: int, msg: str) -> None:
        match format:
            case 0: print('[STATUS]', msg)
            case 1: print('[EVENT]', msg)
            case 2: print('[REQUEST]', msg)

    """
    Database
    """
    def init_db(self) -> None:
        if not exists(join(*['data', 'database.db'])): self.create_db()
        self.database: sqlite3.Connection = \
            sqlite3.connect(join(*['data', 'database.db']))
        self.cursor: sqlite3.Cursor = self.database.cursor()

    def create_db(self) -> None:
        self.log(0, f'Ninguna base de datos encontrada. Creando una...')
        database: sqlite3.Connection = \
            sqlite3.connect(join(*['data', 'database.db']))
        cursor: sqlite3.Cursor = database.cursor()
        
        with open(join(*['data', 'create_users.sql']), 'r') as file:
            instructions = file.read()
            cursor.execute(instructions)
        
        with open(join(*['data', 'create_mobs.sql']), 'r') as file:
            instructions = file.read()
            cursor.execute(instructions)
        
        with open(join(*['data', 'create_collection.sql']), 'r') as file:
            instructions = file.read()
            cursor.execute(instructions)
        
        database.close()
        self.log(1, f'Base de datos creada')

    """
    Connection
    """
    def init_connection(self) -> None:
        self.sv_socket.bind((self.host, self.port))
        self.sv_socket.listen()
        self.log(0, f'Servidor escuchando en {self.host}:{self.port}...')
        self.start_connection_thread()

    def start_connection_thread(self) -> None:
        thread = threading.Thread(target=self.accept_connection, daemon=True)
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
                len_in_bytes = client_socket.recv(4)
                len_content = int.from_bytes(len_in_bytes, byteorder='big')
                msg = Router.receive_bytes(len_content, client_socket)
                self.read_request(msg)
        except ConnectionError:
            self.handle_disconnection(client_socket)

    def handle_disconnection(self, client_socket: socket) -> None:
        pass

    def starken(self, object, wing: socket) -> None:
        pass

    def read_request(self, request: dict) -> None:
        match request.get('request'):
            case 0: self.create_user(request)

    """
    Tasks
    """
    def create_user(self, request: dict) -> None:
        self.log(2, f'Creación de usuario {request.get("username")}')