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

    def get_estado(self):
        return self._estado

    def get_temp(self):
        return self._temp

    def get_id(self):
        return self._id
    
    def altState(self, newState):
        self._estado = newState
    
    def startMonitoring(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            while self.get_estado() == 1:
                for i in range(1, 101):
                    data = f"{self.get_id()}|{i}".encode()
                    s.sendto(data, (HOST, PORT))
                    time.sleep(0.5)
                    if self.get_estado() != 1:
                        break

    def startTxThread(self, thread: thr.Thread):
        thread = thr.Thread(target=self.startMonitoring,args=(self,))
        return thread
        
    def altSensor(self):
        self.altState(2)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            while self.get_estado() == 2:
                data = f"{self.get_id()}|{self.get_temp}".encode()
                s.sendto(data, (HOST, PORT))
                time.sleep(0.5)
                if self.get_estado() != 2:
                    break
        pass
    
    def stopSensor(self):
        self.altState(0)


def msgMenu():
   print("DIGITE:\n"
         "1 - PARA INSTANCIAR UM NOVO SENSOR\n"
         "2 - PARA APAGAR UM SENSOR\n"
         "3 - PARA DESLIGAR UM SENSOR\n"
         "4 - PARA LIGAR UM SENSOR\n"
         "5 - PARA VISUALIZAR OS SENSORES\n"
         "0 - PARA SAIR"
         )
   pass

def print_Sns_ID(sensores: list[Sensor]):
    for i in sensores:
        print(f"ID: {i.get_id()} ULTIMA LEITURA: {i.get_temp()}")
    input("Enter para continuar...")

def createId(sensores: list[Sensor]):
    return sensores[-1].get_id()+1

def createNewSensor(sensores: list):
    if sensores.__len__() == 0:
        new_id = 0
    else:
        new_id = createId(sensores)

    newSrs = Sensor(temp=-1,estado=0,new_id=new_id)
    sensores.append(newSrs)
    print("Novo sensor instanciado com ID:", new_id)    
    pass

def excludeSensor(id: int, sensores: list[Sensor]):
    rmv = searchSensor(id,sensores)
    if rmv:
        rmv.altState(0)
        sensores.remove(rmv)
        rmv = True
        print("Sensor removido")
    else:
        print("ID:",id,"- não encontrado.")
    pass

def searchSensor(id: int, sensores: list[Sensor]):
    fd = 0
    for i in sensores:
        if i.get_id()==id:
          fd = i
          break
    return fd

def startSensor(id: int, sensores: list[Sensor]):
    sensor = searchSensor(id, sensores)
    sensor.altState(0)

    pass

sensores = []
txThreads = []
rxThreads =[]
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
        excludeSensor(x_id,sensores)
        pass
    elif menu == 3:

        pass
    elif menu == 4:
        r_id = int(input("Digite o ID do sensor a ser ligado, -1 para cancelar.\nID:"))
        if r_id==-1:
            pass
        else:
            startSensor(r_id,sensores)
            pass
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