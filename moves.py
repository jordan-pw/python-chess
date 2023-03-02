import bitscan
import numpy as np
from enum import Enum

import time

leading_one = np.uint64(9223372036854775808)

file_a = np.uint64(72340172838076673)
file_h = np.uint64(9259542123273814144)
rank_1 = np.uint64(255)
rank_4 = np.uint64(4278190080)
rank_5 = np.uint64(1095216660480)
rank_7 = np.uint64(71776119061217280)
rank_8 = np.uint64(18374686479671623680)

white_noncapturable = np.uint64()
black_pieces = np.uint64()
empty = np.uint64()

test = False

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

def possible_moves_white(history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk):
    global white_noncapturable
    global black_pieces
    global empty
    white_noncapturable = ~(wp|wn|wb|wr|wq|wk|bk)
    black_pieces = bp|bn|bb|br|bq
    empty = ~(wp|wn|wb|wr|wq|wk|bp|bn|bb|br|bq|bk)

    move_list = possible_pmoves_white(history, wp, bp)
    print(move_list)

def possible_pmoves_white(history, wp, bp):
    move_list = list()

    pawn_moves = np.uint64()

    # Moves and captures
    # Capture right
    pawn_moves = northeast_one(wp) & black_pieces & ~rank_8 & ~file_a
    target_squares = bitscan.square_index_serialization(pawn_moves)
    for target in target_squares:
        start_square = target - 9
        move_list.append(Move(start_square, target, MoveType.CAPTURE))

    # Capture left
    pawn_moves = northwest_one(wp) & black_pieces & ~rank_8 & ~file_h
    target_squares = bitscan.square_index_serialization(pawn_moves)
    for target in target_squares:
        start_square = target - 7
        move_list.append(Move(start_square, target, MoveType.CAPTURE))

    # Move forward 1
    pawn_moves = north_one(wp) & empty & ~rank_8
    target_squares = bitscan.square_index_serialization(pawn_moves)
    for target in target_squares:
        start_square = target - 8
        move_list.append(Move(start_square, target, MoveType.NORMAL))

    # Move forward 2
    pawn_moves = north_one(north_one(wp)) & empty & (empty << np.uint64(8)) & rank_4
    target_squares = bitscan.square_index_serialization(pawn_moves)
    for target in target_squares:
        start_square = target - 16
        move_list.append(Move(start_square, target, MoveType.PAWN_DOUBLE))

    # Promotions
    # Promotion by capture right
    pawn_moves = northeast_one(wp) & black_pieces & rank_8 & ~file_a
    target_squares = bitscan.square_index_serialization(pawn_moves)
    for target in target_squares:
        start_square = target - 9
        move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.QUEEN))
        move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.KNIGHT))
        move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.ROOK))
        move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.BISHOP))

    # Promotion by capture left
    pawn_moves = northwest_one(wp) & black_pieces & rank_8 & ~file_h
    target_squares = bitscan.square_index_serialization(pawn_moves)
    for target in target_squares:
        start_square = target - 7
        move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.QUEEN))
        move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.KNIGHT))
        move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.ROOK))
        move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.BISHOP))

    # Promotion by move forward 1
    pawn_moves = north_one(wp) & black_pieces & rank_8
    target_squares = bitscan.square_index_serialization(pawn_moves)
    for target in target_squares:
        start_square = target - 8
        move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.QUEEN))
        move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.KNIGHT))
        move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.ROOK))
        move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.BISHOP))
    
    # En Passant 
    if history:
        if history[-1].move_type == MoveType.PAWN_DOUBLE:
            pawn_moves = east_one(wp) & bp & rank_5 & ~file_a
            target_squares = bitscan.square_index_serialization(pawn_moves)
            for target in target_squares:
                start_square = target - 1
                end_square = target + 8
                if target == history[-1].to_square:
                    move_list.append(Move(start_square, end_square, MoveType.EN_PASSANT))

            pawn_moves = west_one(wp) & bp & rank_5 & ~file_h
            target_squares = bitscan.square_index_serialization(pawn_moves)
            for target in target_squares:
                start_square = target + 1
                end_square = target + 8
                if target == history[-1].to_square:
                    move_list.append(Move(start_square, end_square, MoveType.EN_PASSANT))
    return move_list

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