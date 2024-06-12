from copy import deepcopy
import random
from time import time

DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
WHITE = 0
BLACK = 1
UNOCCUPIED = -1
OPPONENT_PIECE_COLOR = {WHITE: BLACK, BLACK: WHITE}


class Board:
    def __init__(self):
        self.board = [[-1 for _ in range(8)] for _ in range(8)]
        self.whitePieces = {(3, 3), (4, 4)}
        self.blackPieces = {(3, 4), (4, 3)}

        self.board[3][3] = WHITE
        self.board[4][4] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK

        self.turn = BLACK
        self.movesMade = 0

    def boardScore(self):
        return (len(self.whitePieces), len(self.blackPieces))

    def isInBounds(self, row, col):
        return  8 > row > -1 and 8 > col > -1

    def getPiecesPositions(self, color):
        pieces = set()
        if color == WHITE:
            pieces = self.whitePieces
        else:
            pieces = self.blackPieces
        return (pos for pos in pieces)

    def hasDirValidPlacement(self, row, col, x, y):
        # looking for position in (x, y) direction we can put the pawn
        # if so - return this position
        while self.isInBounds(row + x, col + y) and self.board[row + x][col + y] == OPPONENT_PIECE_COLOR[self.turn]:
            row += x
            col += y
            if self.isInBounds(row + x, col + y) and self.board[row + x][col + y] == UNOCCUPIED:
                return row + x, col + y
        return False

    def allPossibleMoves(self):
        moves = set()
        for (r, c) in self.getPiecesPositions(OPPONENT_PIECE_COLOR[self.turn]):
            for (x, y) in DIRS:
                move = self.hasDirValidPlacement(r, c, x, y)
                if move:
                    moves.add(move)
        return list(moves)

    def placeDiscAt(self, row, col):
        winningPieces = set()
        loosingPieces = set()
        if self.turn == WHITE:
            winningPieces = self.whitePieces
            loosingPieces = self.blackPieces
        else:
            loosingPieces = self.whitePieces
            winningPieces = self.blackPieces

        winningPieces.add((row, col))
        self.board[row][col] = self.turn

        piecesToFlip = set()
        # looking for captured pawns
        for (x, y) in DIRS:
            current = set()
            next_x = row + x
            next_y = col + y
            while self.isInBounds(next_x, next_y) and self.board[next_x][next_y] == OPPONENT_PIECE_COLOR[self.turn]:
                current.add((next_x, next_y))
                next_x += x
                next_y += y
                if self.isInBounds(next_x, next_y) and self.board[next_x][next_y] == self.turn:
                    for pos in current:
                        piecesToFlip.add(pos)
                    break

        # collecting captured pawns
        for pos in piecesToFlip:
            self.board[pos[0]][pos[1]] = self.turn
            winningPieces.add(pos)
            loosingPieces.remove(pos)

        # opponent's turn
        self.turn = OPPONENT_PIECE_COLOR[self.turn]

    def copy(self):
        new_board = Board()
        new_board.board = deepcopy(self.board)
        new_board.whitePieces = deepcopy(self.whitePieces)
        new_board.blackPieces = deepcopy(self.blackPieces)
        new_board.movesMade = deepcopy(self.movesMade)
        new_board.turn = deepcopy(self.turn)
        return new_board


########################################################## AGENTS ##########################################################

class RandomPlayer:
    def __init__(self, color, board):
        self.board = board
        self.color = color

    def move(self):
        moves = self.board.allPossibleMoves()
        if len(moves) == 0:
            return False
        randomID = random.randint(0, len(moves) - 1)
        randomMove = moves[randomID]
        self.board.placeDiscAt(randomMove[0], randomMove[1])


class AI:
    __priority = [[30, -10, 11, 8, 8, 11, -10, 30],
                  [-10, -7, -4, 1, 1, -4, -7, -10],
                  [11, - 4, 2, 2, 2, 2, -4, 11],
                  [8, 1, 2, 0, 0, 2, 1, 8],
                  [8, 1, 2, 0, 0, 2, 1, 8],
                  [11, -4, 2, 2, 2, 2, -4, 11],
                  [-10, -7, -4, 1, 1, -4, -7, -10],
                  [30, -10, 11, 8, 8, 11, -10, 30]]

    def __init__(self, color, board):
        self.board = board
        self.color = color
        self.pieces = board.getPiecesPositions(color)

    def score(self, board, priorities):
        score = 0
        for row in range(8):
            for col in range(8):
                if board[row][col] == self.color:
                    score += priorities[row][col]
                if board[row][col] == OPPONENT_PIECE_COLOR[self.color]:
                    score -= priorities[row][col]
        return score

    def stability(self, color):
        def directionStability(pos, pieces, x, y):
            res = set()
            if pos in pieces:
                res.add(pos)
                while (pos[0] + x, pos[1] + y) in pieces:
                    res.add((pos[0] + x, pos[1] + y))
                    pos = (pos[0] + x, pos[1] + y)
            return res

        pieces = self.board.getPiecesPositions(color)
        stableFields = set()

        # left top
        stableFields.update(directionStability((0, 0), pieces, 0, 1))
        stableFields.update(directionStability((0, 0), pieces, 1, 0))
        # left bottom
        stableFields.update(directionStability((7, 0), pieces, -1, 0))
        stableFields.update(directionStability((7, 0), pieces, 0, 1))
        # right top
        stableFields.update(directionStability((0, 7), pieces, 1, 0))
        stableFields.update(directionStability((0, 7), pieces, 0, -1))
        # right bottom
        stableFields.update(directionStability((7, 7), pieces, -1, 0))
        stableFields.update(directionStability((7, 7), pieces, 0, -1))

        return len(stableFields)

    def heuristic(self):
        # TODO: improve
        h = 0
        h += self.score(self.board.board, self.__priority)

        (w, b) = self.board.boardScore()
        if self.board.movesMade > 50:
            if self.color == WHITE:
                h += 3 * (w - b)
            else:
                h += 3 * (b - w)

        h += 30 * (self.stability(self.color) - self.stability(OPPONENT_PIECE_COLOR[self.color]))

        return h

    def move(self):
        moves = self.board.allPossibleMoves()
        if len(moves) == 0:
            return False

        bestScore = (float('-inf'), 0, 0)
        for (x, y) in moves:
            board2 = self.board.copy()

            self.board.placeDiscAt(x, y)
            self.board.turn = OPPONENT_PIECE_COLOR[self.board.turn]

            score = self.heuristic()

            self.board = board2

            if score > bestScore[0]:
                bestScore = (score, x, y)

            self.board.turn = self.color

        self.board.placeDiscAt(bestScore[1], bestScore[2])


########################################################## SIMULATIONS ##########################################################

def playGame(agent1, agent2):
    board = Board()
    white = agent1(WHITE, board)
    black = agent2(BLACK, board)

    while True:
        board.movesMade += 1
        if black.move() == False:
            board.movesMade -= 1
        board.movesMade += 1
        if white.move() == False:
            board.movesMade -= 1
        if black.move() == False and white.move() == False:
            break

    (whiteScore, blackScore) = board.boardScore()
    if whiteScore > blackScore:
        return 'WHITE'
    elif whiteScore < blackScore:
        return 'BLACK'
    else:
        return 'DRAW'


def makeSimulation(agent1, agent2, games=1000):
    winner1 = 0
    winner2 = 0
    draws = 0

    for i in range(games):
        game = playGame(agent1, agent2)
        if game == 'WHITE':
            winner1 += 1
        elif game == 'BLACK':
            winner2 += 1
        else:
            draws += 1

    print(f'Agent 1 WON {winner1} times, tied {draws} times, lost {winner2} times')


if __name__ == '__main__':
    timer = time()
    makeSimulation(AI, RandomPlayer)
    print(f'Simulation time: {(time() - timer) / 60} ')



