# -*- coding: utf-8 -*-

from colorama import Fore, Style
from util.terminal import print_sep_line
from time import sleep

class Train(object):
    def __init__(self, board, route_values):
        self.board = board
        self.route_values = route_values

    def does_player_have_cards_for_edge(self, player, city1, city2):
        route_length = self.board.get_edge_weight(city1, city2)
        available_colors = self.board.get_edge_colors(city1, city2)

        for color in available_colors:
            if color == 'cinza':
                regular_cards = []
                for card_type, count in player.hand.items():
                    if card_type != 'coringa':
                        regular_cards.append(count)
                
                # o jogador deve ter ao menos uma carta regular
                # para reivindicar uma rota cinza
                if len(regular_cards) == 0:
                    continue

                best_color_count = max(regular_cards)
                wild_cards = player.hand['coringa']
                if best_color_count + wild_cards >= route_length:
                    return True
            else:
                color_cards = player.hand[color]
                wild_cards = player.hand['coringa']
                if color_cards + wild_cards >= route_length:
                    return True
        return False

    def _get_legal_routes(self, player):
        legal_routes = []
        # Itera sobre as bordas do tabuleiro e verifica se o jogador pode fazer a rota
        for edge in sorted(self.board.iter_edges()):
            if self.does_player_have_cards_for_edge(player, edge[0], edge[1]):
                legal_routes.append(edge)

        return legal_routes
    
    def _get_legal_destinations(self, player, city1):
        """
        Retorna uma lista de cidades de destino legais a partir de uma cidade de origem.
        Uma cidade de destino é legal se o jogador tiver cartas suficientes para fazer a rota.
        """
        legal_destinations = []
        for neighbor in self.board.graph.neighbors(city1):
            if self.does_player_have_cards_for_edge(player, city1, neighbor):
                legal_destinations.append(neighbor)
        
        return legal_destinations
    
    def show_cities(self, player):
        print(f"{Fore.YELLOW}Cidades disponíveis:{Style.RESET_ALL}")
        legal_routes = self._get_legal_routes(player)

        # Se não houver rotas legais, exibe uma mensagem de erro
        if not legal_routes:
            print(f"{Fore.RED}Não há rotas disponíveis com suas cartas atuais!{Style.RESET_ALL}")
            sleep(5)
            return
        
        print_sep_line(legal_routes)
        print('\n')

    
    def place_trains(self, player, deck):

        city1 = self._input_city("origem", self.board.get_cities())
        if not city1:
            return

        legal_destinations = self._get_legal_destinations(player, city1)
        if not legal_destinations:
            print(f"{Fore.RED}Você selecionou uma cidade sem destino legal.{Style.RESET_ALL}")
            sleep(5)
            return

        print(f"{Fore.YELLOW}Cidades de destino disponíveis:{Style.RESET_ALL}")
        print_sep_line(legal_destinations)
        city2 = self._input_city("destino", legal_destinations, city1)
        if not city2:
            return

        success = self._process_route_selection(player, city1, city2, deck)
        if success:
            print(f"{Fore.GREEN}Você colocou trens com sucesso na rota {city1} -> {city2}.{Style.RESET_ALL}")
            sleep(5)

    def _input_city(self, tipo, opcoes, origem=None):
        prompt = f"{Fore.CYAN}Por favor, digite a cidade de {tipo}" + \
                 (f" a partir de {Fore.WHITE}{origem}{Fore.CYAN}" if origem else "") + \
                 f": {Style.RESET_ALL}"
        
        cidade = input(prompt)
        while cidade not in opcoes:
            cidade = input(f"{Fore.RED}Resposta inválida. Por favor, selecione da lista acima: {Style.RESET_ALL}")
        
        return cidade

    def _process_route_selection(self, player, city1, city2, deck):
        route_dist = self.board.get_edge_weight(city1, city2)
        span_colors = self.board.get_edge_colors(city1, city2)

        if not span_colors:
            print(f"{Fore.RED}Você selecionou duas cidades sem rota legal.{Style.RESET_ALL}")
            sleep(5)
            return False

        print(f"{Fore.YELLOW}Esta rota tem comprimento: {route_dist} {Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Sua mão consiste em: {Style.RESET_ALL}")
        print_sep_line(player.get_hand())

        if len(span_colors) == 1:
            color = span_colors[0]
            print(f"{Fore.GREEN}Esta rota é: {Fore.WHITE}{color}{Style.RESET_ALL}")
        else:
            # para o caso de multigrafo / nao estamos lidando com iso por enquanto!!!!!!!!!!
            color = input(f"{Fore.CYAN}Qual cor de trilho você gostaria de reivindicar? ({Fore.WHITE}{span_colors}{Fore.CYAN} disponíveis): {Style.RESET_ALL}")
            if color not in span_colors:
                print(f"{Fore.RED}Cor inválida.{Style.RESET_ALL}")
                sleep(5)
                return False

        return self._select_cards_for_route(player, city1, city2, color, route_dist, deck)

    def _select_cards_for_route(self, player, city1, city2, color, route_dist, deck):
        # Verificar se o jogador tem cartas suficientes
        if not self.does_player_have_cards_for_edge(player, city1, city2):
            print(f"{Fore.RED}Você não tem cartas suficientes para esta rota{Style.RESET_ALL}")
            return False
        
        # Obter cartas disponíveis
        if color in player.hand:
            avail_color = player.hand[color]
        else:
            avail_color = 0
            
        avail_wild = player.hand['coringa']

        # Tratamento especial para rotas cinzas
        if color == 'cinza':

            color = input(f"{Fore.CYAN}Que cor você gostaria de jogar nesta rota cinza? (escolha uma cor, não 'coringa'): {Style.RESET_ALL}")

            # Verificar se a cor é válida
            while color not in deck.possible_colors:
                color = input(f"{Fore.RED}Cor inválida. Por favor, escolha uma cor válida: {Style.RESET_ALL}")
            
            # Atualizar cartas disponíveis para a nova cor
            if color in player.hand:
                avail_color = player.hand[color]
            else:
                avail_color = 0

        # Entrada para número de cartas coloridas
        num_color = 0
        num_wild = 0

        while True:
            try:
                entrada = input(f"{Fore.CYAN}Quantas cartas {Fore.WHITE}{color}{Fore.CYAN} você gostaria de jogar? ({Fore.WHITE}{avail_color}{Fore.CYAN} disponíveis): {Style.RESET_ALL}")
                num_color = int(entrada)

                if num_color < 0:
                    print(f"{Fore.RED}Você não pode jogar um número negativo de cartas!{Style.RESET_ALL}")
                    continue

                if num_color > avail_color:
                    print(f"{Fore.RED}Você não tem tantas cartas {color}!{Style.RESET_ALL}")
                    continue

                if num_color < route_dist:
                    while True:
                        try:
                            entrada = input(f"{Fore.CYAN}Quantas cartas coringa você gostaria de jogar? ({Fore.WHITE}{avail_wild}{Fore.CYAN} disponíveis): {Style.RESET_ALL}")
                            num_wild = int(entrada)

                            if num_wild < 0:
                                print(f"{Fore.RED}Você não pode jogar um número negativo de curingas!{Style.RESET_ALL}")
                                continue

                            if num_wild > avail_wild:
                                print(f"{Fore.RED}Você não tem tantos curingas!{Style.RESET_ALL}")
                                continue

                            break  # entrada válida para curingas
                        except ValueError:
                            print(f"{Fore.RED}Entrada inválida - digite um número inteiro.{Style.RESET_ALL}")

                total_cartas = num_color + num_wild
                if total_cartas != route_dist:
                    print(f"{Fore.RED}As cartas selecionadas não cobrem adequadamente a rota. Você precisa de exatamente {route_dist} cartas.{Style.RESET_ALL}")
                    continue

                break  # entrada válida geral
            except ValueError:
                print(f"{Fore.RED}Entrada Inválida - você deve digitar um número.{Style.RESET_ALL}")

        # Se chegou até aqui, pode completar a colocação da rota
        resultado = self._complete_route_placement(player, city1, city2, color, route_dist, num_color, num_wild, deck)
        return resultado

    def _complete_route_placement(self, player, city1, city2, color, route_dist, num_color, num_wild, deck):
        player.player_board.add_edge(city1, city2, route_dist, color)
        self.board.remove_connection(city1, city2, color)

        points_earned = self.route_values[route_dist]
        player.add_points(points_earned)
        print(f"{Fore.GREEN}Você ganhou {points_earned} pontos com esta rota!{Style.RESET_ALL}")

        player.remove_cards_from_hand(color, num_color)
        player.remove_cards_from_hand('coringa', num_wild)

        deck.add_to_discard([color] * num_color + ['coringa'] * num_wild)

        player.play_num_trains(route_dist)
        print(f"{Fore.YELLOW}Número de trens restantes para jogar: {Style.RESET_ALL}")
        print_sep_line(player.get_num_trains())

        return True