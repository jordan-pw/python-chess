import pygame
import sys

# Initialize pygame display
width, height = 826, 826
board_offset = 13 # Size of padding on board sprite
screen = pygame.display.set_mode((width, height))

# Load in images
surface = pygame.image.load('resources\\board.png').convert()
select = pygame.image.load('resources\\selection.png').convert_alpha()
highlight = pygame.image.load('resources\\highlight.png').convert_alpha()
highlightred = pygame.image.load('resources\\highlight_red.png').convert_alpha()
highlightgreen = pygame.image.load('resources\\highlight_green.png').convert_alpha()

wp = 'resources\\wpawn.png'
wn = 'resources\\wknight.png'
wr = 'resources\\wrook.png'
wb = 'resources\\wbishop.png'
wq = 'resources\\wqueen.png'
wk = 'resources\\wking.png'
bp = 'resources\\bpawn.png'
bn = 'resources\\bknight.png'
br = 'resources\\brook.png'
bb = 'resources\\bbishop.png'
bq = 'resources\\bqueen.png'
bk = 'resources\\bking.png'


class UI:
    def __init__(self):
        self.selected = False
        self.selection = None
        self.selected_moves = set()
        self.player_move = None

    def update_ui(self, board, player_move_list):
        for event in pygame.event.get():
            # pylint: disable=no-member
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            # pylint: enable=no-member
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # print(selected)
                if self.selected == False:
                    self.check_square(player_move_list)
                    self.player_move = None
                    if self.selection is not None:
                        self.selected = True
                elif self.selected == True:
                    self.check_move()

                    if not self.player_move:
                        self.selected = False
                        self.check_square(player_move_list)
                        if self.selection is not None:
                            self.selected = True
                    
                    if self.player_move:
                        self.selected = False
                        self.selected_moves = set()

                print(f"selection: {self.selection}")
                print(f"selected: {self.selected}")
                print(f"selected moves: {self.selected_moves}")
                print(f"player move: {self.player_move}")
        
        # Render pieces and other bits
        screen.blit(surface, (0,0))
        self.select_pos()
        self.draw_pieces(board)
        self.show_position()
        pygame.display.update()

    def draw_pieces(self, board):
        for i in range(64):
            y = i // 8
            x = i - y * 8

            posy = y
            posx = x
            match board[y][x]:
                case 'P':
                    psprite = pygame.image.load(wp).convert()
                    screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
                case 'R':
                    psprite = pygame.image.load(wr).convert()
                    screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
                case 'N':
                    psprite = pygame.image.load(wn).convert()
                    screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
                case 'B':
                    psprite = pygame.image.load(wb).convert()
                    screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
                case 'Q':
                    psprite = pygame.image.load(wq).convert()
                    screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
                case 'K':
                    psprite = pygame.image.load(wk).convert()
                    screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
                case 'p':
                    psprite = pygame.image.load(bp).convert()
                    screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
                case 'r':
                    psprite = pygame.image.load(br).convert()
                    screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
                case 'n':
                    psprite = pygame.image.load(bn).convert()
                    screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
                case 'b':
                    psprite = pygame.image.load(bb).convert()
                    screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
                case 'q':
                    psprite = pygame.image.load(bq).convert()
                    screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
                case 'k':
                    psprite = pygame.image.load(bk).convert()
                    screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))

    def show_position(self):
        x, y = pygame.mouse.get_pos()
        x = ((x // 100) * 100) + board_offset - 1
        y = ((y // 100) * 100) + board_offset - 1
        screen.blit(select, (x, y))

    def check_square(self, move_list):
        self.selected_moves = set()
        x, y = pygame.mouse.get_pos()

        x = x // 100
        y = 7 - (y // 100)

        found_flag = False

        for m in move_list:

            square_y = m.from_square // 8
            square_x = m.from_square - square_y * 8
            
            if y == square_y and x == square_x:
                self.selection = m
                self.selected_moves.add(m)
                found_flag = True
        
        if found_flag == False:
            self.selection = None

    def check_move(self):
        x, y = pygame.mouse.get_pos()

        x = x // 100
        y = 7 - (y // 100)

        for sm in self.selected_moves:
            square_y = sm.to_square // 8
            square_x = sm.to_square - square_y * 8
            
            if y == square_y and x == square_x:
                self.player_move = sm
                break
            self.player_move = None
        
        self.selection = None

    def highlight_moves(self):
        for m in self.selected_moves:
            y = 7 - m.to_square//8
            x = m.to_square%8
            screen.blit(highlight, (x*100 + board_offset, y*100 + board_offset))

    def select_pos(self):
        if self.selection is None:
            return

        posy = 7 - (self.selection.from_square // 8)
        posx = self.selection.from_square % 8

        screen.blit(highlight, (posx*100 + board_offset, posy*100 + board_offset))

        self.highlight_moves()
        # if debug == True:
        #     for attack in piece.attacked_by:
        #         screen.blit(highlightgreen, (attack[0]*100 + board_offset, attack[1]*100 + board_offset))
        #     for target in piece.attacking:
        #         screen.blit(highlightred, (target[0]*100 + board_offset, target[1]*100 + board_offset))

    def get_player_move(self):
        return self.player_move
    
    def reset_player_move(self):
        self.player_move = None