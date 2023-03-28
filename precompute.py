import numpy as np

from bitutils import northeast_one, northwest_one, southeast_one, southwest_one

def precompute_knight_moves():

    knight_moves = [None] * 64
    knight_bitboards = [None] * 64

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

    return knight_moves, knight_bitboards

def precompute_king_moves():
    king_moves = [None] * 64
    king_bitboards = [None] * 64

    king_potential_moves = [8, -8, 7, -7, 9, -9, 1, -1]

    for square in range(64):
        y = square // 8
        x = square - y * 8

        valid_king_moves = list()
        king_bitboard = np.uint64(0)

        for move in king_potential_moves:
            king_target_square = square + move


            if king_target_square >= 0 and king_target_square < 64:
                king_target_square_y = king_target_square // 8
                king_target_square_x = king_target_square - king_target_square_y * 8

                max_move_dist = max(abs(x - king_target_square_x), abs(y - king_target_square_y))
                if max_move_dist == 1:
                    valid_king_moves.append(king_target_square)
                    king_bitboard |= np.uint64(1) << np.uint64(king_target_square)
        
        king_moves[square] = valid_king_moves
        king_bitboards[square] = king_bitboard

    return king_moves, king_bitboards

def precompute_rays():

    rays = list()

    north_rays = list()
    east_rays = list()
    west_rays = list()
    south_rays = list()
    northeast_rays = list()
    northwest_rays = list()
    southeast_rays = list()
    southwest_rays = list()

    for square in range(64):

        y = square // 8
        x = square - y * 8

        # Rank and File
        # North
        north_rays.append(np.uint64(72340172838076672) << np.uint64(square))

        # South
        south_rays.append(np.uint64(36170086419038336) >> np.uint64((63 - square)))

        # East
        east_rays.append(np.uint64(2 * ((np.uint64(1) << np.uint64((square | 7))) - (np.uint64(1) << np.uint64(square)))))

        # West
        west_rays.append(((np.uint64(1) << np.uint64(square)) - (np.uint64(1) << np.uint64((square & 56)))))

        # Diagonals
        # Northeast
        ray_calc = np.uint64(1) << np.uint64(square)
        ray_x = x
        ray_y = y

        for delta in range(8):
            if ray_x >= 7 or ray_y >= 7:
                break
            ray_calc |= northeast_one(ray_calc)
            ray_x += 1
            ray_y += 1
        ray_calc ^= np.uint64(1) << np.uint64(square)
        northeast_rays.append(ray_calc)

        # Diagonals
        # Northwest
        ray_calc = np.uint64(1) << np.uint64(square)
        ray_x = x
        ray_y = y

        for delta in range(8):
            if ray_x < 0 or ray_y >= 7:
                break
            ray_calc |= northwest_one(ray_calc)
            ray_x -= 1
            ray_y += 1
        ray_calc ^= np.uint64(1) << np.uint64(square)
        northwest_rays.append(ray_calc)

        # Diagonals
        # Southwest
        ray_calc = np.uint64(1) << np.uint64(square)
        ray_x = x
        ray_y = y

        for delta in range(8):
            if ray_x < 0 or ray_y < 0:
                break
            ray_calc |= southwest_one(ray_calc)
            ray_x -= 1
            ray_y -= 1
        ray_calc ^= np.uint64(1) << np.uint64(square)
        southwest_rays.append(ray_calc)

        # Diagonals
        # Southeast
        ray_calc = np.uint64(1) << np.uint64(square)
        ray_x = x
        ray_y = y

        for delta in range(8):
            if ray_x >= 7 or ray_y < 0:
                break
            ray_calc |= southeast_one(ray_calc)
            ray_x += 1
            ray_y -= 1
        ray_calc ^= np.uint64(1) << np.uint64(square)
        southeast_rays.append(ray_calc)

    rays = {
        'north': north_rays,
        'east': east_rays,
        'west': west_rays,
        'south': south_rays,
        'northeast': northeast_rays,
        'northwest': northwest_rays,
        'southeast': southeast_rays,
        'southwest': southwest_rays
    }
    
    return rays
