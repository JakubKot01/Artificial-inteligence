import random
import sys
from copy import deepcopy

class WrongMove(Exception):
    pass

class Jungle:
    DEN_DISTANCE = [
        [
            [8, 9, 10, 11, 10, 9, 8],
            [7, 8, 9, 10, 9, 8, 7],
            [6, 7, 8, 9, 8, 7, 6],
            [5, 6, 7, 8, 7, 6, 5],
            [4, 5, 6, 7, 6, 5, 4],
            [3, 4, 5, 6, 5, 4, 3],
            [2, 3, 4, 5, 4, 3, 2],
            [1, 2, 3, 4, 3, 2, 1],
            [0, 1, 2, 3, 2, 1, 0]
        ],
        [
            [0, 1, 2, 3, 2, 1, 0],
            [1, 2, 3, 4, 3, 2, 1],
            [2, 3, 4, 5, 4, 3, 2],
            [3, 4, 5, 6, 5, 4, 3],
            [4, 5, 6, 7, 6, 5, 4],
            [5, 6, 7, 8, 7, 6, 5],
            [6, 7, 8, 9, 8, 7, 6],
            [7, 8, 9, 10, 9, 8, 7],
            [8, 9, 10, 11, 10, 9, 8]
        ]
        # [
        #     [11, 10, 9, 8, 9, 10, 11],
        #     [10, 9, 8, 7, 8, 9, 10],
        #     [9, 8, 7, 6, 7, 8, 9],
        #     [8, 7, 6, 5, 6, 7, 8],
        #     [7, 6, 5, 4, 5, 6, 7],
        #     [6, 5, 4, 3, 4, 5, 6],
        #     [5, 4, 3, 2, 3, 4, 5],
        #     [4, 3, 2, 1, 2, 3, 4],
        #     [3, 2, 1, 0, 1, 2, 3]
        # ],
        # [
        #     [3, 2, 1, 0, 1, 2, 3],
        #     [4, 3, 2, 1, 2, 3, 4],
        #     [5, 4, 3, 2, 3, 4, 5],
        #     [6, 5, 4, 3, 4, 5, 6],
        #     [7, 6, 5, 4, 5, 6, 7],
        #     [8, 7, 6, 5, 6, 7, 8],
        #     [9, 8, 7, 6, 7, 8, 9],
        #     [10, 9, 8, 7, 8, 9, 10],
        #     [11, 10, 9, 8, 9, 10, 11]
        # ]
    ]
    PIECE_VALUES = {
        0: 4,
        1: 1,
        2: 2,
        3: 3,
        4: 5,
        5: 7,
        6: 8,
        7: 10
    }
    MAXIMAL_PASSIVE = 30
    DENS_DIST = 0.1
    MX = 7
    MY = 9
    traps = {(2, 0), (4, 0), (3, 1), (2, 8), (4, 8), (3, 7)}
    ponds = {(x, y) for x in [1, 2, 4, 5] for y in [3, 4, 5]}
    dens = [(3, 8), (3, 0)]
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    rat, cat, dog, wolf, jaguar, tiger, lion, elephant = range(8)

    def __init__(self):
        self.board = self.initial_board()
        self.pieces = {0: {}, 1: {}}

        for y in range(Jungle.MY):
            for x in range(Jungle.MX):
                C = self.board[y][x]
                if C:
                    player, figure_index = C
                    self.pieces[player][figure_index] = (x, y)
        self.current_player = 0
        self.peace_counter = 0
        self.winner = None

    def initial_board(self):
        pieces = """
        L.....T
        .D...C.
        R.J.W.E
        .......
        .......
        .......
        e.w.j.r
        .c...d.
        t.....l
        """

        B = [x.strip() for x in pieces.split() if len(x) > 0]
        # Disctionary mapping figures letters on indexes
        T = dict(zip('rcdwjtle', range(8)))

        res = []
        for y in range(9):
            raw = 7 * [None]
            for x in range(7):
                c = B[y][x]
                if c != '.':
                    if 'A' <= c <= 'Z':
                        player = 1
                    else:
                        player = 0
                    # Tuple: (player number, figure index from T)
                    raw[x] = (player, T[c.lower()])
            res.append(raw)
        return res

    def random_move(self, player):
        ms = self.moves(player)
        if ms:
            return random.choice(ms)
        return None

    def can_beat(self, p1, p2, pos1, pos2):
        if pos1 in Jungle.ponds and pos2 in Jungle.ponds:
            return True  # rat vs rat
        if pos1 in Jungle.ponds:
            return False  # rat in pond cannot beat any piece on land
        if p1 == Jungle.rat and p2 == Jungle.elephant:
            return True
        if p1 == Jungle.elephant and p2 == Jungle.rat:
            return False
        if p1 >= p2:
            return True
        if pos2 in Jungle.traps:
            return True
        return False

    def pieces_comparison(self):
        for i in range(7,-1,-1):
            ps = []
            for p in [0,1]:
                if i in self.pieces[p]:
                    ps.append(p)
            if len(ps) == 1:
                return ps[0]
        return None
                
    def rat_is_blocking(self, player_unused, pos, dx, dy):        
        x, y = pos
        nx = x + dx
        for player in [0,1]:
            if Jungle.rat not in self.pieces[1-player]:
                continue
            rx, ry = self.pieces[1-player][Jungle.rat]
            if (rx, ry) not in self.ponds:
                continue
            if dy != 0:
                if x == rx:
                    return True
            if dx != 0:
                if y == ry and abs(x-rx) <= 2 and abs(nx-rx) <= 2:
                    return True
        return False

    def moves(self, player):
        res = []
        for pawn, pos in self.pieces[player].items():
            x, y = pos
            for (dx, dy) in Jungle.dirs:
                pos2 = (nx, ny) = (x+dx, y+dy)
                if 0 <= nx < Jungle.MX and 0 <= ny < Jungle.MY:
                    # cannot get to your own den
                    if Jungle.dens[player] == pos2:
                        continue
                    if pos2 in self.ponds:
                        # only rat can stay in the pond
                        # lion and tiget jump over the pond
                        if pawn not in (Jungle.rat, Jungle.tiger, Jungle.lion):
                            continue
                        if pawn == Jungle.tiger or pawn == Jungle.lion:
                            if dx != 0:
                                dx *= 3
                            if dy != 0:
                                dy *= 4
                            if self.rat_is_blocking(player, pos, dx, dy):
                                continue
                            pos2 = (nx, ny) = (x+dx, y+dy)
                    if self.board[ny][nx] is not None:
                        player2, pawn2 = self.board[ny][nx]
                        if player2 == player:
                            continue
                        if not self.can_beat(pawn, pawn2, pos, pos2):
                            continue
                    res.append((pos, pos2))
        return res

    def do_move(self, m):
        self.current_player = 1 - self.current_player
        if m is None:
            return
        pos1, pos2 = m
        x, y = pos1
        pl, pc = self.board[y][x]

        x2, y2 = pos2
        if self.board[y2][x2]:  # piece taken!
            pl2, pc2 = self.board[y2][x2]
            del self.pieces[pl2][pc2]
            self.peace_counter = 0
        else:
            self.peace_counter += 1    

        self.pieces[pl][pc] = (x2, y2)
        self.board[y2][x2] = (pl, pc)
        self.board[y][x] = None
        
    def result(self, player):
        res = 0
        for piece, pos in self.pieces[1 - player].items():
            res -= self.PIECE_VALUES[piece]
        for piece, pos in self.pieces[player].items():
            res += self.PIECE_VALUES[piece]

        return res
    
    def den_dist(self, player):
        res = 0
        for piece, pos in self.pieces[1 - player].items():
            res -= 2 * self.DEN_DISTANCE[1 - player][pos[1]][pos[0]]
        for piece, pos in self.pieces[player].items():
            res += 2 * self.DEN_DISTANCE[player][pos[1]][pos[0]]
        
        return res

    def run_simulation(self, move, player):
        saved_board = deepcopy(self.board)
        saved_pieces = deepcopy(self.pieces)
        saved_player = self.current_player
        saved_peace_counter = self.peace_counter

        self.do_move(move)
        result = self.result(player) + self.den_dist(player)

        self.board = saved_board
        self.pieces = saved_pieces
        self.current_player = saved_player
        self.peace_counter = saved_peace_counter

        return result

    def run_simulations(self, moves, player):
        best_move = None
        best_res = float("-inf")
        for move in moves:
            res = self.run_simulation(move, player)

            if res > best_res:
                best_res = res
                best_move = move

        return best_move

    def best_move(self, player):
        moves = self.moves(player)
        return self.run_simulations(moves, player)

class Player(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.game = Jungle()
        self.my_player = 1
        self.say('RDY')

    def say(self, what):
        sys.stdout.write(what)
        sys.stdout.write('\n')
        sys.stdout.flush()

    def hear(self):
        line = sys.stdin.readline().split()
        return line[0], line[1:]

    def loop(self):
        while True:
            cmd, args = self.hear()
            if cmd == 'HEDID':
                unused_move_timeout, unused_game_timeout = args[:2]
                move = tuple((int(m) for m in args[2:]))
                if move == (-1, -1, -1, -1):
                    move = None
                else:
                    xs, ys, xd, yd = move
                    move = (xs, ys), (xd, yd)
                        
                self.game.do_move(move)
            elif cmd == 'ONEMORE':
                self.reset()
                continue
            elif cmd == 'BYE':
                break
            else:
                assert cmd == 'UGO'
                #assert not self.game.move_list
                self.my_player = 0

            moves = self.game.moves(self.my_player)
            if moves:
                move = self.game.best_move(self.my_player)
                self.game.do_move(move)
                move = (move[0][0], move[0][1], move[1][0], move[1][1])
            else:
                self.game.do_move(None)
                move = (-1, -1, -1, -1)
            self.say('IDO %d %d %d %d' % move)


if __name__ == '__main__':
    player = Player()
    player.loop()
