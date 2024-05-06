import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import threading as thr
import requests
import json
import time


SERVERIP = '192.168.1.101'
TCPPORT='8080'

class SensorManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sensor Management")
        self.subs = []

        # Create table
        self.tree = ttk.Treeview(self.root, columns=("UC", "ID", "TEMP", "Estado"), show="headings")
        self.tree.heading("UC", text="UC")
        self.tree.heading("ID", text="ID")
        self.tree.heading("TEMP", text="TEMP")
        self.tree.heading("Estado", text="Estado")
        self.tree.pack(padx=10, pady=10)

        # Create buttons
        connect_button = tk.Button(self.root, text="Conectar-se a uma UC", command=self.connect_uc)
        connect_button.pack(padx=10, pady=5)

        instantiate_button = tk.Button(self.root, text="Instanciar um ou mais sensores", command=self.instantiate_sensor)
        instantiate_button.pack(padx=10, pady=5)

        delete_button = tk.Button(self.root, text="Excluir sensor", command=self.delete_sensor)
        delete_button.pack(padx=10, pady=5)

        turn_off_button = tk.Button(self.root, text="Desligar sensor", command=self.turn_off_sensor)
        turn_off_button.pack(padx=10, pady=5)

        turn_on_button = tk.Button(self.root, text="Ligar sensor", command=self.turn_on_sensor)
        turn_on_button.pack(padx=10, pady=5)

        # Dados iniciais da tabela
        self.sensor_data = []

        # Armazena a seleção atual
        self.selected_item = None

        # Cria e inicia a thread de atualização da tabela
        self.update_thread = thr.Thread(target=self.update_table_thread)
        self.update_thread.daemon = True  # Define a thread como um daemon para que ela termine quando o programa principal terminar
        self.update_thread.start()

    def connect_uc(self):
        uc_name = simpledialog.askstring("Conectar-se a uma UC", "Digite o nome da UC:")
        if uc_name:
            response = requests.post("http://"+SERVERIP+":"+TCPPORT+'/verificar', json={
                "UcName": uc_name
            })
            if response.status_code == 200:
                if self.subs.count(uc_name):
                    messagebox.showinfo("Erro", "Já inscrito na unidade de controle!")
                else:

                    messagebox.showinfo("Sucesso", "Conexão bem-sucedida!")
                    self.subs.append(uc_name)
            else:
                messagebox.showerror("Erro", f"Erro ao conectar: {response.text}")

    def instantiate_sensor(self):
        #uc_name = simpledialog.askstring("Instanciar um sensor", "Digite o nome da UC:")
        uc_name = "TST"
        if uc_name:
            #sensor_count = simpledialog.askinteger("Instanciar um sensor", "Digite a quantidade de sensores:")
            sensor_count = 4
            if sensor_count:
  
                err = requests.post(SERVERIP+TCPPORT+"/instSensor",json={
                "ucName": uc_name,
                "sensorCount": sensor_count
                })

                print(err)
                # Aqui você pode implementar a lógica para instanciar os sensores
                pass

    def delete_sensor(self):
        # Aqui você pode implementar a lógica para excluir o sensor selecionado na tabela
        pass

    def turn_off_sensor(self):
        # Aqui você pode implementar a lógica para desligar o sensor selecionado na tabela
        pass

    def turn_on_sensor(self):
        # Aqui você pode implementar a lógica para ligar o sensor selecionado na tabela
        pass

    def update_table(self):
        # Armazena o item selecionado
        self.selected_item = self.tree.selection()
        if self.sensor_data.__len__()!=0:

            try:

                # Limpa a tabela
                for row in self.tree.get_children():
                    self.tree.delete(row)
                
                # Adiciona os dados atualizados à tabela
                for byte_data in self.sensor_data:
                    data = json.loads(byte_data.decode('utf-8'))  # Decodifica bytes para string e, em seguida, faz o parsing JSON
                    self.tree.insert("", "end", values=(data["UC"], data["ID"], data["TEMP"], data["Estado"]))

            except tk.TclError:
                pass
                # Restaura a seleção
                if self.selected_item:
                    self.tree.selection_set(self.selected_item)
            except AttributeError:
                pass


    def update_table_thread(self):
        while True:
            # Atualiza a tabela a cada 1 segundo
            self.update_table()
            time.sleep(1)

    def getterSensors(self):
        while True:
            # Cria o corpo da solicitação JSON com a lista de unidades de controle inscritas
            data = {"subs": self.subs}
            if data["subs"].__len__()!=0:
                try:
                    # Envia a solicitação POST para o servidor
                    response = requests.post("http://192.168.1.101:8080/sensors", json=data)
                    
                    # Verifica se a solicitação foi bem-sucedida (código de status 200)
                    if response.status_code == 200:
                        self.sensor_data = response.json()
                        print(self.sensor_data)
                    else:
                        print("Erro:", response.status_code)
                    
                except Exception as e:
                    print("Erro ao enviar solicitação de sensores:", e)

            time.sleep(0.5)

def main():
    app = SensorManagementApp(tk.Tk())
    getterThread = thr.Thread(target=app.getterSensors,daemon=True)
    getterThread.start()
    app.root.mainloop()

if __name__ == "__main__":
    main()
