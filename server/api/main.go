package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

var Usuarios []User
var UnidadesControle []CUnits

func main() {

	http.HandleFunc("/sensors", getSensors)
	http.HandleFunc("/instSensor", instSensors)
	http.HandleFunc("/subscribe", subscribe)
	http.HandleFunc("/register", registerUC)

	fmt.Println("API is ON :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func registerUC(w http.ResponseWriter, r *http.Request) {
	var newUnit CUnits
	err := json.NewDecoder(r.Body).Decode(&newUnit)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	UnidadesControle = append(UnidadesControle, newUnit)
	w.WriteHeader(http.StatusCreated)
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
