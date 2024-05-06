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

type CUnits struct {
	Name      string
	Sensores  map[string]Sensor
	Inscritos []string
	IP        net.IP
}
type Mensagem struct {
	Tipo     int
	Conteudo string
}

type Sensor struct {
	ID     string `json:"ID"`
	UC     string `json:"UC"`
	TEMP   int    `json:"TEMP"`
	ESTADO int    `json:"ESTADO"`
}

type InstJson struct {
	UcName      string `json:"ucName"`
	SensorCount int    `json:"sensorCount"`
}

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
		Sensores: make(map[string]Sensor), // Inicialize o mapa de sensores
		IP:       conn.RemoteAddr().(*net.TCPAddr).IP,
	}
	// Envie uma mensagem de sucesso para a conexão indicando que a operação foi bem-sucedida
	conn.Write([]byte("Unidade de controle registrada com sucesso"))
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

	ucID := pack[0]
	sensorID := pack[1]

	temp, err := strconv.Atoi(pack[2])
	if err != nil {
		fmt.Println("Erro ao converter temperatura:", err)
		return
	}

	estado, err := strconv.Atoi(pack[3])
	if err != nil {
		fmt.Println("Erro ao converter estado:", err)
		return
	}

	// Verifique se a unidade de controle existe no mapa UnidadesControle
	unit, ok := UnidadesControle[ucID]
	if !ok {
		fmt.Println("Unidade de controle não encontrada:", ucID)
		return
	}

	// Verifique se o sensor existe no mapa de sensores da unidade de controle
	sensor, ok := unit.Sensores[sensorID]

	// Se o sensor não existir, crie um novo sensor e adicione ao mapa de sensores da unidade de controle
	sensor = Sensor{ID: sensorID, TEMP: temp, ESTADO: estado, UC: ucID}
	unit.Sensores[sensorID] = sensor

}

func main() {
	// Endereço e porta para o servidor HTTP
	Addr := "192.168.1.101"
	httpPort := 8080

	// porta para o servidor TCP/IP
	tcpPort := 8081

	//  porta para o servidor UDP
	udpPort := 8082

	done := make(chan struct{})

	// Inicie o servidor HTTP em uma goroutine separada
	go func() {
		defer close(done)
		http.HandleFunc("/sensors", getSensors)
		http.HandleFunc("/instSensor", instSensors)
		http.HandleFunc("/verificar", verificar)

		log.Printf("HTTP server is ON %s:%d\n", Addr, httpPort)
		log.Fatal(http.ListenAndServe(fmt.Sprintf("%s:%d", Addr, httpPort), nil))
	}()

	// Inicie o servidor TCP/IP em uma goroutine separada
	go func() {
		defer close(done)
		receiverTCP(Addr, tcpPort, done)
	}()

	// Inicie o servidor UDP em uma goroutine separada
	go func() {
		defer close(done)
		receiverUDP(Addr, udpPort, done)
	}()

	<-done // Aguarde a conclusão de todos os servidores
}

type User struct {
	Name string
	Subs []string
}

func verificar(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, http.StatusText(http.StatusMethodNotAllowed), http.StatusMethodNotAllowed)
		return
	}

	// Decodificar o corpo da solicitação em uma estrutura
	var item struct {
		UnitName string `json:"UcName"`
	}
	err := json.NewDecoder(r.Body).Decode(&item)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Verificar se a unidade de controle está presente no mapa
	if _, ok := UnidadesControle[item.UnitName]; !ok {
		http.Error(w, "Unidade de controle não encontrada", http.StatusNotFound)
		return
	}

	w.WriteHeader(http.StatusOK)
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
	if r.Method != "POST" {
		http.Error(w, http.StatusText(http.StatusMethodNotAllowed), http.StatusMethodNotAllowed)
		return
	}

	// Decodificar o JSON do corpo da solicitação para obter os tópicos (unidades de controle)
	var data struct {
		Subs []string `json:"subs"`
	}
	err := json.NewDecoder(r.Body).Decode(&data)
	if err != nil {
		http.Error(w, "Erro ao decodificar os dados JSON da solicitação", http.StatusBadRequest)
		return
	}

	// Mapa para armazenar os dados de todos os sensores
	sensoresData := make(map[string][]Sensor)

	// Iterar sobre cada tópico (unidade de controle)
	for _, topico := range data.Subs {
		// Verificar se o tópico existe no mapa UnidadesControle
		unit, ok := UnidadesControle[topico]
		if !ok {
			fmt.Println("Unidade de controle não encontrada:", topico)
			continue
		}

		// Lista para armazenar os sensores desta unidade de controle
		var sensores []Sensor

		// Iterar sobre os sensores desta unidade de controle
		for _, sensor := range unit.Sensores {
			// Adicionar os dados do sensor à lista de sensores
			sensores = append(sensores, sensor)
		}

		// Adicionar a lista de sensores ao mapa de sensoresData
		sensoresData[topico] = sensores
	}

	// Codificar os dados dos sensores em JSON
	jsonData, err := json.Marshal(sensoresData)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Configurar o cabeçalho da resposta
	w.Header().Set("Content-Type", "application/json")

	// Escrever os dados JSON na resposta
	w.WriteHeader(http.StatusOK)
	w.Write(jsonData)
}
