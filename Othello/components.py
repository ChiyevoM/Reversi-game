"""
components.py

Game logic for the Othello (Reversi) game.
"""


def pad(value):
    """
    Pad a board value to 5 characters for printing.
    """
    return str(value).ljust(5)


def initialise_board(size=8):
    """
    Create and return a new Othello board.
    """
    board = [[pad("None") for _ in range(size)] for _ in range(size)]

    middle = size // 2
    board[middle - 1][middle - 1] = pad("Light")
    board[middle - 1][middle] = pad("Dark")
    board[middle][middle - 1] = pad("Dark")
    board[middle][middle] = pad("Light")

    return board


def print_board(board):
    """
    Print an ASCII representation of the board.
    """
    print("   " + " ".join(str(i + 1) for i in range(len(board))))
    for index, row in enumerate(board):
        print(f"{index + 1}  " + "".join(row))


def get_flippable_pieces(board, row, col, colour):
    """
    Return a list of coordinates of opponent pieces that would be flipped
    if 'colour' is placed at (row, col).
    """
    size = len(board)
    opponent = "Light" if colour == "Dark" else "Dark"

    if board[row][col].strip() != "None":
        return []

    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]

    flippable = []

    for dr, dc in directions:
        r, c = row + dr, col + dc
        captured = []

        while 0 <= r < size and 0 <= c < size:
            cell = board[r][c].strip()

            if cell == opponent:
                captured.append((r, c))
            elif cell == colour and captured:
                flippable.extend(captured)
                break
            else:
                break

            r += dr
            c += dc

    return flippable


def legal_move(colour, coord, board):
    """
    Check whether a move is legal for the given colour.
    """
    row, col = coord
    size = len(board)

    if not (0 <= row < size and 0 <= col < size):
        return False

    return bool(get_flippable_pieces(board, row, col, colour))

def choose_ai_move(board, player):
    """
    Choose the best move for AI.
    Simple strategy:
    1. Evaluate all legal moves.
    2. Score moves by number of pieces flipped.
    3. Prefer corners.
    Returns the (row, col) of the best move.
    """
    best_score = -1
    best_move = None
    BOARD_SIZE = len(board)
    corners = [(0, 0), (0, BOARD_SIZE-1), (BOARD_SIZE-1, 0), (BOARD_SIZE-1, BOARD_SIZE-1)]

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if legal_move(player, (r, c), board):
                flippable = get_flippable_pieces(board, r, c, player)
                score = len(flippable)

                # bonus for corners
                if (r, c) in corners:
                    score += 3

                if score > best_score:
                    best_score = score
                    best_move = (r, c)

    return best_move
