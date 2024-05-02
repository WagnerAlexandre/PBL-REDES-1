import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import threading as thr
import requests
import time




class InitialScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Identificação")
        self.root.geometry("300x200")

        self.identifier = ""

        self.label = tk.Label(root, text="Digite seu nome identificador:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(root)
        self.entry.pack(pady=5)

        self.button = tk.Button(root, text="Confirmar", command=self.confirm_identifier)
        self.button.pack(pady=5)

    def confirm_identifier(self):
        self.identifier = self.entry.get()
        self.root.destroy()

class SensorManagementApp:
    def __init__(self, root, identifier):
        self.root = root
        self.root.title("Sensor Management")
        self.identifier = identifier

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
            response = requests.post('http://localhost:8080/subscribe',json={
                "userName": self.identifier
            }).json()
            
            pass

    def instantiate_sensor(self):
        #uc_name = simpledialog.askstring("Instanciar um sensor", "Digite o nome da UC:")
        uc_name = "TST"
        if uc_name:
            #sensor_count = simpledialog.askinteger("Instanciar um sensor", "Digite a quantidade de sensores:")
            sensor_count = 4
            if sensor_count:
  
            
                err = requests.post("http://localhost:8080/instSensor",json={
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

        try:

            # Limpa a tabela
            for row in self.tree.get_children():
                self.tree.delete(row)
            
            # Adiciona os dados atualizados à tabela
            for data in self.sensor_data:
                self.tree.insert("", "end", values=(data["UC"], data["ID"], data["TEMP"], data["Estado"]))
        except tk.TclError:
            pass
            # Restaura a seleção
            if self.selected_item:
                self.tree.selection_set(self.selected_item)


    def update_table_thread(self):
        while True:
            # Atualiza a tabela a cada 1 segundo
            self.update_table()
            time.sleep(1)


def main():
    root = tk.Tk()
    # Exibe a tela inicial para pegar o nome identificador
    initial_screen = InitialScreen(root)
    root.wait_window(initial_screen.root)

    # Se um identificador foi fornecido, inicia a aplicação principal
    if initial_screen.identifier:
        app = SensorManagementApp(tk.Tk(), initial_screen.identifier)
        app.root.mainloop()

if __name__ == "__main__":
    main()
