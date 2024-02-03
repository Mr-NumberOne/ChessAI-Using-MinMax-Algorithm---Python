# ! Libraries needed for The Game
import pygame
from chessEngine import gameState, Move
import smartMoveFinder

# ! Shared
from SharedDomain import Shared
# ! time
from time import time as currenttime_stamp


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION  # Square size
MAX_FPS = 15  # for animation (Frames Per Second)
IMAGES = {}  # The dictionary that will hold the images after loading


# load images
# initialize a global dictionary and use it only once in main
# ! we only load the images onece because it is an expensive operation

def loadImages():
    """Load the piece images into the global Dictionary Images"""
    pieces = ['bR', 'bN', "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(Shared.Theme["path"] + piece + ".png"),
                                               (SQ_SIZE, SQ_SIZE))
        # * python transform scale takes the image and the dimension


def drawGameState(screen, gs, validMoves, sqSelected):
    """Draws the new board, pieces and, highlighting """
    drawBoard(screen)
    highlight(screen, gs, validMoves, sqSelected)
    # ! NOTE: the highlight is drawn then the piece is on it
    drawPieces(screen, gs.board)


def drawBoard(screen):
    """
    Drawing The board and the squares on it
    =======================================
    Takes the surface to draw on as an argument
    """
    global colors
    colors = [pygame.Color(Shared.Theme["colorA"]), pygame.Color(Shared.Theme["colorB"])]  # Setting square colors

    # ! Drawing the Colors
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(col + row) % 2]  # row + col if even use ColorA else ColorB
            # !  Draw that actual squares
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            # * takes Surface = screen || to draw On
            # * takes color || color of the drawn rectangle
            # * takes Rect || The rectangle object (x, y, width, height)


def drawPieces(screen, board):
    """
    Draw the pieces on the board
    ============================
    Takes the surface to draw on &
    Takes the board: which the game state dictionary that tells us where the pieces are
    """
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = (board[row][col])
            if piece != "--":  # if there is a piece then draw it
                screen.blit(IMAGES[piece], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, 2 * SQ_SIZE))
                # * takes image & rect to draw the image (x ,y , width, height)


def highlight(screen, gs, validMoves, sqlSelected):
    """High light the valid moves and current selected piece"""
    if (gs.inCheck()):
        s = pygame.Surface((SQ_SIZE, SQ_SIZE))  # (x,y) as one parameter
        s.fill(pygame.Color('red'))
        if (gs.whiteMove):
            r, c = gs.whiteKingLoc
        else:
            r, c = gs.blackKingLoc
        screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))  # draw
    if sqlSelected != ():  # ! square selected is not empty (There is a square selected)
        r, c = sqlSelected
        if gs.board[r][c][0] == ('w' if gs.whiteMove else 'b'):  # ! check what piece is selected
            # highlight
            # * create a surface:
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))  # (x,y) as one parameter
            s.set_alpha(100)  # * transparency 0-255
            s.fill(pygame.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))  # draw it where the selected piece is located
            # ! highlight moves from that square (Valid moves for selected square)
            s.fill(pygame.Color('yellow'))
            for move in validMoves:
                # * search valid moves for the selected piece's valid moves
                if move.startCol == c and move.startRow == r:
                    # * check
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


def animateMove(move, screen, board, clock):
    """ANIMATES Piece movement"""
    global colors
    dR = move.endRow - move.startRow  # distance between rows
    dC = move.endCol - move.startCol  # distance between columns
    framesPerSquare = 10  # frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square:
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pygame.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, color, endSquare)
        # ! Draws the captured piece & hides it with the move is done
        if move.pieceCaptured != "--":
            if move.isEnpassantMove:  # this becomes false when we reach the end square
                if move.pieceCaptured[0] == 'b':
                    enpassantRow = move.endRow + 1
                else:
                    enpassantRow = move.endRow - 1
                endSquare = pygame.Rect(move.endCol * SQ_SIZE, enpassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # ! Draw moved piece again in its right place
        screen.blit(IMAGES[move.pieceMoved], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.display.flip()
        clock.tick(60)

def drawText(screen, text):
    """This Draws the text when check mate or stalemate"""
    font = pygame.font.SysFont("Impact", 32, False, False)
    textObj = font.render(text, False, pygame.Color("tomato"))
    textLoc = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObj.get_width() / 2,
                                                    HEIGHT / 2 - textObj.get_height() / 2)
    # * Draws the Text at ( 0 ,0 ) the with .move(To center screen)
    screen.blit(textObj, textLoc)  # actually draws TextObj at TextLoc

def main():
    """Main Chess Function"""
    # ! Initialize pygame
    pygame.init()

    # ! title and icon
    pygame.display.set_caption("ChessGeeks AI vs " + Shared.playerName)
    Icon = pygame.image.load('images/logo.png')
    pygame.display.set_icon(Icon)  # We use set_icon to set new icon

    # ! Window Size
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()  # * used in the animation
    # ! NOTE: NOT NEED cause the squares and pieces cover it
    # screen.fill(pygame.Color("black"))

    # ! create a object of game state
    gs = gameState()
    validMoves = gs.getValidMoves
    moveMade = False  # to check if a move is made

    # ! when we should animate
    animate = False
    gameOver = False

    # ! Players variables
    # human == true , computer == False
    playerOne = True if Shared.playas == 1 else False
    playerTwo = True if Shared.playas == 2 else False

    # ! level
    level = Shared.level

    sqSelected = ()  # holds selected square as (x , y)
    playerClicks = []  # keep two clicks : before (piece selection) and after move (where piece moves to)

    # ! Get all the valid moves for the first turn
    validMoves = gs.getValidMoves()

    # ! Calling load images
    loadImages()  # to load all images in the right size to the dict IMAGES

    # ! Game Loop - Keeps Listening for events and drawing the board
    running = True
    while running:

        humanTurn = ((gs.whiteMove and playerOne) or (not gs.whiteMove and playerTwo))
        # * Checks if white's turn and Human is white
        # * Or Checks if not white's turn (blacks Turn) and Human is black

        for event in pygame.event.get():  # get events
            if event.type == pygame.QUIT:  # Exit game
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # if player clicks the mouse
                if not gameOver and humanTurn:
                    location = pygame.mouse.get_pos()  # (x,y) location of mouse => tuple

                    # ! Convert location to columns and rows
                    mouseCol = location[0] // SQ_SIZE
                    mouseRow = location[1] // SQ_SIZE

                    if sqSelected == (mouseRow, mouseCol):  # if moved to same position (empty)
                        sqSelected = ()  # selected square
                        playerClicks = []  # Players Clicked Squares
                    else:
                        sqSelected = (mouseRow, mouseCol)
                        playerClicks.append(sqSelected)  # add selected square to players clicks
                        # ! NOTE:
                        # * the first click to select a piece
                        # * the second one the position where it should be moved

                    if len(playerClicks) == 2:  # after the second click
                        move = Move(playerClicks[0], playerClicks[1], gs.board)
                        # *  Takes Start Square => Targeted square => and the board dict
                        # todo print(Move.getChessNotaion(move))  # ! print player moves

                        for i in range(len(validMoves)):
                            if move == validMoves[i]:  # ! if the move is valid then make it
                                gs.makeMove(validMoves[i])  # make the move generated by engine
                                # print(gs.checkMate)
                                moveMade = True  # ! if move made, make it true
                                animate = True
                                sqSelected = ()  # empty square holder
                                playerClicks = []  # empty the start and end squares

                        if not moveMade:
                            playerClicks = [sqSelected]
                            # * saves the second move so that
                            # * if you change to another piece you just have to provide the second move

            # ! keyboard events:
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:  # undo => press Z
                    gs.undo()  # ! call undo function
                    moveMade = True
                    animate = False
                    gameOver = False
                if event.key == pygame.K_r:  # reset => press R
                    gs = gameState()  # ! creates a new game instance replacing the old one
                    Shared.starttime = currenttime_stamp()  # reset timer
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        # ! AI move finder logic:
        if not gameOver and not humanTurn:  # AI's turn
            AIMove = smartMoveFinder.findBestNega(gs, validMoves, level)  # ! Call negamax to see best moves
            if AIMove is None:  # todo ??
                # * should not happen unless there are no moves (when AI can't decide)
                AIMove = smartMoveFinder.findRandomMove(validMoves)
                # print(AIMove, "=====================================================#")
            gs.makeMove(AIMove)  # make the Ai's Move
            moveMade = True
            animate = True

        # ! Checks if a move is made => to generate the next turns valid moves
        if moveMade:
            if animate:  # If animation is on animate the move
                animateMove(gs.moveLog[-1], screen, gs.board, clock)

            validMoves = gs.getValidMoves()  # generating all the next valid moves
            # reset animation and move made
            moveMade = False
            animate = False

        # ! draw the new game state (board, highlight, pieces)
        drawGameState(screen, gs, validMoves, sqSelected)
        if gs.checkMate:  # ! check if it is checkmate
            gameOver = True
            whiteMoves = blackMoves = None   # ! hold the number of moves made by a player

            # * moveLog : Contains all the moves made during the entire game (for both sides)
            if len(gs.moveLog) % 2 == 0:  # even
                whiteMoves = int(len(gs.moveLog) / 2)
                blackMoves = int(len(gs.moveLog) / 2)
            else:  # odd
                whiteMoves = int((len(gs.moveLog) // 2) + 1)
                blackMoves = int((len(gs.moveLog) // 2))
            # setting the number of moves
            Shared.movesmade = whiteMoves if Shared.playas == 1 else blackMoves

            # ! Draws on the screen the Winner
            if gs.whiteMove:  # if black played last, and now it is whites turn => black wins
                drawText(screen, 'Black wins by checkmate')
                Shared.playerWon = True if Shared.playas == 2 else False
                # * Tells us that human is black and stores that black won
            else:
                drawText(screen, 'White wins by checkmate')
                Shared.playerWon = True if Shared.playas == 1 else False
                # * Tells us that human is White and stores that White won
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')  # it is when the opponent has no valid moves to play (it is a Draw)

        clock.tick(MAX_FPS)  # * controls the frames per second
        pygame.display.flip()  # * updates the display surface (window)
    pygame.quit()


if __name__ == "__main__":
    main()
