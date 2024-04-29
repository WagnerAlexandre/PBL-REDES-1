from sensor import Sensor
import threading as thr
import socket
import os

HOST = '127.0.0.1'
PORT = 65000

def clear():
    os.system('cls')

def print_Sns_ID(sensores: list[Sensor]):
    for i in sensores:
        print(f"ID: {i.get_id()} ULTIMA LEITURA: {i.get_temp()}")
    input("Enter para continuar...")

def createId(sensores: list[Sensor]):
    return sensores[-1].get_id()+1

def createNewSensor(sensores: list[Sensor]):
    if sensores.__len__() == 0:
        new_id = 0
    else:
        new_id = createId(sensores)

    newSrs = Sensor(temp= False,estado=0,id=new_id)
    sensores.append(newSrs)
  
    return new_id

def excludeSensor(id: int, sensores: list[Sensor]):
    rmv = searchSensor(id,sensores)
    if rmv:
        rmv.altState(0)
        sensores.remove(rmv)
        rmv = True
        return 1
    else:
        return 0

def searchSensor(id: int, sensores: list[Sensor]):
    fd = 0
    for i in sensores:
        if i.get_id()==id:
          fd = i
          break
    return fd

def print_Sns_ID():
    for sensor in sensores:
        print(f"ID: {sensor.get_id()} ULTIMA LEITURA: {sensor.get_temp()}")


sensores = []
snrsThreads = {}
newID = 0

def msgMenu():
    clear()
    print("DIGITE:\n"
            "1 - PARA INSTANCIAR UM NOVO SENSOR\n"
            "2 - PARA APAGAR UM SENSOR\n"
            "3 - PARA LIGAR UM SENSOR\n"
            "4 - PARA DESLIGAR UM SENSOR\n"
            "5 - PARA VISUALIZAR OS SENSORES\n"
            "0 - PARA SAIR"
            )
    pass




menu = 1
while menu in (1,2,3,4,5):

    msgMenu()
    menu = int(input("Comando: "))
    if menu == 1:
        newID = createNewSensor(sensores)
        print("Novo sensor instanciado com ID:", newID)
        pass

    elif menu == 2:
        x_id = int(input("Digite o ID do sensor a ser excluido: "))
        if excludeSensor(x_id,sensores):
            print("Sensor removido")
        else:
            print("ID:",x_id,"- não encontrado.")
        pass

    elif menu == 3:
        r_id = int(input("Digite o ID do sensor a ser ligado, -1 para cancelar.\nID:"))
        if r_id==-1:
            pass
        else:
            sensor = searchSensor(r_id, sensores)
            if sensor:
                sensor.altState(1)
                ex_thread = thr.Thread(target=sensor.startMonitoring,args=(HOST, PORT,),daemon=True)
                snrsThreads[r_id] = ex_thread
                snrsThreads[r_id].start()
                pass
            else:  
                print("SENSOR COM ID: ", r_id," - NAO ENCONTRADO!" )
        pass

    elif menu == 4:
        r_id = int(input("Digite o ID do sensor a ser desligado, -1 para cancelar.\nID:"))
        if r_id==-1:
            pass
        else:
            sensor = searchSensor(r_id, sensores)
            sensor.altState(0)
            print("Sensor desligado!")
        pass

    elif menu == 5:
        print_Sns_ID()
        pass

    elif menu == 0:
        print("Desligando...")
        exit()
    else:
        menu = 1
        print("ENTRADA INCORRETA!")
        pass
    input("Enter para continuar...")
