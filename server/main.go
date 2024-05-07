package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
	"strconv"
	"strings"
	"time"
)

func main() {
	Addr := "192.168.1.101"
	httpPort := 8080
	tcpPort := 8081
	udpPort := 8082

	done := make(chan struct{})

	// iniciando go routines para cada acesso no servidor
	go func() {
		defer close(done)
		http.HandleFunc("/sensors", getSensors)
		http.HandleFunc("/instSensor", instSensors)
		http.HandleFunc("/verificar", verificar)
		http.HandleFunc("/excludeSensor", excludeSensor)
		http.HandleFunc("/ligarSensor", ligarSensor)
		http.HandleFunc("/desligarSensor", desligarSensor)

		log.Printf("HTTP server is ON %s:%d\n", Addr, httpPort)
		log.Fatal(http.ListenAndServe(fmt.Sprintf("%s:%d", Addr, httpPort), nil))
	}()

	go checkConnections()

	go func() {
		defer close(done)
		receiverTCP(Addr, tcpPort, done)
	}()

	go func() {
		defer close(done)
		receiverUDP(Addr, udpPort, done)
	}()

	<-done
}

// Unidades de controle
type CUnits struct {
	Name      string
	Sensores  map[string]Sensor
	Inscritos []string
	IP        net.IP
}

// mensagens da aplicacao
type Mensagem struct {
	Tipo     int
	Conteudo string
}

// sensores (dispositivos implementados)
type Sensor struct {
	ID     string `json:"ID"`
	UC     string `json:"UC"`
	TEMP   int    `json:"TEMP"`
	ESTADO int    `json:"ESTADO"`
}

// comando de intanciamento de sensores
type InstJson struct {
	UcName      string `json:"ucName"`
	SensorCount int    `json:"sensorCount"`
}

// "BANCO DE DADOS" das unidades de controle
var UnidadesControle = make(map[string]CUnits)

// receptor TCP
func receiverTCP(ip string, TCPport int, done chan struct{}) {
	listener, err := net.Listen("tcp", fmt.Sprintf("%s:%d", ip, TCPport))
	if err != nil {
		fmt.Println("Erro ao criar o listener TCP:", err)
		return
	}
	defer listener.Close()

	for {
		select {
		case <-done:
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

// o manipulador de conexoes, recebe os dados do pedido de conexao feito pelas unidades de controle
// e registra a UC no sistema
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
		registerUC(infor.Conteudo, conn)
	}
}

// checa se as unidades de controle ainda estao conectadas
func checkConnections() {
	for {
		time.Sleep(15 * time.Second)

		var keysToRemove []string

		for ucName, unit := range UnidadesControle {
			conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:8083", unit.IP.String()), 2*time.Second)
			if err != nil {
				fmt.Println("Unidade de controle desconectada:", ucName)
				keysToRemove = append(keysToRemove, ucName)
				continue
			}
			conn.Close()
		}

		for _, key := range keysToRemove {
			delete(UnidadesControle, key)
		}
	}
}

// registra as unidades de controle no sistema
func registerUC(nomeUC string, conn net.Conn) {
	if _, ok := UnidadesControle[nomeUC]; ok {
		conn.Write([]byte("ERROA1"))
		return
	}

	UnidadesControle[nomeUC] = CUnits{
		Name:     nomeUC,
		Sensores: make(map[string]Sensor),
		IP:       conn.RemoteAddr().(*net.TCPAddr).IP,
	}
	conn.Write([]byte("Unidade de controle registrada com sucesso"))
}

// receptor de conexoes UDP (dados dos sensores)
func receiverUDP(ip string, UDPport int, done chan struct{}) {
	address, err := net.ResolveUDPAddr("udp", fmt.Sprintf("%s:%d", ip, UDPport))
	if err != nil {
		fmt.Println("Erro ao resolver endereço UDP:", err)
		return
	}

	conn, err := net.ListenUDP("udp", address)
	if err != nil {
		fmt.Println("Erro ao criar conexão UDP:", err)
		return
	}
	defer conn.Close()

	buffer := make([]byte, 1024)

	for {
		select {
		case <-done:
			return
		default:
			n, _, err := conn.ReadFromUDP(buffer)
			if err != nil {
				fmt.Println("Erro ao ler dados UDP:", err)
				continue
			}

			freshInfo(string(buffer[:n]))
		}
	}
}

// atualiza as informacoes dos sensores no "banco de dados"
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

	unit, ok := UnidadesControle[ucID]
	if !ok {
		fmt.Println("Unidade de controle não encontrada:", ucID)
		return
	}

	sensor, ok := unit.Sensores[sensorID]
	sensor = Sensor{ID: sensorID, TEMP: temp, ESTADO: estado, UC: ucID}
	unit.Sensores[sensorID] = sensor

}

// estrutura basica de requisicao
type Requisicao struct {
	UcName   string `json:"UcName"`
	SensorID int    `json:"Sensor_id"`
}

// multiplexador basico para lidar com requisicoes para alterar os sensores
func controlSensor(w http.ResponseWriter, r *http.Request, command string) {
	if r.Method != "POST" {
		http.Error(w, http.StatusText(http.StatusMethodNotAllowed), http.StatusMethodNotAllowed)
		return
	}

	var item Requisicao
	err := json.NewDecoder(r.Body).Decode(&item)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	err = sendCommandToUC(item.UcName, string(rune(item.SensorID))+"|"+command)

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	if command == "exclude" {
		delete(UnidadesControle[item.UcName].Sensores, strconv.Itoa(item.SensorID))
	}

	w.WriteHeader(http.StatusOK)
}

// rota para ligar algum sensor
func ligarSensor(w http.ResponseWriter, r *http.Request) {
	controlSensor(w, r, "ligar")
}

// rota para desligar algum sensor
func desligarSensor(w http.ResponseWriter, r *http.Request) {
	controlSensor(w, r, "desligar")
}

// rota para excluir algum sensor
func excludeSensor(w http.ResponseWriter, r *http.Request) {
	controlSensor(w, r, "exclude")
}

// rota para verificar se alguma unidade de controle especifica existe no sistema
func verificar(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, http.StatusText(http.StatusMethodNotAllowed), http.StatusMethodNotAllowed)
		return
	}

	var item struct {
		UnitName string `json:"UcName"`
	}
	err := json.NewDecoder(r.Body).Decode(&item)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

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
	err := json.NewDecoder(r.Body).Decode(&item)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	err = sendCommandToUC(item.UcName, string(rune(item.SensorCount))+"|"+"instSen")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Comando enviado com sucesso para a unidade de controle"))
}

// envia o comando para a unidade de controle correspondente
func sendCommandToUC(UcName string, command string) error {
	ip := UnidadesControle[UcName].IP

	conn, err := net.Dial("tcp", ip.String()+":8083")

	if err != nil {
		return fmt.Errorf("Erro ao conectar ao endereço IP %s: %s", ip, err.Error())
	}
	defer conn.Close()

	_, err = conn.Write([]byte(command))

	if err != nil {
		return fmt.Errorf("Erro ao enviar comando para a unidade de controle: %s", err.Error())
	}

	fmt.Println("Comando enviado com sucesso para a unidade de controle:", UcName)
	return nil
}

// rota para pegar as informacoes dos sensores
func getSensors(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, http.StatusText(http.StatusMethodNotAllowed), http.StatusMethodNotAllowed)
		return
	}

	var data struct {
		Subs []string `json:"subs"`
	}
	err := json.NewDecoder(r.Body).Decode(&data)
	if err != nil {
		http.Error(w, "Erro ao decodificar os dados JSON da solicitação", http.StatusBadRequest)
		return
	}

	sensoresData := make(map[string][]Sensor)

	for _, topico := range data.Subs {
		unit, ok := UnidadesControle[topico]
		if !ok {
			http.Error(w, topico, http.StatusNotFound)
			return
		}

		var sensores []Sensor

		for _, sensor := range unit.Sensores {
			sensores = append(sensores, sensor)
		}

		sensoresData[topico] = sensores
	}

	jsonData, err := json.Marshal(sensoresData)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")

	w.WriteHeader(http.StatusOK)
	w.Write(jsonData)
}
