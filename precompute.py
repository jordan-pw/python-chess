import numpy as np

knight_moves = [None] * 64
knight_bitboards = [None] * 64

def precompute_knight_moves():
    global knight_moves
    global knight_bitboards

    knight_jumps = [15, 17, -17, -15, 10, -6, 6, -10]

    for square in range(64):
        y = square // 8
        x = square - y * 8

        valid_knight_jumps = list()
        knight_bitboard = np.uint64(0)

        for jump in knight_jumps:
            knight_jump_square = square + jump

            if knight_jump_square >= 0 and knight_jump_square < 64:
                knight_jump_square_y = knight_jump_square // 8
                knight_jump_square_x = knight_jump_square - knight_jump_square_y * 8

                max_move_dist = max(abs(x - knight_jump_square_x), abs(y - knight_jump_square_y))
                if max_move_dist == 2:
                    valid_knight_jumps.append(knight_jump_square)
                    knight_bitboard |= np.uint64(1) << np.uint64(knight_jump_square)
        
        knight_moves[square] = valid_knight_jumps
        knight_bitboards[square] = knight_bitboard