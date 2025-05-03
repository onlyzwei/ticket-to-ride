from colorama import Fore, Style

def register_players(num_players):
    """
    Registra os jogadores e retorna uma lista com seus nomes.
    
    Args:
        num_players (int): Número de jogadores a serem registrados.
    
    Returns:
        list: Lista com os nomes dos jogadores.
    """
    players = []
    for i in range(num_players):
        count = 0
        name = input(Fore.CYAN + f"Jogador {i + 1}, por favor digite seu nome: " + Style.RESET_ALL)
        while (name in players or len(name) > 50) and count < 5:
            name = input(Fore.RED + f"Jogador {i + 1}, por favor digite um nome único (máx. 50 caracteres): " + Style.RESET_ALL)
            count += 1
        if len(name) > 50 or name == '' or name in players:
            name = f"Jogador {i + 1}"
        players.append(name)
    return players