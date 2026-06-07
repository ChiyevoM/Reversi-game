"""
game_engine.py

Command-line interface (CLI) game loop for Othello.
Handles user input, turn switching, scoring, and AI moves.
"""

from components import (
    initialise_board,
    print_board,
    get_flippable_pieces,
    pad,
    choose_ai_move
)
from logger import log_event, log_error

BOARD_SIZE = 8

def cli_coords_input():
    """
    Prompt the user for row and column input.
    Returns a tuple (row, col).
    """
    while True:
        try:
            row = int(input("Enter row (1-8): ")) - 1
            col = int(input("Enter column (1-8): ")) - 1
            return row, col
        except ValueError:
            print("Please enter numbers only.")


def has_legal_move(board, player):
    """
    Return True if the player has at least one legal move.
    """
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if get_flippable_pieces(board, r, c, player):
                return True
    return False


def simple_game_loop():
    """
    Run a complete two-player Othello game in the terminal.
    Human = Dark, AI = Light.
    """
    print("Welcome to Othello!")
    print("Official rules:")
    print("https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english\n")

    board = initialise_board()
    print_board(board)

    move_counter = 60
    players = ["Dark", "Light"]
    current_player_index = 0

    while move_counter > 0:
        player = players[current_player_index]
        print(f"\n{player}'s turn. Moves left: {move_counter}")

        if not has_legal_move(board, player):
            print(f"No legal moves for {player}. Switching player.")
            current_player_index = 1 - current_player_index
            if not has_legal_move(board, players[current_player_index]):
                print("No legal moves for either player.")
                break
            continue

        # Determine move
        if player == "Light":  # AI turn
            move = choose_ai_move(board, player)
            if move is None:
                print(f"No legal moves for {player}.")
                current_player_index = 1 - current_player_index
                continue
            row, col = move
            print(f"AI chooses row {row + 1}, col {col + 1}")
        else:  # Human turn
            row, col = cli_coords_input()

        if not get_flippable_pieces(board, row, col, player):
            print("Illegal move. Try again.")
            log_error(f"{player} attempted illegal move at ({row},{col}) in CLI game")
            continue
        
        # Apply move
        flippable = get_flippable_pieces(board, row, col, player)
        board[row][col] = pad(player)
        for r, c in flippable:
            board[r][c] = pad(player)

        log_event(f"{player} placed a piece at ({row},{col}) in CLI game")

        print_board(board)
        move_counter -= 1
        current_player_index = 1 - current_player_index

    # Final score
    dark_count = sum(row.count(pad("Dark")) for row in board)
    light_count = sum(row.count(pad("Light")) for row in board)

    print("\nGame over!")
    print(f"Dark: {dark_count}, Light: {light_count}")

    if dark_count > light_count:
        print("Dark wins!")
    elif light_count > dark_count:
        print("Light wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    simple_game_loop()
