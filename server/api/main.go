package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
)

var Usuarios []User
var UnidadesControle []CUnits

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
		registerUC(infor.Conteudo)
	}

}

func registerUC(nomeUC string) {
	var newUnit CUnits
	newUnit.Name = nomeUC
	UnidadesControle = append(UnidadesControle, newUnit)
}

func receiverUDP(ip string, UDPport int) {

}

func main() {
	ip := "127.0.0.1"
	TCPport := 8080
	UDPport := 1080

	done := make(chan struct{})

	go receiverTCP(ip, TCPport, done)

	go receiverUDP(ip, UDPport)

	http.HandleFunc("/sensors", getSensors)
	http.HandleFunc("/instSensor", instSensors)
	http.HandleFunc("/subscribe", subscribe)

	fmt.Println("API is ON :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
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

	for i := range UnidadesControle {
		if UnidadesControle[i].Name == item.UnitName {
			UnidadesControle[i].Inscritos = append(UnidadesControle[i].Inscritos, item.UserName)
			w.WriteHeader(http.StatusCreated)
			return
		}
	}

	http.Error(w, "Unidade de controle não encontrada", http.StatusNotFound)
}

type CUnits struct {
	Name      string
	Sensores  []Sensor
	Inscritos []string
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
