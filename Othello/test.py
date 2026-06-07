"""
Tests for core Othello game logic.
Stage 5 – Testing and Evaluation
"""

from components import (
    initialise_board,
    legal_move,
    get_flippable_pieces,
    pad
)


def test_initial_board_setup():
    """Test that the initial board has the correct starting pieces."""
    board = initialise_board()

    assert board[3][3] == pad("Light")
    assert board[3][4] == pad("Dark")
    assert board[4][3] == pad("Dark")
    assert board[4][4] == pad("Light")


def test_illegal_move_on_occupied_square():
    """Test that a move on an occupied square is illegal."""
    board = initialise_board()
    assert not legal_move("Dark", (3, 3), board)


def test_legal_move_returns_true():
    """Test a known legal opening move for Dark."""
    board = initialise_board()
    assert legal_move("Dark", (2, 3), board)


def test_flippable_pieces_found():
    """Test that outflanked pieces are detected correctly."""
    board = initialise_board()
    flippable = get_flippable_pieces(board, 2, 3, "Dark")
    assert (3, 3) in flippable
