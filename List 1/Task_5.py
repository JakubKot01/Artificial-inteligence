import random
from pprint import pprint
from Task_4 import opt_dist

VERBOSE = False


def get_column(board, col_index):
    return [row[col_index] for row in board]


def is_completed(rows, cols):
    is_rows_completed = all(row == 1 for row in rows)
    is_cols_completed = all(col == 1 for col in cols)
    return is_rows_completed and is_cols_completed


def get_random_row(completed_rows, number_of_rows):
    random_row = random.randint(0, number_of_rows - 1)
    while completed_rows[random_row] == 1:
        random_row = random.randint(0, number_of_rows - 1)

    return random_row


def get_best_modification(number_of_cols,
                          row_index,
                          board,
                          counter,
                          rows_desc,
                          cols_desc,
                          completed_rows,
                          completed_cols,
                          possibility=1):
    best_result = 0
    best_change = board

    random_value = random.randint(0, 100)

    if random_value <= possibility:
        print(f'\rRandom value: {random_value}', end="")
        new_board = [row[:] for row in board]
        random_column = random.randint(0, number_of_cols - 1)
        new_board[row_index][random_column] = 1 - new_board[row_index][random_column]
        row_result = opt_dist(board[row_index], rows_desc[row_index])
        col_result = opt_dist(get_column(board, random_column), cols_desc[random_column])

        new_row_result = opt_dist(new_board[row_index], rows_desc[row_index])
        new_col_result = opt_dist(get_column(new_board, random_column), cols_desc[random_column])

        if row_result > new_row_result or col_result > new_col_result:

            rows_desc[row_index] = int(new_row_result == 0)
            cols_desc[random_column] = int(new_col_result == 0)

            return best_change, counter + 1, completed_rows, completed_cols

    if counter >= 25:
        new_board = []
        for _ in range(number_of_rows):
            row = [random.choice([0, 1]) for _ in range(number_of_cols)]
            new_board.append(row)
        return new_board, 0, completed_rows, completed_cols

    for column_index in range(number_of_cols):
        new_board = [row[:] for row in board]
        new_board[row_index][column_index] = 1 - new_board[row_index][column_index]

        row_result = opt_dist(board[row_index], rows_desc[row_index])
        col_result = opt_dist(get_column(board, column_index), cols_desc[column_index])

        new_row_result = opt_dist(new_board[row_index], rows_desc[row_index])
        new_col_result = opt_dist(get_column(new_board, column_index), cols_desc[column_index])

        new_result = (row_result - new_row_result) + (col_result - new_col_result)

        if new_result > best_result:
            print(f'Old result: {row_result, col_result}, New result: {new_row_result, new_col_result}')

            completed_rows[row_index] = int(new_row_result == 0)
            completed_cols[column_index] = int(new_col_result == 0)

            print(completed_rows, completed_cols)

            if new_col_result == 0:
                cols_desc[column_index] = 1
            else:
                cols_desc[column_index] = 0

            best_result = new_result
            best_change = [row[:] for row in new_board]

    return best_change, counter, completed_rows, completed_cols


def update_completion(rows_desc, cols_desc):
    updated_completed_rows = [1 if row == 0 else 0 for row in rows_desc]
    updated_completed_cols = [1 if col == 0 else 0 for col in cols_desc]

    return updated_completed_rows, updated_completed_cols


def solve(completed_rows, completed_cols, board, number_of_rows, number_of_cols, rows_desc, cols_desc):
    counter = 0
    while not is_completed(completed_rows, completed_cols):
        random_row = get_random_row(completed_rows, number_of_rows)

        best_change, counter, completed_rows, completed_cols = get_best_modification(number_of_cols,
                                                                           random_row,
                                                                           board,
                                                                           counter,
                                                                           rows_desc,
                                                                           cols_desc,
                                                                           completed_rows,
                                                                           completed_cols,
                                                                           possibility=1)

        print(completed_rows, completed_cols)

        if board == best_change:
            counter += 1
        else:
            print(f'Result improved')
            pprint(board)
            pprint(best_change)

        board = [row[:] for row in best_change]

        # completed_rows, completed_cols = update_completion(rows_desc, cols_desc)

        if VERBOSE:
            pprint(best_change)

    return board


if __name__ == '__main__':
    input_file_path = "zad5_input.txt"
    output_file_path = "zad5_output.txt"
    input_file = open(input_file_path, 'r', encoding='utf-8')
    output_file = open(output_file_path, 'w', encoding='utf-8')

    first_line = input_file.readline().split()
    number_of_rows = int(first_line[0])
    number_of_cols = int(first_line[1])

    rows_desc = []
    cols_desc = []
    for i in range(number_of_rows):
        rows_desc.append(int(input_file.readline().strip()))
    for i in range(number_of_cols):
        cols_desc.append(int(input_file.readline().strip()))

    print(f"rows_desc: {rows_desc}, cols_desc: {cols_desc}")

    completed_rows = [1 if row == 0 else 0 for row in rows_desc]
    completed_cols = [1 if col == 0 else 0 for col in cols_desc]

    print(f"Completed rows: {completed_rows}, completed cols: {completed_cols}")

    initial_board = [[0] * number_of_cols for _ in range(number_of_rows)]
    solution_board = solve(completed_rows, completed_cols, initial_board, number_of_rows, number_of_cols,
                           rows_desc, cols_desc)

    pprint(solution_board)

    for row in solution_board:
        output_file.write(''.join(['#' if cell == 1 else '.' for cell in row]) + '\n')
