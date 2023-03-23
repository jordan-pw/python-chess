import numpy as np

from move import Move, MoveType, Promotion, PieceType

def binarystring_to_bitboard(binary):
    bitboard = np.uint64(int(binary, 2))
    return bitboard

def bitboard_to_binarystring(bitboard):
    return np.binary_repr(bitboard).zfill(64)

def reverse_rows(board):
    for row in board:
        row.reverse()

class Board:
    def __init__(self):
        self.wp = np.uint64()
        self.wn = np.uint64()
        self.wb = np.uint64()
        self.wr = np.uint64()
        self.wq = np.uint64()
        self.wk = np.uint64()
        self.bp = np.uint64()
        self.bn = np.uint64()
        self.bb = np.uint64()
        self.br = np.uint64()
        self.bq = np.uint64()
        self.bk = np.uint64()
        self.pieces = [self.wp, self.wn, self.wb, self.wr, self.wq, self.wk, self.bp, self.bn, self.bb, self.br, self.bq, self.bk]
        self.history = list()

    def make_move(self, move):
        # Standard Move
        if move.move_type == MoveType.NORMAL or move.move_type == MoveType.PAWN_DOUBLE:
            match move.piece:
                case PieceType.PAWN:
                    if move.color:
                        self.move_piece(self.wp, move.from_square, move.to_square)
                    else:
                        self.move_piece(self.bp, move.from_square, move.to_square)
                case PieceType.KNIGHT:
                    if move.color:
                        self.move_piece(self.wn, move.from_square, move.to_square)
                    else:
                        self.move_piece(self.bn, move.from_square, move.to_square)
                case PieceType.ROOK:
                    if move.color:
                        self.move_piece(self.wr, move.from_square, move.to_square)
                    else:
                        self.move_piece(self.br, move.from_square, move.to_square)
                case PieceType.BISHOP:
                    if move.color:
                        self.move_piece(self.wb, move.from_square, move.to_square)
                    else:
                        self.move_piece(self.bb, move.from_square, move.to_square)
                case PieceType.QUEEN:
                    if move.color:
                        self.move_piece(self.wq, move.from_square, move.to_square)
                    else:
                        self.move_piece(self.bq, move.from_square, move.to_square)
                case PieceType.KING:
                    if move.color:
                        self.move_piece(self.wk, move.from_square, move.to_square)
                    else:
                        self.move_piece(self.bk, move.from_square, move.to_square)
        
        # Capture

    def move_piece(self, bb, from_square, to_square):
        pass

    def remove_piece(self, move):
        pass

    def add_piece(self, move):
        pass

    def piece_at_square(self, square):
        square_bb = np.uint64(1) << np.unint64(square)

        for bb in self.pieces:
            if square_bb == bb & square_bb:
                return bb

    def print_board(self):
        chessboard = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        for i in range(64):
            if bitboard_to_binarystring(self.wp)[i] == '1':
                chessboard[i//8][i%8] = 'P'
            if bitboard_to_binarystring(self.wn)[i] == '1':
                chessboard[i//8][i%8] = 'N'
            if bitboard_to_binarystring(self.wb)[i] == '1':
                chessboard[i//8][i%8] = 'B'
            if bitboard_to_binarystring(self.wr)[i] == '1':
                chessboard[i//8][i%8] = 'R'
            if bitboard_to_binarystring(self.wq)[i] == '1':
                chessboard[i//8][i%8] = 'Q'
            if bitboard_to_binarystring(self.wk)[i] == '1':
                chessboard[i//8][i%8] = 'K'
            
            if bitboard_to_binarystring(self.bp)[i] == '1':
                chessboard[i//8][i%8] = 'p'
            if bitboard_to_binarystring(self.bn)[i] == '1':
                chessboard[i//8][i%8] = 'n'
            if bitboard_to_binarystring(self.bb)[i] == '1':
                chessboard[i//8][i%8] = 'b'
            if bitboard_to_binarystring(self.br)[i] == '1':
                chessboard[i//8][i%8] = 'r'
            if bitboard_to_binarystring(self.bq)[i] == '1':
                chessboard[i//8][i%8] = 'q'
            if bitboard_to_binarystring(self.bk)[i] == '1':
                chessboard[i//8][i%8] = 'k'

        reverse_rows(chessboard)
        for row in chessboard:
            print(row)

    def list_to_bitboard(self, board):
        reverse_rows(board)
        for i in range(64):
            binary = "0000000000000000000000000000000000000000000000000000000000000000"
            binary = binary[:i] + "1" + binary[i+1:] 
            match board[i//8][i%8]:
                case 'P':
                    self.wp += binarystring_to_bitboard(binary)
                case 'R':
                    self.wr += binarystring_to_bitboard(binary)
                case 'N':
                    self.wn += binarystring_to_bitboard(binary)
                case 'B':
                    self.wb += binarystring_to_bitboard(binary)
                case 'Q':
                    self.wq += binarystring_to_bitboard(binary)
                case 'K':
                    self.wk += binarystring_to_bitboard(binary)
                case 'p':
                    self.bp += binarystring_to_bitboard(binary)
                case 'r':
                    self.br += binarystring_to_bitboard(binary)
                case 'n':
                    self.bn += binarystring_to_bitboard(binary)
                case 'b':
                    self.bb += binarystring_to_bitboard(binary)
                case 'q':
                    self.bq += binarystring_to_bitboard(binary)
                case 'k':
                    self.bk += binarystring_to_bitboard(binary)

    def get_all_bitboards(self):
        return self.wp, self.wn, self.wb, self.wr, self.wq, self.wk, self.bp, self.bn, self.bb, self.br, self.bq, self.bk