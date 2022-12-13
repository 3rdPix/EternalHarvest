import json
from socket import socket


class Router:

    @staticmethod
    def receive_bytes(leng: int, socket_de_origen: socket) -> bytearray:
        """
        Recibe un mensaje codificado y encriptado de largo determinado,
        y retorna el mensaje original
        """
        # Primera parte: reagrupa los paquetes de 32 bytes
        recibido_bruto: bytearray = bytearray()
        offset = 0 if leng % 32 == 0 else 1
        for _ in range((leng // 32) + offset):
            num_bloque: int = int.from_bytes(socket_de_origen.recv(4), 'little')
            if not num_bloque: break
            bloque_n = socket_de_origen.recv(32)
            recibido_bruto.extend(bloque_n)
        recibido_bruto = recibido_bruto[0:leng]

        # Segunda parte: interpreta los bytes del mensaje
        not_encriptado = Router.decrypt(recibido_bruto)
        not_coded = not_encriptado.decode()
        not_dumped = json.loads(not_coded)
        return not_dumped

    @staticmethod
    def codify_bytes(written: any) -> bytearray:
        """
        Recibe un objeto a ser enviado, lo encripta y codifica para
        ser enviado.
        """
        # Primera parte: encriptación
        dumped = json.dumps(written)
        coded = dumped.encode()
        encriptado = Router.encrypt(bytearray(coded))
        
        # Segunda parte: construcción del mensaje
        mensaje: bytearray = bytearray()
        
        leng: bytearray = len(encriptado).to_bytes(4, 'big')
        mensaje.extend(leng)
        
        block_counter = 1
        while encriptado:
            add = min(32, len(encriptado))
            mensaje.extend(block_counter.to_bytes(4, 'little'))
            nuevo_bloque = bytearray()
            for _ in range(add): nuevo_bloque.extend(encriptado.pop(0).to_bytes(1, 'big'))
            mensaje.extend(nuevo_bloque)
            block_counter += 1
            if add % 32 != 0:
                for _ in range(32 - add):
                    mensaje.extend(int(0).to_bytes(1, 'big'))
        return mensaje

    @staticmethod
    def encrypt(msg : bytearray) -> bytearray:
        box_1: bytearray = bytearray()
        box_2: bytearray = bytearray()
        box_3: bytearray = bytearray()
        for indice, trozo in enumerate(msg):
            match indice % 3:
                case 0: box_1.extend(trozo.to_bytes(1, 'big'))
                case 1: box_2.extend(trozo.to_bytes(1, 'big'))
                case 2: box_3.extend(trozo.to_bytes(1, 'big'))
        match len(box_2) % 2:
            case 0:
                suma = (
                    int(box_1[0]) + # byte de arreglo A
                    int(box_3[-1]) + # byte de arreglo C
                    int(box_2[int(len(box_2) / 2)]) # byte central de B
                )
            case 1:
                suma = (
                    int(box_1[0]) + # byte de arreglo A
                    int(box_3[-1]) + # byte de arreglo C
                    int(box_2[len(box_2) // 2]) + # bytes centrales de B
                    int(box_2[int(len(box_2) // 2) + 1])
                    )
        match suma % 2:
            case 0: return bytearray(int(0).to_bytes(1, 'big') + box_3 + box_1 + box_2)
            case 1: return bytearray(int(1).to_bytes(1, 'big') + box_1 + box_3 + box_2)

    @staticmethod
    def decrypt(msg : bytearray) -> bytearray:
        order: int = msg.pop(0)
        min_size: int = len(msg) // 3
        fix: int = 0 if len(msg) % 3 == 0 else 1
        
        # Determine the boxes
        match order:
            case 0:
                box_3: bytearray = msg[0:min_size]
                box_1: bytearray = msg[min_size:(min_size * 2) + fix]
                box_2: bytearray = msg[(min_size * 2) + fix::]
            case 1:
                box_1: bytearray = msg[0:(min_size + fix)]
                box_3: bytearray = msg[(min_size + fix):(min_size * 2) + fix]
                box_2: bytearray = msg[(min_size * 2) + fix::]
        
        # Create the message
        message: bytearray = bytearray()
        for index in range(len(msg)):
            match index % 3:
                case 0: message.extend(box_1.pop(0).to_bytes(1, 'big'))
                case 1: message.extend(box_2.pop(0).to_bytes(1, 'big'))
                case 2: message.extend(box_3.pop(0).to_bytes(1, 'big'))
        return message