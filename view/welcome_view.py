from colorama import Fore, Style

def show_welcome_message():
    """
    Exibe a mensagem de boas-vindas e solicita o número de jogadores.
    """
    print(Fore.GREEN + "\nBem-vindo ao Ticket to Ride!\n" + Style.RESET_ALL)
    num_players = input(Fore.WHITE + "Quantos jogadores participarão hoje? (1-6): " + Style.RESET_ALL)
    count = 0
    while not num_players.isdigit() or int(num_players) not in range(1, 7) and count < 5:
        if num_players.lower() == 'exit': 
            print(Fore.GREEN + "Obrigado por jogar!" + Style.RESET_ALL)
            return None
        num_players = input(Fore.RED + "Por favor, digite um número entre 1 e 6: " + Style.RESET_ALL)
        count += 1
    if count >= 5:
        print(Fore.YELLOW + "O número padrão de jogadores foi definido como 2." + Style.RESET_ALL)
        return 2
    return int(num_players)