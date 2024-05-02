import socket
import time


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
    
    def startMonitoring(self,HOST, PORT, UCname):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            while self.get_estado() == 1:
                for i in range(1, 101):
                    self._temp = i
                    data = f"{UCname}|{self.get_id()}|{self.get_temp()}|{self.get_estado()}".encode()
                    s.sendto(data, (HOST, PORT))
                    time.sleep(0.5)
                    if self.get_estado() != 1:
                        break
        
    def altSensor(self,HOST, PORT):
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
