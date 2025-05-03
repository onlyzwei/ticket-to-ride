from colorama import Fore, Style
from time import sleep

def play_turn(player, game):
    print(Fore.GREEN + f"\nÉ a sua vez, {player.get_name()}!" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Pontos atuais: {player.get_points()}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Trens restantes: {player.get_num_trains()}" + Style.RESET_ALL)

    # Mostrar todas as informações antes de fazer uma ação
    game.show_player_cards(player)
    print('\n')
    game.show_pile_cards(player)
    print('\n')
    game.train_handler.show_cities(player)
    print('\n')
    
    while True:
        choice = input(
        Fore.YELLOW + "Digite" + Fore.CYAN + ": \n " +
        Fore.YELLOW + "cartas -"+ Fore.CYAN + " Comprar cartas de vagão \n " +
        Fore.YELLOW + "trens -" + Fore.CYAN + " Conquistar um caminho ou rota\n " +
        Fore.YELLOW + "tickets -" + Fore.CYAN + " Comprar um bilhete de destino\n \n " +
        Style.RESET_ALL
)
        
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