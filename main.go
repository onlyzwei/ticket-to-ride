package main

import (
	"log"
	"net/http"
	"ticket-to-ride\pkg\api"
)

func main() {
	http.HandleFunc("/api/game/create", api.CreateGameHandler)
	http.HandleFunc("/api/game/state", api.GetGameStateHandler)
	http.HandleFunc("/api/game/play", api.PlayMoveHandler)
	http.HandleFunc("/api/game/buy-train-card", api.BuyTrainCardHandler)
	http.HandleFunc("/api/game/swap-tickets", api.SwapTicketHandler)

	log.Println("Servidor iniciado em :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
