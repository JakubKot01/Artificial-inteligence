from heapq import heappop, heappush

MAP_WIDTH = 0
MAP_HEIGHT = 0
MAP = []
STARTING_POINTS = set()
GOALS = set()
MOVES = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

epsilon = 0.09


def parse_input():
    global MAP_HEIGHT, MAP_WIDTH, MAP, GOALS, STARTING_POINTS

    with open('zad3_input.txt', 'r') as file:
        for line in file:
            MAP.append(list(line.strip()))
        MAP_HEIGHT = len(MAP)
        MAP_WIDTH = len(MAP[0])

    for i in range(MAP_HEIGHT):
        for j in range(MAP_WIDTH):
            if MAP[i][j] == '#':
                continue
            elif MAP[i][j] == 'S':
                STARTING_POINTS.add((i, j))
            elif MAP[i][j] == 'G':
                GOALS.add((i, j))
            elif MAP[i][j] == 'B':
                GOALS.add((i, j))
                STARTING_POINTS.add((i, j))


def make_moves(positions, direction):
    global MOVES

    new_positions = set()
    (i, j) = MOVES[direction]
    for (x, y) in positions:
        if MAP[x + i][y + j] != '#':
            new_positions.add((x + i, y + j))
        else:
            new_positions.add((x, y))

    return new_positions


def can_plant_the_bomb(positions):
    global GOALS

    for pos in positions:
        if pos not in GOALS:
            return False
    return True


distances_cache = dict()


def closest_distances(pos):
    global distances_cache, GOALS, MAP

    if pos in distances_cache:
        return distances_cache[pos]

    if pos in GOALS:
        return 0

    q = set()
    q.add(pos)
    it = 0

    while True:
        new_q = set()
        for (x, y) in q:
            neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for (i, j) in neighbours:
                if (i, j) in GOALS:
                    distances_cache[pos] = it + 1
                    return distances_cache[pos]

                if MAP[i][j] != '#':
                    new_q.add((i, j))
                else:
                    new_q.add((x, y))

        q = new_q
        it += 1


def heuristic(positions, epsilon):
    return (1 + epsilon) * max([closest_distances(pos) for pos in positions])


def A_star(positions, epsilon):
    global MAP, GOALS

    heap = []  # (wartość_heurystyki, pozycje, ścieżka)
    visited = set(tuple(positions))

    heappush(heap, (heuristic(positions, epsilon), positions, ''))

    while heap:
        h, commando, path = heappop(heap)
        visited.add(tuple(commando))

        for direction in 'UDLR':
            new_commando = make_moves(commando, direction)

            if tuple(new_commando) in visited:
                continue

            if can_plant_the_bomb(new_commando):
                return path + direction

            h = heuristic(new_commando, epsilon) + len(path)
            heappush(heap, (h, new_commando, path + direction))


def solve():
    global STARTING_POINTS, epsilon

    parse_input()
    return A_star(STARTING_POINTS, epsilon)


with open('zad3_output.txt', 'w') as file:
    print(solve(), file=file)


