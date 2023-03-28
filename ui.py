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



selected = False # True when a piece is selected
selection = None # Currently selected piece

def update_ui(board):
    for event in pygame.event.get():
        # pylint: disable=no-member
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        # pylint: enable=no-member
        
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     # print(selected)
        #     print(the_board.bottom_king.attacked_by)
        #     if selected == False:
        #         selection = check_square()
        #         if selection is not None:
        #             selected = True
        #     if selected == True:
        #         if attempt_move(selection):
        #             selected = False
        #             selection = None
        #         else:
        #             selection = check_square()
        #             if selection is not None:
        #                 selected = True
    # Render pieces and other bits

    screen.blit(surface, (0,0))
    # select_piece(selection)
    draw_pieces(board)
    show_position()
    pygame.display.update()

def draw_pieces(board):
    for i in range(64):
        y = i // 8
        x = i - y * 8
        posy = 7 - y
        posx = x
        match board[y][x]:
            case 'P':
                psprite = pygame.image.load(bp).convert()
                screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
            case 'R':
                psprite = pygame.image.load(br).convert()
                screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
            case 'N':
                psprite = pygame.image.load(bn).convert()
                screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
            case 'B':
                psprite = pygame.image.load(bb).convert()
                screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
            case 'Q':
                psprite = pygame.image.load(bq).convert()
                screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
            case 'K':
                psprite = pygame.image.load(bk).convert()
                screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
            case 'p':
                psprite = pygame.image.load(wp).convert()
                screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
            case 'r':
                psprite = pygame.image.load(wr).convert()
                screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
            case 'n':
                psprite = pygame.image.load(wn).convert()
                screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
            case 'b':
                psprite = pygame.image.load(wb).convert()
                screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
            case 'q':
                psprite = pygame.image.load(wq).convert()
                screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))
            case 'k':
                psprite = pygame.image.load(wk).convert()
                screen.blit(psprite, (board_offset+(posx*100), board_offset+(posy*100)))

def show_position():
    x, y = pygame.mouse.get_pos()
    x = ((x // 100) * 100) + board_offset - 1
    y = ((y // 100) * 100) + board_offset - 1
    screen.blit(select, (x, y))

def highlight_moves(move_list):
    for m in move_list:
        x = m.to_square//8
        y = m.to_square%8
        screen.blit(highlight, (x*100 + board_offset, y*100 + board_offset)) 