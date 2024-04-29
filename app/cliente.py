import socket
import threading as THR
import os

import device.sensor as sensor

def printAllSensors(sensorArray):
    print("\n Situação atual dos sensores:\n")
    print("\n----------------   ----------------   ----------------   ----------------\n")

    for i in range(0,32):
        # i = numero do sensor;
        print("|%2d|T:%-2iC H:%-2i%%|".format(i, sensorArray[i].temp, sensorArray[i].humidity))
        print("   ") # Adicionar 4 espaços entre conjuntos de informações

        if ((i + 1) % 4 == 0):
            if (i != 31):
                print("\n|--|-----------|   |--|-----------|   |--|-----------|   |--|-----------|\n")
            else:
                print("\n----------------   ----------------   ----------------   ----------------\n")
            
    


# Endereço e porta do servidor
HOST = '127.0.0.1'  # localhost
PORT = 65432
entrada = 1
sensor_id = int
menu = 1

sensorArray = []
for i in range(32):
    newS = sensor
    sensorArray.append(newS)

while menu:
    
    os.system("cls")
    printAllSensors(sensorArray)
    entrada = int(input("Digite o comando:\n"
                        "1 - Solicitar Temperatura de algum sensor.\n"
                        "2 - Solicitar Temperatura de algum sensor.\n"
                        "3 - Ligar Monitoramento continuo de algum sensor.\n"
                        "4 - Desligar Monitoramento continuo de algum sensor.\n"
                        "5 - Ligar Monitoramento continuo de todos os sensores.\n"
                        "6 - Desligar Monitoramento continuo de todos os sensores.\n"
                        "7 - Sair do cliente.\n ->"
                        ))
    
    if entrada in (1,2,3,4):
        sensor_id = int(input("Digite o ID do sensor: "))
        pass
    elif entrada in (5,6):
        pass
    elif entrada == 7:
        print("saindo...")
        exit()
    else:
        print("Entrada desconhecida, Digite uma das seguintes: ")


#    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Envia uma mensagem para o servidor
 #       s.sendto(entrada, (HOST, PORT))

