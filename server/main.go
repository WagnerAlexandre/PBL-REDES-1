package main

import (
	"fmt"
	"net"
)

type Sensor struct {
	UC     string
	ID     int
	TEMP   int
	ESTADO int
}

func main() {
	// Endereço e porta do servidor
	udpAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:65000")
	if err != nil {
		fmt.Println("Erro ao resolver o endereço UDP:", err)
		return
	}

	// Cria um socket UDP
	conn, err := net.ListenUDP("udp", udpAddr)
	if err != nil {
		fmt.Println("Erro ao criar o socket UDP:", err)
		return
	}
	defer conn.Close()

	fmt.Println("Aguardando mensagens...")

	for {
		buffer := make([]byte, 1024)
		n, addr, err := conn.ReadFromUDP(buffer)
		if err != nil {
			fmt.Println("Erro ao ler os dados:", err)
			continue
		}

		data := string(buffer[:n])
		fmt.Printf("Mensagem recebida de %s: %s\n", addr, data)
	}
}
