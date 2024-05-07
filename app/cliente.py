import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import threading as thr
import requests
from tkinter.simpledialog import askstring

import time

SERVERIP = '192.168.1.101'
TCPPORT = '8080'
MAX_RETRIES = 10  # Número máximo de tentativas de reconexão

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
        self.sensor_data = {}

        # Cria e inicia a thread de atualização da tabela
        self.update_thread = thr.Thread(target=self.update_table_thread)
        self.update_thread.daemon = True  # Define a thread como um daemon para que ela termine quando o programa principal terminar
        self.update_thread.start()

    def connect_uc(self):
        uc_name = simpledialog.askstring("Conectar-se a uma UC", "Digite o nome da UC:")
        if uc_name:
            response = requests.post("http://" + SERVERIP + ":" + TCPPORT + '/verificar', json={
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
        uc_name = simpledialog.askstring("Instanciar um sensor", "Digite o nome da UC:")

        if uc_name:
            if uc_name in self.subs:
                sensor_count = simpledialog.askinteger("Instanciar um sensor", "Digite a quantidade de sensores:")
                if sensor_count:
                    err = requests.post("http://"+SERVERIP +":"+ TCPPORT + "/instSensor", json={
                        "UcName": uc_name,
                        "SensorCount": sensor_count
                    })
                    if err.status_code != 200:
                        messagebox.showerror("Erro", f"Erro ao conectar: {err}")
            else:
                messagebox.showerror("Erro", f"Erro ao requisitar: Não conectado a unidade de controle!")

    def delete_sensor(self):
        # Solicita a UC e o ID do sensor a ser excluído
        uc_name = askstring("Excluir Sensor", "Digite o nome da UC:")
        sensor_id = simpledialog.askinteger("Excluir Sensor", "Digite o ID do sensor:")

        if uc_name:
            err = requests.post("http://"+SERVERIP +":"+ TCPPORT + "/excludeSensor", json={
                "UcName": uc_name,
                "Sensor_id": sensor_id
                })
            if err.status_code==200:
                messagebox.showinfo("Sucesso", "Exclusão bem-sucedida!")
            else:
                messagebox.showerror("Erro", f"Erro: {err.text}")

    def turn_off_sensor(self):
        # Solicita a UC e o ID do sensor a ser desligado
        uc_name = askstring("Desligar Sensor", "Digite o nome da UC:")

        if uc_name:
            sensor_id = simpledialog.askinteger("Desligar Sensor", "Digite o ID do sensor:")

            err = requests.post("http://"+SERVERIP +":"+ TCPPORT + "/desligarSensor", json={
                "UcName": uc_name,
                "Sensor_id": sensor_id
                })
            if err.status_code==200:
                messagebox.showinfo("Sucesso", "Sensor Desligado!")
            else:
                messagebox.showerror("Erro", f"Erro: {err.text}")

    def turn_on_sensor(self):
        # Solicita a UC e o ID do sensor a ser ligado
        uc_name = askstring("Ligar Sensor", "Digite o nome da UC:")

        if uc_name:
            sensor_id = simpledialog.askinteger("Ligar Sensor", "Digite o ID do sensor:")

            err = requests.post("http://"+SERVERIP +":"+ TCPPORT + "/ligarSensor", json={
                "UcName": uc_name,
                "Sensor_id": sensor_id
                })
            if err.status_code==200:
                messagebox.showinfo("Sucesso", "Sensor ligarSensor!")
            else:
                messagebox.showerror("Erro", f"Erro: {err.text}")

    def update_table(self):
        # Limpa a TreeView
        self.tree.delete(*self.tree.get_children())

        for uc_key, uc_sensors in self.sensor_data.items():

            # Ordena os sensores da UC pelo ID
            if uc_sensors != None:
                sorted_sensors = sorted(uc_sensors, key=lambda x: x['ID'])
                
                for sensor_data in sorted_sensors:
                    uc = sensor_data['UC']
                    id = sensor_data['ID']
                    temp = sensor_data['TEMP']
                    estado = sensor_data['ESTADO']
                    
                    # Insere os valores na TreeView
                    self.tree.insert("", "end", values=(uc, id, temp, estado))

    def update_table_thread(self):
        while True:
            # Atualiza a tabela a cada 1 segundo
            self.update_table()
            time.sleep(0.6)

    def getterSensors(self):
        retries = 0
        while True:
            # Cria o corpo da solicitação JSON com a lista de unidades de controle inscritas
            data = {"subs": self.subs}
            if data["subs"]:
                try:
                    # Envia a solicitação POST para o servidor
                    response = requests.post("http://192.168.1.101:8080/sensors", json=data)

                    # Verifica se a solicitação foi bem-sucedida (código de status 200)
                    if response.status_code == 200:
                        self.sensor_data = response.json()
                        # Remova o aviso de desconexão, se estiver sendo exibido
                        self.hide_offline_message()
                        retries = 0  # Reinicie o contador de tentativas em caso de sucesso
                    elif response.status_code == 404:
                        if response.text in self.subs:
                            self.subs.remove(response.text)
                        # Exibir aviso de desconexão na GUI
                        self.show_offline_message()
                    else:
                        # Exibir aviso de desconexão na GUI
                        self.show_offline_message()

                except requests.ConnectionError as e:
                    # Exibir aviso de desconexão na GUI
                    self.show_offline_message()
                    retries += 1
                    if retries >= MAX_RETRIES:
                        # Se exceder o número máximo de tentativas, pare de tentar e limpe os dados
                        self.sensor_data = {}
                        retries = 0
                        self.subs = []
                    time.sleep(1)  # Espera 1 segundo antes de tentar novamente
                    continue  # Tenta novamente na próxima iteração

                except Exception as e:
                    # Exibir aviso de desconexão na GUI
                    self.show_offline_message()

            time.sleep(0.4)

    def show_offline_message(self):
        # Exibir aviso de desconexão na GUI
        offline_label = tk.Label(self.root, text="Sistema Offline", fg="red")
        offline_label.pack(side="bottom", pady=5, fill="x")
        self.root.update_idletasks()  # Atualize a GUI para garantir que o aviso seja exibido imediatamente

    def hide_offline_message(self):
        # Remover o aviso de desconexão da GUI
        for widget in self.root.winfo_children():
            if widget.winfo_class() == "Label" and widget.cget("text") == "Sistema Offline":
                widget.destroy()
        self.root.update_idletasks()  # Atualize a GUI para garantir que o aviso seja removido imediatamente

def main():
    app = SensorManagementApp(tk.Tk())
    getterThread = thr.Thread(target=app.getterSensors, daemon=True)
    getterThread.start()
    app.root.mainloop()

if __name__ == "__main__":
    main()
