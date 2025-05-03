# -*- coding: utf-8 -*-

from colorama import Fore, Back, Style, init
from model.board import Board, PlayerBoard
from model.player import Player
from model.card import Card
from model.ticket import Ticket
from model.train import Train
from util.terminal import clear_screen, print_sep_line
from time import sleep

class Game(object):
    def __init__(self, num_players):
        self.size_draw_pile = 5
        self.max_wilds = 3
        self.size_starting_hand = 4
        self.ending_train_count = 3
        self.points_for_longest_route = 10
        self.starting_num_of_trains = 45
        self.deck = Card(self.size_draw_pile, self.max_wilds)
        self.board = Board()
        self.num_players = num_players
        self.players = []
        self.pos_to_move = 0
        self.route_values = {1: 1, 2: 2, 3: 4, 4: 7, 5: 10, 6: 15}
        self.ticket_handler = Ticket(self.deck)  # Instância do gerenciador de tickets
        self.train_handler = Train(self.board, self.route_values)  # Instância do gerenciador de trens
        
        for position in range(num_players):
            starting_hand = self.deck.deal_cards(self.size_starting_hand)
            starting_tickets = []
            player_board = PlayerBoard()
            player = Player(
                starting_hand, 
                starting_tickets, 
                player_board, 
                position, 
                self.starting_num_of_trains
            )                          
            self.players.append(player)
                
    def advance_one_player(self):
        self.pos_to_move += 1
        self.pos_to_move %= self.num_players
    
    def get_current_player(self):
        return self.players[self.pos_to_move]
    
    def check_ending_condition(self, player):
        return player.get_num_trains() < self.ending_train_count
    
    def initialize(self):
        selected_names = []
        for player in self.players:
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
            print(Fore.YELLOW + "\n--- Escolha de Tickets Iniciais ---" + Style.RESET_ALL)
            self.ticket_handler.pick_tickets(player, 2)  # Usando o Ticket para selecionar tickets
            self.advance_one_player()
    
    def score_longest_path(self):
        print(Fore.YELLOW + "\n===== BÔNUS DE ROTA MAIS LONGA =====" + Style.RESET_ALL)
        scores = {x: (0, ()) for x in self.players}
        longest_path = 0
        for player in scores:
            for city in player.player_board.get_cities():
                path_info = player.player_board.longest_path(city)
                if path_info[0] > scores[player][0]:
                    scores[player] = path_info
            if scores[player][0] > longest_path:
                longest_path = scores[player][0]
        print(Fore.CYAN + "Tamanho das rotas mais longas por jogador:" + Style.RESET_ALL)
        for player in scores:
            print(f"  {player.name}: {scores[player][0]} conexões")
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
        for player in self.players:
            print(Fore.YELLOW + player.name + Style.RESET_ALL)
            print(Fore.CYAN + "------------------------------" + Style.RESET_ALL)
            for x in player.__dict__:
                print(f"{Fore.GREEN}{x}: {Fore.WHITE}{player.__dict__[x]}{Style.RESET_ALL}")
            print(Fore.YELLOW + "==============================" + Style.RESET_ALL)

    def play_turn(self, player):
        print(f"\n{Fore.YELLOW}Pontos atuais: {player.get_points()}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Trens restantes: {player.get_num_trains()}{Style.RESET_ALL}\n")
        choice = input(f"{Fore.CYAN}Por favor digite: {Fore.WHITE}cards{Fore.CYAN} (cartas), {Fore.WHITE}trains{Fore.CYAN} (trens) ou {Fore.WHITE}tickets{Fore.CYAN}: {Style.RESET_ALL}")
        count = 0
        while choice not in ['cards', 'trains', 'tickets'] and count < 5:
            choice = input(f"{Fore.RED}Resposta inválida. Por favor escolha entre {Fore.WHITE}cards{Fore.RED}, "
                           + f"{Fore.WHITE}trains{Fore.RED} ou {Fore.WHITE}tickets{Fore.RED}: {Style.RESET_ALL}")
            count += 1
        if count >= 5:
            return
        if choice == 'cards':
            self._pick_cards(player)
        elif choice == 'trains':
            self.train_handler.place_trains(player, self.deck)
        else:
            self.ticket_handler.pick_tickets(player)  # Usando o Ticket
    
    def _pick_cards(self, player):
        count = 0
        
        # Mostrar as cartas na mão do jogador
        print(f"{Fore.YELLOW}Sua mão consiste em: {Style.RESET_ALL}")
        hand = player.get_hand()
        if hand:
            print_sep_line(hand)
        else:
            print(f"{Fore.WHITE}Sua mão está vazia{Style.RESET_ALL}")
            
        # Mostrar a pilha de compra (cartas viradas para cima)
        print(f"{Fore.YELLOW}A pilha de compra consiste em: {Style.RESET_ALL}")
        draw_pile = self.deck.get_draw_pile()
        if draw_pile:
            print_sep_line(draw_pile)
        else:
            print(f"{Fore.WHITE}A pilha de compra está vazia{Style.RESET_ALL}")
            
        # Primeira escolha de carta
        choice1 = input(f"{Fore.CYAN}Por favor digite uma carta da lista acima ou "
                        + f"digite '{Fore.WHITE}drawPile{Fore.CYAN}' para comprar do monte: {Style.RESET_ALL}")
                                                
        while choice1 not in draw_pile + ['drawPile'] and count < 5:
            choice1 = input(f"{Fore.RED}Resposta inválida. Por favor digite uma carta de " 
                            + f"{Fore.WHITE}{str(draw_pile)}{Fore.RED} "
                            + f"ou digite '{Fore.WHITE}drawPile{Fore.RED}' para comprar do monte: {Style.RESET_ALL}")
            count += 1
            
        if count >= 5:
            return "Movimento cancelado"
            
        # Processar a escolha da primeira carta
        if choice1 == 'drawPile':
            chosen_card = self.deck.pick_face_down()
            print(f"{Fore.GREEN}Você comprou do monte: {Fore.WHITE}{chosen_card}{Style.RESET_ALL}")
            player.add_card_to_hand(chosen_card)
        else:
            chosen_card = self.deck.pick_face_up_card(choice1)
            print(f"{Fore.GREEN}Você selecionou: {Fore.WHITE}{choice1}{Style.RESET_ALL}")
            player.add_card_to_hand(chosen_card)
            
        # Se escolheu um curinga (wild), termina o turno
        if choice1 == 'wild':
            print(f"{Fore.YELLOW}Sua mão agora consiste em: {Style.RESET_ALL}")
            print_sep_line(player.get_hand()) 
            return "Movimento concluído"
            
        # Segunda escolha de carta (atualiza a pilha de compra primeiro)
        count = 0
        print(f"{Fore.YELLOW}A pilha de compra atualizada: {Style.RESET_ALL}")
        draw_pile = self.deck.get_draw_pile()  # Pega a pilha atualizada
        if draw_pile:
            print_sep_line(draw_pile)
        else:
            print(f"{Fore.WHITE}A pilha de compra está vazia{Style.RESET_ALL}")
            
        choice2 = input(f"{Fore.CYAN}Por favor digite outra carta da lista acima ou "
                        + f"digite '{Fore.WHITE}drawPile{Fore.CYAN}' para comprar do monte: {Style.RESET_ALL}")
                        
        while (choice2 == 'wild' or choice2 not in draw_pile + ['drawPile']) and count < 5:
            choice2 = input(f"{Fore.RED}Resposta inválida. Por favor digite uma carta de " 
                            + f"{Fore.WHITE}{str(draw_pile)}{Fore.RED} "
                            + f"ou digite '{Fore.WHITE}drawPile{Fore.RED}' \n"
                            + f"NOTA: a segunda escolha não pode ser 'wild': {Style.RESET_ALL}")
            count += 1
            
        if count >= 5:
            return "Movimento cancelado"
            
        # Processar a escolha da segunda carta
        if choice2 == 'drawPile':
            chosen_card = self.deck.pick_face_down()
            print(f"{Fore.GREEN}Você comprou do monte: {Fore.WHITE}{chosen_card}{Style.RESET_ALL}")
            player.add_card_to_hand(chosen_card)
        else:
            chosen_card = self.deck.pick_face_up_card(choice2)
            print(f"{Fore.GREEN}Você selecionou: {Fore.WHITE}{choice2}{Style.RESET_ALL}")
            player.add_card_to_hand(chosen_card)
            
        # Mostrar a mão atualizada
        print(f"{Fore.YELLOW}Sua mão agora consiste em: {Style.RESET_ALL}")
        print_sep_line(player.get_hand())
        
        return "Movimento concluído"