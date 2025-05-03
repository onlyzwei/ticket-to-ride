from colorama import Fore, Style
from time import sleep

def play_turn(player, game):
    print(Fore.GREEN + f"\nÉ a sua vez, {player.get_name()}!" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Pontos atuais: {player.get_points()}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Trens restantes: {player.get_num_trains()}" + Style.RESET_ALL)
    
    while True:
        choice = input(Fore.CYAN + "Digite: 'cartas', 'trens' ou 'tickets': " + Style.RESET_ALL)
        
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