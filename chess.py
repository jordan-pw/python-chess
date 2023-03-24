import numpy as np
import move_gen
import move
import board

from random import choice

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


print("START")
b = board.Board()
b.list_to_bitboard(chessboard)
b.print_board()

turn = 1
checkmate = False

history = list()

white_move_list = list()
black_move_list = list()
white_attacks = np.uint64()
black_attacks = np.uint64()

white_moves = move_gen.Moves(1)
black_moves = move_gen.Moves(-1)

while(1):
    wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk = b.get_all_bitboards()
    white_move_list, white_attacks = white_moves.possible_moves(history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk)
    black_move_list, black_attacks = black_moves.possible_moves(history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk)
    b.update_white_attacks(white_attacks)
    b.update_black_attacks(black_attacks)
    if turn == 1:
        print("\n White Turn \n")
        cur_legal_moves = white_moves.legal_moves(b, white_move_list)
        if not cur_legal_moves:
            print("Checkmate! Black Win")
        the_move = choice(cur_legal_moves)
        print("White's Move: \n")
        print(the_move)
    if turn == -1:
        print("\n Black Turn \n")
        cur_legal_moves = black_moves.legal_moves(b, black_move_list)
        if not cur_legal_moves:
            print("Checkmate! White Win")
        the_move = choice(cur_legal_moves)
        print("Blacks's Move: \n")
        print(the_move)
    b.make_move(the_move)
    print("\nUpdated Board:\n")
    b.print_board()
    turn *= -1




history = []
history.append(move.Move(1, move.PieceType.PAWN, 12, 28, move.MoveType.PAWN_DOUBLE))

move_test = move.Move(1, move.PieceType.PAWN, 49, 56, move.MoveType.PROMOTION, move.Promotion.QUEEN)

white_moves = move_gen.Moves(1)
move_list, attacks = white_moves.possible_moves(history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk)

black_moves = move_gen.Moves(-1)
black_move_list, black_attacks = black_moves.possible_moves(history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk)

black_legal_moves = black_moves.legal_moves(b, black_move_list)

print(black_legal_moves)

# # b.make_move(move_test)
# b.print_board()