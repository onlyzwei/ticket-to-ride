package player

import (
	"ticket-to-ride/pkg/game"

	"github.com/mcaci/graphgo/graph"
)

// Scorer define o que um jogador precisa para ser pontuado
// (linhas de trem e tickets)
type Scorer interface {
	TrainLines() []*graph.Edge[game.City]
	Tickets() []game.Ticket
}

// Score calcula a pontuação total do jogador
// Soma pontos das linhas de trem e dos tickets concluídos
func Score(l Scorer) int {
	// Mapeia o tamanho da linha de trem para a quantidade de pontos
	scores := map[int]int{
		1: 1,
		2: 2,
		3: 4,
		4: 7,
		5: 10,
		6: 15,
	}
	var score int

	// Soma os pontos das linhas de trem construídas pelo jogador
	for _, tl := range l.TrainLines() {
		// Obtém o tamanho da linha de trem (número de vagões)
		ln := tl.P.(*game.TrainLineProperty).Weight()
		// Adiciona os pontos correspondentes ao tamanho da linha
		score += scores[ln]
	}

	// Soma os pontos dos tickets concluídos pelo jogador
	for _, t := range l.Tickets() {
		if t.Done {
			// Adiciona o valor do ticket à pontuação
			score += t.Value
		}
	}

	return score
}
