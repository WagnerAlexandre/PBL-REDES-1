import socket

import random as rd
import time

# Endereço e porta do servidor
HOST = '127.0.0.1'  # localhost
PORT = 65432


# Cria um socket UDP
class sensor:
    def __init__(self,temp,hum,id,estado):
        self.estado = estado
        self.temp = temp
        self.humidity = hum
        self.id = id


'''leitura = 0
while True:
    for i in range (0,100):
            
        leitura = (i.to_bytes())
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Envia uma mensagem para o servidor
            s.sendto(leitura, (HOST, PORT))
        time.sleep(0.5)'''


