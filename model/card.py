import random

class Card(object):
    """
    Classe responsável pelo gerenciamento de cartas e tickets no jogo.
    
    Attributes:
        size_draw_pile (int): Tamanho da pilha de cartas visíveis.
        max_wilds (int): Número máximo de curingas permitidos na pilha visível.
        possible_colors (list): Lista de cores disponíveis para as cartas.
        cards (list): Lista de todas as cartas do baralho.
        tickets (list): Lista de tickets de destino disponíveis.
        draw_pile (list): Pilha de cartas visíveis para compra.
        discard_pile (list): Pilha de descarte de cartas.
        ticket_discard_pile (list): Pilha de descarte de tickets.
    """
    def __init__(self, size_draw_pile, max_wilds):
        """
        Inicializa uma nova instância da classe Card.
        
        Args:
            size_draw_pile (int): Tamanho da pilha de cartas visíveis.
            max_wilds (int): Número máximo de curingas permitidos na pilha visível.
        """
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
        self._shuffle(self.cards)

        # Lista de tickets de destino (cidade1, cidade2, valor)
        self.tickets = [
            ('Vancouver', 'Seattle', 21),
            ('Helena', 'Portland', 8),
            ('Los Angeles', 'Seattle', 8),
            ('Portland', 'Vancouver', 6),
            ('Calgary', 'Seattle', 17),
            ('Los Angeles', 'Vancouver', 20)
        ]

        self._shuffle(self.tickets)

        # Pilhas de jogo
        self.draw_pile = []
        self.discard_pile = []
        self.ticket_discard_pile = []

        self._add_to_draw_pile()

    def _shuffle(self, cards):
        """
        Embaralha uma lista de cartas ou tickets.
        
        Args:
            cards (list): Lista de cartas ou tickets a serem embaralhados.
        """
        random.shuffle(cards)

    def deal_card(self):
        """
        Retorna uma carta do topo da pilha.
        
        Returns:
            object: Uma carta do topo da pilha ou None se não houver cartas.
        """
        if len(self.cards) == 0:
            self._restock_cards()
        try:
            return self.cards.pop()
        except IndexError:
            print("\n Não há mais cartas no baralho! \n")

    def deal_ticket(self):
        """
        Retorna um ticket de destino.
        
        Returns:
            tuple: Um ticket de destino (cidade1, cidade2, valor) ou None se não houver tickets.
        """
        if len(self.tickets) == 0:
            self.__restock_tickets()
        try:
            return self.tickets.pop()
        except IndexError:
            print("\n Não há mais bilhetes no baralho! \n")

    def deal_cards(self, num_cards):
        """
        Retorna uma lista com várias cartas.
        
        Args:
            num_cards (int): Número de cartas a serem distribuídas.
            
        Returns:
            list: Lista contendo as cartas distribuídas.
        """
        return [self.deal_card() for _ in range(num_cards)]

    def deal_tickets(self, num_tickets):
        """
        Retorna uma lista com vários tickets.
        
        Args:
            num_tickets (int): Número de tickets a serem distribuídos.
            
        Returns:
            list: Lista contendo os tickets distribuídos.
        """
        return [self.deal_ticket() for _ in range(num_tickets)]

    def pick_face_up_card(self, card):
        """
        Permite ao jogador pegar uma carta visível específica.
        
        Args:
            card (object): A carta visível que o jogador deseja pegar.
            
        Returns:
            object: A carta selecionada.
            
        Raises:
            AssertionError: Se a carta não estiver na pilha visível.
        """
        assert card in self.draw_pile
        self.draw_pile.remove(card)
        self._add_to_draw_pile()
        return card

    def pick_face_down(self):
        """
        Permite ao jogador pegar uma carta virada para baixo.
        
        Returns:
            object: Uma carta do topo da pilha.
        """
        return self.deal_card()

    def _add_to_draw_pile(self):
        """
        Reabastece e atualiza a pilha de cartas visíveis.
        """
        next_card = self.deal_card()
        if next_card is not None:
            self.draw_pile.append(next_card)

        if len(self.draw_pile) < self.size_draw_pile:
            self._restock_draw_pile()

        # Se houver muitos curingas, reinicia a pilha
        if self.draw_pile.count('wild') >= self.max_wilds:
            self.add_to_discard(self.draw_pile)
            self.draw_pile = []
            self._add_to_draw_pile()

    def get_draw_pile(self):
        """
        Retorna a pilha de cartas visíveis.
        
        Returns:
            list: Lista contendo as cartas na pilha visível.
        """
        return self.draw_pile

    def add_to_discard(self, cards):
        """
        Adiciona cartas ao descarte.
        
        Args:
            cards (list): Lista de cartas a serem descartadas.
        """
        for card in cards:
            self.discard_pile.append(card)
        if len(self.draw_pile) < self.size_draw_pile:
            self._restock_draw_pile()

    def _restock_draw_pile(self):
        """
        Reabastece a pilha de cartas visíveis com cartas novas.
        """
        while len(self.draw_pile) < self.size_draw_pile:
            if len(self.cards) == 0 and len(self.discard_pile) == 0:
                break
            elif len(self.cards) == 0:
                self._restock_cards()
            next_card = self.deal_card()
            if next_card is not None:
                self.draw_pile.append(next_card)

    def add_to_ticket_discard(self, ticket):
        """
        Adiciona um ticket ao descarte de bilhetes.
        
        Args:
            ticket (tuple): O ticket a ser descartado.
        """
        self.ticket_discard_pile.append(ticket)

    def tickets_left(self):
        """
        Retorna o número de tickets restantes.
        
        Returns:
            int: Número de tickets disponíveis.
        """
        return len(self.tickets)

    def _restock_cards(self):
        """
        Reabastece as cartas com o descarte.
        
        Raises:
            AssertionError: Se ainda houver cartas na pilha principal.
        """
        assert len(self.cards) == 0
        self.cards = self.discard_pile
        self._shuffle(self.cards)
        self.discard_pile = []

    def _restock_tickets(self):
        """
        Reabastece os tickets com o descarte.
        
        Raises:
            AssertionError: Se ainda houver tickets na pilha principal.
        """
        assert len(self.tickets) == 0
        self.tickets = self.ticket_discard_pile
        self._shuffle(self.tickets)
        self.ticket_discard_pile = []

    def num_tickets_left_to_deal(self):
        """
        Retorna o número de tickets que ainda podem ser comprados.
        
        Returns:
            int: Número de tickets disponíveis para compra.
        """
        if len(self.tickets) == 0:
            self._restock_tickets()
        return len(self.tickets)