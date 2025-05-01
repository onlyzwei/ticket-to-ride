# -*- coding: utf-8 -*-

import collections
from colorama import Fore, Back, Style, init

from model.board import Board, PlayerBoard
from model.player import Player
from model.card import Card

class Game(object):
    """
    Classe principal do jogo Ticket to Ride. Controla toda a mecânica e regras do jogo.
    
    Atributos:
        size_draw_pile (int): Tamanho da pilha de compra.
        max_wilds (int): Número máximo de cartas curinga permitidas.
        num_tickets_dealt (int): Número de tickets distribuídos por vez.
        size_starting_hand (int): Tamanho da mão inicial.
        ending_train_count (int): Número mínimo de trens para acionar a última rodada.
        points_for_longest_route (int): Pontos concedidos pela rota mais longa.
        starting_num_of_trains (int): Número inicial de trens para cada jogador.
        deck (Card): Baralho de cartas.
        board (Board): Tabuleiro do jogo.
        num_players (int): Número de jogadores.
        players (list): Lista de objetos jogador.
        pos_to_move (int): Posição do jogador atual.
        route_values (dict): Valores de pontos para diferentes tamanhos de rotas.
    """
    def __init__(self, num_players):
        """
        Inicializa o jogo com os parâmetros especificados.
        
        Args:
            num_players (int): Número de jogadores participando do jogo.
        """
        # Configurações do jogo
        self.size_draw_pile = 5
        self.max_wilds = 3
        self.num_tickets_dealt = 3
        self.size_starting_hand = 4

        self.ending_train_count = 3  # Condição de término para acionar a rodada final
        self.points_for_longest_route = 10
        self.starting_num_of_trains = 45
        
        # Inicialização de componentes principais
        self.deck = Card(self.size_draw_pile, self.max_wilds)
        self.board = Board()
        self.num_players = num_players
        self.players = []
        
        self.pos_to_move = 0
        
        # Valores de pontos para rotas de diferentes comprimentos
        self.route_values = {1: 1, 2: 2, 3: 4, 4: 7, 5: 10, 6: 15}

        # Criação e inicialização dos jogadores
        for position in range(num_players):
            starting_hand = self.deck.deal_cards(self.size_starting_hand)
            starting_tickets = None  # Use None em vez de lista vazia
            player_board = PlayerBoard()

            player = Player(
                starting_hand, 
                starting_tickets, 
                player_board, 
                position, 
                self.starting_num_of_trains
            )                          
            self.players.append(player)

    def get_player(self, player_number):
        """
        Retorna o objeto jogador com base no número do jogador.
        
        Args:
            player_number (int): O número do jogador a ser recuperado.
        
        Returns:
            Player: O objeto jogador correspondente.
        """
        return self.players[player_number]
    
    def get_player_name(self, player_number):
        """
        Retorna o nome do jogador com base no número do jogador.
        
        Args:
            player_number (int): Número do jogador.
            
        Returns:
            str: Nome do jogador.
        """
        return self.get_player(player_number).name
    
    def highest_score(self, players):
        """
        Determina qual jogador tem a pontuação mais alta.
        
        Args:
            players (list): Lista de objetos jogador.
            
        Returns:
            Player: Jogador com a maior pontuação.
            
        Note:
            Ainda não implementado completamente.
        """
        # Não implementado ainda
        pass
        
    def advance_one_player(self):
        """
        Avança para o próximo jogador na rotação.
        Atualiza self.pos_to_move para o próximo jogador.
        """
        self.pos_to_move += 1
        self.pos_to_move %= self.num_players
    
    def get_current_player(self):
        """
        Retorna o jogador atual.
        
        Returns:
            Player: O jogador atual.
        """
        return self.players[self.pos_to_move]
    
    def does_player_have_cards_for_edge(self, player, city1, city2):
        """
        Verifica se o jogador tem cartas suficientes para construir uma rota.
        
        Args:
            player (Player): O jogador a verificar.
            city1 (str): Cidade de origem.
            city2 (str): Cidade de destino.
            
        Returns:
            bool: True se o jogador pode construir a rota, False caso contrário.
        """
            
        route_dist = self.board.get_edge_weight(city1, city2)
        route_colors = self.board.get_edge_colors(city1, city2)
        
        for col in route_colors:
            if col == 'grey':
                # Para rotas cinzas, verifica se o jogador tem cartas suficientes de qualquer cor
                if max([x for x in player.hand.values() if x != 'wild']) + player.hand['wild'] >= route_dist:
                    return True
            else:
                # Para rotas coloridas, verifica se tem cartas suficientes da cor específica ou curingas
                route_dist = self.board.get_edge_weight(city1, city2)
                if player.hand[col] + player.hand['wild'] >= route_dist:
                    return True
        return False      
    
    def check_ending_condition(self, player):
        """
        Verifica se a condição de fim de jogo foi atingida.
        
        Args:
            player (Player): O jogador a verificar.
            
        Returns:
            bool: True se o jogador tem menos trens que o limite, False caso contrário.
        """
        return player.get_num_trains() < self.ending_train_count
    
    def initialize(self):
        """
        Inicializa o jogo antes do início das rodadas.
        Os jogadores escolhem nomes e tickets de destino iniciais.
        """
        selected_names = []
        for player in self.players:
            # Escolha de nomes
            count = 0
            name = input(Fore.CYAN + "Jogador " 
                        + str(self.pos_to_move + 1) 
                        + " por favor digite seu nome: " + Style.RESET_ALL
                        )
            while (name in selected_names or len(name) > 50) and count < 5:
                name = input(Fore.RED + "Jogador " 
                            + str(self.pos_to_move + 1) 
                            + " por favor digite seu nome: (Deve ser único) " + Style.RESET_ALL
                            )
                count += 1
                
            if len(name) > 50 or name == '' or name in selected_names:
                name = str(self.pos_to_move + 1)
                player.set_player_name(name)
                selected_names.append(name)
            else:
                player.set_player_name(name)
                selected_names.append(name)
                
            # Escolha de tickets de destino
            print(Fore.YELLOW + "\n--- Escolha de Tickets Iniciais ---" + Style.RESET_ALL)
            self.pick_tickets(player, 2)
            
            self.advance_one_player()

    def print_sep_line(self, group):
        """
        Imprime cada item do grupo em sua própria linha com formatação.
        
        Args:
            group: lista, dicionário, conjunto ou iterável para imprimir.
        """
        print("")
        if isinstance(group, dict) or isinstance(group, collections.Counter):
            for i in group:
                print(f"{Fore.CYAN}{i}\t{Fore.WHITE}{group[i]}{Style.RESET_ALL}")
            print(Fore.YELLOW + "__________________________________________" + Style.RESET_ALL)
        elif isinstance(group, list) or isinstance(group, set):
            for i in group:
                print(Fore.CYAN + str(i) + Style.RESET_ALL)
            print(Fore.YELLOW + "__________________________________________" + Style.RESET_ALL) 
        else:
            print(Fore.CYAN + str(group) + Style.RESET_ALL)
            print(Fore.YELLOW + "__________________________________________" + Style.RESET_ALL)

    def score_player_tickets(self, player):
        """
        Pontua os tickets de destino do jogador e adiciona/subtrai pontos.
        
        Args:
            player (Player): O jogador a pontuar.
        """
        print(Fore.GREEN + f"\nPontuando tickets para {player.name}:" + Style.RESET_ALL)
        
        for ticket in player.tickets:
            city1 = ticket[0]
            city2 = ticket[1]
            value = ticket[2]
            pos_nodes = player.player_board.get_nodes()
            
            # Se alguma das cidades não está no tabuleiro do jogador, subtrai pontos
            if city1 not in pos_nodes or city2 not in pos_nodes:
                player.subtract_points(value)
                print(f"  {Fore.RED}- {city1} para {city2}: -{value} pontos (não concluído){Style.RESET_ALL}")
                continue
                
            # Se existe um caminho entre as cidades, adiciona pontos
            if player.player_board.has_path(city1, city2):
                player.add_points(value)
                print(f"  {Fore.GREEN}+ {city1} para {city2}: +{value} pontos (concluído){Style.RESET_ALL}")
                
    def score_longest_path(self):
        """
        Determina qual jogador tem a rota mais longa e ajusta sua pontuação.
        Adiciona self.points_for_longest_route ao jogador com a rota mais longa.
        """
        print(Fore.YELLOW + "\n===== BÔNUS DE ROTA MAIS LONGA =====" + Style.RESET_ALL)
        
        scores = {x: (0, ()) for x in self.players}
        longest_path = 0
        
        for player in scores:
            # Verifica o caminho mais longo a partir de cada cidade
            for city in player.player_board.get_cities():
                path_info = player.player_board.longest_path(city)
                if path_info[0] > scores[player][0]:
                    scores[player] = path_info
        
            # Atualiza o caminho mais longo global
            if scores[player][0] > longest_path:
                longest_path = scores[player][0]
        
        print(Fore.CYAN + "Tamanho das rotas mais longas por jogador:" + Style.RESET_ALL)
        for player in scores:
            print(f"  {player.name}: {scores[player][0]} conexões")
        
        # Adiciona pontos ao(s) jogador(es) com a rota mais longa
        winners = []
        for player in scores:
            if scores[player][0] == longest_path:
                player.add_points(self.points_for_longest_route)
                winners.append(player.name)
        
        if len(winners) == 1:
            print(f"{Fore.GREEN}Jogador {winners[0]} recebe {self.points_for_longest_route} pontos de bônus!{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}Jogadores {', '.join(winners)} recebem {self.points_for_longest_route} pontos de bônus!{Style.RESET_ALL}")

    def print_all_player_data(self):
        """
        Imprime todos os atributos (não métodos) de todos os jogadores.
        Útil para depuração e análise de fim de jogo.
        """
        for player in self.players:
            print(Fore.YELLOW + player.name + Style.RESET_ALL)
            print(Fore.CYAN + "------------------------------" + Style.RESET_ALL)
            for x in player.__dict__:
                print(f"{Fore.GREEN}{x}: {Fore.WHITE}{player.__dict__[x]}{Style.RESET_ALL}")
                    
            print(Fore.YELLOW + "==============================" + Style.RESET_ALL)

    def play_turn(self, player):
        """
        Permite ao jogador escolher uma ação: pegar cartas, colocar trens ou pegar tickets.
        
        Args:
            player (Player): O jogador atual.
            
        Returns:
            str: Mensagem de conclusão do movimento.
        """
        print(f"\n{Fore.YELLOW}Pontos atuais: {player.get_points()}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Trens restantes: {player.get_num_trains()}{Style.RESET_ALL}\n")
        
        choice = input(f"{Fore.CYAN}Por favor digite: {Fore.WHITE}cards{Fore.CYAN} (cartas), {Fore.WHITE}trains{Fore.CYAN} (trens) ou {Fore.WHITE}tickets{Fore.CYAN}: {Style.RESET_ALL}")
    
        count = 0  # Uma saída do loop em caso de 5 respostas inválidas
        while choice not in ['cards', 'trains', 'tickets'] and count < 5:
            choice = input(f"{Fore.RED}Resposta inválida. Por favor escolha entre {Fore.WHITE}cards{Fore.RED}, "
                           + f"{Fore.WHITE}trains{Fore.RED} ou {Fore.WHITE}tickets{Fore.RED}: {Style.RESET_ALL}")
            count += 1

        if count >= 5:
            return "Movimento concluído"
            
        if choice == 'cards':
            self.pick_cards(player)
            return "Movimento concluído"
        
        elif choice == 'trains':
            self.place_trains(player)
            return "Movimento concluído"
        else:
            self.pick_tickets(player)
            return "Movimento concluído"
    
    def pick_cards(self, player):
        """
        Permite ao jogador pegar cartas, seja da pilha de compra ou das cartas viradas para cima.
        
        Args:
            player (Player): O jogador atual.
            
        Returns:
            str: Mensagem de conclusão do movimento.
        """
        count = 0  # Uma saída do loop em caso de 5 respostas inválidas
        print(f"{Fore.YELLOW}Sua mão consiste em: {Style.RESET_ALL}")
        self.print_sep_line(player.get_hand())
        
        print(f"{Fore.YELLOW}A pilha de compra consiste em: {Style.RESET_ALL}")
        self.print_sep_line(self.deck.get_draw_pile())
        
        # Primeira carta
        choice1 = input(f"{Fore.CYAN}Por favor digite uma carta da lista acima ou "
                        + f"digite '{Fore.WHITE}drawPile{Fore.CYAN}' para comprar do monte: {Style.RESET_ALL}")
        while choice1 not in self.deck.get_draw_pile() + ['drawPile'] and count < 5:
            choice1 = input(f"{Fore.RED}Resposta inválida. Por favor digite uma carta de " 
                            + f"{Fore.WHITE}{str(self.deck.get_draw_pile())}{Fore.RED} "
                            + f"ou digite '{Fore.WHITE}drawPile{Fore.RED}' para comprar do monte: {Style.RESET_ALL}"
                            )
            count += 1
        
        # Adiciona carta à mão do jogador e remove da pilha
        if count >= 5:
            pass
        elif choice1 == 'drawPile':
            chosen_card = self.deck.pick_face_down()
            print(f"{Fore.GREEN}Você selecionou: {Fore.WHITE}{chosen_card}{Style.RESET_ALL}")
            player.add_card_to_hand(chosen_card)
        else:
            player.add_card_to_hand(self.deck.pick_face_up_card(choice1))
            print(f"{Fore.GREEN}Você selecionou: {Fore.WHITE}{choice1}{Style.RESET_ALL}")
        
        # Se a primeira carta escolhida for curinga, encerra o turno
        if choice1 == 'wild':
            print(f"{Fore.YELLOW}Sua mão agora consiste em: {Style.RESET_ALL}")
            self.print_sep_line(player.get_hand()) 
            return "Movimento concluído"

        count = 0
        print(f"{Fore.YELLOW}A pilha de compra consiste em: {Style.RESET_ALL}")
        self.print_sep_line(self.deck.get_draw_pile())
         
        # Segunda carta
        choice2 = input(f"{Fore.CYAN}Por favor digite outra carta da lista acima ou "
                        + f"digite '{Fore.WHITE}drawPile{Fore.CYAN}' para comprar do monte: {Style.RESET_ALL}")
        while choice2 == 'wild' or (choice2 not in self.deck.get_draw_pile() + ['drawPile'] and count < 5):
            choice2 = input(f"{Fore.RED}Resposta inválida. Por favor digite uma carta de " 
                            + f"{Fore.WHITE}{str(self.deck.get_draw_pile())}{Fore.RED} "
                            + f"ou digite '{Fore.WHITE}drawPile{Fore.RED}' \n"
                            + f"NOTA: a segunda escolha não pode ser 'wild': {Style.RESET_ALL}"
                            )
            count += 1
            
        # Adiciona segunda carta à mão do jogador
        if count >= 5:
            return "Movimento concluído"
        elif choice2 == 'drawPile':
            chosen_card = self.deck.pick_face_down()
            print(f"{Fore.GREEN}Você selecionou: {Fore.WHITE}{chosen_card}{Style.RESET_ALL}")
            player.add_card_to_hand(chosen_card)
        else:
            player.add_card_to_hand(self.deck.pick_face_up_card(choice2))
            print(f"{Fore.GREEN}Você selecionou: {Fore.WHITE}{choice2}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}Sua mão agora consiste em: {Style.RESET_ALL}")
        self.print_sep_line(player.get_hand())  
        return "Movimento concluído"
    
    def place_trains(self, player):
        """
        Permite ao jogador colocar trens em uma rota.
        
        Args:
            player (Player): O jogador atual.
            
        Returns:
            str: Mensagem de conclusão do movimento.
        """
        count = 0
        print(f"{Fore.YELLOW}Cidades disponíveis:{Style.RESET_ALL}")

        # Só imprime rotas que são legais dadas as cartas do jogador (ordenadas alfabeticamente)
        legal_routes = [x for x in sorted(self.board.iter_edges()) 
                        if self.does_player_have_cards_for_edge(player, x[0], x[1])]
        
        if not legal_routes:
            print(f"{Fore.RED}Não há rotas disponíveis com suas cartas atuais!{Style.RESET_ALL}")
            return "Movimento concluído"
            
        self.print_sep_line(legal_routes)
        
        print(f"{Fore.YELLOW}Sua mão consiste em: {Style.RESET_ALL}")
        self.print_sep_line(player.get_hand())
        
        # Seleção da cidade de origem
        city1 = input(f"{Fore.CYAN}Por favor digite a cidade de origem da rota desejada: {Style.RESET_ALL}")
        
        while city1 not in self.board.get_cities() and count < 5:
            city1 = input(f"{Fore.RED}Resposta inválida. "
                          + f"Por favor selecione da lista de cidades acima: {Style.RESET_ALL}"
                          )
            count += 1
        
        if count >= 5:
            return "Movimento concluído"
            
        # Verifica se há destinos legais a partir da cidade escolhida
        legal_destinations = [x for x in self.board.graph.neighbors(city1) 
                             if self.does_player_have_cards_for_edge(player, city1, x)]
                             
        if not legal_destinations:
            print(f"{Fore.RED}Você selecionou uma cidade sem destino legal{Style.RESET_ALL}")
            return "Movimento concluído"
        
        # Seleção da cidade de destino
        count = 0
        
        print(f"{Fore.YELLOW}Cidades de destino disponíveis:{Style.RESET_ALL}")
        self.print_sep_line(legal_destinations)
        
        city2 = input(f"{Fore.CYAN}Por favor digite a cidade de destino a partir de " 
                      + f"{Fore.WHITE}{city1}{Fore.CYAN}: {Style.RESET_ALL}"
                      )
        
        while not self.board.has_edge(city1, city2) and count < 5:
            city2 = input(f"{Fore.RED}Resposta inválida. "
                          + f"Por favor digite uma das seguintes cidades "
                          + f"(sem aspas): \n{Fore.WHITE}" 
                          + f"{legal_destinations}{Fore.RED}: {Style.RESET_ALL}"
                          )
            count += 1    
            
        if count >= 5:
            return "Movimento concluído"
    
        # Início da troca de cartas e colocação de trens
        route_dist = self.board.get_edge_weight(city1, city2)
        span_colors = self.board.get_edge_colors(city1, city2)
        
        if len(span_colors) == 0:
            print(f"{Fore.RED}Você selecionou duas cidades sem rota legal{Style.RESET_ALL}")
            return "Movimento concluído"
        
        print(f"\n{Fore.YELLOW}Esta rota tem comprimento: {Style.RESET_ALL}")
        self.print_sep_line(route_dist)
        print(f"{Fore.YELLOW}Sua mão consiste em: {Style.RESET_ALL}")
        self.print_sep_line(player.get_hand())
        
        # Seleção da cor da rota
        if len(span_colors) == 1:
            color = span_colors[0]  # Usa o primeiro elemento, get_edge_colors retorna lista
            print(f"{Fore.GREEN}Esta rota é: {Fore.WHITE}{color}{Style.RESET_ALL}")
        else:
            color = input(f"{Fore.CYAN}Qual cor de trilho você gostaria de reivindicar? ({Fore.WHITE}"
                          + f"{span_colors}{Fore.CYAN} disponíveis): {Style.RESET_ALL}"
                          )
            if color not in span_colors:
                print(f"{Fore.RED}Cor Inválida{Style.RESET_ALL}")
                return "Movimento concluído"
                
        # Verifica se o jogador tem cartas apropriadas para a rota
        if not self.does_player_have_cards_for_edge(player, city1, city2):
            print(f"{Fore.RED}Você não tem cartas suficientes para esta rota{Style.RESET_ALL}")
            return "Movimento concluído"
            
        # Prepara para jogar as cartas
        if color == 'grey':
            avail_color = max(x for x in player.hand.values())
        else:
            avail_color = player.hand[color]

        avail_wild = player.hand['wild']
        
        # Para rotas cinzas, o jogador escolhe a cor para jogar
        if color == 'grey':
            color = input(f"{Fore.CYAN}Que cor você gostaria de jogar "
                          + f"nesta rota cinza? "
                          + f"(escolha uma cor, não 'wild'): {Style.RESET_ALL}"
                         )

            if color not in self.deck.possible_colors:
                print(f"{Fore.RED}Cor Inválida{Style.RESET_ALL}")
                return "Movimento concluído"
                
            avail_color = player.hand[color]
            num_color = input(f"{Fore.CYAN}Quantas cartas {Fore.WHITE}{color}{Fore.CYAN}"
                             + f" você gostaria de jogar? ({Fore.WHITE}"
                             + f"{avail_color}{Fore.CYAN} disponíveis): {Style.RESET_ALL}"
                             )
        else:
            num_color = input(f"{Fore.CYAN}Quantas cartas {Fore.WHITE}"
                             + f"{color}{Fore.CYAN} você gostaria de jogar? ({Fore.WHITE}"
                             + f"{avail_color}{Fore.CYAN} disponíveis) {Style.RESET_ALL}"
                             )
                             
        # Validação de entrada
        if num_color not in [str(x) for x in range(route_dist + 1)]:
            print(f"{Fore.RED}Entrada Inválida{Style.RESET_ALL}")
            return "Movimento concluído"
            
        num_color = int(num_color)  # Converte string para int
        if num_color not in range(0, avail_color + 1):
            print(f"{Fore.RED}Você não tem essa quantidade{Style.RESET_ALL}")
            return "Movimento concluído"

        # Se faltam cartas para cobrir a rota, usa curingas
        if num_color < route_dist:
            num_wild = input(f"{Fore.CYAN}Quantas cartas curinga você gostaria de jogar? ({Fore.WHITE}"
                            + f"{avail_wild}{Fore.CYAN} disponíveis) {Style.RESET_ALL}"
                            )
            num_wild = int(num_wild)
            if num_wild not in range(0, avail_wild + 1):
                print(f"{Fore.RED}Você não tem essa quantidade{Style.RESET_ALL}")
                return "Movimento concluído"
        else:
            num_wild = 0

        # Verifica se é um movimento legal
        if num_wild + num_color != route_dist:
            print(f"{Fore.RED}As cartas selecionadas não cobrem adequadamente a rota{Style.RESET_ALL}")
            return "Movimento concluído"
        
        # Reivindica a rota para o jogador
        player.player_board.add_edge(city1, city2, route_dist, color)
        
        # Remove a rota do tabuleiro principal
        self.board.remove_connection(city1, city2, color)
        
        # Calcula pontos
        points_earned = self.route_values[route_dist]
        player.add_points(points_earned)
        print(f"{Fore.GREEN}Você ganhou {points_earned} pontos com esta rota!{Style.RESET_ALL}")
    
        # Remove cartas da mão do jogador
        player.remove_cards_from_hand(color, num_color)
        player.remove_cards_from_hand('wild', num_wild)
        
        # Adiciona cartas à pilha de descarte
        self.deck.add_to_discard([color for x in range(num_color)] 
                              + ['wild' for x in range(num_wild)]
                              )
        
        # Remove trens do estoque do jogador
        player.play_num_trains(route_dist)
        
        print(f"{Fore.YELLOW}Número de trens restantes para jogar: {Style.RESET_ALL}")
        self.print_sep_line(player.get_num_trains())  
                    
        return "Movimento concluído"
    
    def pick_tickets(self, player, min_num_to_select=1):
        """
        Permite ao jogador pegar novos tickets de destino.
        
        Args:
            player (Player): O jogador atual.
            min_num_to_select (int): Número mínimo de tickets a selecionar.
            
        Returns:
            str: Mensagem de conclusão do movimento.
        """
        count = 0
        num_tickets_to_deal = min(self.deck.num_tickets_left_to_deal(), 
                               self.num_tickets_dealt)
        if num_tickets_to_deal <= 0:
            print(f"{Fore.RED}Não restam mais tickets! Movimento concluído{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Todos os seus tickets: {Style.RESET_ALL}")
            self.print_sep_line(player.get_tickets())
            return
            
        tickets = self.deck.deal_tickets(num_tickets_to_deal)

        # Atribui um número a cada ticket para facilitar a escolha
        tickets = {x[0]: x[1] for x in zip(range(len(tickets)), tickets)}
        print(f"{Fore.YELLOW}Por favor selecione pelo menos {min_num_to_select}: {Style.RESET_ALL}")
        
        self.print_sep_line(tickets)

        choices = set()
        choice = ''

        # Loop de seleção de tickets
        while True:
            try:
                choice = input("Selecione o número correspondente aos "
                               + "tickets acima, digite 'done' quando terminar: "
                               )
                choices.add(tickets[int(choice)])
            except: 
                if choice != 'done':
                    print("Escolha Inválida: ")
            
            if choice == 'done':
                if len(choices) >= min_num_to_select:
                    break
                else:
                    print(f"Deve selecionar pelo menos {min_num_to_select}")
            if count > 7:
                break
            count += 1
            if len(choices) >= min_num_to_select:
                break
        
        # Adiciona tickets à pilha de descarte ou à mão do jogador
        for ticket in tickets.values():
            if ticket in choices:
                player.add_ticket(ticket)
                print(f"Você selecionou: {ticket}")
            else:
                self.deck.add_to_ticket_discard(ticket)
       
        print(f"{len(self.deck.tickets)}, {len(self.deck.ticket_discard_pile)}")    
                      
        print("Todos os seus tickets: ")
        self.print_sep_line(player.get_tickets())
        
        return "Movimento concluído"
