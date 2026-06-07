# Othello / Reversi Game – Technical Documentation

**Author:** Chiyevo Mukonoweshuro 
**Date:** 8 Dec 2025  
**License:** University of Exeter
**Project:** Programming 2



## Project Overview
This is a Python implementation of the Othello (Reversi) board game. It supports:
- Two-player CLI game
- Web version via Flask
- AI opponent for one player
- Save and load functionality using JSON

The pieces are navy (#0A2342) for Dark and warm sand (#F2E5C4) for Light.



## Modules

### `components.py`
Contains the core game logic:
- `initialise_board(size=8)` → Sets up the board with the four starting pieces.
- `print_board(board)` → Prints ASCII board in the terminal.
- `legal_move(colour, coord, board)` → Checks if a move is legal.
- `get_flippable_pieces(board, row, col, player)` → Returns opponent pieces to flip.
- `pad(value)` → Pads piece strings for CLI printing.
- `choose_ai_move(board, player)` → AI move selection algorithm.

### `game_engine.py`
Handles the CLI gameplay loop:
- `cli_coords_input()` → Reads user input and validates coordinates.
- `has_legal_move(board, player)` → Checks if player can move.
- `simple_game_loop()` → Runs the full game loop which includes alternating turns, flipping outflanked pieces, and ending game.

### `flask_game_engine.py`
Flask web server:
- Routes:
  - `/` → Serves HTML board
  - `/get_board` → Sends current board and player
  - `/make_move` → Processes a move
  - `/save` → Saves game state to JSON
  - `/load` → Loads game state from JSON
- Uses same `components.py` logic for game rules and AI.
- Sends `message` field for start and game over notifications.



## Algorithms

### Move Flipping
1. Check all 8 directions from the placed piece.
2. Collect opponent pieces until a player's piece is found.
3. Only flip pieces if outflanked by the player.

### AI
- Evaluates all legal moves.
- Scores moves:
  - +1 per piece flipped
  - +3 for corners
  - +1 for edges
- Chooses move with highest score.

### Flowchart:
- AI Opponent Flowchart
START
  │
  ▼
Check all empty board positions
  │
  ▼
For each empty position:
  ├─> Is move legal? (outflanks at least one opponent piece)
  │      │
  │      ▼
  │   If NO → skip
  │
  ▼
  If YES → Calculate move score:
           • +1 per piece flipped
           • +3 if corner
           • +1 if edge
  │
  ▼
Store legal moves with scores
  │
  ▼
Select move with highest score
  │
  ▼
Place AI piece on selected position
  │
  ▼
Flip opponent pieces accordingly
  │
  ▼
Switch turn to human player
  │
  ▼
END



