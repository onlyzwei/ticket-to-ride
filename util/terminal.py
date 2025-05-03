from os import system, name
from colorama import Fore, Back, Style, init
import collections

def clear_screen():
    """
    Limpa a tela do terminal para melhorar a experiência visual.
    """
    # Verifica o sistema operacional para usar o comando correto
    system('cls' if name == 'nt' else 'clear')

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


def print_sep_line(group=None):
    """
    Imprime uma linha separadora com formatação para diferentes tipos de dados.
    Versão específica para o jogo Ticket to Ride que trata rotas corretamente.
    
    Args:
        group: O grupo de dados a ser impresso (dicionário, lista, etc.)
    """
    print(Fore.YELLOW + "__________________________________________" + Style.RESET_ALL)
    
    # Se for None
    if group is None:
        print(Fore.YELLOW + "__________________________________________" + Style.RESET_ALL)
        return
        
    # Para dicionários e contadores (como a mão do jogador)
    if isinstance(group, dict) or isinstance(group, collections.Counter):
        max_key_length = max(len(str(key)) for key in group) if group else 0
        for key, value in group.items():
            print(f"{Fore.CYAN}{str(key).ljust(max_key_length)}\t{Fore.WHITE}{value}{Style.RESET_ALL}")
    
    # Para listas de rotas (como legal_routes)
    elif isinstance(group, list) and all(isinstance(item, tuple) and len(item) >= 3 for item in group):
        for route in group:
            city1, city2, details = route[0], route[1], route[2]
            weight = details.get('weight', '?')
            colors = ', '.join(details.get('edge_colors', ['?']))
            print(f"{Fore.CYAN}{city1} → {city2}{Fore.WHITE} (Distância: {weight}, Cores: {colors}){Style.RESET_ALL}")
    
    # Para listas simples (como nomes de cidades)
    elif isinstance(group, list) or isinstance(group, set) or isinstance(group, tuple):
        for item in group:
            if isinstance(item, tuple) and len(item) == 2:
                # Tupla simples de duas cidades
                print(f"{Fore.CYAN}{item[0]} → {item[1]}{Style.RESET_ALL}")
            else:
                print(f"{Fore.CYAN}{str(item)}{Style.RESET_ALL}")
    
    # Para valores simples (como números)
    else:
        print(f"{Fore.CYAN}{str(group)}{Style.RESET_ALL}")
        
    print(Fore.YELLOW + "__________________________________________" + Style.RESET_ALL)