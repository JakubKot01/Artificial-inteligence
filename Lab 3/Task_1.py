from queue import Queue

WHITE = "."
BLACK = "#"
BOARD = []
QUEUE = Queue()


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


def deduce_row(row, possible_rows, number_of_cols):
    global BOARD, QUEUE

    possibilities = possible_rows[row]
    new_possibilities = possibilities.copy()

    board_row = BOARD[row]
    for i in range(number_of_cols):
        if board_row[i] != 0:
            for j in range(len(possibilities)):
                # Delete settings that not meet expectations
                if possibilities[j][i] != board_row[i] and possibilities[j] in new_possibilities:
                    new_possibilities.remove(possibilities[j])

    possible_rows[row] = new_possibilities

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

    return possible_rows


def get_column(col):
    return [row[col] for row in BOARD]


def deduce_col(col, possible_cols, number_of_rows):
    global BOARD, QUEUE

    possibilities = possible_cols[col]
    new_possibilities = possibilities.copy()

    board_column = get_column(col)
    for i in range(number_of_rows):
        if board_column[i] != 0:
            for j in range(len(possibilities)):
                # Delete possibilities that not meet expectations
                if possibilities[j][i] != board_column[i] and possibilities[j] in new_possibilities:
                    new_possibilities.remove(possibilities[j])

    possible_cols[col] = new_possibilities

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

    return possible_cols


def print_board(number_of_rows, number_of_cols):
    res = ""
    for i in range(number_of_rows):
        for j in range(number_of_cols):
            if BOARD[i][j] == BLACK:
                res += '#'
            else:
                res += '.'
        res += "\n"

    return res


def solve(rows, cols, number_of_rows, number_of_cols):
    global BOARD, QUEUE
    BOARD = [[0] * number_of_cols for _ in range(number_of_rows)]

    # Generate all possible settings for all rows and cols
    possible_rows = [generate_possibilities(setting, number_of_cols) for setting in rows]
    possible_cols = [generate_possibilities(setting, number_of_rows) for setting in cols]

    QUEUE = Queue()

    for i in range(number_of_rows):
        QUEUE.put(('col', i))  # i-col
    for j in range(number_of_cols):
        QUEUE.put(('row', j))  # j-row

    while not QUEUE.empty():
        (what, i) = QUEUE.get()
        # print(what, i)

        if what == 'row':
            possible_cols = deduce_col(i, possible_cols, number_of_rows)
        elif what == 'col':
            possible_rows = deduce_row(i, possible_rows, number_of_cols)

    return print_board(number_of_rows, number_of_cols)


if __name__ == '__main__':
    number_of_rows, number_of_cols = -1, -1
    desc = []
    rows = []
    columns = []
    with open('zad_input.txt', 'r') as input:
        input = input.readlines()
        number_of_rows, number_of_cols = [int(x) for x in input[0].split()]
        desc = [[int(x) for x in line.split()] for line in input[1:]]

    rows = desc[:number_of_rows]
    columns = desc[number_of_rows:]

    with open('zad_output.txt', 'w') as output:
        output.write(solve(rows, columns, number_of_rows, number_of_cols))
