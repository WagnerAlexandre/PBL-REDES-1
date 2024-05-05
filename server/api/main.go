package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
	"strconv"
	"strings"
)

var UnidadesControle = make(map[string]CUnits)

func receiverTCP(ip string, TCPport int, done chan struct{}) {
	listener, err := net.Listen("tcp", fmt.Sprintf("%s:%d", ip, TCPport))
	if err != nil {
		fmt.Println("Erro ao criar o listener TCP:", err)
		return
	}
	defer listener.Close()

	fmt.Println("Receptor TCP está escutando em", listener.Addr())

	for {
		select {
		case <-done:
			fmt.Println("Receptor TCP encerrado.")
			return
		default:
			conn, err := listener.Accept()
			if err != nil {
				fmt.Println("Erro ao aceitar a conexão:", err)
				continue
			}
			go handleConnection(conn)
		}
	}
}

type Mensagem struct {
	Tipo     int
	Conteudo string
}

func handleConnection(conn net.Conn) {
	defer conn.Close()

	buffer := make([]byte, 1024)
	n, err := conn.Read(buffer)
	if err != nil {
		fmt.Println("Erro ao ler os dados:", err)
		return
	}

	var infor Mensagem

	err = json.Unmarshal(buffer[:n], &infor)
	if err != nil {
		fmt.Println("Erro ao decodificar a mensagem:", err)
		return
	}

	if infor.Tipo == 1 {
		// Chame a função registerUC passando o nome da unidade de controle
		registerUC(infor.Conteudo, conn)
	}
}

func registerUC(nomeUC string, conn net.Conn) {
	// Verifique se a unidade de controle já existe no mapa UnidadesControle
	if _, ok := UnidadesControle[nomeUC]; ok {
		// Se a unidade de controle já existe, envie uma mensagem de erro para a conexão indicando que a operação falhou
		conn.Write([]byte("ERROA1"))
		return
	}

	// Caso contrário, crie uma nova unidade de controle e adicione ao mapa
	UnidadesControle[nomeUC] = CUnits{
		Name:     nomeUC,
		Sensores: make(map[int]Sensor), // Inicialize o mapa de sensores
		IP:       conn.RemoteAddr().(*net.TCPAddr).IP,
	}
	// Envie uma mensagem de sucesso para a conexão indicando que a operação foi bem-sucedida
	conn.Write([]byte("Unidade de controle registrada com sucesso"))
}

type CUnits struct {
	Name      string
	Sensores  map[int]Sensor
	Inscritos []string
	IP        net.IP
}

func receiverUDP(ip string, UDPport int, done chan struct{}) {
	// Crie um endereço UDP
	address, err := net.ResolveUDPAddr("udp", fmt.Sprintf("%s:%d", ip, UDPport))
	if err != nil {
		fmt.Println("Erro ao resolver endereço UDP:", err)
		return
	}

	// Crie uma conexão UDP
	conn, err := net.ListenUDP("udp", address)
	if err != nil {
		fmt.Println("Erro ao criar conexão UDP:", err)
		return
	}
	defer conn.Close()

	fmt.Println("Receptor UDP está escutando em", conn.LocalAddr())

	// Buffer para armazenar os dados recebidos
	buffer := make([]byte, 1024)

	// Loop infinito para aguardar mensagens UDP
	for {
		select {
		case <-done:
			fmt.Println("Receptor UDP encerrado.")
			return
		default:
			// Aguardar a recepção de dados
			n, _, err := conn.ReadFromUDP(buffer)
			if err != nil {
				fmt.Println("Erro ao ler dados UDP:", err)
				continue
			}

			//atualizar no dicionario os dados recebidos:
			freshInfo(string(buffer[:n]))
		}
	}
}

func freshInfo(info string) {
	pack := strings.Split(info, "|")
	id, _ := strconv.Atoi(pack[1])   // Convertendo o ID do sensor para inteiro
	temp, _ := strconv.Atoi(pack[2]) // Convertendo a temperatura para inteiro

	// Verifique se a unidade de controle existe no mapa UnidadesControle
	unit, ok := UnidadesControle[pack[0]]
	if !ok {
		fmt.Println("Unidade de controle não encontrada:", pack[0])
		return
	}

	// Verifique se o sensor existe no mapa de sensores da unidade de controle
	sensor, ok := unit.Sensores[id]
	if !ok {
		// Se o sensor não existir, crie um novo sensor e adicione ao mapa de sensores da unidade de controle
		unit.Sensores[id] = Sensor{ID: id}
		sensor = unit.Sensores[id]
	}

	// Atualize a temperatura do sensor
	sensor.TEMP = temp

}

func main() {
	ip := "192.168.1.101"
	TCPport := 8080
	UDPport := 1080
	done := make(chan struct{})

	go receiverTCP(ip, TCPport, done)
	go receiverUDP(ip, UDPport, done)

	http.HandleFunc("/sensors", getSensors)
	http.HandleFunc("/instSensor", instSensors)
	http.HandleFunc("/subscribe", subscribe)

	fmt.Println("API is ON :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))

	<-done

}

func subscribe(w http.ResponseWriter, r *http.Request) {
	var item struct {
		UserName string `json:"userName"`
		UnitName string `json:"unitName"`
	}
	err := json.NewDecoder(r.Body).Decode(&item)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	unit, ok := UnidadesControle[item.UnitName]
	if !ok {
		http.Error(w, "Unidade de controle não encontrada", http.StatusNotFound)
		return
	}

	unit.Inscritos = append(unit.Inscritos, item.UserName)
	w.WriteHeader(http.StatusCreated)
}

type Sensor struct {
	ID     int
	UC     string
	TEMP   int
	ESTADO int
}

type InstJson struct {
	UcName      string `json:"ucName"`
	SensorCount int    `json:"sensorCount"`
}

type User struct {
	Name string
	Subs []string
}

func instSensors(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, http.StatusText(http.StatusMethodNotAllowed), http.StatusMethodNotAllowed)
		return
	}
	var item InstJson
	json.NewDecoder(r.Body).Decode(&item)

}

func getSensors(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
		http.Error(w, http.StatusText(http.StatusMethodNotAllowed), http.StatusMethodNotAllowed)
		return
	}
}
