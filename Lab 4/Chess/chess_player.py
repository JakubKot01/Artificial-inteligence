from functools import cmp_to_key
import chess
import sys
import chess.polyglot

PAWN_WHITE = [
    0,   0,   0,   0,   0,   0,   0,   0,
    5,   10,  10,  -20, -20, 10,  10,  5,
    5,   -5,  -10, 0,   0,   -10, -5,  5,
    0,   0,   0,   20,  20,  0,   0,   0,
    5,   5,   10,  25,  25,  10,  5,   5,
    10,  10,  20,  30,  30,  20,  10,  10,
    50,  50,  50,  50,  50,  50,  50,  50,
    0,   0,   0,   0,   0,   0,   0,   0
]
PAWN_BLACK = PAWN_WHITE[::-1]

KNIGHT_WHITE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]
KNIGHT_BLACK = KNIGHT_WHITE[::-1]

BISHOP_WHITE = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
BISHOP_BLACK = BISHOP_WHITE[::-1]

ROOK_WHITE = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, 10, 10, 10, 10, 5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    0, 0, 0, 5, 5, 0, 0, 0
]
ROOK_BLACK = ROOK_WHITE[::-1]

QUEEN_WHITE = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]
QUEEN_BLACK = QUEEN_WHITE[::-1]

KING_WHITE = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 20, 0, 0, 0, 0, 20, 20,
    20, 30, 10, 0, 0, 10, 30, 20
]
KING_BLACK = KING_WHITE[::-1]

MVV_LVA = [
    [15, 14, 13, 12, 11, 10], # victim P; attacker: P N B R Q K
    [25, 24, 23, 22, 21, 20], # victim N
    [35, 34, 33, 32, 31, 30], # victim B
    [45, 44, 43, 42, 41, 40], # victim R
    [55, 54, 53, 52, 51, 50], # victim Q
    [0, 0, 0, 0, 0, 0]        # victim K
]

PST = [
    (PAWN_BLACK, PAWN_WHITE),
    (KNIGHT_BLACK, KNIGHT_WHITE),
    (BISHOP_BLACK, BISHOP_WHITE),
    (ROOK_BLACK, ROOK_WHITE),
    (QUEEN_BLACK, QUEEN_WHITE)
]

PIECE_VALUE = {
    chess.PAWN : 100,
    chess.BISHOP : 320,
    chess.KNIGHT : 320,
    chess.ROOK : 500,
    chess.QUEEN : 900,
    chess.KING : 0
}

KNIGHT_MOBILITY = 5.5
BISHOP_MOBILITY = 4
ROOK_MOBILITY = 1
QUEEN_MOBILITY = 2
KING_MOBILITY = 0

class AI:
    def __init__(self, white=False):
        self.reset(white)
    
    def reset(self, white=False):
        self.board = chess.Board()
        self.color = white
        self.current_board_evaluation = 0
        self.strong_pieces_count = 14
        self.depth = 4
        self.say('RDY')

    def make_move(self, move):
        square_from, square_to = move.from_square, move.to_square
        piece_from, piece_to = self.board.piece_at(square_from), self.board.piece_at(square_to)

        # remove taken piece from board
        if piece_to is not None:
            self.place_or_remove_piece_from_board(piece_to, square_to, True)
        
        # move piece
        self.place_or_remove_piece_from_board(piece_from, square_from, True)
        if move.promotion is not None:
            self.place_or_remove_piece_from_board(chess.Piece(move.promotion, self.board.turn), square_to, False)
        else:
            self.place_or_remove_piece_from_board(piece_from, square_to, False)
        self.board.push(move)

    def place_or_remove_piece_from_board(self, piece, square, remove_flag):
        """
        Places or removes piece from board.
        Updates current_board_evaluation to changes
        """
        if piece.piece_type not in (chess.PAWN, chess.KING):
            if remove_flag:
                self.strong_pieces_count -= 1
            else:
                self.strong_pieces_count += 1
        
        factor = 1
        if not piece.color:
            factor = -1
        if remove_flag:
            factor *= -1
        
        self.current_board_evaluation += factor * PIECE_VALUE[piece.piece_type]
        if piece.piece_type != chess.KING:
            self.current_board_evaluation += factor * PST[piece.piece_type-1][piece.color][square]
            return
        
        #TODO: add king in middle/end game
        if piece.color:
            self.current_board_evaluation += factor * KING_WHITE[square]
        else:
            self.current_board_evaluation += factor * KING_BLACK[square]

    def get_best_move(self):
        #TODO: dodać ograniczenie czasowe do ABS
        score, move = self.AlphaBetaSearch(self.depth, self.color, -float('inf'), float('inf'), False)
        return move

    def get_attacked(self, piece, color):
        squares = self.board.pieces(piece_type=piece, color=color)
        attacked = chess.SquareSet()
        a = [self.board.attacks(sq) for sq in squares]
        for x in a:
            attacked.update(x)
        return attacked
    
    def mobility(self):
        score = 0
        w_knights, b_knights = self.get_attacked(chess.KNIGHT, True), self.get_attacked(chess.KNIGHT, False)
        w_bishops, b_bishops = self.get_attacked(chess.BISHOP, True), self.get_attacked(chess.BISHOP, False)
        w_rooks, b_rooks = self.get_attacked(chess.ROOK, True), self.get_attacked(chess.ROOK, False)
        w_queens, b_queens = self.get_attacked(chess.QUEEN, True), self.get_attacked(chess.QUEEN, False)

        score += KNIGHT_MOBILITY * (len(w_knights) - len(b_knights))
        score += BISHOP_MOBILITY * (len(w_bishops) - len(b_bishops))
        score += ROOK_MOBILITY * (len(w_rooks) - len(b_rooks))
        score += QUEEN_MOBILITY * (len(w_queens) - len(b_queens))

        return score


    def heura(self):
        #TODO: dodać: strukture pionów, bicie, itp
        return self.current_board_evaluation + self.mobility()
    
    def move_ordering(self, move1, move2):
        c1, c2 = self.board.is_capture(move1), self.board.is_capture(move2)
        if c1 and c2:

            attacker, victim = self.board.piece_at(move1.from_square).piece_type-1, self.board.piece_at(move1.to_square)
            if victim is None: # exception: en_passant does not 'directly' capture pawn
                victim = chess.PAWN-1
            else:
                victim = victim.piece_type-1
            val1 = MVV_LVA[victim][attacker]

            attacker, victim = self.board.piece_at(move2.from_square).piece_type-1, self.board.piece_at(move2.to_square)
            if victim is None: # exception: en_passant does not 'directly' capture pawn
                victim = chess.PAWN-1
            else:
                victim = victim.piece_type-1
            val2 = MVV_LVA[victim][attacker]
            return val1 - val2

        return c1 - c2

    def AlphaBetaSearch(self, depth, maximizing_player, alpha, beta, pawn_captured):
        #TODO: outcome(claim_draw=True) po 40 ruchach?
        outcome = self.board.outcome()
        if outcome is not None:
            result = outcome.winner
            if result is None:
                return 0, None
            if result:
                return float('inf'), None
            return -float('inf'), None

        if depth == 0:
            # if pawn_captured or self.board.is_check():
            #     print("quick_search!", file=sys.stderr)
            #     return self.quick_search(2, maximizing_player, alpha, beta)
            return self.heura(), None
        
        moves = list(self.board.legal_moves)
        moves.sort(key=cmp_to_key(self.move_ordering), reverse=True)
        best_move = moves[0]

        if maximizing_player:
            best_score = -float('inf')
            for move in moves:
                saved_eval, saved_count = self.current_board_evaluation, self.strong_pieces_count
                pawn_captured = self.board.is_capture(move)
                self.make_move(move)

                child_score, _ = self.AlphaBetaSearch(depth-1, False, alpha, beta, pawn_captured)

                # undo move
                self.board.pop()
                self.current_board_evaluation = saved_eval
                self.strong_pieces_count = saved_count

                if child_score > best_score:
                    best_score = child_score
                    best_move = move
                    alpha = max(alpha, best_score)
                
                if best_score >= beta:
                    break

        else: # minimizing_player
            best_score = float('inf')
            for move in moves:
                saved_eval, saved_count = self.current_board_evaluation, self.strong_pieces_count
                pawn_captured = self.board.is_capture(move)
                self.make_move(move)

                child_score, _ = self.AlphaBetaSearch(depth-1, True, alpha, beta, pawn_captured)

                # undo move
                self.board.pop()
                self.current_board_evaluation = saved_eval
                self.strong_pieces_count = saved_count

                if child_score < best_score:
                    best_score = child_score
                    best_move = move
                    beta = min(beta, best_score)
                
                if best_score <= alpha:
                    break
        
        return best_score, best_move

    def quick_search(self, depth, maximizing_player, alpha, beta):
        outcome = self.board.outcome()
        if outcome is not None:
            result = outcome.winner
            if result is None:
                return 0, None
            if result:
                return float('inf'), None
            return -float('inf'), None
        
        if depth == 0:
            return self.heura(), None
        
        moves = [x for x in self.board.legal_moves if self.board.is_capture(x) or self.board.is_check()]
        if not moves:
            return self.heura(), None
        
        moves.sort(key=cmp_to_key(self.move_ordering), reverse=True)
        best_move = moves[0]

        if maximizing_player:
            best_score = -float('inf')
            for move in moves:
                saved_eval, saved_count = self.current_board_evaluation, self.strong_pieces_count
                self.make_move(move)

                child_score, _ = self.quick_search(depth-1, False, alpha, beta)

                # undo move
                self.board.pop()
                self.current_board_evaluation = saved_eval
                self.strong_pieces_count = saved_count

                if child_score > best_score:
                    best_score = child_score
                    best_move = move
                    alpha = max(alpha, best_score)
                
                if best_score >= beta:
                    break

        else: # minimizing_player
            best_score = float('inf')
            for move in moves:
                saved_eval, saved_count = self.current_board_evaluation, self.strong_pieces_count
                self.make_move(move)

                child_score, _ = self.quick_search(depth-1, True, alpha, beta)

                # undo move
                self.board.pop()
                self.current_board_evaluation = saved_eval
                self.strong_pieces_count = saved_count

                if child_score < best_score:
                    best_score = child_score
                    best_move = move
                    beta = min(beta, best_score)
                
                if best_score <= alpha:
                    break
        
        return best_score, best_move

    ###################### COMMUNICATION ############################

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
                move = args[2]
                self.make_move(chess.Move.from_uci(move))

            elif cmd == 'ONEMORE':
                self.reset()
                continue

            elif cmd == 'BYE':
                break
            else:
                assert cmd == 'UGO'
                self.color = 1
            try:
                entry = reader.choice(agent.board)
                move = entry.move
            except IndexError:                
                move = agent.get_best_move()
            self.make_move(move)
            self.say('IDO ' + str(move))

if __name__ == '__main__':
    with chess.polyglot.open_reader('Chess/baron30.bin') as reader:
        agent = AI()
        agent.loop()