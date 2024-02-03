class gameState:
    """
    This class is responsible for starting all the information about the current state if a chess game.
    It will also be responsible for determining the valid movers in the current state,
    and it will also contain the move Log
    """

    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],

        ]

        # ! to call the appropriate function depending on the piece name - used in the get all moves function
        self.moveFun = {'p': self.getPawnMoves, 'R': self.getRockMoves, 'N': self.getKnighMoves,
                        'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteMove = True  # white turn
        self.moveLog = []  # to save all move - used for undo() & Player Move Count

        # ! Keep Kings Locations for Castling
        self.whiteKingLoc = (7, 4)  # white King
        self.blackKingLoc = (0, 4)  # Black King

        # ! End Game
        self.checkMate = False  # true if there is no valid moves and the king is attacked by an opponent piece
        self.staleMate = False  # true if there is no valid moves

        # ! special move variables
        # * enpassant
        self.enpassantPossible = ()  # coordinates where en passant is possible
        self.enpassantPossibleLog = [self.enpassantPossible]  # there are no possibles at the beginning

        # * Castling
        # set all rights(wks,bks,wqs,bqs) to be true at first
        self.currentCastlingRights = castlingRights(True, True, True,True)

        # save current rights in a log, so we can get the previous rights after undo
        self.castlingRightsLog = [castlingRights(self.currentCastlingRights.wks,  # * white king side castling
                                                 self.currentCastlingRights.bks,  # * black king side castling
                                                 self.currentCastlingRights.wqs,  # * white queen side castling
                                                 self.currentCastlingRights.bqs)]  # * black queen side castling

    def makeMove(self, move):
        """"This method used to make tha actual change in board """
        self.board[move.startRow][move.startCol] = "--"  # make the start square empty
        self.board[move.endRow][move.endCol] = move.pieceMoved
        # * put the piece moved(taken from start square) in end square

        self.moveLog.append(move)  # add the move to the log
        self.whiteMove = not self.whiteMove  # switch turns

        # ! check if piece moved update kings location
        if move.pieceMoved == "wK":
            self.whiteKingLoc = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLoc = (move.endRow, move.endCol)

        # ! pawn promotion
        # * when a pawn reaches the other end ( opponenet's end ) becomes a queen
        if move.isPawnPromotion:  # checked in the move class below
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # ! enpassant = we need to add to the move incase it was enpassant
        # * we need to erase the opponent's pawn since it is not erase normally
        # because our pawn does not land on that square
        # todo??
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"
            # * To remove the pawn that was castled

        # ! update enpassant possible:
        # * when we move any pawn 2 steps --> the opponent can make an enpassant move against "us"
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:  # on 2 squares move
            # ! specify where enpassant is possible
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)  # or start col
        else:
            # ! it has to be directly after the move is made
            self.enpassantPossible = ()

        # ! NOTES
        # * castle move : we have more than one piece moved when it is a castle move
        # above: we move the king itself - (Cause it initiates the move)
        # here: we move the rock
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # ! king castle move
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = "--"  # erase old rock

            else:  # ! queen castle move
                # * king is move above but we need to move the rock
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = "--"  # erase old rock

        # * save enpassant square to pop it if we make undo
        self.enpassantPossibleLog.append(self.enpassantPossible)

        # update castling rights whenever it is a rock or a king moves
        self.updateCastlingRights(move)
        # ! NOTE:
        # * this method checks if the move violates any castling rights and if so, it sets the violated right to false

        self.castlingRightsLog.append(castlingRights(self.currentCastlingRights.wks,
                                                     self.currentCastlingRights.bks,
                                                     self.currentCastlingRights.wqs,
                                                     self.currentCastlingRights.bqs))

    def undo(self):  # the opposite of make move
        """
        - reverse moves using the moveLog
        - set enpassant possible back to the last enpassant possible using the enpassantPossibleLog
        - set castling rights back using castlingRightsLog
        """
        if len(self.moveLog) > 0:  # ! check if there are any moves to pop
            move = self.moveLog.pop()  # gets the last move (by popping it)

            # ! Resetting the previous pieces back in the
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteMove = not self.whiteMove # ! change the Turns

            # ! resets the kings previous locations
            if move.pieceMoved == "wK":
                self.whiteKingLoc = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLoc = (move.startRow, move.startCol)

            # ! enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"  # leave landing square empty
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            self.enpassantPossibleLog.pop()  # remove the last one (which is the current one)
            self.enpassantPossible = self.enpassantPossibleLog[-1]  # save the last one

            # ! undo castling rights
            self.castlingRightsLog.pop()  # delete the last state we saved
            newRights = self.castlingRightsLog[-1]  # make the current = last
            self.currentCastlingRights = castlingRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            # undo castle move (because 2 pieces where moved)
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # king side
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "--"  # erase old rock
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"  # erase old rock
        # undo game over
        self.checkMate = False
        self.staleMate = False

    def updateCastlingRights(self, move):
        """
        # this method checks if the move made violates the castling rights. If so, it changes the flags
        # when a king moves, no right to make any side of castling
        # when a rock moves or being captured , we cannot castle in its side only( right or left)
        """

        if move.pieceMoved == "wK":

            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == "bK":

            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False

        elif move.pieceMoved == "wR":

            if move.startRow == 7:
                if move.startCol == 7:  # right rock
                    self.currentCastlingRights.wks = False

                if move.startCol == 0:  # left rock
                    self.currentCastlingRights.wqs = False

        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 7:  # right rock
                    self.currentCastlingRights.bks = False

                if move.startCol == 0:  # left rock
                    self.currentCastlingRights.bqs = False

        # when a rock is captured:
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.wks = False

        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.bks = False

    def getValidMoves(self):
        """
        # Gets all the possible moves
        # Eliminates all the moves that cause checkmate
        """
        tempEnpassant = self.enpassantPossible
        tempCastleRights = castlingRights(self.currentCastlingRights.wks,
                                          self.currentCastlingRights.bks,
                                          self.currentCastlingRights.wqs,
                                          self.currentCastlingRights.bqs)

        # ! 1- generate all possible moves
        moves = self.getAllMoves()  # gets all moves except castling moves
        # castle moves
        if self.whiteMove:
            self.getCastleMoves(self.whiteKingLoc[0], self.whiteKingLoc[1], moves)
        else:
            self.getCastleMoves(self.blackKingLoc[0], self.blackKingLoc[1], moves)

        # ! 2- for each move, make the move
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            # ! 3- generate all opponent's moves and see if they attack king on each one
            # * NOTE: if so, we remove it. No one can sacrifice the king piece
            self.whiteMove = not self.whiteMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteMove = not self.whiteMove
            self.undo()

        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = tempEnpassant
        self.currentCastlingRights = tempCastleRights

        return moves

    def inCheck(self):
        """checks if the king is in danger"""
        if self.whiteMove:
            return self.squareUnderAttack(self.whiteKingLoc[0], self.whiteKingLoc[1])
        else:
            return self.squareUnderAttack(self.blackKingLoc[0], self.blackKingLoc[1])

    def squareUnderAttack(self, r, c):
        """checks if a specific square can be attacked by opponent"""
        self.whiteMove = not self.whiteMove
        opMoves = self.getAllMoves()
        self.whiteMove = not self.whiteMove
        for move in opMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteMove) or (turn == 'b' and not self.whiteMove):
                    piece = self.board[r][c][1]
                    self.moveFun[piece](r, c,
                                        moves)  # we call the function that matches the peice type using the dictionary
        return moves

    def getPawnMoves(self, r, c, moves):

        if self.whiteMove:
            if self.board[r - 1][c] == "--":  # no peiece in its way
                moves.append(Move((r, c), (r - 1, c), self.board))  # pawn can move one square

                if r == 6 and self.board[r - 2][c] == "--":  # pawn has the right to move to squares
                    moves.append(Move((r, c), (r - 2, c), self.board))
            # pawn captures - pawn can capture a peice when its position in r-1 and c-1 or r-1 and c+1
            if c - 1 >= 0:  # make sure we are still on the board
                if self.board[r - 1][c - 1][0] == 'b':  # opponent's peice in correct postition to be captured
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:

                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))

            if c + 1 <= 7:  # make sure we are still on the board
                if self.board[r - 1][c + 1][0] == 'b':  # opponent's peice in correct postition to be captured
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:

                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True))


        else:  # here we check black pawn moves- same rule but differnt postions(rows and cols)
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))

                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:

                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))

            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:

                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))

    def getRockMoves(self, r, c, moves):

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up,right,left,down
        enemy_color = "b" if self.whiteMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # in board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    elif endPiece[0] == enemy_color:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break  # cannot jump others pieces, so no need to check other squares in this direction
                    else:  # my piece
                        break  # cannot jump my pieces
                else:  # out of board
                    break

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = "b" if self.whiteMove else "w"
        for d in directions:
            for i in range(1, 8):

                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    elif endPiece[0] == enemy_color:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break  # cannot jump others peices
                    else:  # my piece
                        break  # cannot jump my pieces
                else:  # out of board
                    break

    def getQueenMoves(self, r, c, moves):  # queens can moce like rocks and bishops at the same time
        self.getRockMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--":  # conditin 2
            if (not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2)):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

    def getKnighMoves(self, r, c, moves):
        # knight can jump so no need to check if a specfic piece is blcoking it

        knitemoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2),
                      (2, -1), (2, 1))
        ally_color = "w" if self.whiteMove else "b"
        for m in knitemoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally_color:  # -- or b -- make sure that you are not capturing your own piece
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getKingMoves(self, r, c, moves):
        kingmoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_color = "w" if self.whiteMove else "b"
        for i in range(8):
            endRow = r + kingmoves[i][0]
            endCol = c + kingmoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # still in board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally_color:  # -- or b-- make sure that you are not capturing your own piece
                    moves.append(Move((r, c), (endRow, endCol), self.board))

        # here we add the castle moves that satisfies the rights

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):  # ! condition 1-- king should not be under attack
            return  # can't castle
        # ! condition 2 --
        # * kings are not yet moved nor the rock in the specific side.
        # * This right can be checked using the castling right class
        # using the attribute currentCastlingRights
        if (self.whiteMove and self.currentCastlingRights.wks) or (
                not self.whiteMove and self.currentCastlingRights.bks):
            self.getKingSideCastleMoves(r, c, moves)

        if (self.whiteMove and self.currentCastlingRights.wqs) or (
                not self.whiteMove and self.currentCastlingRights.bqs):
            self.getQueenSideCastleMoves(r, c, moves)

    def getKingSideCastleMoves(self, r, c, moves):
        if c < 5:  # because king is at 4
            if self.board[r][c + 1] == "--" and self.board[r][c + 2] == "--":
                # ! conditin 3 there is space for king and rock to switch position
                if (not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2)):
                    moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))
                    # this move satisfies all conditions, so it is a valid move


class castlingRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks  # possible from white kings side
        self.bks = bks  # possible from black queen side
        self.wqs = wqs  # possible from white kings side
        self.bqs = bqs  # possible from black queen side


class Move:

    def __init__(self, startSQ, endSQ, board, isEnpassantMove=False, isCastleMove=False):
        # ! we need to save the move so we can undo it later on
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        # ! pawn promotion -- reached the other side( opponent's side)
        self.isPawnPromotion = (
                    (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7))

        # ! enpassant -- to keep the value of the argument and save it
        # Above , we sent  isEnpassantMove = True when the move was enpassant (in the pawm moves)

        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"

        # ! castle move -- to keep the value of the argument and save it
        # Above , we sent  isCastleMove = True when the move was enpassant
        self.isCastleMove = isCastleMove

        # used to compare objects of type move. if they have the same moveID , they are equal
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        # * Makes sure it is the same piece

    def __eq__(self, other):
        """ mouse vs valid moves"""
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
