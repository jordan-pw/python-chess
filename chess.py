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

        self.white_move_list, white_attacks = self.white_moves.possible_moves(self.history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk)
        self.black_move_list, black_attacks = self.black_moves.possible_moves(self.history, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk)

        self.b.update_white_attacks(white_attacks)
        self.b.update_black_attacks(black_attacks)

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
    screen = ui.UI()

    while(1):
        game.update_game_state()
        b = game.get_board()

        screen.update_ui(b, game.get_white_moves())

        white_move = screen.get_player_move()

        t = game.get_turn()

        if t == 1:
            # print("\n White Turn \n")
            legal_moves = game.get_white_moves()
            if not legal_moves:
                print("Checkmate! Black Win")
            if white_move:
                the_move = white_move
                game.make_move(the_move)
                screen.reset_player_move()
                game.b.print_board()
        if t == -1:
            #print("\n Black Turn \n")
            legal_moves = game.get_black_moves()
            if not legal_moves:
                print("Checkmate! White Win")
            the_move = choice(legal_moves)
            game.make_move(the_move)