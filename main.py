from colorama import init
from model.game import Game
from util.terminal import clear_screen
from view.welcome_view import show_welcome_message
from view.player_registration_view import register_players
from view.turn_view import play_turn
from view.final_score_view import show_final_scores

def play_ttr():
    init(autoreset=True)
    clear_screen()
    
    # View de boas-vindas
    num_players = show_welcome_message()
    if num_players is None:
        return
    
    # Registro de jogadores
    clear_screen()
    player_names = register_players(num_players)

    # Inicializa o jogo
    game = Game(num_players)
    for i, player in enumerate(game.players):
        player.set_player_name(player_names[i])

        # Escolha de tickets iniciais
        clear_screen()
        print(f"Jogador {player.get_name()}, escolha seus tickets iniciais:")
        game.ticket_handler.pick_tickets(player, min_num_to_select=2)
    
    # Loop principal do jogo
    while True:
        clear_screen()
        current_player = game.get_current_player()
        result = play_turn(current_player, game)
        if result == "voltar":
            continue  # Volta para o início do loop principal
        
        if game.check_ending_condition(current_player):
            break
        game.advance_one_player()
    
    # Pontuação final
    clear_screen()
    show_final_scores(game.players)

if __name__ == "__main__":
    play_ttr()