import socket
import threading as thr
import time

HOST = '127.0.0.1'
PORT = 65432

class Sensor:
    def __init__(self, temp: int, id: int, estado: int):
        self._estado = estado
        self._temp = temp
        self._id = id
        self._rxThr = thr.Thread
        self._txThr = thr.Thread

    def get_estado(self):
        return self._estado

    def get_temp(self):
        return self._temp

    def get_id(self):
        return self._id
    
    def altState(self, newState):
        self._estado = newState
    
    def startMonitoring(self):
        self.altState(1)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            while self.get_estado() == 1:
                for i in range(1, 101):
                    data = f"{self.get_id()}|{i}".encode()
                    s.sendto(data, (HOST, PORT))
                    time.sleep(0.5)
                    if self.get_estado() != 1:
                        break

    def startThread(self):
        self._txThr = thr.Thread(target=startMonitoring,args=(self,))
        pass



    def altSensor(self):
        self.altState(2)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            while self.get_estado() == 2:
                data = f"{self.get_id()}|{i}".encode()
                s.sendto(data, (HOST, PORT))
                time.sleep(0.5)
                if self.get_estado() != 2:
                    break
        pass

    def startSensor(self):
        thr.Thread(target=self.startMonitoring).start()

    def stopSensor(self):
        time.sleep(5)
        self.altState(0)


def msgMenu():
   print("DIGITE:\n"
         "1 - PARA INSTANCIAR UM NOVO SENSOR\n"
         "2 - PARA APAGAR UM SENSOR\n"
         "3 - PARA DESLIGAR UM SENSOR\n"
         "4 - PARA LIGAR UM SENSOR"
         "5 - PARA VISUALIZAR OS SENSORES"
         "0 - PARA SAIR"
         )
   pass

def print_Sns_ID(sensores: list[Sensor]):
    for i in sensores:
        print(f"ID: {i.get_id} ULTIMA LEITURA: {i.get_temp}")
    input("Enter para continuar...")

def createId(sensores: list[Sensor]):
    return sensores[-1].get_id()

def createNewSensor(sensores):
    if sensores.__sizeof__() == 0:
        new_id = 0
    else:
        new_id = createId(sensores)

    newSrs = Sensor(0,0,new_id)
    sensores.append(newSrs)
    print("Novo sensor instanciado com ID:", new_id)    
    pass

def excludeSensor(id: int, sensores: list[Sensor]):
    for i in sensores:
        if i.get_id()==id:
            i.
            sensores.remove(i)
            rmv = True
            break
    if rmv:
        print("Sensor removido.")
    else:
        print("ID:",id,"- não encontrado.")
    pass

sensores = []
new_id = 0
menu = 1

while menu in (1,2,3,4):
    msgMenu()
    menu = int(input("Comando: "))
    if menu == 1:
        createNewSensor(sensores)
        pass
    elif menu == 2:
        x_id = int(input("Digite o ID do sensor a ser excluido"))
        pass
    elif menu == 3:

        pass
    elif menu == 4:
        print_Sns_ID()
        pass
    elif menu == 0:
        print("Desligando...")
        exit()
    else:
        menu = 1
        print("ENTRADA INCORRETA!")
