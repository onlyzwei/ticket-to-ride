# -*- coding: utf-8 -*-

import os
import time
from colorama import Fore, Back, Style, init
from model.game import Game

def clear_screen():
    """
    Limpa a tela do terminal para melhorar a experiência visual.
    """
    # Verifica o sistema operacional para usar o comando correto
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """
    Imprime o cabeçalho do jogo com estilo.
    """
    print(Fore.YELLOW + Style.BRIGHT)
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + " " * 24 + "TICKET TO RIDE" + " " * 25 + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    print(Style.RESET_ALL)

def print_section(title):
    """
    Imprime um separador de seção com título.
    
    Args:
        title (str): Título da seção a ser exibido
    """
    print("\n" + Fore.CYAN + "=" * 20 + f" {title} " + "=" * 20 + Style.RESET_ALL + "\n")

def play_ttr():
    """
    Função principal para jogar Ticket to Ride.
    
    Gerencia todo o fluxo do jogo, desde a inicialização até a determinação dos vencedores.
    """
    # Inicializa o colorama para suporte a cores no terminal
    init(autoreset=True)
    
    clear_screen()
    print_header()
    
    print(Fore.GREEN + "\nBem-vindo ao Ticket to Ride!\n" + Style.RESET_ALL)
    
    # Solicita o número de jogadores
    num_players = input(Fore.WHITE + "Quantos jogadores participarão hoje? (1-6): " + Style.RESET_ALL)
    
    count = 0
    while not num_players.isdigit() or int(num_players) not in range(1, 7) and count < 5:
        if num_players.lower() == 'exit': 
            print(Fore.GREEN + "Obrigado por jogar!" + Style.RESET_ALL)
            return
        num_players = input(Fore.RED + "Por favor, digite um número entre 1 e 6: " + Style.RESET_ALL)
        count += 1
        
    if count >= 5:
        print(Fore.YELLOW + "O número padrão de jogadores foi definido como 2." + Style.RESET_ALL)
        num_players = 2
    else:
        num_players = int(num_players)
        
    # Cria uma nova instância do jogo
    game = Game(num_players)
    
    # Inicializa o jogo (escolha de nomes e tickets iniciais)
    game.initialize()
    
    player = game.players[game.pos_to_move]
    
    # Loop principal do jogo
    while True:
        clear_screen()
        print_section(f"TURNO DE {player.get_name().upper()}")
        print(Fore.GREEN + f"É a sua vez, {player.get_name()}!" + Style.RESET_ALL)
        
        game.play_turn(player)
        
        # Verifica condição de término
        if game.check_ending_condition(player):
            game.advance_one_player()
            player = game.get_current_player()
            break
            
        game.advance_one_player()
        player = game.get_current_player()
        
        # Pausa para melhor visualização
        input(Fore.YELLOW + "\nPressione ENTER para continuar para o próximo jogador..." + Style.RESET_ALL)
    
    clear_screen()
    print_section("ÚLTIMA RODADA")
    print(Fore.YELLOW + "Este é o último turno! Todos têm mais uma jogada!" + Style.RESET_ALL)
    
    # Última rodada para todos os jogadores
    for i in range(len(game.players)):
        print_section(f"ÚLTIMO TURNO DE {player.get_name().upper()}")
        print(Fore.MAGENTA + f"Este é seu ÚLTIMO TURNO, {player.get_name()}!" + Style.RESET_ALL)
        
        game.play_turn(player)
        game.advance_one_player()
        player = game.get_current_player()
        
        if i < len(game.players) - 1:
            input(Fore.YELLOW + "\nPressione ENTER para continuar para o próximo jogador..." + Style.RESET_ALL)
    
    # Pontuação final
    for player in game.players:
        game.score_player_tickets(player)
    
    game.score_longest_path()
    
    clear_screen()
    print_section("PONTUAÇÃO FINAL")
    
    scores = []
    print(Fore.CYAN + "TABELA DE PONTUAÇÃO:" + Style.RESET_ALL)
    print("-" * 30)
    print(f"{'Jogador':<15} | {'Pontos':>10}")
    print("-" * 30)
    
    for player in game.players:
        score = player.get_points()
        scores.append(score)
        print(f"{player.get_name():<15} | {Fore.YELLOW}{score:>10}{Style.RESET_ALL}")
    
    print("-" * 30)
    
    # Definição dos vencedores
    winners = [x.get_name() for x in game.players if x.get_points() == max(scores)]
    
    print("\n" + Fore.GREEN + Style.BRIGHT)
    if len(winners) == 1:
        print(f"🏆 O vencedor é {winners[0]}! 🏆")
    else:
        print(f"🏆 Os vencedores são {' e '.join(winners)}! 🏆")
    print(Style.RESET_ALL)
    
    # Opção para ver dados detalhados
    see_details = input("\nDeseja ver dados detalhados do jogo? (s/n): ").lower()
    if see_details == 's':
        print_section("DADOS DETALHADOS")
        game.print_all_player_data()
    
    print(Fore.GREEN + "\nObrigado por jogar Ticket to Ride!" + Style.RESET_ALL)

if __name__ == "__main__":
    play_ttr()