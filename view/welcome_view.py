from colorama import Fore, Style

def show_welcome_message():
    """
    Exibe a mensagem de boas-vindas e solicita o número de jogadores.
    """
    print(Fore.GREEN + "\nBem-vindo ao Ticket to Ride!\n" + Style.RESET_ALL)

    while True:
        entrada = input(Fore.WHITE + "Número de jogadores (1-6) ou 'exit' para sair: " + Style.RESET_ALL)
        if entrada.lower() == 'exit':
            print(Fore.GREEN + "Obrigado por jogar!" + Style.RESET_ALL)
            return None
        try:
            num_players = int(entrada)
            if 1 <= num_players <= 6:
                return num_players
            else:
                print(Fore.RED + "Por favor, digite um número entre 1 e 6." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Entrada inválida. Digite um número inteiro ou 'exit' para sair." + Style.RESET_ALL)