from enum import Enum

class Move:
    def __init__(self, color, piece, from_square, to_square, move_type, promoted_piece=None):
        self.color = color
        self.piece = piece
        self.from_square = from_square
        self.to_square = to_square
        self.move_type = move_type
        self.promoted_piece = promoted_piece
    
    def __repr__(self):
        return f"{self.color} {self.piece}: {self.from_square} -> {self.to_square} ({self.move_type})"


class MoveType(Enum):
    NORMAL = 1
    PAWN_DOUBLE = 2
    CAPTURE = 3
    EN_PASSANT = 4
    PROMOTION = 5
    CASTLE_KINGSIDE = 6
    CASTLE_QUEENSIDE = 7

class Promotion(Enum):
    QUEEN = 1
    KNIGHT = 2
    ROOK = 3
    BISHOP = 4

class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    ROOK = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6

class Color(Enum):
    WHITE = 1
    BLACK = -1