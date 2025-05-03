# -*- coding: utf-8 -*-

import random
from time import sleep
from typing import List
from colorama import Fore, Style
from util.terminal import clear_screen

class Ticket:
    """
    Classe responsável pelo gerenciamento de tickets de destino no jogo.
    """
    def __init__(self):
        self.tickets_file = "util/tickets.txt"
        self.tickets = self._read_tickets(self.tickets_file)
        self._shuffle(self.tickets)
        self.ticket_discard_pile = []
        self.num_tickets_dealt = 3

    def _shuffle(self, tickets):
        random.shuffle(tickets)

    def _read_tickets(self, tickets_file: str) -> List[tuple]:
        tickets = []
        
        # Abrir o arquivo para leitura
        with open(tickets_file, 'r') as file:
            for line in file:
                # Separar os valores por vírgula
                parts = line.strip().split(',')
                
                # Extrair os valores da linha
                city1 = parts[0]
                city2 = parts[1]
                value = int(parts[2])  # O peso é um número inteiro
                
                # Adicionar a tupla à lista de arestas
                tickets.append((city1, city2, value))
        
        return tickets
    
    def deal_ticket(self):
        if len(self.tickets) == 0:
            self._restock_tickets()
        try:
            return self.tickets.pop()
        except IndexError:
            print(f"{Fore.RED}\nNão há mais bilhetes no baralho!\n{Style.RESET_ALL}")
            return None

    def deal_tickets(self, num_tickets):
        result = []
        for _ in range(num_tickets):
            ticket = self.deal_ticket()
            if ticket is not None:
                result.append(ticket)
        return result

    def add_to_ticket_discard(self, ticket):
        self.ticket_discard_pile.append(ticket)

    def tickets_left(self):
        return len(self.tickets)

    def _restock_tickets(self):
        assert len(self.tickets) == 0
        self.tickets = self.ticket_discard_pile
        self._shuffle(self.tickets)
        self.ticket_discard_pile = []

    def num_tickets_left_to_deal(self):
        if len(self.tickets) == 0:
            self._restock_tickets()
        return len(self.tickets)

    def pick_tickets(self, player, min_num_to_select=1):
        clear_screen()
        available_tickets = self.num_tickets_left_to_deal()
        if available_tickets <= 0:
            print(f"{Fore.RED}Não restam mais tickets!{Style.RESET_ALL}")
            sleep(3)
            self._print_sep_line(player.get_tickets())
            print(f"{Fore.YELLOW}Todos os seus tickets: {Style.RESET_ALL}")
            self._print_sep_line(player.get_tickets())
            return

        tickets_to_deal = min(self.num_tickets_dealt, available_tickets)
        dealt_tickets = self.deal_tickets(tickets_to_deal)
        indexed_tickets = {i: ticket for i, ticket in enumerate(dealt_tickets)}

        print(f"{Fore.GREEN}Olá {player.get_name()}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Por favor selecione pelo menos {min_num_to_select} ticket(s): {Style.RESET_ALL}")
        self._print_available_tickets(indexed_tickets)

        selected_tickets = set()
        while True:
            user_input = input("Digite o número do ticket, 'done' para finalizar: ")

            if user_input.lower() == 'done':
                if len(selected_tickets) >= min_num_to_select:
                    break
                print(f"{Fore.RED}Você deve selecionar pelo menos {min_num_to_select} ticket(s).{Style.RESET_ALL}")
                continue

            try:
                ticket_index = int(user_input)
                if ticket_index in indexed_tickets:
                    ticket = indexed_tickets[ticket_index]
                    if ticket not in selected_tickets:
                        selected_tickets.add(ticket)
                    else:
                        print(f"{Fore.RED}Este ticket já foi selecionado.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Número inválido. Tente novamente.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Entrada inválida. Digite um número ou 'done'.{Style.RESET_ALL}")

        for ticket in dealt_tickets:
            if ticket in selected_tickets:
                player.add_ticket(ticket)
            else:
                self.add_to_ticket_discard(ticket)

        clear_screen()
        self._print_sep_line()
        print(f"Tickets restantes no baralho: {len(self.tickets)}")
        print(f"Tickets na pilha de descarte: {len(self.ticket_discard_pile)}")
        print(f"{Fore.YELLOW}Todos os seus tickets:{Style.RESET_ALL}")
        self._print_sep_line(player.get_tickets())

    def score_player_tickets(self, player):
        print(Fore.GREEN + f"\nPontuando tickets para {player.name}:" + Style.RESET_ALL)
        for ticket in player.get_tickets():
            city1, city2, value = ticket
            pos_nodes = player.player_board.get_nodes()
            if city1 not in pos_nodes or city2 not in pos_nodes:
                player.subtract_points(value)
                print(f"  {Fore.RED}- {city1} para {city2}: -{value} pontos (não concluído){Style.RESET_ALL}")
            elif player.player_board.has_path(city1, city2):
                player.add_points(value)
                print(f"  {Fore.GREEN}+ {city1} para {city2}: +{value} pontos (concluído){Style.RESET_ALL}")

    def _print_sep_line(self, info=None):
        print(Fore.CYAN + "------------------------------" + Style.RESET_ALL)
        if info is not None:
            if isinstance(info, list):
                for ticket in info:
                    city1, city2, value = ticket
                    print(f"{Fore.WHITE}{city1} -> {city2} : {value} pontos{Style.RESET_ALL}")
            else:
                print(f"{Fore.WHITE}{info}{Style.RESET_ALL}")
            print(Fore.CYAN + "------------------------------" + Style.RESET_ALL)

    def _print_available_tickets(self, tickets):
        print(Fore.CYAN + "-------- TICKETS DISPONÍVEIS --------" + Style.RESET_ALL)
        for idx, (city1, city2, value) in tickets.items():
            print(
                f"{Fore.YELLOW}[{idx}] "
                f"{Fore.BLUE}{city1} {Fore.WHITE}-> {Fore.BLUE}{city2} "
                f"{Fore.MAGENTA}: {value} pontos{Style.RESET_ALL}"
            )
        print(Fore.CYAN + "-------------------------------------" + Style.RESET_ALL)
