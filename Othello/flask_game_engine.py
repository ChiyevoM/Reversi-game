"""
flask_game_engine.py

Flask server for Othello web game with AI opponent.
"""

from flask import Flask, render_template, request, jsonify
from components import initialise_board, legal_move, get_flippable_pieces, pad, choose_ai_move

import json
import os

app = Flask(__name__)
SAVE_FILE = "saved_game.json"

# Game state
GAME = {
    "board": initialise_board(),
    "current_player": "Dark"
}


@app.route("/")
def home():
    """Render the Othello board page."""
    return render_template("Othello_Board.html")


@app.route("/get_board")
def get_board():
    """Return current board state and current player as JSON."""
    return jsonify({
        "board": [[cell.strip() for cell in row] for row in GAME["board"]],
        "current_player": GAME["current_player"]
    })


@app.route("/make_move", methods=["POST"])
def make_move():
    """Handle a human move and then AI move if applicable."""
    data = request.get_json()
    row = data["row"]
    col = data["col"]
    player = GAME["current_player"]
    board = GAME["board"]

    # Human move
    if not legal_move(player, (row, col), board):
        from logger import log_error
        log_error(f"{player} attempted illegal move at ({row},{col}) via web interface")
        return jsonify({"error": "Illegal move"}), 400

    flippable = get_flippable_pieces(board, row, col, player)
    board[row][col] = pad(player)
    for r, c in flippable:
        board[r][c] = pad(player)
        
    from logger import log_event
    log_event(f"{player} placed a piece at ({row},{col}) via web interface")

    # Switch turn to AI if Light's turn
    GAME["current_player"] = "Light" if player == "Dark" else "Dark"

    # AI move
    if GAME["current_player"] == "Light":
        ai_move = choose_ai_move(board, "Light")
        if ai_move:
            r, c = ai_move
            flippable_ai = get_flippable_pieces(board, r, c, "Light")
            board[r][c] = pad("Light")
            for rr, cc in flippable_ai:
                board[rr][cc] = pad("Light")
        GAME["current_player"] = "Dark"

    return jsonify({
        "board": [[cell.strip() for cell in row] for row in board],
        "next_player": GAME["current_player"]
    })


@app.route("/save", methods=["POST"])
def save():
    """Save the current game state to JSON."""
    clean_board = [[cell.strip() for cell in row] for row in GAME["board"]]
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump({
            "board": clean_board,
            "current_player": GAME["current_player"]
        }, file)
    return "", 204


@app.route("/load")
def load():
    """Load game state from JSON."""
    if not os.path.exists(SAVE_FILE):
        return jsonify({"error": "No save file"}), 404

    with open(SAVE_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    GAME["board"] = [[pad(cell if cell != "None" else None) for cell in row] for row in data["board"]]
    GAME["current_player"] = data["current_player"]

    return jsonify({
        "board": [[cell.strip() for cell in row] for row in GAME["board"]],
        "current_player": GAME["current_player"]
    })


if __name__ == "__main__":
    app.run(debug=True)
