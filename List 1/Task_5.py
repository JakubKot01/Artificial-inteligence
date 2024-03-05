import random
from pprint import pprint
from Task_4 import opt_dist


def get_column(board, col_index):
    return [row[col_index] for row in board]


def is_completed(rows, cols):
    is_rows_completed = all(row == 1 for row in rows)
    is_cols_completed = all(col == 1 for col in cols)
    return is_rows_completed and is_cols_completed


def solve(completed_rows, completed_cols, board, number_of_rows, number_of_cols, rows_desc, cols_desc):
    if is_completed(completed_rows, completed_cols):
        return board, number_of_rows, number_of_cols
    i = random.randint(0, number_of_rows - 1)
    while completed_rows[i] == 1:
        i = random.randint(0, number_of_rows - 1)

    best_result = 0
    best_change = board
    for j in range(number_of_cols):
        new_board = [row[:] for row in board]
        new_board[i][j] = 1 - new_board[i][j]
        row_result = opt_dist(new_board[i], rows_desc[i])
        col_result = opt_dist(get_column(new_board, j), cols_desc[j])
        new_row_result = opt_dist(board[i], rows_desc[i])
        new_col_result = opt_dist(get_column(board, j), cols_desc[j])
        new_result = (row_result - new_row_result) + (col_result - new_col_result)
        if new_result > best_result:
            best_result = new_result
            best_change = new_board

    pprint(best_change)

    return solve(completed_rows, completed_cols, best_change, number_of_rows, number_of_cols, rows_desc, cols_desc)


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

    completed_rows = [1 if row == 0 else 0 for row in rows_desc]
    completed_cols = [1 if col == 0 else 0 for col in cols_desc]

    initial_board = [[0] * number_of_cols for _ in range(number_of_rows)]
    solution_board, _, _ = solve(completed_rows, completed_cols, initial_board, number_of_rows, number_of_cols,
                                  rows_desc, cols_desc)

    pprint(solution_board)

    for row in solution_board:
        output_file.write(''.join(['#' if cell == 1 else '.' for cell in row]) + '\n')
