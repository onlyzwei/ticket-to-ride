package game

import (
	"math/rand/v2"
	"strconv"

	"github.com/mcaci/graphgo/graph"
)

// --- Tipos principais do jogo ---
type City = string

// Estrutura de propriedades de uma linha de trem
// Usada para armazenar informações de cada rota
// (distância, cor, ocupação, etc)
type TrainLineProperty struct {
	Distance   int
	Color      Color
	Occupied   bool
	OccupiedBy string
}

type TrainStation = graph.Vertex[City]
type TrainLine graph.Edge[City]
type Board = graph.Graph[City]

// --- Cores e cartas ---
type Color int8

const (
	All Color = iota
	Blue
	Red
	Green
	Yellow
	White
	Pink
	Orange
	Black
)

type Card = Color

var availableTrainCars = 40

var TotalCards = map[Color]int{
	All:    14,
	Blue:   12,
	Red:    12,
	Green:  12,
	Yellow: 12,
	White:  12,
	Pink:   12,
	Orange: 12,
	Black:  12,
}

// --- Tickets (objetivos dos jogadores) ---
type Ticket struct {
	X, Y  City
	Value int
	Done  bool
	Ok    bool
}

func (t Ticket) String() string {
	return string(t.X) + " -> " + string(t.Y) + " : " + strconv.Itoa(t.Value) + "."
}

// Sorteia n tickets e remove do slice original
func GetTickets(n int, tickets *[]Ticket) []Ticket {
	t := *tickets
	ids := rand.Perm(len(t))
	for i := 0; i < n; i++ {
		t[ids[i]], t[i] = t[i], t[ids[i]]
	}
	selected := t[:n]
	*tickets = t[n:]
	return selected
}

// --- Funções utilitárias para o tabuleiro ---

// Retorna true se existe pelo menos uma rota livre
func FreeRoutesAvailable(b Board) bool {
	return FindLineFunc(func(tl *TrainLine) bool {
		return !tl.P.(*TrainLineProperty).Occupied
	}, b) != nil
}

// Retorna um novo tabuleiro apenas com rotas livres
func FreeRoutesBoard(b Board) Board {
	frb := graph.New[City](graph.ArcsListType, false)
	for _, v := range b.Vertices() {
		frb.AddVertex(v)
	}
	for _, e := range b.Edges() {
		if !e.P.(*TrainLineProperty).Occupied {
			frb.AddEdge(e)
		}
	}
	return frb
}

// Busca uma cidade pelo nome
func FindCity(name City, b Board) *TrainStation {
	for _, v := range b.Vertices() {
		if v.E == name {
			return (*TrainStation)(v)
		}
	}
	return nil
}

// Busca uma linha de trem que satisfaça a função f
func FindLineFunc(f func(*TrainLine) bool, b Board) *TrainLine {
	for _, e := range b.Edges() {
		t := TrainLine(*e)
		if f(&t) {
			return &t
		}
	}
	return nil
}

// Representação textual de uma linha de trem
func (t TrainLine) String() string {
	return string(t.X.E) + " -> " + strconv.Itoa(t.P.(*TrainLineProperty).Distance) + " -> " + string(t.Y.E)
}

// Métodos utilitários para TrainLineProperty
func (t TrainLineProperty) Weight() int { return t.Distance }
func (t *TrainLineProperty) Occupy()    { t.Occupied = true }
func (t *TrainLineProperty) Free()      { t.Occupied = false }
