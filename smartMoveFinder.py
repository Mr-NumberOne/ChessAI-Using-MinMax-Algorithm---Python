import random  # to suffuse

# ! assigning values to pieces (Normal values )
pieceScore = {"K": 0, "Q": 8, "R": 5, "B": 3, "N": 3, "p": 1}
# * NOTE: King is 0 because the whole game is build on avoiding checkmates
CHECKMATE = 1000
STALEMATE = 0  # * draw
DEPTH = 2  # * Depth of the negamax

# ! Positional Values
# * NOTE: Each piece has positions where it is the strongest at
knightScores = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]
bishopScore = [
    [4, 3, 2, 1, 1, 2, 3, 4],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [4, 3, 2, 1, 1, 2, 3, 4],

]
queenScore = [
    [1, 1, 1, 3, 1, 1, 1, 1],
    [1, 2, 3, 3, 3, 1, 1, 1],
    [1, 4, 3, 3, 3, 4, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 4, 3, 3, 3, 4, 2, 1],
    [1, 2, 3, 3, 3, 1, 1, 1],
    [1, 1, 1, 3, 1, 1, 1, 1],

]
rockScore = [
    [4, 3, 4, 4, 4, 4, 3, 4],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [4, 3, 4, 4, 4, 4, 3, 4],

]
whitePawnScore = [
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [2, 3, 3, 4, 4, 3, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],

]
blackPawnScore = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 3, 4, 4, 3, 3, 2],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [8, 8, 8, 8, 8, 8, 8, 8],

]

# ! using a dictionary to avoid switches
piecePosScores = {"N": knightScores, "Q": queenScore, "R": rockScore, "B": bishopScore, "bp": blackPawnScore,
                  "wp": whitePawnScore}


def findRandomMove(validMoves):
    """Returns a random move"""
    random.shuffle(validMoves)
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestNega(gs, validMoves, level):
    """ helper method to find first recursive call"""
    random.shuffle(validMoves)  # ! to shuffle the search tree
    global nextMove
    nextMove = None  # so it picks a random move from main if => it cannot decide
    findNegaMaxMoveAlphaBeta(level, gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteMove else -1)
    return nextMove

 
def findNegaMaxMoveAlphaBeta(level, gs, validMoves, depth, alpha, beta, turnMultiplier):  # alpha-max, beta-min
    """eliminate bad paths from beginning"""
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs, level)
    # move ordering - evaluate moves with the highest scores first

    maxscore = -CHECKMATE
    for move in validMoves:

        gs.makeMove(move)  # makes move
        nextMoves = gs.getValidMoves()
        score = -findNegaMaxMoveAlphaBeta(level, gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)

        if score > maxscore:
            maxscore = score
            if depth == DEPTH:
                nextMove = move
        gs.undo()
        if maxscore > alpha:  # ! puring happens
            alpha = maxscore
        if alpha >= beta:
            break

    return maxscore


def scoreBoard(gs, level):
    """Static Evaluation"""
    if gs.checkMate:
        # ! NOTE: positive good for white and negative good for black
        if gs.whiteMove:
            return -CHECKMATE  # black wins  -
        else:
            return CHECKMATE  # white wins  +
    elif gs.staleMate:
        return STALEMATE  # 0

    score = 0
    if level == 2:
        # ! A level 2 "Normal" the static evaluation depends on maintaining the number of pieces
        for row in gs.board:
            for square in row:
                if square[0] == 'w':
                    score += pieceScore[square[1]]
                elif square[0] == 'b':
                    score -= pieceScore[square[1]]
    elif level == 1:
        # ! A level 1 "Easy" the static evaluation depends on maintaining the number of pieces
        for row in gs.board:
            for square in row:
                if square[0] == 'w':
                    score += 1
                elif square[0] == 'b':
                    score -= 1
    elif level == 3:
        # ! A level 3 "hard" the static evaluation depends on the position and piece value
        for row in range(len(gs.board)):
            for col in range(len(gs.board[row])):
                square = gs.board[row][col]
                if square != "--":
                    # * score positionally
                    posScore = 0
                    if square[1] != 'K':  # ! not a king
                        if square[1] == 'p':  # ! for pawns
                            posScore = piecePosScores[square][row][col]
                        else:  # ! for other pieces
                            posScore = piecePosScores[square[1]][row][col]
                # * Total Score
                if square[0] == 'w':
                    score += pieceScore[square[1]] + posScore * 0.1
                    # print(score)
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + posScore * 0.1
                # ! NOTE:
                # * 0.1 to normalize to positional score so that it does not cause the AI to prefer putting
                # * its pieces in the middle over winning  the game or other pieces
    return score
