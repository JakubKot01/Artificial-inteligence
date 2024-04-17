"""
# - ściana
G - punkt docelowy
S - punkt startowy (>= 1)
B - punkt startowo-docelowy (>= 0)
  - pozostałe (spacja)
"""

from collections import deque
import random
import time
import turtle

################################## TURTLE BOARD DRAWING ################################################

CELL_SIZE = 20
OFFSET_X = -200
OFFSET_Y = 200
COLORS = {'#': 'black', ' ': 'white', 'S': 'blue', 'G': 'green', 'B': 'orange'}


def draw(points):
    screen = turtle.Screen()
    screen.setup(800, 800)
    screen.tracer(0, 0)

    for i in range(MAP_HEIGHT):
        for j in range(MAP_WIDTH):
            draw_cell(j, i, MAP[i][j])

    for (i, j) in points:
        draw_cell(j, i, 'S')

    for (i, j) in GOALS:
        draw_cell(j, i, 'G')

    screen.update()


def draw_cell(i, j, cell):
    turtle.penup()
    turtle.goto(OFFSET_X + i * CELL_SIZE, OFFSET_Y - j * CELL_SIZE)
    turtle.pendown()

    turtle.color(COLORS[cell])
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(CELL_SIZE)
        turtle.right(90)
    turtle.end_fill()


########################################################################################################

MAP_WIDTH = 0
MAP_HEIGHT = 0
MAP = []
GOALS = set()
MOVES = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}


class State:
    def __init__(self, pos=None, path=''):
        if pos is None:
            pos = set()
        self.positions = pos
        self.path = path


def parse_input() -> State:
    global MAP_HEIGHT, MAP_WIDTH, MAP

    with open('zad2_input.txt', 'r') as file:
        for line in file:
            MAP.append(list(line.strip()))
        MAP_HEIGHT = len(MAP)
        MAP_WIDTH = len(MAP[0])

    init_state = State()

    for i in range(MAP_HEIGHT):
        for j in range(MAP_WIDTH):
            if MAP[i][j] == '#':
                continue
            elif MAP[i][j] == 'S':
                init_state.positions.add((i, j))
            elif MAP[i][j] == 'G':
                GOALS.add((i, j))
            elif MAP[i][j] == 'B':
                GOALS.add((i, j))
                init_state.positions.add((i, j))
            MAP[i][j] = ' '

    return init_state


def make_moves(state: State, direction: str) -> State:
    next_state = State()

    for pos in state.positions:
        new_pos = (pos[0] + MOVES[direction][0], pos[1] + MOVES[direction][1])

        if MAP[new_pos[0]][new_pos[1]] == '#':
            next_state.positions.add(pos)
        else:
            next_state.positions.add(new_pos)

    next_state.path = state.path + direction

    return next_state


def reduce_states(state: State, MAX_POINTS=10) -> State:
    global MAP_HEIGHT, MAP_HEIGHT

    dirs = 'UDLR'
    points = state.positions
    best_state = state
    i = 0
    opposite_dir = {'R': 'L', 'D': 'U', 'L': 'R', 'U': 'D'}
    while len(points) > MAX_POINTS:
        if i > 80:
            points = state.positions
            best_state = state
            i = 0

        # ban useless moves like moving Right after we moved Left
        # banned: LR, RL, UD, DU
        prev_move = 'X'
        if len(best_state.path) > 0:
            prev_move = best_state.path[-1]
        direction = random.choice(dirs)
        while prev_move == opposite_dir[direction]:
            direction = random.choice(dirs)

        best_state = make_moves(best_state, direction)
        points = best_state.positions
        i += 1

        # draw(best_state.positions)

    # print(f'Before: {state.positions}\nAfter: {best_state.positions}')
    # time.sleep(5)
    return best_state


def can_plant_the_bomb(state: State) -> bool:
    for pos in state.positions:
        if pos not in GOALS:
            return False
    return True


def BFS(start_state: State) -> State:
    queue = deque()
    visited = set()

    queue.append(start_state)
    points = len(start_state.positions)

    while queue:
        actual_state = queue.popleft()

        if len(actual_state.path) > 150:
            continue

        if tuple(actual_state.positions) in visited:
            continue

        visited.add(tuple(actual_state.positions))

        if can_plant_the_bomb(actual_state):
            return actual_state

        states = []
        for direction in 'UDLR':
            new_state = make_moves(actual_state, direction)
            states.append(new_state)

            # better state
            if len(new_state.positions) < points:
                points = len(new_state.positions)
                queue.clear()
                visited.clear()

        for state in states:
            queue.append(state)


def solve() -> str:
    starting_state = parse_input()

    solution = None
    while True:
        reduced_state = reduce_states(starting_state, 4)
        solution = BFS(reduced_state)
        if solution and len(solution.path) < 150:
            print(len(solution.path))
            return solution.path


with open('zad2_output.txt', 'w') as file:
    print(solve(), file=file)
