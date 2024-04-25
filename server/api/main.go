package main

import (
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/sensors", getSensors)

	println("API IS ON: 8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

type Sensor struct {
	ID    int
	Temp  int
	State int
}

func getSensors(w http.ResponseWriter, request *http.Request) {

	if request.Method != "GET" {
		http.Error(w, http.StatusText(http.StatusMethodNotAllowed), http.StatusMethodNotAllowed)
		return
	}

	w.Header().Set("Content-Type", "application/json")

}
