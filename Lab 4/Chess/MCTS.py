from sys import stdout
import chess
from time import time
from math import sqrt, log
from random import choice

C = 1.0

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9
}

board = chess.Board()


def reset_board():
    global board
    board = chess.Board()


class Node:
    def __init__(self, game_over, parent, move, agent_player):
        self.children = {}
        self.heuristics_sum = 0
        self.visit_count = 0
        self.game_over = game_over
        self.parent = parent
        self.move = move
        self.agent_player = agent_player

    def ucb_score(self):
        if self.heuristics_sum == 0:
            return float("inf")

        parent_visits = self.parent.visit_count if self.parent else self.visit_count
        return self.heuristics_sum / self.visit_count + C * sqrt(log(parent_visits) / self.visit_count)

    def expand(self):
        if self.game_over:
            return

        self.children = {
            m: self.create_child_node(m) for m in board.legal_moves
        }

    def create_child_node(self, move):
        board.push(move)
        child_node = Node(board.is_game_over(), self, move, self.agent_player)
        board.pop()
        return child_node

    def explore(self):
        current = self
        path = []

        while current.children:
            move, current = self.select_child(current)
            board.push(move)
            path.append(current)

        if current.visit_count == 0:
            current.heuristics_sum += current.run_simulation()
        else:
            current.expand()
            if current.children:
                move, current = self.select_random_child(current)
                board.push(move)
                current.heuristics_sum += current.run_simulation()
                board.pop()
            else:
                current.heuristics_sum += current.run_simulation()

        current.visit_count += 1
        self.backpropagate(current, path)

    @staticmethod
    def select_child(node):
        max_ucb = max(child.ucb_score() for child in node.children.values())
        selected_moves = [move for move, child in node.children.items() if child.ucb_score() == max_ucb]
        selected_move = choice(selected_moves)
        return selected_move, node.children[selected_move]

    @staticmethod
    def select_random_child(node):
        selected_move = choice(list(node.children.keys()))
        return selected_move, node.children[selected_move]

    @staticmethod
    def backpropagate(node, path):
        for parent in reversed(path):
            parent.visit_count += 1
            parent.heuristics_sum += node.heuristics_sum
            board.pop()

    def run_simulation(self):
        if self.game_over:
            return 0

        total_value = 0
        depth = 0
        for depth in range(20):
            if board.is_game_over():
                break
            move = choice(list(board.legal_moves))
            board.push(move)
            total_value += Node.heuristic(board, self.agent_player)
            depth += 1

        for _ in range(depth):
            board.pop()

        return total_value

    def next(self):
        if self.game_over:
            raise ValueError("Game over in next")

        if not self.children:
            raise ValueError("There are no children in next")

        max_visit_count = max(node.visit_count for node in self.children.values())
        best_children = [c for a, c in self.children.items() if c.visit_count == max_visit_count]
        best_child = choice(best_children)
        best_child.parent = None
        board.push(best_child.move)

        return best_child, best_child.move.uci()

    def next_opponent(self, move):
        if self.game_over:
            raise ValueError("Game over in next_opponent")

        if not self.children:
            self.expand()

        for m, child in list(self.children.items()):
            if m.uci() == move:
                child.parent = None
                board.push(m)
                return child

        raise ValueError("Opponent move not found")

    @staticmethod
    def checkmate_heuristic(game, player):
        if game.is_checkmate():
            return float("inf") if game.turn != player else -float("inf")
        return 0

    @staticmethod
    def mobility_heuristic(game, player):
        return sum(1 if game.color_at(move.from_square) == player else -1 for move in game.legal_moves)

    @staticmethod
    def score_heuristic(game, player):
        score = 0
        for square in chess.SQUARES:
            piece = game.piece_at(square)
            if piece:
                value = PIECE_VALUES.get(piece.piece_type, 0)
                score += value if piece.color == player else -value

        return score

    @staticmethod
    def heuristic(game, player):
        return (
            Node.score_heuristic(game, player) +
            0.5 * Node.mobility_heuristic(game, player) +
            Node.checkmate_heuristic(game, player)
        )


class MCTS:
    def __init__(self):
        self.explores = 2

    def search(self, tree):
        start_time = time()
        explores = self.explores
        for _ in range(explores):
            tree.explore()

        if time() - start_time > 0.5 and self.explores > 2:
            self.explores -= 1
        else:
            self.explores += 1

        return tree


def read_input():
    return input().split()


def send_output(output):
    stdout.flush()
    print(output)
    stdout.flush()


if __name__ == '__main__':
    tree = Node(False, None, None, chess.BLACK)
    mcts = MCTS()
    send_output("RDY")
    while True:
        command = input().split()
        if command[0] == "UGO":
            tree = Node(False, None, None, chess.WHITE)
            tree = mcts.search(tree)
            tree, move = tree.next()
            send_output(f"IDO {move}")
        elif command[0] == "HEDID":
            move = command[3]
            tree = tree.next_opponent(move)
            tree = mcts.search(tree)
            tree, move = tree.next()
            send_output(f"IDO {move}")
        elif command[0] == "ONEMORE":
            tree = Node(False, None, None, chess.BLACK)
            reset_board()
            send_output("RDY")
        elif command[0] == "BYE":
            break