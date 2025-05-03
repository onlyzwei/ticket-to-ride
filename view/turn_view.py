from colorama import Fore, Style
from time import sleep

def play_turn(player, game):
    print(Fore.GREEN + f"\nÉ a sua vez, {player.get_name()}!" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Pontos atuais: {player.get_points()}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Trens restantes: {player.get_num_trains()}" + Style.RESET_ALL)

    # Mostrar todas as informações antes de fazer uma ação
    game.show_player_cards(player)
    game.show_pile_cards(player)
    game.train_handler.show_cities(player)
    
    while True:
        choice = input(
            Fore.YELLOW + "Digite uma das opções abaixo:\n\n" +
            Fore.YELLOW + "  cartas  " + Fore.CYAN + "- Comprar cartas de vagão\n" +
            Fore.YELLOW + "  trens   " + Fore.CYAN + "- Conquistar um caminho ou rota\n" +
            Fore.YELLOW + "  tickets " + Fore.CYAN + "- Comprar um bilhete de destino\n\n" +
            Fore.YELLOW + "Escolha: " + Fore.CYAN +
            Style.RESET_ALL
        ).lower()
        
        if choice == 'cartas':
            result = game._pick_cards(player)
            break
        elif choice == 'trens':
            result = game.train_handler.place_trains(player, game.deck)
            break
        elif choice == 'tickets':
            result = game.ticket_handler.pick_tickets(player)
            break
        else:
            print(Fore.RED + "Escolha inválida. Tente novamente." + Style.RESET_ALL)
    
    print(Fore.GREEN + "Turno concluído!" + Style.RESET_ALL)
    sleep(2)