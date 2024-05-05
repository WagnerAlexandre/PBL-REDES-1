from sensor import Sensor
import threading as thr
import socket
import json
import os

SERVERTCPPORT = 8080
SERVERUDPPORT = 1080
SERVEIP = '192.168.1.101'




def clear():
    os.system('cls')

def print_Sns_ID(sensores):
    for i in sensores:
        print(f"ID: {i.get_id()} ULTIMA LEITURA: {i.get_temp()}")
    input("Enter para continuar...")

def createId(sensores):
    return sensores[-1].get_id()+1

def createNewSensor(sensores):
    if sensores.__len__() == 0:
        new_id = 0
    else:
        new_id = createId(sensores)

    newSrs = Sensor(temp= False,estado=0,id=new_id)
    sensores.append(newSrs)
  
    return new_id

def excludeSensor(id: int, sensores):
    rmv = searchSensor(id,sensores)
    if rmv:
        rmv.altState(0)
        sensores.remove(rmv)
        rmv = True
        return 1
    else:
        return 0

def searchSensor(id: int, sensores):
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

class Messagem():
    def __init__(self,tipo: int,conteudo: str) -> None:
        self.Tipo = tipo
        self.Conteudo = conteudo
        pass

def register(UCname):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVEIP, SERVERTCPPORT))
        msg = json.dumps({
        "Tipo": 1,
        "Conteudo": UCname
    }).encode()
        s.sendall(msg)
        print("Registro enviado para o servidor")
        resp = s.recv(1024).decode()
        if resp == "ERROA1":
            return 1
    return 0

def receiver_tcp(REGUC, port, done):
    # Cria um socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while done:
            # Associa o socket à porta
            s.bind((REGUC, port))
            # Coloca o socket para escutar conexões
            s.listen()
            # Aceita a conexão
            conn, addr = s.accept()
            with conn:
                while True:
                    # Recebe os dados
                    data = conn.recv(1024)
                    if not data:
                        break
                    else:
                        multiplexador(data)

def multiplexador(data):
    print(data)

    pass

def process_commands(comando_str):
    comando, id_sensor, ip_requisitante = comando_str.split('|')
    process_command(comando, id_sensor, ip_requisitante)

def process_command(comando, id_sensor, ip_requisitante):
    print(f"Comando recebido - Comando: {comando}, ID do sensor: {id_sensor}, IP do requisitante: {ip_requisitante}")

err = 1
while err:
    clear()
    UCname = input("Nomeie esta UC (Unidade Controladora): ")   

    err = register(UCname)
    if err==1:
        print("Controladora já existe no sistema.")
    elif err ==0:
        print("Registro feito com sucesso!")
    input()
    
receiver_thr = thr.Thread(target=receiver_tcp,daemon=True)
receiver_thr.start()
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
                ex_thread = thr.Thread(target=sensor.startMonitoring,args=(SERVEIP, SERVERUDPPORT,UCname,),daemon=True)
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
