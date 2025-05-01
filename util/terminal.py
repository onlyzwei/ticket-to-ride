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
    
    Args:
        group: O grupo de dados a ser impresso (dicionário, lista, etc.)
    """
    print("")
    if isinstance(group, dict) or isinstance(group, collections.Counter):
        for i in group:
            print(f"{Fore.CYAN}{i}\t{Fore.WHITE}{group[i]}{Style.RESET_ALL}")
        print(Fore.YELLOW + "__________________________________________" + Style.RESET_ALL)
    elif isinstance(group, list) or isinstance(group, set):
        for i in group:
            print(Fore.CYAN + str(i) + Style.RESET_ALL)
        print(Fore.YELLOW + "__________________________________________" + Style.RESET_ALL) 
    else:
        if group is None:
            print(Fore.YELLOW + "__________________________________________" + Style.RESET_ALL)
            return
        print(Fore.CYAN + str(group) + Style.RESET_ALL)
        print(Fore.YELLOW + "__________________________________________" + Style.RESET_ALL)