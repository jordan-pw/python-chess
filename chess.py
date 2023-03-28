import numpy as np
import move_gen
import move
import board
import ui
import time

from random import choice

# pipiris

class Chess:
    def __init__(self, chessboard):
        self.b = board.Board()
        self.b.list_to_bitboard(chessboard)

        self.turn = 1
        self.checkmate = False

        self.history = list()

        self.white_move_list = list()
        self.black_move_list = list()

        self.white_legal_moves = list()
        self.black_legal_moves = list()

        self.white_attacks = np.uint64()
        self.black_attacks = np.uint64()

        self.white_moves = move_gen.Moves(1)
        self.black_moves = move_gen.Moves(-1)

    def update_board(self):
        wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk = self.b.get_all_bitboards()
        wcl = self.b.can_castle_left(1)
        bcl = self.b.can_castle_left(-1)
        wcr = self.b.can_castle_right(1)
        bcr = self.b.can_castle_right(-1)

        self.white_moves.update_castle_flag(wcl, wcr)
        self.black_moves.update_castle_flag(bcl, bcr)

        self.white_move_list, self.white_attacks = self.white_moves.possible_moves(self.history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk)
        self.black_move_list, self.black_attacks = self.black_moves.possible_moves(self.history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk)
        
        self.b.update_white_attacks(self.white_attacks)
        self.b.update_black_attacks(self.black_attacks)

    def update_game_state(self):
        self.update_board()
        self.white_legal_moves = self.white_moves.legal_moves(self.b, self.white_move_list)
        self.black_legal_moves = self.black_moves.legal_moves(self.b, self.black_move_list)

    def make_move(self, m):
        self.b.make_move(m)
        self.history = self.b.get_history()
        self.turn *= -1

    def get_white_moves(self):
        return self.white_legal_moves
    
    def get_black_moves(self):
        return self.black_legal_moves
    
    def get_board(self):
        return self.b.get_board_list()
    
    def get_turn(self):
        return self.turn

if __name__ == "__main__":

    chessboard = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], #56-63
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], #48-55
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #40-47
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #32-39
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #24-31
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], #16-23
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], #8-15
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']] #0-7

    game = Chess(chessboard)

    while(1):
        game.update_game_state()
        b = game.get_board()

        ui.update_ui(b)

        turn = game.get_turn()

        if turn == 1:
            print("\n White Turn \n")
            legal_moves = game.get_white_moves()
            if not legal_moves:
                print("Checkmate! Black Win")
            the_move = choice(legal_moves)
            print("White's Move: \n")
            print(the_move)
        if turn == -1:
            print("\n Black Turn \n")
            legal_moves = game.get_black_moves()
            if not legal_moves:
                print("Checkmate! White Win")
            the_move = choice(legal_moves)
            print("Blacks's Move: \n")
            print(the_move)

        game.make_move(the_move)


    # wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk = b.get_all_bitboards()
    # white_move_list, white_attacks = white_moves.possible_moves(history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk)
    # black_move_list, black_attacks = black_moves.possible_moves(history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk)
    # b.update_white_attacks(white_attacks)
    # b.update_black_attacks(black_attacks)
    # ui.update_ui(b.get_board_string())
    # time.sleep(1)
    # if turn == 1:
    #     print("\n White Turn \n")
    #     cur_legal_moves = white_moves.legal_moves(b, white_move_list)
    #     if not cur_legal_moves:
    #         print("Checkmate! Black Win")
    #     the_move = choice(cur_legal_moves)
    #     print("White's Move: \n")
    #     print(the_move)
    # if turn == -1:
    #     print("\n Black Turn \n")
    #     cur_legal_moves = black_moves.legal_moves(b, black_move_list)
    #     if not cur_legal_moves:
    #         print("Checkmate! White Win")
    #     the_move = choice(cur_legal_moves)
    #     print("Blacks's Move: \n")
    #     print(the_move)
    # b.make_move(the_move)
    # print("\nUpdated Board:\n")
    # b.print_board()
    # turn *= -1


# history = []
# history.append(move.Move(1, move.PieceType.PAWN, 12, 28, move.MoveType.PAWN_DOUBLE))

# move_test = move.Move(1, move.PieceType.PAWN, 49, 56, move.MoveType.PROMOTION, move.Promotion.QUEEN)

# white_moves = move_gen.Moves(1)
# move_list, attacks = white_moves.possible_moves(history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk)

# black_moves = move_gen.Moves(-1)
# black_move_list, black_attacks = black_moves.possible_moves(history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk)

# black_legal_moves = black_moves.legal_moves(b, black_move_list)

# print(black_legal_moves)

# # b.make_move(move_test)
# b.print_board()
