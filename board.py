import numpy as np

from move import MoveType

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
        wp = np.uint64()
        wn = np.uint64()
        wb = np.uint64()
        wr = np.uint64()
        wq = np.uint64()
        wk = np.uint64()
        bp = np.uint64()
        bn = np.uint64()
        bb = np.uint64()
        br = np.uint64()
        bq = np.uint64()
        bk = np.uint64()

        self.pieces = {
            'wp': wp, 
            'wn': wn, 
            'wb': wb, 
            'wr': wr, 
            'wq': wq, 
            'wk': wk, 
            'bp': bp, 
            'bn': bn, 
            'bb': bb, 
            'br': br, 
            'bq': bq, 
            'bk': bk
        }

        self.white_attacks = np.uint64()
        self.black_attacks = np.uint64()

        self.black_castle_left_flag = True
        self.black_castle_right_flag = True
        self.white_castle_left_flag = True
        self.white_castle_right_flag = True

        self.history = list()

    def make_move(self, m):
        # Standard Move
        if m.color == 1:
            col_char = 'w'
        if m.color == -1:
            col_char = 'b'
        piece = f"{col_char}{m.piece.value}"

        if m.move_type == MoveType.NORMAL or m.move_type == MoveType.PAWN_DOUBLE:
            self.move_piece(piece, m.from_square, m.to_square)

        # Castle
        if m.move_type == MoveType.CASTLE_KINGSIDE:
            rook_start = m.to_square - 2
            rook_target = m.to_square + 1
            if m.color == 1:
                self.move_piece('wk', m.from_square, m.to_square)
                self.move_piece('wr', rook_start, rook_target)
            else:
                self.move_piece('bk', m.from_square, m.to_square)
                self.move_piece('br', rook_start, rook_target)
        if m.move_type == MoveType.CASTLE_QUEENSIDE:
            rook_start = m.to_square + 1
            rook_target = m.to_square - 2
            if m.color == 1:
                self.move_piece('wk', m.from_square, m.to_square)
                self.move_piece('wr', rook_start, rook_target)
            else:
                self.move_piece('bk', m.from_square, m.to_square)
                self.move_piece('br', rook_start, rook_target)

        # Capture
        if m.move_type == MoveType.CAPTURE:

            cap_piece = self.piece_at_square(m.to_square)
            self.remove_piece(cap_piece, m.to_square)
            self.move_piece(piece, m.from_square, m.to_square)

        # Promotion
        if m.move_type == MoveType.PROMOTION:
            cap_piece = self.piece_at_square(m.to_square)
            # Capture
            if cap_piece is not None:
                self.remove_piece(cap_piece, m.to_square)
            if m.color == 1:
                self.remove_piece('wp', m.from_square)
            else:
                self.remove_piece('bp', m.from_square)
            
            prom_piece = f"{col_char}{m.promoted_piece.value}"
            self.add_piece(prom_piece, m.to_square)

        self.history.append(m)

    def move_piece(self, bb, from_square, to_square):
        square_bb = (np.uint64(1) << np.uint64(to_square)) | (np.uint64(1) << np.uint64(from_square))

        self.pieces[bb] ^= square_bb

    def remove_piece(self, bb, square):
        square_bb = (np.uint64(1) << np.uint64(square))

        self.pieces[bb] ^= square_bb

    def add_piece(self, bb, square):
        square_bb = (np.uint64(1) << np.uint64(square))

        self.pieces[bb] |= square_bb

    def piece_at_square(self, square):
        square_bb = np.uint64(1) << np.uint64(square)

        for piece, bb in self.pieces.items():
            if square_bb == bb & square_bb:
                return piece
        return None

    def is_piece_attacked(self, piece, col):
        if col == 1:
            attacks = self.black_attacks
        if col == -1:
            attacks = self.white_attacks
        if self.pieces[piece] & attacks:
            return True
        else:
            return False

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
            if bitboard_to_binarystring(self.pieces['wp'])[i] == '1':
                chessboard[i//8][i%8] = 'P'
            if bitboard_to_binarystring(self.pieces['wn'])[i] == '1':
                chessboard[i//8][i%8] = 'N'
            if bitboard_to_binarystring(self.pieces['wb'])[i] == '1':
                chessboard[i//8][i%8] = 'B'
            if bitboard_to_binarystring(self.pieces['wr'])[i] == '1':
                chessboard[i//8][i%8] = 'R'
            if bitboard_to_binarystring(self.pieces['wq'])[i] == '1':
                chessboard[i//8][i%8] = 'Q'
            if bitboard_to_binarystring(self.pieces['wk'])[i] == '1':
                chessboard[i//8][i%8] = 'K'
            
            if bitboard_to_binarystring(self.pieces['bp'])[i] == '1':
                chessboard[i//8][i%8] = 'p'
            if bitboard_to_binarystring(self.pieces['bn'])[i] == '1':
                chessboard[i//8][i%8] = 'n'
            if bitboard_to_binarystring(self.pieces['bb'])[i] == '1':
                chessboard[i//8][i%8] = 'b'
            if bitboard_to_binarystring(self.pieces['br'])[i] == '1':
                chessboard[i//8][i%8] = 'r'
            if bitboard_to_binarystring(self.pieces['bq'])[i] == '1':
                chessboard[i//8][i%8] = 'q'
            if bitboard_to_binarystring(self.pieces['bk'])[i] == '1':
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
                    self.pieces['wp'] += binarystring_to_bitboard(binary)
                case 'R':
                    self.pieces['wr'] += binarystring_to_bitboard(binary)
                case 'N':
                    self.pieces['wn'] += binarystring_to_bitboard(binary)
                case 'B':
                    self.pieces['wb'] += binarystring_to_bitboard(binary)
                case 'Q':
                    self.pieces['wq'] += binarystring_to_bitboard(binary)
                case 'K':
                    self.pieces['wk'] += binarystring_to_bitboard(binary)
                case 'p':
                    self.pieces['bp'] += binarystring_to_bitboard(binary)
                case 'r':
                    self.pieces['br'] += binarystring_to_bitboard(binary)
                case 'n':
                    self.pieces['bn'] += binarystring_to_bitboard(binary)
                case 'b':
                    self.pieces['bb'] += binarystring_to_bitboard(binary)
                case 'q':
                    self.pieces['bq'] += binarystring_to_bitboard(binary)
                case 'k':
                    self.pieces['bk'] += binarystring_to_bitboard(binary)

        self.white_pieces = self.pieces['wp']|self.pieces['wn']|self.pieces['wb']|self.pieces['wr']|self.pieces['wq']|self.pieces['wk']
        self.black_pieces = self.pieces['bp']|self.pieces['bn']|self.pieces['bb']|self.pieces['br']|self.pieces['bq']|self.pieces['bk']

    def get_all_bitboards(self):
        return self.pieces['wp'], self.pieces['wn'], self.pieces['wb'], self.pieces['wr'], self.pieces['wq'], self.pieces['wk'], self.pieces['bp'], self.pieces['bn'], self.pieces['bb'], self.pieces['br'], self.pieces['bq'], self.pieces['bk']
    
    def get_history(self):
        return self.history

    def can_castle_left(self, color):
        if color == 1:
            return self.white_castle_left_flag
        if color == -1:
            return self.black_castle_left_flag
        
    def can_castle_right(self, color):
        if color == 1:
            return self.white_castle_right_flag
        if color == -1:
            return self.black_castle_right_flag
        
    def update_white_attacks(self, attacks):
        self.white_attacks = attacks

    def update_black_attacks(self, attacks):
        self.black_attacks = attacks