import numpy as np
import moves
import board

chessboard = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', 'P', ' ', ' ', ' ', ' ', ' ', ' '],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]

b = board.Board()
b.list_to_bitboard(chessboard)
b.print_board()

wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk = b.get_all_bitboards()
history = []
history.append(moves.Move(52, 34, moves.MoveType.PAWN_DOUBLE))
moves.possible_moves_white(history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk)