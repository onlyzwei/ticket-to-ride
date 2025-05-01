# -*- coding: utf-8 -*-

from colorama import Fore, Style
from util.terminal import clear_screen, print_sep_line

class Ticket:
    def __init__(self, deck):
        self.deck = deck
        self.num_tickets_dealt = 3
        
    def pick_tickets(self, player, min_num_to_select=1):
        # Verifica se há tickets disponíveis
        clear_screen()
        available_tickets = self.deck.num_tickets_left_to_deal()
        tickets_to_deal = available_tickets
        if available_tickets > self.num_tickets_dealt:
            tickets_to_deal = self.num_tickets_dealt

        if tickets_to_deal <= 0:
            print(f"{Fore.RED}Não restam mais tickets!{Style.RESET_ALL}")
            self._print_sep_line(player.get_tickets())
            print(f"{Fore.YELLOW}Todos os seus tickets: {Style.RESET_ALL}")
            self._print_sep_line(player.get_tickets())
            return

        # Distribui os tickets e cria um dicionário para indexá-los
        dealt_tickets = self.deck.deal_tickets(tickets_to_deal)
        indexed_tickets = {}

        for index in range(tickets_to_deal):
            indexed_tickets[index] = dealt_tickets[index]

        # Mostra os tickets disponíveis
        print(f"{Fore.YELLOW}Por favor selecione pelo menos {min_num_to_select} ticket(s): {Style.RESET_ALL}")
        self._print_sep_line(indexed_tickets)

        # Coleta as escolhas do jogador
        selected_tickets = set()  # Usar set para evitar duplicatas
        while len(selected_tickets) < tickets_to_deal:
            user_input = input("Digite o número do ticket ou 'done' para finalizar: ")

            if user_input == 'done':
                if len(selected_tickets) >= min_num_to_select:
                    break
                else:
                    print(f"Deve selecionar pelo menos {min_num_to_select} ticket(s)")
                    continue

            try:
                ticket_index = int(user_input)
                if ticket_index in indexed_tickets:
                    if indexed_tickets[ticket_index] not in selected_tickets:
                        selected_tickets.add(indexed_tickets[ticket_index])
                    else:
                        print("Este ticket já foi selecionado. Escolha outro.")
                else:
                    print("Número de ticket inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número ou 'done'.")

        # Processa os tickets
        for ticket_index, ticket in indexed_tickets.items():
            if ticket in selected_tickets:
                player.add_ticket(ticket)
            else:
                self.deck.add_to_ticket_discard(ticket)  # Assumindo que a pilha de descarte é reutilizada corretamente

        # Exibe o estado final
        clear_screen()
        self._print_sep_line()
        print(f"Tickets restantes no baralho: {len(self.deck.tickets)}")
        print(f"Tickets na pilha de descarte: {len(self.deck.ticket_discard_pile)}")
        print(f"{Fore.YELLOW}Todos os seus tickets:{Style.RESET_ALL}")
        self._print_sep_line(player.get_tickets())
    
    def score_player_tickets(self, player):
        """Calcula a pontuação dos tickets completados por um jogador"""
        print(Fore.GREEN + f"\nPontuando tickets para {player.name}:" + Style.RESET_ALL)
        for ticket in player.tickets:
            city1 = ticket[0]
            city2 = ticket[1]
            value = ticket[2]
            pos_nodes = player.player_board.get_nodes()
            if city1 not in pos_nodes or city2 not in pos_nodes:
                player.subtract_points(value)
                print(f"  {Fore.RED}- {city1} para {city2}: -{value} pontos (não concluído){Style.RESET_ALL}")
                continue
            if player.player_board.has_path(city1, city2):
                player.add_points(value)
                print(f"  {Fore.GREEN}+ {city1} para {city2}: +{value} pontos (concluído){Style.RESET_ALL}")
                
    def _print_sep_line(self, info=None):
        """Imprime uma linha separadora com informações opcionais"""
        if info is None:
            print(Fore.CYAN + "------------------------------" + Style.RESET_ALL)
        else:
            print(Fore.CYAN + "------------------------------" + Style.RESET_ALL)
            print(f"{Fore.WHITE}{info}{Style.RESET_ALL}")
            print(Fore.CYAN + "------------------------------" + Style.RESET_ALL)