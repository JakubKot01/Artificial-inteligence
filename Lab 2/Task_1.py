import random
from pprint import pprint
from itertools import permutations
from queue import Queue

VERBOSE = False

WHITE = "."
BLACK = "#"
BOARD = []
QUEUE = Queue()


class Block:
    def __init__(self, value, length):
        self.value = value
        self.length = length


def check_order(original, permutated):
    original_order = []
    permutated_order = []

    for element in original:
        if element.value == "#":
            original_order.append(element.length)

    for element in permutated:
        if element.value == "#":
            permutated_order.append(element.length)

    return original_order == permutated_order


def generate_permutations(original):
    print("TEST DUPA 1")
    perm = permutations(original)

    print("TEST DUPA 2")

    filtered_permutations = []

    for p in perm:
        print(p)
        valid = True
        for i in range(len(p) - 1):
            if p[i].value == '#' and p[i + 1].value == '#':
                valid = False
                break
        if valid:
            if check_order(original, p):
                filtered_permutations.append(p)

    return filtered_permutations


def prepare_setting(permutation):
    result = []
    for element in permutation:
        for _ in range(element.length):
            result.append(element.value)
    return result


def find_all_settings(number_of_elements, descriptions):
    print(number_of_elements, descriptions)
    all_settings = []
    basic_setting = []
    number_of_active_blocks = len(descriptions)
    number_of_break_blocks = number_of_active_blocks - 1
    number_of_blocks = number_of_active_blocks + number_of_break_blocks
    filled_fields = 0
    for counter in range(number_of_blocks):
        if counter % 2 == 0:
            basic_setting.append(Block("#", descriptions[counter // 2]))
            filled_fields += descriptions[counter // 2]
        else:
            basic_setting.append(Block(".", 1))
            filled_fields += 1

    number_of_left_fields = number_of_elements - filled_fields
    for counter in range(number_of_left_fields):
        basic_setting.append(Block(".", 1))

    print("TEST1")

    all_settings.append(prepare_setting(basic_setting))

    print("TEST2")

    permutations_list = generate_permutations(basic_setting.copy())

    print("TEST3")

    for permutation in permutations_list:
        print(permutation)
        setting = prepare_setting(permutation)
        if setting not in all_settings:
            all_settings.append(setting)

    for setting in all_settings:
        print(setting)

    return all_settings


def deduce_row(row, possible_rows, m):
    global BOARD, QUEUE

    possibilities = possible_rows[row]
    new_possibilities = possibilities.copy()

    board_row = BOARD[row]
    for i in range(m):
        if board_row[i] != 0:
            for j in range(len(possibilities)):
                # usuwamy błędne możliwości
                if possibilities[j][i] != board_row[i] and possibilities[j] in new_possibilities:
                    new_possibilities.remove(possibilities[j])

    possible_rows[row] = new_possibilities

    for i in range(m):
        white = 0
        black = 0
        for poss in new_possibilities:
            if poss[i] == WHITE:
                white += 1
            elif poss[i] == BLACK:
                black += 1

        # pole musi być czarne
        if BOARD[row][i] == 0 and black == len(new_possibilities):
            BOARD[row][i] = BLACK
            QUEUE.put(('row', i))

        # pole musi być białe
        if BOARD[row][i] == 0 and white == len(new_possibilities):
            BOARD[row][i] = WHITE
            QUEUE.put(('row', i))

    return possible_rows


def get_column(col):
    return [row[col] for row in BOARD]


def deduce_col(col, possible_cols, n):
    global BOARD, QUEUE

    possibilities = possible_cols[col]
    new_possibilities = possibilities.copy()

    board_column = get_column(col)
    for i in range(n):
        if board_column[i] != 0:
            for j in range(len(possibilities)):
                # usuwamy błędne możliwości
                if possibilities[j][i] != board_column[i] and possibilities[j] in new_possibilities:
                    new_possibilities.remove(possibilities[j])

    possible_cols[col] = new_possibilities

    for i in range(n):
        white = 0
        black = 0
        for poss in new_possibilities:
            if poss[i] == WHITE:
                white += 1
            if poss[i] == BLACK:
                black += 1

        # pole musi być czarne
        if BOARD[i][col] == 0 and black == len(new_possibilities):
            BOARD[i][col] = BLACK
            QUEUE.put(('col', i))

        # pole musi byc białe
        if BOARD[i][col] == 0 and white == len(new_possibilities):
            BOARD[i][col] = WHITE
            QUEUE.put(('col', i))

    return possible_cols


def print_board(n, m):
    res = ""
    for i in range(n):
        for j in range(m):
            if BOARD[i][j] == BLACK:
                res += '#'
            else:
                res += '.'
        res += "\n"

    return res


def solve(rows, cols, n, m):
    global BOARD, QUEUE
    BOARD = [[0] * m for _ in range(n)]

    print(rows)

    # wszystkie możliwe ustawienia klocków dla rzędów i kolumn
    possible_rows = [find_all_settings(m, filling) for filling in rows]
    pprint(possible_rows)
    possible_cols = [find_all_settings(n, filling) for filling in cols]
    pprint(possible_cols)

    QUEUE = Queue()
    for i in range(n):
        QUEUE.put(('col', i))  # i-ta kolumna
    for j in range(m):
        QUEUE.put(('row', j))  # j-ty wiersz

    while not QUEUE.empty():
        (what, i) = QUEUE.get()

        if what == 'row':
            possible_cols = deduce_col(i, possible_cols, n)
        elif what == 'col':
            possible_rows = deduce_row(i, possible_rows, m)

    return print_board(n, m)


if __name__ == '__main__':
    n, m = -1, -1
    desc = []
    rows = []
    columns = []
    with open('zad1_input.txt', 'r') as input:
        input = input.readlines()
        n, m = [int(x) for x in input[0].split()]
        desc = [[int(x) for x in line.split()] for line in input[1:]]

    rows = desc[:n]
    columns = desc[n:]

    with open('zad1_output.txt', 'w') as output:
        output.write(solve(rows, columns, n, m))
