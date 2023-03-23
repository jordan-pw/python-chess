import numpy as np
import move_gen
import move
import board

# pipiris


chessboard = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], #56-63
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], #48-55
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #40-47
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #32-39
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #24-31
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #16-23
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], #8-15
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']] #0-7


b = board.Board()
b.list_to_bitboard(chessboard)
b.print_board()

wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk = b.get_all_bitboards()
history = []
history.append(move.Move(1, move.PieceType.PAWN, 12, 28, move.MoveType.PAWN_DOUBLE))

white_moves = move_gen.Moves(b, 1)
# white_moves.possible_moves(history, b)

black_moves = move_gen.Moves(b, -1)
black_moves.possible_moves(history, b)