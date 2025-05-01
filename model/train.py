# -*- coding: utf-8 -*-

from colorama import Fore, Style
from util.terminal import print_sep_line

class Train(object):
    def __init__(self, board, route_values):
        self.board = board
        self.route_values = route_values
    
    def does_player_have_cards_for_edge(self, player, city1, city2):
        route_length = self.board.get_edge_weight(city1, city2)
        available_colors = self.board.get_edge_colors(city1, city2)
        
        for color in available_colors:
            # Para rotas cinzas, o jogador pode usar qualquer cor
            if color == 'grey':
                # Encontra a cor com mais cartas na mão (exceto curingas)
                regular_cards = [count for color, count in player.hand.items() if color != 'wild']
                if not regular_cards:  # Se não tiver cartas regulares
                    continue
                    
                best_color_count = max(regular_cards)
                wild_cards = player.hand['wild']
                
                # Verifica se a soma das cartas é suficiente para a rota
                if best_color_count + wild_cards >= route_length:
                    return True
            else:
                # Para rotas coloridas, o jogador precisa de cartas da cor específica + curingas
                color_cards = player.hand[color]
                wild_cards = player.hand['wild']
                
                # Verifica se a soma das cartas é suficiente para a rota
                if color_cards + wild_cards >= route_length:
                    return True
                    
        return False

    def place_trains(self, player, deck):
        count = 0
        print(f"{Fore.YELLOW}Cidades disponíveis:{Style.RESET_ALL}")
        legal_routes = [x for x in sorted(self.board.iter_edges()) 
                        if self.does_player_have_cards_for_edge(player, x[0], x[1])]
        if not legal_routes:
            print(f"{Fore.RED}Não há rotas disponíveis com suas cartas atuais!{Style.RESET_ALL}")
            return "Movimento concluído"
        print_sep_line(legal_routes)
        print(f"{Fore.YELLOW}Sua mão consiste em: {Style.RESET_ALL}")
        print_sep_line(player.get_hand())
        city1 = input(f"{Fore.CYAN}Por favor digite a cidade de origem da rota desejada: {Style.RESET_ALL}")
        while city1 not in self.board.get_cities() and count < 5:
            city1 = input(f"{Fore.RED}Resposta inválida. "
                          + f"Por favor selecione da lista de cidades acima: {Style.RESET_ALL}"
                          )
            count += 1
        if count >= 5:
            return "Movimento concluído"
        legal_destinations = [x for x in self.board.graph.neighbors(city1) 
                             if self.does_player_have_cards_for_edge(player, city1, x)]
        if not legal_destinations:
            print(f"{Fore.RED}Você selecionou uma cidade sem destino legal{Style.RESET_ALL}")
            return "Movimento concluído"
        count = 0
        print(f"{Fore.YELLOW}Cidades de destino disponíveis:{Style.RESET_ALL}")
        print_sep_line(legal_destinations)
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
        
        return self._process_route_selection(player, city1, city2, deck)
    
    def _process_route_selection(self, player, city1, city2, deck):
        route_dist = self.board.get_edge_weight(city1, city2)
        span_colors = self.board.get_edge_colors(city1, city2)
        if len(span_colors) == 0:
            print(f"{Fore.RED}Você selecionou duas cidades sem rota legal{Style.RESET_ALL}")
            return "Movimento concluído"
        print(f"\n{Fore.YELLOW}Esta rota tem comprimento: {Style.RESET_ALL}")
        print_sep_line(route_dist)
        print(f"{Fore.YELLOW}Sua mão consiste em: {Style.RESET_ALL}")
        print_sep_line(player.get_hand())
        
        # Determinar a cor da rota
        if len(span_colors) == 1:
            color = span_colors[0]
            print(f"{Fore.GREEN}Esta rota é: {Fore.WHITE}{color}{Style.RESET_ALL}")
        else:
            color = input(f"{Fore.CYAN}Qual cor de trilho você gostaria de reivindicar? ({Fore.WHITE}"
                          + f"{span_colors}{Fore.CYAN} disponíveis): {Style.RESET_ALL}"
                          )
            if color not in span_colors:
                print(f"{Fore.RED}Cor Inválida{Style.RESET_ALL}")
                return "Movimento concluído"
        
        return self._select_cards_for_route(player, city1, city2, color, route_dist, deck)
    
    def _select_cards_for_route(self, player, city1, city2, color, route_dist, deck):
        if not self.does_player_have_cards_for_edge(player, city1, city2):
            print(f"{Fore.RED}Você não tem cartas suficientes para esta rota{Style.RESET_ALL}")
            return "Movimento concluído"
            
        if color == 'grey':
            avail_color = max((x for x in player.hand.items() if x[0] != 'wild'), key=lambda x: x[1])[1]
        else:
            avail_color = player.hand[color]
        avail_wild = player.hand['wild']
        
        # Para rotas cinzas, o jogador precisa especificar a cor
        if color == 'grey':
            color = input(f"{Fore.CYAN}Que cor você gostaria de jogar "
                          + f"nesta rota cinza? "
                          + f"(escolha uma cor, não 'wild'): {Style.RESET_ALL}"
                         )
            if color not in deck.possible_colors:
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
        
        if num_color not in [str(x) for x in range(route_dist + 1)]:
            print(f"{Fore.RED}Entrada Inválida{Style.RESET_ALL}")
            return "Movimento concluído"
            
        num_color = int(num_color)
        if num_color not in range(0, avail_color + 1):
            print(f"{Fore.RED}Você não tem essa quantidade{Style.RESET_ALL}")
            return "Movimento concluído"
            
        # Se o jogador não usar todas as cartas coloridas, precisa completar com curingas
        num_wild = 0
        if num_color < route_dist:
            num_wild = input(f"{Fore.CYAN}Quantas cartas curinga você gostaria de jogar? ({Fore.WHITE}"
                            + f"{avail_wild}{Fore.CYAN} disponíveis) {Style.RESET_ALL}"
                            )
            num_wild = int(num_wild)
            if num_wild not in range(0, avail_wild + 1):
                print(f"{Fore.RED}Você não tem essa quantidade{Style.RESET_ALL}")
                return "Movimento concluído"
                
        if num_wild + num_color != route_dist:
            print(f"{Fore.RED}As cartas selecionadas não cobrem adequadamente a rota{Style.RESET_ALL}")
            return "Movimento concluído"
            
        return self._complete_route_placement(player, city1, city2, color, route_dist, num_color, num_wild, deck)
    
    def _complete_route_placement(self, player, city1, city2, color, route_dist, num_color, num_wild, deck):
        # Adicionar a rota ao tabuleiro do jogador
        player.player_board.add_edge(city1, city2, route_dist, color)
        # Remover a conexão do tabuleiro principal
        self.board.remove_connection(city1, city2, color)
        
        # Calcular e adicionar pontos
        points_earned = self.route_values[route_dist]
        player.add_points(points_earned)
        print(f"{Fore.GREEN}Você ganhou {points_earned} pontos com esta rota!{Style.RESET_ALL}")
        
        # Remover cartas da mão do jogador
        player.remove_cards_from_hand(color, num_color)
        player.remove_cards_from_hand('wild', num_wild)
        
        # Adicionar cartas à pilha de descarte
        deck.add_to_discard([color for x in range(num_color)] 
                          + ['wild' for x in range(num_wild)]
                          )
        
        # Usar os trens do jogador
        player.play_num_trains(route_dist)
        print(f"{Fore.YELLOW}Número de trens restantes para jogar: {Style.RESET_ALL}")
        print_sep_line(player.get_num_trains())  
        
        return "Movimento concluído"