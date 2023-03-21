import bitscan
import numpy as np
import precompute

from enum import Enum

file_a = np.uint64(72340172838076673)
file_h = np.uint64(9259542123273814144)
rank_1 = np.uint64(255)
rank_4 = np.uint64(4278190080)
rank_5 = np.uint64(1095216660480)
rank_7 = np.uint64(71776119061217280)
rank_8 = np.uint64(18374686479671623680)

knight_moves_table, knight_bitboards_table = precompute.precompute_knight_moves()
king_moves_table, king_bitboards_table = precompute.precompute_king_moves()

class Move:
    def __init__(self, from_square, to_square, move_type, promoted_piece=None):
        self.from_square = from_square
        self.to_square = to_square
        self.move_type = move_type
        self.promoted_piece = promoted_piece
    
    def __repr__(self):
        return f"{self.from_square} -> {self.to_square} ({self.move_type})"


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


class WhiteMoves:
    def __init__(self, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk):
        self.white_noncapturable = ~(wp|wn|wb|wr|wq|wk|bk)
        self.black_pieces = bp|bn|bb|br|bq
        self.empty = ~(wp|wn|wb|wr|wq|wk|bp|bn|bb|br|bq|bk)
        self.castle_left_flag = True
        self.castle_right_flag = True

    def possible_moves(self, history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk):
        move_list = list()
        move_list += self.possible_pawn_moves(history, wp, bp)
        move_list += self.possible_knight_moves(wn)
        move_list += self.possible_king_moves(wk, wr)
        print(move_list)

    def possible_pawn_moves(self, history, wp, bp):
        move_list = list()

        captures = self.pawn_captures(wp)
        pushes = self.pawn_pushes(wp)
        pawn_promotions = self.pawn_promotions(wp)
        en_passant = self.pawn_en_passant(history, wp, bp)

        move_list = captures + pushes + pawn_promotions + en_passant
        return move_list

    def pawn_captures(self, wp):

        move_list = list()

        pawn_moves = np.uint64()
        # Capture right
        pawn_moves = northeast_one(wp) & self.black_pieces & ~rank_8 & ~file_a
        target_squares = bitscan.square_index_serialization(pawn_moves)
        for target in target_squares:
            start_square = target - 9
            move_list.append(Move(start_square, target, MoveType.CAPTURE))

        # Capture left
        pawn_moves = northwest_one(wp) & self.black_pieces & ~rank_8 & ~file_h
        target_squares = bitscan.square_index_serialization(pawn_moves)
        for target in target_squares:
            start_square = target - 7
            move_list.append(Move(start_square, target, MoveType.CAPTURE))

        return move_list

    def pawn_pushes(self, wp):

        move_list = list()

        pawn_moves = np.uint64()
        # Push forward 1
        pawn_moves = north_one(wp) & self.empty & ~rank_8
        target_squares = bitscan.square_index_serialization(pawn_moves)
        for target in target_squares:
            start_square = target - 8
            move_list.append(Move(start_square, target, MoveType.NORMAL))

        # Push forward 2
        pawn_moves = north_one(north_one(wp)) & self.empty & (self.empty << np.uint64(8)) & rank_4
        target_squares = bitscan.square_index_serialization(pawn_moves)
        for target in target_squares:
            start_square = target - 16
            move_list.append(Move(start_square, target, MoveType.PAWN_DOUBLE))

        return move_list
    
    def pawn_promotions(self, wp):

        move_list = list()

        pawn_moves = np.uint64()
        # Promotion by capture right
        pawn_moves = northeast_one(wp) & self.black_pieces & rank_8 & ~file_a
        target_squares = bitscan.square_index_serialization(pawn_moves)
        for target in target_squares:
            start_square = target - 9
            move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.QUEEN))
            move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.KNIGHT))
            move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.ROOK))
            move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.BISHOP))

        # Promotion by capture left
        pawn_moves = northwest_one(wp) & self.black_pieces & rank_8 & ~file_h
        target_squares = bitscan.square_index_serialization(pawn_moves)
        for target in target_squares:
            start_square = target - 7
            move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.QUEEN))
            move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.KNIGHT))
            move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.ROOK))
            move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.BISHOP))

        # Promotion by move forward 1
        pawn_moves = north_one(wp) & self.black_pieces & rank_8
        target_squares = bitscan.square_index_serialization(pawn_moves)
        for target in target_squares:
            start_square = target - 8
            move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.QUEEN))
            move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.KNIGHT))
            move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.ROOK))
            move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.BISHOP))

        return move_list

    def pawn_en_passant(self, history, wp, bp):

        move_list = list()

        pawn_moves = np.uint64()
        # En Passant 
        if history:
            if history[-1].move_type == MoveType.PAWN_DOUBLE:
                # En Passant Right
                pawn_moves = east_one(wp) & bp & rank_5 & ~file_a
                target_squares = bitscan.square_index_serialization(pawn_moves)
                for target in target_squares:
                    start_square = target - 1
                    end_square = target + 8
                    if target == history[-1].to_square:
                        move_list.append(Move(start_square, end_square, MoveType.EN_PASSANT))

                # En Passant Left
                pawn_moves = west_one(wp) & bp & rank_5 & ~file_h
                target_squares = bitscan.square_index_serialization(pawn_moves)
                for target in target_squares:
                    start_square = target + 1
                    end_square = target + 8
                    if target == history[-1].to_square:
                        move_list.append(Move(start_square, end_square, MoveType.EN_PASSANT))

        return move_list

    def possible_knight_moves(self, wn):

        move_list = list()
        knight_moves = np.uint64()

        knight_squares = bitscan.square_index_serialization(wn)

        for knight_square in knight_squares:
            # Moves
            knight_moves = knight_bitboards_table[knight_square] & self.empty
            target_squares = bitscan.square_index_serialization(knight_moves)
            for target in target_squares:
                start_square = knight_square
                move_list.append(Move(start_square, target, MoveType.NORMAL))
            
            # Capture
            knight_moves = knight_bitboards_table[knight_square] & self.black_pieces
            target_squares = bitscan.square_index_serialization(knight_moves)
            for target in target_squares:
                start_square = knight_square
                move_list.append(Move(start_square, target, MoveType.CAPTURE))

        return move_list

    def possible_king_moves(self, wk, wr):

        move_list = list()
        king_moves = np.uint64()

        king_squares = bitscan.square_index_serialization(wk)

        for king_square in king_squares:
            # Moves
            king_moves = king_bitboards_table[king_square] & self.empty
            target_squares = bitscan.square_index_serialization(king_moves)
            for target in target_squares:
                start_square = king_square
                move_list.append(Move(start_square, target, MoveType.NORMAL))
            
            # Capture
            king_moves = king_bitboards_table[king_square] & self.black_pieces
            target_squares = bitscan.square_index_serialization(king_moves)
            for target in target_squares:
                start_square = king_square
                move_list.append(Move(start_square, target, MoveType.CAPTURE))

            # Castle left
            if self.castle_left_flag:
                king_moves = west_one(west_one(west_one(west_one(wk)))) & wr & (self.empty >> np.uint64(1)) & (self.empty >> np.uint64(2)) & (self.empty >> np.uint64(3))
                target_squares = bitscan.square_index_serialization(king_moves)
                for target in target_squares:
                    start_square = king_square
                    move_list.append(Move(start_square, target, MoveType.EN_PASSANT))

            # Castle right
            if self.castle_right_flag:
                king_moves = east_one(east_one(east_one(wk))) & wr & (self.empty << np.uint64(1)) & (self.empty << np.uint64(2))
                target_squares = bitscan.square_index_serialization(king_moves)
                for target in target_squares:
                    start_square = king_square
                    move_list.append(Move(start_square, target, MoveType.EN_PASSANT))

        return move_list
        
    def horizontal_slide_moves(self):
        pass

    def vertical_slide_moves(self):
        pass

    def diagonal_left_moves(self):
        pass

    def diagonal_right_moves(self):
        pass

def north_one(bitboard):
    return bitboard << np.uint64(8)

def northwest_one(bitboard):
    return bitboard << np.uint64(7)

def northeast_one(bitboard):
    return bitboard << np.uint64(9)

def west_one(bitboard):
    return bitboard >> np.uint64(1)

def east_one(bitboard):
    return bitboard << np.uint64(1)

def south_one(bitboard):
    return bitboard >> np.uint64(8)

def southwest_one(bitboard):
    return bitboard >> np.uint64(9)

def southeast_one(bitboard):
    return bitboard >> np.uint64(7)