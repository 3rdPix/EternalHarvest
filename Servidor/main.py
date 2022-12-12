import sys
import json
from servidor import Servidor

if __name__ == "__main__":
    with open('net_info.json', 'r') as file: net_info: dict = json.load(file)
    port: int = net_info.get('port')
    host: str = net_info.get('host')
    servidor = Servidor(host=host, port=port)

    try:
        while True:
            input("[Presione Ctrl+C para cerrar]".center(82, "+") + "\n")
    
    except KeyboardInterrupt:
        print("\n\n")
        print("Cerrando servidor...".center(80, " "))
        print("".center(82, "-"))
        print("".center(82, "-") + "\n")
        sys.exit()