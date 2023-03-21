import numpy as np
import moves
import board

chessboard = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], #56-64
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
history.append(moves.Move(52, 34, moves.MoveType.PAWN_DOUBLE))

white_moves = moves.WhiteMoves(wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk)
white_moves.possible_moves(history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk)