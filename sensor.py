import socket

import random as rd
import time

# Endereço e porta do servidor
HOST = '127.0.0.1'  # localhost
PORT = 65432


class Sensor:
    def __init__(self, temp, id, estado):
        self.estado = estado
        self.temp = temp
        self.id = id

    def get_estado(self):
        return self.estado

    def get_temp(self):
        return self.temp

    def get_id(self):
        return self.id
    


leitura = 0
while True:
    for i in range (0,100):

        leitura = f"{i}".encode()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Envia uma mensagem para o servidor
            s.sendto(leitura, (HOST, PORT))
        time.sleep(0.5)


    