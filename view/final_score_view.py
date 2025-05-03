from colorama import Fore, Style

def show_final_scores(players):
    """
    Exibe a pontuação final e os vencedores.
    
    Args:
        players (list): Lista de jogadores.
    """
    print(Fore.CYAN + "\nTABELA DE PONTUAÇÃO:" + Style.RESET_ALL)
    print("-" * 30)
    print(f"{'Jogador':<15} | {'Pontos':>10}")
    print("-" * 30)
    
    scores = []
    for player in players:
        score = player.get_points()
        scores.append(score)
        print(f"{player.get_name():<15} | {Fore.YELLOW}{score:>10}{Style.RESET_ALL}")
    print("-" * 30)
    
    winners = [p.get_name() for p in players if p.get_points() == max(scores)]
    print(Fore.GREEN + "\n🏆 Vencedor(es): " + ", ".join(winners) + " 🏆" + Style.RESET_ALL)