import pygame
import sys
from enum import Enum

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (240, 217, 181)
DARK_GRAY = (181, 136, 99)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()
FPS = 60

# Piece types
class PieceType(Enum):
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6

# Piece colors
class PieceColor(Enum):
    WHITE = 1
    BLACK = 2

class ChessPiece:
    def __init__(self, color, piece_type, row, col):
        self.color = color
        self.piece_type = piece_type
        self.row = row
        self.col = col
        self.has_moved = False
        self.symbol = self._get_symbol()
    
    def _get_symbol(self):
        symbols = {
            PieceType.PAWN: 'P',
            PieceType.ROOK: 'R',
            PieceType.KNIGHT: 'K',
            PieceType.BISHOP: 'B',
            PieceType.QUEEN: 'Q',
            PieceType.KING: 'K',
        }
        return symbols[self.piece_type]
    
    def get_possible_moves(self, board):
        """Returns list of possible moves for this piece"""
        moves = []
        
        if self.piece_type == PieceType.PAWN:
            moves = self._get_pawn_moves(board)
        elif self.piece_type == PieceType.ROOK:
            moves = self._get_rook_moves(board)
        elif self.piece_type == PieceType.KNIGHT:
            moves = self._get_knight_moves(board)
        elif self.piece_type == PieceType.BISHOP:
            moves = self._get_bishop_moves(board)
        elif self.piece_type == PieceType.QUEEN:
            moves = self._get_queen_moves(board)
        elif self.piece_type == PieceType.KING:
            moves = self._get_king_moves(board)
        
        return moves
    
    def _get_pawn_moves(self, board):
        moves = []
        direction = -1 if self.color == PieceColor.WHITE else 1
        start_row = 6 if self.color == PieceColor.WHITE else 1
        
        # Move forward
        next_row = self.row + direction
        if 0 <= next_row < 8 and board[next_row][self.col] is None:
            moves.append((next_row, self.col))
            
            # Double move from start
            if self.row == start_row:
                next_next_row = self.row + 2 * direction
                if board[next_next_row][self.col] is None:
                    moves.append((next_next_row, self.col))
        
        # Captures
        for dc in [-1, 1]:
            next_col = self.col + dc
            next_row = self.row + direction
            if 0 <= next_row < 8 and 0 <= next_col < 8:
                target = board[next_row][next_col]
                if target and target.color != self.color:
                    moves.append((next_row, next_col))
        
        return moves
    
    def _get_rook_moves(self, board):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = self.row + dr * i, self.col + dc * i
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                target = board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                else:
                    if target.color != self.color:
                        moves.append((new_row, new_col))
                    break
        return moves
    
    def _get_knight_moves(self, board):
        moves = []
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dr, dc in knight_moves:
            new_row, new_col = self.row + dr, self.col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None or target.color != self.color:
                    moves.append((new_row, new_col))
        return moves
    
    def _get_bishop_moves(self, board):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = self.row + dr * i, self.col + dc * i
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                target = board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                else:
                    if target.color != self.color:
                        moves.append((new_row, new_col))
                    break
        return moves
    
    def _get_queen_moves(self, board):
        # Queen moves like both rook and bishop
        return self._get_rook_moves(board) + self._get_bishop_moves(board)
    
    def _get_king_moves(self, board):
        moves = []
        king_moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in king_moves:
            new_row, new_col = self.row + dr, self.col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None or target.color != self.color:
                    moves.append((new_row, new_col))
        return moves

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()
    
    def setup_pieces(self):
        """Setup the chess board with all pieces in starting positions"""
        # Black pieces
        self.board[0][0] = ChessPiece(PieceColor.BLACK, PieceType.ROOK, 0, 0)
        self.board[0][1] = ChessPiece(PieceColor.BLACK, PieceType.KNIGHT, 0, 1)
        self.board[0][2] = ChessPiece(PieceColor.BLACK, PieceType.BISHOP, 0, 2)
        self.board[0][3] = ChessPiece(PieceColor.BLACK, PieceType.QUEEN, 0, 3)
        self.board[0][4] = ChessPiece(PieceColor.BLACK, PieceType.KING, 0, 4)
        self.board[0][5] = ChessPiece(PieceColor.BLACK, PieceType.BISHOP, 0, 5)
        self.board[0][6] = ChessPiece(PieceColor.BLACK, PieceType.KNIGHT, 0, 6)
        self.board[0][7] = ChessPiece(PieceColor.BLACK, PieceType.ROOK, 0, 7)
        
        for col in range(8):
            self.board[1][col] = ChessPiece(PieceColor.BLACK, PieceType.PAWN, 1, col)
        
        # White pieces
        for col in range(8):
            self.board[6][col] = ChessPiece(PieceColor.WHITE, PieceType.PAWN, 6, col)
        
        self.board[7][0] = ChessPiece(PieceColor.WHITE, PieceType.ROOK, 7, 0)
        self.board[7][1] = ChessPiece(PieceColor.WHITE, PieceType.KNIGHT, 7, 1)
        self.board[7][2] = ChessPiece(PieceColor.WHITE, PieceType.BISHOP, 7, 2)
        self.board[7][3] = ChessPiece(PieceColor.WHITE, PieceType.QUEEN, 7, 3)
        self.board[7][4] = ChessPiece(PieceColor.WHITE, PieceType.KING, 7, 4)
        self.board[7][5] = ChessPiece(PieceColor.WHITE, PieceType.BISHOP, 7, 5)
        self.board[7][6] = ChessPiece(PieceColor.WHITE, PieceType.KNIGHT, 7, 6)
        self.board[7][7] = ChessPiece(PieceColor.WHITE, PieceType.ROOK, 7, 7)
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        """Move a piece from one position to another"""
        piece = self.board[from_row][from_col]
        if piece:
            piece.row = to_row
            piece.col = to_col
            piece.has_moved = True
            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = None
            return True
        return False
    
    def get_piece_at(self, row, col):
        """Get piece at specific position"""
        return self.board[row][col]

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.selected_piece = None
        self.possible_moves = []
        self.current_player = PieceColor.WHITE
    
    def handle_click(self, pos):
        """Handle mouse click to select/move pieces"""
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE
        
        if self.selected_piece is None:
            # Select a piece
            piece = self.board.get_piece_at(row, col)
            if piece and piece.color == self.current_player:
                self.selected_piece = (row, col)
                self.possible_moves = piece.get_possible_moves(self.board.board)
        else:
            # Try to move the piece
            if (row, col) in self.possible_moves:
                from_row, from_col = self.selected_piece
                self.board.move_piece(from_row, from_col, row, col)
                self.current_player = PieceColor.BLACK if self.current_player == PieceColor.WHITE else PieceColor.WHITE
            
            self.selected_piece = None
            self.possible_moves = []
    
    def draw_board(self):
        """Draw the chessboard"""
        for row in range(8):
            for col in range(8):
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                color = LIGHT_GRAY if (row + col) % 2 == 0 else DARK_GRAY
                pygame.draw.rect(screen, color, rect)
    
    def draw_pieces(self):
        """Draw all pieces on the board"""
        font = pygame.font.Font(None, SQUARE_SIZE - 10)
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece_at(row, col)
                if piece:
                    text = font.render(piece.symbol, True, WHITE if piece.color == PieceColor.BLACK else BLACK)
                    text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                    screen.blit(text, text_rect)
    
    def draw_highlights(self):
        """Highlight selected piece and possible moves"""
        if self.selected_piece:
            row, col = self.selected_piece
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, GREEN, rect, 3)
            
            # Highlight possible moves
            for move_row, move_col in self.possible_moves:
                center_x = move_col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = move_row * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.circle(screen, YELLOW, (center_x, center_y), 5)
    
    def draw(self):
        """Draw the entire game"""
        self.draw_board()
        self.draw_pieces()
        self.draw_highlights()
        pygame.display.flip()

def main():
    game = ChessGame()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
        
        game.draw()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()