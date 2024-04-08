import socket

import random as rd
import time

# Endereço e porta do servidor
HOST = '127.0.0.1'  # localhost
PORT = 65432

# Cria um socket UDP
leitura = 0
while True:
    leitura = (rd.randint(0,60).to_bytes())
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Envia uma mensagem para o servidor
        s.sendto(leitura, (HOST, PORT))
    time.sleep(0.5)


