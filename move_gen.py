import bitutils
import numpy as np
import precompute

from copy import deepcopy
from move import Move, MoveType, Promotion, PieceType
from bitutils import north_one, northeast_one, northwest_one, east_one, west_one, south_one, southeast_one, southwest_one

file_a = np.uint64(72340172838076673)
file_h = np.uint64(9259542123273814144)
rank_1 = np.uint64(255)
rank_4 = np.uint64(4278190080)
rank_5 = np.uint64(1095216660480)
rank_7 = np.uint64(71776119061217280)
rank_8 = np.uint64(18374686479671623680)

knight_moves_table, knight_bitboards_table = precompute.precompute_knight_moves()
king_moves_table, king_bitboards_table = precompute.precompute_king_moves()
rays_table = precompute.precompute_rays()

class Moves:
    def __init__(self, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk, col):
        self.color = col # 1 = white, -1 = black

        # Initialize noncapturable pieces
        if self.color == 1:
            self.noncapturable = ~(wp|wn|wb|wr|wq|wk|bk)
        if self.color == -1:
            self.noncapturable = ~(bp|bn|bb|br|bq|bk|wk)

        # Get opposing pieces
        if self.color == 1:
            self.opp_pieces = bp|bn|bb|br|bq|bk
        if self.color == -1:
            self.opp_pieces = wp|wn|wb|wr|wq|wk

        self.empty = ~(wp|wn|wb|wr|wq|wk|bp|bn|bb|br|bq|bk)
        
        self.castle_left_flag = True
        self.castle_right_flag = True

        self.attacks = np.uint64(0)

    def possible_moves(self, history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk):
        move_list = list()
        self.attacks = np.uint64(0)
        if self.color == 1:
            move_list += self.possible_pawn_moves(history, wp, bp)
            move_list += self.possible_knight_moves(wn)
            move_list += self.possible_king_moves(wk, wr)
            move_list += self.possible_bishop_moves(wb)
            move_list += self.possible_rook_moves(wr)
            move_list += self.possible_queen_moves(wq)
        if self.color == -1:
            move_list += self.possible_pawn_moves(history, bp, wp)
            move_list += self.possible_knight_moves(bn)
            move_list += self.possible_king_moves(bk, br)
            move_list += self.possible_bishop_moves(bb)
            move_list += self.possible_rook_moves(br)
            move_list += self.possible_queen_moves(bq)

        return move_list, self.attacks

    def legal_moves(self, b, move_list, opp_attacks):
        legal_move_list = list()

        print(opp_attacks)

        for m in move_list:
            temp_board = deepcopy(b)
            temp_board.make_move(m)

            if self.color == 1 and not temp_board.is_piece_attacked('wk', opp_attacks):
                legal_move_list.append(m)
            if self.color == -1 and not temp_board.is_piece_attacked('bk', opp_attacks):
                legal_move_list.append(m)

        return legal_move_list

    def possible_pawn_moves(self, history, p, op):
        move_list = list()

        captures = self.pawn_captures(p)
        pushes = self.pawn_pushes(p)
        pawn_promotions = self.pawn_promotions(p)
        en_passant = self.pawn_en_passant(history, p, op)

        move_list = captures + pushes + pawn_promotions + en_passant
        return move_list

    def pawn_captures(self, p):

        move_list = list()

        pawn_moves = np.uint64()
        # Capture right
        if self.color == 1:
            pawn_moves = northeast_one(p) & self.opp_pieces & ~rank_8 & ~file_a
            offset = 9
        if self.color == -1:
            pawn_moves = southeast_one(p) & self.opp_pieces & ~rank_1 & ~file_a
            offset = -7

        target_squares = bitutils.square_index_serialization(pawn_moves)
        for target in target_squares:
            start_square = target - offset
            self.attacks |= pawn_moves
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.CAPTURE))

        # Capture left
        if self.color == 1:
            pawn_moves = northwest_one(p) & self.opp_pieces & ~rank_8 & ~file_h
            offset = 7
        if self.color == -1:
            pawn_moves = southwest_one(p) & self.opp_pieces & ~rank_1 & ~file_h
            offset = -9
            
        target_squares = bitutils.square_index_serialization(pawn_moves)
        for target in target_squares:
            start_square = target - offset
            self.attacks |= pawn_moves
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.CAPTURE))

        return move_list

    def pawn_pushes(self, p):

        move_list = list()

        pawn_moves = np.uint64()
        # Push forward 1
        if self.color == 1:
            pawn_moves = north_one(p) & self.empty & ~rank_8
        if self.color == -1:
            pawn_moves = south_one(p) & self.empty & ~rank_1
        
        target_squares = bitutils.square_index_serialization(pawn_moves)
        for target in target_squares:
            start_square = target - (8 * self.color)
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.NORMAL))

        # Push forward 2
        if self.color == 1:
            pawn_moves = north_one(north_one(p)) & self.empty & (self.empty << np.uint64(8)) & rank_4
        if self.color == -1:
            pawn_moves = south_one(south_one(p)) & self.empty & (self.empty >> np.uint64(8)) & rank_5
        
        target_squares = bitutils.square_index_serialization(pawn_moves)
        for target in target_squares:
            start_square = target - (16 * self.color)
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.PAWN_DOUBLE))

        return move_list
    
    def pawn_promotions(self, p):

        move_list = list()

        pawn_moves = np.uint64()
        # Promotion by capture right
        if self.color == 1:
            pawn_moves = northeast_one(p) & self.opp_pieces & rank_8 & ~file_a
            offset = 9
        if self.color == -1:
            pawn_moves = southeast_one(p) & self.opp_pieces & rank_1 & ~file_a
            offset = -7

        target_squares = bitutils.square_index_serialization(pawn_moves)
        for target in target_squares:
            start_square = target - offset
            self.attacks |= pawn_moves
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.PROMOTION, Promotion.QUEEN))
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.PROMOTION, Promotion.KNIGHT))
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.PROMOTION, Promotion.ROOK))
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.PROMOTION, Promotion.BISHOP))

        # Promotion by capture left
        if self.color == 1:
            pawn_moves = northwest_one(p) & self.opp_pieces & rank_8 & ~file_h
            offset = 7
        if self.color == -1:
            pawn_moves = southwest_one(p) & self.opp_pieces & rank_1 & ~file_h
            offset = -9

        target_squares = bitutils.square_index_serialization(pawn_moves)
        for target in target_squares:
            start_square = target - offset
            self.attacks |= pawn_moves
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.PROMOTION, Promotion.QUEEN))
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.PROMOTION, Promotion.KNIGHT))
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.PROMOTION, Promotion.ROOK))
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.PROMOTION, Promotion.BISHOP))

        # Promotion by move forward 1
        if self.color == 1:
            pawn_moves = north_one(p) & self.empty & rank_8
        if self.color == -1:
            pawn_moves = south_one(p) & self.empty & rank_1
        
        target_squares = bitutils.square_index_serialization(pawn_moves)
        for target in target_squares:
            start_square = target - (8 * self.color)
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.PROMOTION, Promotion.QUEEN))
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.PROMOTION, Promotion.KNIGHT))
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.PROMOTION, Promotion.ROOK))
            move_list.append(Move(self.color, PieceType.PAWN, start_square, target, MoveType.PROMOTION, Promotion.BISHOP))

        return move_list

    def pawn_en_passant(self, history, p, op):

        move_list = list()

        pawn_moves = np.uint64()
        # En Passant 
        if history:
            if history[-1].move_type == MoveType.PAWN_DOUBLE:
                # En Passant Right
                if self.color == 1:
                    pawn_moves = east_one(p) & op & rank_5 & ~file_a
                if self.color == -1:
                    pawn_moves = east_one(p) & op & rank_4 & ~file_a

                target_squares = bitutils.square_index_serialization(pawn_moves)
                for target in target_squares:
                    start_square = target - (1 * self.color)
                    end_square = target + (8 * self.color)
                    self.attacks |= pawn_moves
                    if target == history[-1].to_square:
                        move_list.append(Move(self.color, PieceType.PAWN, start_square, end_square, MoveType.EN_PASSANT))

                # En Passant Left
                if self.color == 1:
                    pawn_moves = west_one(p) & op & rank_5 & ~file_h
                if self.color == -1:
                    pawn_moves = west_one(p) & op & rank_4 & ~file_h

                target_squares = bitutils.square_index_serialization(pawn_moves)
                for target in target_squares:
                    start_square = target + (1 * self.color)
                    end_square = target + (8 * self.color)
                    self.attacks |= pawn_moves
                    if target == history[-1].to_square:
                        move_list.append(Move(self.color, PieceType.PAWN, start_square, end_square, MoveType.EN_PASSANT))

        return move_list

    def possible_knight_moves(self, n):

        move_list = list()
        knight_moves = np.uint64()

        knight_squares = bitutils.square_index_serialization(n)

        for knight_square in knight_squares:
            # Moves
            knight_moves = knight_bitboards_table[knight_square] & self.empty
            target_squares = bitutils.square_index_serialization(knight_moves)
            for target in target_squares:
                start_square = knight_square
                move_list.append(Move(self.color, PieceType.KNIGHT, start_square, target, MoveType.NORMAL))
            
            # Capture
            knight_moves = knight_bitboards_table[knight_square] & self.opp_pieces
            target_squares = bitutils.square_index_serialization(knight_moves)
            for target in target_squares:
                start_square = knight_square
                self.attacks |= knight_moves
                move_list.append(Move(self.color, PieceType.KNIGHT, start_square, target, MoveType.CAPTURE))

        return move_list

    def possible_rook_moves(self, r):
        move_list = self.possible_rf_moves(r, PieceType.ROOK)
        return move_list

    def possible_bishop_moves(self, b):
        move_list = self.possible_diag_moves(b, PieceType.BISHOP)
        return move_list

    def possible_queen_moves(self, q):
        move_list = self.possible_rf_moves(q, PieceType.QUEEN)
        move_list += self.possible_diag_moves(q, PieceType.QUEEN)
        return move_list

    def possible_king_moves(self, k, r):

        move_list = list()
        king_moves = np.uint64()

        king_squares = bitutils.square_index_serialization(k)

        for king_square in king_squares:
            # Moves
            king_moves = king_bitboards_table[king_square] & self.empty
            target_squares = bitutils.square_index_serialization(king_moves)
            for target in target_squares:
                start_square = king_square
                move_list.append(Move(self.color, PieceType.KING, start_square, target, MoveType.NORMAL))
            
            # Capture
            king_moves = king_bitboards_table[king_square] & self.opp_pieces
            target_squares = bitutils.square_index_serialization(king_moves)
            for target in target_squares:
                start_square = king_square
                self.attacks |= king_moves
                move_list.append(Move(self.color, PieceType.KING, start_square, target, MoveType.CAPTURE))

            # Castle kingside
            if self.castle_left_flag:
                king_moves = west_one(west_one(west_one(west_one(k)))) & r & (self.empty >> np.uint64(1)) & (self.empty >> np.uint64(2)) & (self.empty >> np.uint64(3))
                target_squares = bitutils.square_index_serialization(king_moves)
                for target in target_squares:
                    start_square = king_square
                    move_list.append(Move(self.color, PieceType.KING, start_square, target+2, MoveType.CASTLE_QUEENSIDE))

            # Castle queenside
            if self.castle_right_flag:
                king_moves = east_one(east_one(east_one(k))) & r & (self.empty << np.uint64(1)) & (self.empty << np.uint64(2))
                target_squares = bitutils.square_index_serialization(king_moves)
                for target in target_squares:
                    start_square = king_square
                    move_list.append(Move(self.color, PieceType.KING, start_square, target-1, MoveType.CASTLE_KINGSIDE))

        return move_list
        
    def possible_rf_moves(self, bb, p):

        occ = ~self.empty    

        move_list = list()
        rf_moves = np.uint64()
        rf_attacks = np.uint64()

        start_squares = bitutils.square_index_serialization(bb)
        for start_square in start_squares:
            # Positive
            keys = ['north', 'east']
            for key in keys:
                rf_moves = rays_table[key][start_square]
                blocker = rf_moves & occ
                if blocker:
                    square = bitutils.bitscan_forward(blocker)
                    rf_moves ^= rays_table[key][square]

                rf_attacks = rf_moves & self.opp_pieces
                rf_moves &= self.empty

                target_squares = bitutils.square_index_serialization(rf_attacks)
                for target in target_squares:
                    self.attacks |= rf_attacks
                    move_list.append(Move(self.color, p, start_square, target, MoveType.CAPTURE))

                target_squares = bitutils.square_index_serialization(rf_moves)
                for target in target_squares:
                    move_list.append(Move(self.color, p, start_square, target, MoveType.NORMAL))

            # Negative
            keys = ['south', 'west']
            for key in keys:
                rf_moves = rays_table[key][start_square]
                blocker = rf_moves & occ
                if blocker:
                    square = bitutils.bitscan_reverse(blocker)
                    rf_moves ^= rays_table[key][square]

                rf_attacks = rf_moves & self.opp_pieces
                rf_moves &= self.empty
                
                target_squares = bitutils.square_index_serialization(rf_attacks)
                for target in target_squares:
                    self.attacks |= rf_attacks
                    move_list.append(Move(self.color, p, start_square, target, MoveType.CAPTURE))

                target_squares = bitutils.square_index_serialization(rf_moves)
                for target in target_squares:
                    move_list.append(Move(self.color, p, start_square, target, MoveType.NORMAL))
                
        return move_list

    def possible_diag_moves(self, bb, p):
        occ = ~self.empty    

        move_list = list()
        diag_moves = np.uint64()
        diag_attacks = np.uint64()

        start_squares = bitutils.square_index_serialization(bb)
        for start_square in start_squares:
            # Positive
            keys = ['northeast', 'northwest']
            for key in keys:
                diag_moves = rays_table[key][start_square]
                blocker = diag_moves & occ
                if blocker:
                    square = bitutils.bitscan_forward(blocker)
                    diag_moves ^= rays_table[key][square]

                diag_attacks = diag_moves & self.opp_pieces
                diag_moves &= self.empty

                target_squares = bitutils.square_index_serialization(diag_attacks)
                for target in target_squares:
                    self.attacks |= diag_attacks
                    move_list.append(Move(self.color, p, start_square, target, MoveType.CAPTURE))

                target_squares = bitutils.square_index_serialization(diag_moves)
                for target in target_squares:
                    move_list.append(Move(self.color, p, start_square, target, MoveType.NORMAL))

            # Negative
            keys = ['southeast', 'southwest']
            for key in keys:
                diag_moves = rays_table[key][start_square]
                blocker = diag_moves & occ
                if blocker:
                    square = bitutils.bitscan_reverse(blocker)
                    diag_moves ^= rays_table[key][square]

                diag_attacks = diag_moves & self.opp_pieces
                diag_moves &= self.empty
                
                target_squares = bitutils.square_index_serialization(diag_attacks)
                for target in target_squares:
                    self.attacks |= diag_attacks
                    move_list.append(Move(self.color, p, start_square, target, MoveType.CAPTURE))

                target_squares = bitutils.square_index_serialization(diag_moves)
                for target in target_squares:
                    move_list.append(Move(self.color, p, start_square, target, MoveType.NORMAL))
                
        return move_list


# class WhiteMoves:
#     def __init__(self, b):
#         self.white_noncapturable = ~(b.wp|b.wn|b.wb|b.wr|b.wq|b.wk|b.bk)
#         self.black_pieces = b.bp|b.bn|b.bb|b.br|b.bq
#         self.empty = ~(b.wp|b.wn|b.wb|b.wr|b.wq|b.wk|b.bp|b.bn|b.bb|b.br|b.bq|b.bk)
#         self.castle_left_flag = True
#         self.castle_right_flag = True

#     def possible_moves(self, history, b):
#         move_list = list()
#         move_list += self.possible_pawn_moves(history, b.wp, b.bp)
#         move_list += self.possible_knight_moves(b.wn)
#         move_list += self.possible_king_moves(b.wk, b.wr)
#         move_list += self.possible_bishop_moves(b.wb)
#         move_list += self.possible_rook_moves(b.wr)
#         move_list += self.possible_queen_moves(b.wq)

#         print(move_list)

#     def possible_pawn_moves(self, history, wp, bp):
#         move_list = list()

#         captures = self.pawn_captures(wp)
#         pushes = self.pawn_pushes(wp)
#         pawn_promotions = self.pawn_promotions(wp)
#         en_passant = self.pawn_en_passant(history, wp, bp)

#         move_list = captures + pushes + pawn_promotions + en_passant
#         return move_list

#     def pawn_captures(self, wp):

#         move_list = list()

#         pawn_moves = np.uint64()
#         # Capture right
#         pawn_moves = northeast_one(wp) & self.black_pieces & ~rank_8 & ~file_a
#         target_squares = bitutils.square_index_serialization(pawn_moves)
#         for target in target_squares:
#             start_square = target - 9
#             move_list.append(Move(start_square, target, MoveType.CAPTURE))

#         # Capture left
#         pawn_moves = northwest_one(wp) & self.black_pieces & ~rank_8 & ~file_h
#         target_squares = bitutils.square_index_serialization(pawn_moves)
#         for target in target_squares:
#             start_square = target - 7
#             move_list.append(Move(start_square, target, MoveType.CAPTURE))

#         return move_list

#     def pawn_pushes(self, wp):

#         move_list = list()

#         pawn_moves = np.uint64()
#         # Push forward 1
#         pawn_moves = north_one(wp) & self.empty & ~rank_8
#         target_squares = bitutils.square_index_serialization(pawn_moves)
#         for target in target_squares:
#             start_square = target - 8
#             move_list.append(Move(start_square, target, MoveType.NORMAL))

#         # Push forward 2
#         pawn_moves = north_one(north_one(wp)) & self.empty & (self.empty << np.uint64(8)) & rank_4
#         target_squares = bitutils.square_index_serialization(pawn_moves)
#         for target in target_squares:
#             start_square = target - 16
#             move_list.append(Move(start_square, target, MoveType.PAWN_DOUBLE))

#         return move_list
    
#     def pawn_promotions(self, wp):

#         move_list = list()

#         pawn_moves = np.uint64()
#         # Promotion by capture right
#         pawn_moves = northeast_one(wp) & self.black_pieces & rank_8 & ~file_a
#         target_squares = bitutils.square_index_serialization(pawn_moves)
#         for target in target_squares:
#             start_square = target - 9
#             move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.QUEEN))
#             move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.KNIGHT))
#             move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.ROOK))
#             move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.BISHOP))

#         # Promotion by capture left
#         pawn_moves = northwest_one(wp) & self.black_pieces & rank_8 & ~file_h
#         target_squares = bitutils.square_index_serialization(pawn_moves)
#         for target in target_squares:
#             start_square = target - 7
#             move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.QUEEN))
#             move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.KNIGHT))
#             move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.ROOK))
#             move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.BISHOP))

#         # Promotion by move forward 1
#         pawn_moves = north_one(wp) & self.black_pieces & rank_8
#         target_squares = bitutils.square_index_serialization(pawn_moves)
#         for target in target_squares:
#             start_square = target - 8
#             move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.QUEEN))
#             move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.KNIGHT))
#             move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.ROOK))
#             move_list.append(Move(start_square, target, MoveType.PROMOTION, Promotion.BISHOP))

#         return move_list

#     def pawn_en_passant(self, history, wp, bp):

#         move_list = list()

#         pawn_moves = np.uint64()
#         # En Passant 
#         if history:
#             if history[-1].move_type == MoveType.PAWN_DOUBLE:
#                 # En Passant Right
#                 pawn_moves = east_one(wp) & bp & rank_5 & ~file_a
#                 target_squares = bitutils.square_index_serialization(pawn_moves)
#                 for target in target_squares:
#                     start_square = target - 1
#                     end_square = target + 8
#                     if target == history[-1].to_square:
#                         move_list.append(Move(start_square, end_square, MoveType.EN_PASSANT))

#                 # En Passant Left
#                 pawn_moves = west_one(wp) & bp & rank_5 & ~file_h
#                 target_squares = bitutils.square_index_serialization(pawn_moves)
#                 for target in target_squares:
#                     start_square = target + 1
#                     end_square = target + 8
#                     if target == history[-1].to_square:
#                         move_list.append(Move(start_square, end_square, MoveType.EN_PASSANT))

#         return move_list

#     def possible_knight_moves(self, wn):

#         move_list = list()
#         knight_moves = np.uint64()

#         knight_squares = bitutils.square_index_serialization(wn)

#         for knight_square in knight_squares:
#             # Moves
#             knight_moves = knight_bitboards_table[knight_square] & self.empty
#             target_squares = bitutils.square_index_serialization(knight_moves)
#             for target in target_squares:
#                 start_square = knight_square
#                 move_list.append(Move(start_square, target, MoveType.NORMAL))
            
#             # Capture
#             knight_moves = knight_bitboards_table[knight_square] & self.black_pieces
#             target_squares = bitutils.square_index_serialization(knight_moves)
#             for target in target_squares:
#                 start_square = knight_square
#                 move_list.append(Move(start_square, target, MoveType.CAPTURE))

#         return move_list

#     def possible_rook_moves(self, wr):
#         move_list = self.possible_rf_moves(wr)
#         return move_list

#     def possible_bishop_moves(self, wb):
#         move_list = self.possible_diag_moves(wb)
#         return move_list

#     def possible_queen_moves(self, wq):
#         move_list = self.possible_rf_moves(wq)
#         move_list += self.possible_diag_moves(wq)
#         return move_list

#     def possible_king_moves(self, wk, wr):

#         move_list = list()
#         king_moves = np.uint64()

#         king_squares = bitutils.square_index_serialization(wk)

#         for king_square in king_squares:
#             # Moves
#             king_moves = king_bitboards_table[king_square] & self.empty
#             target_squares = bitutils.square_index_serialization(king_moves)
#             for target in target_squares:
#                 start_square = king_square
#                 move_list.append(Move(start_square, target, MoveType.NORMAL))
            
#             # Capture
#             king_moves = king_bitboards_table[king_square] & self.black_pieces
#             target_squares = bitutils.square_index_serialization(king_moves)
#             for target in target_squares:
#                 start_square = king_square
#                 move_list.append(Move(start_square, target, MoveType.CAPTURE))

#             # Castle left
#             if self.castle_left_flag:
#                 king_moves = west_one(west_one(west_one(west_one(wk)))) & wr & (self.empty >> np.uint64(1)) & (self.empty >> np.uint64(2)) & (self.empty >> np.uint64(3))
#                 target_squares = bitutils.square_index_serialization(king_moves)
#                 for target in target_squares:
#                     start_square = king_square
#                     move_list.append(Move(start_square, target, MoveType.EN_PASSANT))

#             # Castle right
#             if self.castle_right_flag:
#                 king_moves = east_one(east_one(east_one(wk))) & wr & (self.empty << np.uint64(1)) & (self.empty << np.uint64(2))
#                 target_squares = bitutils.square_index_serialization(king_moves)
#                 for target in target_squares:
#                     start_square = king_square
#                     move_list.append(Move(start_square, target, MoveType.EN_PASSANT))

#         return move_list
        
#     def possible_rf_moves(self, bb):

#         occ = ~self.empty    

#         move_list = list()
#         rf_moves = np.uint64()
#         rf_attacks = np.uint64()

#         start_squares = bitutils.square_index_serialization(bb)
#         for start_square in start_squares:
#             # Positive
#             keys = ['north', 'east']
#             for key in keys:
#                 rf_moves = rays_table[key][start_square]
#                 blocker = rf_moves & occ
#                 if blocker:
#                     square = bitutils.bitscan_forward(blocker)
#                     rf_moves ^= rays_table[key][square]

#                 rf_attacks = rf_moves & self.black_pieces
#                 rf_moves &= self.empty

#                 target_squares = bitutils.square_index_serialization(rf_attacks)
#                 for target in target_squares:
#                     move_list.append(Move(start_square, target, MoveType.CAPTURE))

#                 target_squares = bitutils.square_index_serialization(rf_moves)
#                 for target in target_squares:
#                     move_list.append(Move(start_square, target, MoveType.NORMAL))

#             # Negative
#             keys = ['south', 'west']
#             for key in keys:
#                 rf_moves = rays_table[key][start_square]
#                 blocker = rf_moves & occ
#                 if blocker:
#                     square = bitutils.bitscan_reverse(blocker)
#                     rf_moves ^= rays_table[key][square]

#                 rf_attacks = rf_moves & self.black_pieces
#                 rf_moves &= self.empty
                
#                 target_squares = bitutils.square_index_serialization(rf_attacks)
#                 for target in target_squares:
#                     move_list.append(Move(start_square, target, MoveType.CAPTURE))

#                 target_squares = bitutils.square_index_serialization(rf_moves)
#                 for target in target_squares:
#                     move_list.append(Move(start_square, target, MoveType.NORMAL))
                
#         return move_list

#     def possible_diag_moves(self, bb):
#         occ = ~self.empty    

#         move_list = list()
#         diag_moves = np.uint64()
#         diag_attacks = np.uint64()

#         start_squares = bitutils.square_index_serialization(bb)
#         for start_square in start_squares:
#             # Positive
#             keys = ['northeast', 'northwest']
#             for key in keys:
#                 diag_moves = rays_table[key][start_square]
#                 blocker = diag_moves & occ
#                 if blocker:
#                     square = bitutils.bitscan_forward(blocker)
#                     diag_moves ^= rays_table[key][square]

#                 diag_attacks = diag_moves & self.black_pieces
#                 diag_moves &= self.empty

#                 target_squares = bitutils.square_index_serialization(diag_attacks)
#                 for target in target_squares:
#                     move_list.append(Move(start_square, target, MoveType.CAPTURE))

#                 target_squares = bitutils.square_index_serialization(diag_moves)
#                 for target in target_squares:
#                     move_list.append(Move(start_square, target, MoveType.NORMAL))

#             # Negative
#             keys = ['southeast', 'southwest']
#             for key in keys:
#                 diag_moves = rays_table[key][start_square]
#                 blocker = diag_moves & occ
#                 if blocker:
#                     square = bitutils.bitscan_reverse(blocker)
#                     diag_moves ^= rays_table[key][square]

#                 diag_attacks = diag_moves & self.black_pieces
#                 diag_moves &= self.empty
                
#                 target_squares = bitutils.square_index_serialization(diag_attacks)
#                 for target in target_squares:
#                     move_list.append(Move(start_square, target, MoveType.CAPTURE))

#                 target_squares = bitutils.square_index_serialization(diag_moves)
#                 for target in target_squares:
#                     move_list.append(Move(start_square, target, MoveType.NORMAL))
                
#         return move_list