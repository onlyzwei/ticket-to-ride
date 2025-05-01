import collections

class Player(object):
    """
    Classe que representa um jogador no jogo Ticket to Ride.
    Controla mão de cartas, tickets, pontos e o tabuleiro individual do jogador.
    """

    def __init__(self, starting_hand, starting_tickets, player_board, player_position, num_trains):
        # Inicializa os atributos do jogador com mão, tickets, tabuleiro, posição e trens
        self.name = ''  # Nome será solicitado no primeiro turno

        # Usa Counter para representar a mão e permitir remoções eficientes
        self.hand = collections.Counter(starting_hand)

        # Inicializa os tickets, marcando como não completados
        self.tickets = {} if starting_tickets is None else {x: False for x in starting_tickets}

        self.num_trains = num_trains
        self.points = 0
        self.player_position = player_position
        self.player_board = player_board  # Tabuleiro individual do jogador

    # Remove cartas da mão do jogador
    def remove_cards_from_hand(self, color, num_color):
        assert self.hand[color] >= num_color
        self.hand[color] -= num_color

    # Adiciona uma carta à mão do jogador
    def add_card_to_hand(self, card):
        if card is not None:
            self.hand[card] += 1

    # Adiciona um ticket à lista de tickets do jogador
    def add_ticket(self, ticket):
        self.tickets[ticket] = False

    # Marca um ticket como completo
    def complete_ticket(self, ticket):
        assert ticket in self.tickets
        self.tickets[ticket] = True

    # Retorna a mão atual do jogador
    def get_hand(self):
        return self.hand

    # Adiciona pontos ao jogador
    def add_points(self, num_points):
        self.points += num_points

    # Subtrai pontos do jogador
    def subtract_points(self, num_points):
        self.points -= num_points

    # Retorna a pontuação atual
    def get_points(self):
        return self.points

    # Retorna os tickets do jogador
    def get_tickets(self):
        return self.tickets

    # Retorna a quantidade de trens restantes
    def get_num_trains(self):
        return self.num_trains

    # Diminui a quantidade de trens após uma jogada
    def play_num_trains(self, num_trains):
        assert num_trains <= self.num_trains
        self.num_trains -= num_trains

    # Define o nome do jogador
    def set_player_name(self, name):
        self.name = name

    # Retorna o nome do jogador
    def get_name(self):
        return self.name
