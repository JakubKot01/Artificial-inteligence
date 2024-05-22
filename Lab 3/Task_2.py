from queue import Queue

WHITE = "."
BLACK = "#"
BOARD = None
POSSIBLE_ROWS = None
POSSIBLE_COLS = None
QUEUE = None


def generate_possibilities(setting, number_of_elements):
    result = []

    if number_of_elements == 0:
        return [[]]
    elif len(setting) == 0:  # No blocks left to set - return empty setting
        return [[WHITE] * number_of_elements]

    # Add white space at the beginning if possible
    if sum(setting) + len(setting) - 1 < number_of_elements:
        result += [[WHITE] + remainder for remainder in generate_possibilities(setting, number_of_elements - 1)]

    # first block
    block_of_ones = [BLACK for _ in range(setting[0])]
    new_n = number_of_elements - setting[0]

    # if have more than one block - add white space
    if len(setting) > 1:
        block_of_ones += [WHITE]
        new_n -= 1

    result += [block_of_ones + remainder for remainder in generate_possibilities(setting[1:], new_n)]

    # print("RESULT: ", result)
    return result


def print_board():
    global BOARD
    res = ""
    for i in range(number_of_rows):
        for j in range(number_of_cols):
            if BOARD[i][j] == BLACK:
                res += '#'
            else:
                res += '.'
        res += "\n"

    return res


def get_column(col):
    global BOARD
    return [row[col] for row in BOARD]


def deduce_col(col):
    global BOARD, QUEUE, POSSIBLE_COLS

    possibilities = POSSIBLE_COLS[col]

    if len(possibilities) == 0:
        return False

    new_possibilities = possibilities.copy()
    board_column = get_column(col)

    for i in range(number_of_rows):
        if board_column[i] != 0:
            for j in range(len(possibilities)):
                # Delete possibilities that not meet expectations
                if possibilities[j][i] != board_column[i] and possibilities[j] in new_possibilities:
                    new_possibilities.remove(possibilities[j])

    if len(new_possibilities) == 0:
        return False

    POSSIBLE_COLS[col] = new_possibilities

    for i in range(number_of_rows):
        white = 0
        black = 0

        for possibility in new_possibilities:
            if possibility[i] == WHITE:
                white += 1
            if possibility[i] == BLACK:
                black += 1

        # Field has to be black (filled)
        if BOARD[i][col] == 0 and black == len(new_possibilities):
            BOARD[i][col] = BLACK
            QUEUE.put(('col', i))

        # Field has to be white (empty)
        if BOARD[i][col] == 0 and white == len(new_possibilities):
            BOARD[i][col] = WHITE
            QUEUE.put(('col', i))

    return True


def deduce_row(row):
    global BOARD, QUEUE, POSSIBLE_ROWS

    possibilities = POSSIBLE_ROWS[row]
    if len(possibilities) == 0:
        return False

    new_possibilities = possibilities.copy()
    board_row = BOARD[row]

    for i in range(number_of_cols):
        if board_row[i] != 0:
            for j in range(len(possibilities)):
                # Delete settings that not meet expectations
                if possibilities[j][i] != board_row[i] and possibilities[j] in new_possibilities:
                    new_possibilities.remove(possibilities[j])

    if len(new_possibilities) == 0:
        return False

    POSSIBLE_ROWS[row] = new_possibilities

    for i in range(number_of_cols):
        white = 0
        black = 0
        for poss in new_possibilities:
            if poss[i] == WHITE:
                white += 1
            elif poss[i] == BLACK:
                black += 1

        # Field has to be black (filled)
        if BOARD[row][i] == 0 and black == len(new_possibilities):
            BOARD[row][i] = BLACK
            QUEUE.put(('row', i))

        # Field has to be white (empty)
        if BOARD[row][i] == 0 and white == len(new_possibilities):
            BOARD[row][i] = WHITE
            QUEUE.put(('row', i))

    return True


def deduce(op, i):
    if op == 'row':
        return deduce_col(i)
    if op == 'col':
        return deduce_row(i)


def solution_found():
    global BOARD

    for i in range(number_of_rows):
        for j in range(number_of_cols):
            if BOARD[i][j] == 0:
                return False
    return True


def find_free_box():
    for i in range(number_of_rows):
        for j in range(number_of_cols):
            if BOARD[i][j] == 0:
                return i, j


def backtrack():
    global QUEUE, POSSIBLE_COLS, POSSIBLE_ROWS, BOARD

    prev_board = [x[:] for x in BOARD]
    prev_cols = [x[:] for x in POSSIBLE_COLS]
    prev_rows = [x[:] for x in POSSIBLE_ROWS]

    x, y = find_free_box()

    BOARD[x][y] = BLACK
    QUEUE.put(('col', x))
    QUEUE.put(('row', y))

    if solve():
        with open('zad_output.txt', mode='w') as out_file:
            out_file.write(print_board())
    else:
        BOARD = prev_board
        POSSIBLE_COLS = prev_cols
        POSSIBLE_ROWS = prev_rows

        BOARD[x][y] = WHITE
        QUEUE.put(('col', x))
        QUEUE.put(('row', y))

        solve()


def solve():
    global QUEUE

    while True:
        if not QUEUE.empty():
            (op, i) = QUEUE.get()
            if not deduce(op, i):
                return False

        elif solution_found():
            return True

        else:
            backtrack()


if __name__ == '__main__':
    """
    n - number_of_rows
    m - number_of_cols
    """
    global number_of_rows, number_of_cols
    description = []
    rows = []
    columns = []
    with open('zad_input.txt', 'r') as input:
        input = input.readlines()
        number_of_rows, number_of_cols = [int(x) for x in input[0].split()]
        description = [[int(x) for x in line.split()] for line in input[1:]]

    rows = description[:number_of_rows]
    columns = description[number_of_rows:]

    BOARD = [[0] * number_of_cols for _ in range(number_of_rows)]

    POSSIBLE_COLS = [generate_possibilities(filling, number_of_rows) for filling in columns]
    POSSIBLE_ROWS = [generate_possibilities(filling, number_of_cols) for filling in rows]
    QUEUE = Queue()

    for i in range(number_of_rows):
        QUEUE.put(('col', i))
    for j in range(number_of_cols):
        QUEUE.put(('row', j))

    if solve():
        with open('zad_output.txt', 'w') as output:
            output.write(print_board())
