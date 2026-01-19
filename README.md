# Chess-Engine-Project

A fully functional chess game built with **Python** and **Pygame**. This project implements all standard chess rules and features for an interactive two-player gaming experience.

## Features

- **Complete Chess Rules**: Supports all standard chess piece movements (pawns, rooks, knights, bishops, queens, kings)
- **Check & Checkmate Detection**: The game detects when a king is in check and automatically determines checkmate and stalemate conditions
- **Castling**: Both kingside and queenside castling are fully implemented with proper validation
- **Legal Move Validation**: The game prevents illegal moves that would leave your king in check
- **Interactive GUI**: Click-based piece selection and movement with visual feedback
  - Green highlight for selected pieces
  - Yellow dots for possible moves
  - Red highlight for kings in check

## Requirements

- Python 3.7+
- Pygame

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vishnu007nd-coder/Chess-Engine-Project.git
   cd Chess-Engine-Project
   ```

2. Install dependencies:
   ```bash
   pip install pygame
   ```

## How to Play

1. Run the game:
   ```bash
   python chess_app.py
   ```

2. **Select a piece**: Click on any white piece to select it (white plays first)

3. **View possible moves**: Available moves are shown as yellow dots

4. **Move the piece**: Click on a highlighted square to move your piece

5. **Turn alternation**: After you move, black automatically gets a turn

6. **Game End**: The game detects checkmate and stalemate, displaying the result

## Game Controls

- **Mouse Click**: Select pieces and make moves
- **Close Window**: Exit the game

## Board Display

- Pieces are displayed as letters: **P** (Pawn), **R** (Rook), **K** (Knight/King), **B** (Bishop), **Q** (Queen)
- Board squares alternate between light and dark colors for clarity
- White pieces appear in black text, black pieces in white text