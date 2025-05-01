import random

class Card(object):
    def __init__(self, size_draw_pile, max_wilds):
        # Inicializa os parâmetros básicos
        self.size_draw_pile = size_draw_pile
        self.max_wilds = max_wilds

        # Cores disponíveis para as cartas
        self.possible_colors = [
            "red", "orange", "yellow",
            "green", "blue", "purple",
            "white", "black"
        ]

        # Geração das cartas: 14 curingas + 12 de cada cor
        self.cards = ["wild" for _ in range(14)] + [
            color for color in self.possible_colors for _ in range(12)
        ]

        # Embaralha as cartas
        self.shuffle(self.cards)

        # Lista de tickets de destino (cidade1, cidade2, valor)
        self.tickets = [
            ('Vancouver', 'Seattle', 21),
            ('Helena', 'Portland', 8),
            ('Los Angeles', 'Seattle', 8),
            ('Portland', 'Vancouver', 6),
            ('Calgary', 'Seattle', 17),
            ('Los Angeles', 'Vancouver', 20)
        ]

        self.shuffle(self.tickets)

        # Pilhas de jogo
        self.draw_pile = []
        self.discard_pile = []
        self.ticket_discard_pile = []

        self.add_to_draw_pile()

    # Embaralha uma lista de cartas
    def shuffle(self, cards):
        random.shuffle(cards)

    # Retorna uma carta do topo da pilha
    def deal_card(self):
        if len(self.cards) == 0:
            self.restock_cards()
        try:
            return self.cards.pop()
        except IndexError:
            print("\n Não há mais cartas no baralho! \n")

    # Retorna um ticket de destino
    def deal_ticket(self):
        if len(self.tickets) == 0:
            self.restock_tickets()
        try:
            return self.tickets.pop()
        except IndexError:
            print("\n Não há mais bilhetes no baralho! \n")

    # Retorna uma lista com várias cartas
    def deal_cards(self, num_cards):
        return [self.deal_card() for _ in range(num_cards)]

    # Retorna uma lista com vários tickets
    def deal_tickets(self, num_tickets):
        return [self.deal_ticket() for _ in range(num_tickets)]

    # Permite o jogador pegar uma carta visível
    def pick_face_up_card(self, card):
        assert card in self.draw_pile
        self.draw_pile.remove(card)
        self.add_to_draw_pile()
        return card

    # Permite o jogador pegar uma carta virada para baixo
    def pick_face_down(self):
        return self.deal_card()

    # Reabastece e atualiza a pilha de cartas visíveis
    def add_to_draw_pile(self):
        next_card = self.deal_card()
        if next_card is not None:
            self.draw_pile.append(next_card)

        if len(self.draw_pile) < self.size_draw_pile:
            self.restock_draw_pile()

        # Se houver muitos curingas, reinicia a pilha
        if self.draw_pile.count('wild') >= self.max_wilds:
            self.add_to_discard(self.draw_pile)
            self.draw_pile = []
            self.add_to_draw_pile()

    # Retorna a pilha de cartas visíveis
    def get_draw_pile(self):
        return self.draw_pile

    # Retorna a pilha de descarte
    def get_discard_pile(self):
        return self.discard_pile

    # Adiciona cartas ao descarte
    def add_to_discard(self, cards):
        for card in cards:
            self.discard_pile.append(card)
        if len(self.draw_pile) < self.size_draw_pile:
            self.restock_draw_pile()

    # Reabastece a pilha de cartas visíveis com cartas novas
    def restock_draw_pile(self):
        while len(self.draw_pile) < self.size_draw_pile:
            if len(self.cards) == 0 and len(self.discard_pile) == 0:
                break
            elif len(self.cards) == 0:
                self.restock_cards()
            next_card = self.deal_card()
            if next_card is not None:
                self.draw_pile.append(next_card)

    # Adiciona um ticket ao descarte de bilhetes
    def add_to_ticket_discard(self, ticket):
        self.ticket_discard_pile.append(ticket)

    # Retorna o valor de pontos de um ticket
    def get_ticket_point_value(self, ticket):
        return ticket[2]

    # Retorna o número de cartas restantes
    def cards_left(self):
        return len(self.cards)

    # Retorna o número de tickets restantes
    def tickets_left(self):
        return len(self.tickets)

    # Reabastece as cartas com o descarte
    def restock_cards(self):
        assert len(self.cards) == 0
        self.cards = self.discard_pile
        self.shuffle(self.cards)
        self.discard_pile = []

    # Reabastece os tickets com o descarte
    def restock_tickets(self):
        assert len(self.tickets) == 0
        self.tickets = self.ticket_discard_pile
        self.shuffle(self.tickets)
        self.ticket_discard_pile = []

    # Retorna o número de tickets que ainda podem ser comprados
    def num_tickets_left_to_deal(self):
        if len(self.tickets) == 0:
            self.restock_tickets()
        return len(self.tickets)

    # Verifica se uma pilha está vazia
    def is_empty(self, pile):
        return len(pile) == 0
