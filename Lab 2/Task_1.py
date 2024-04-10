import random
from pprint import pprint
from Task_1_helper import opt_dist


VERBOSE = False


def get_column(board, col_index):
    return [row[col_index] for row in board]


def is_completed(rows, cols):
    is_rows_completed = all(row == 1 for row in rows)
    is_cols_completed = all(col == 1 for col in cols)
    return is_rows_completed and is_cols_completed


def get_random_row(completed_rows, number_of_rows):
    if all(row == 1 for row in completed_rows):
        if VERBOSE:
            print("switched")
        return -1
    random_row = random.randint(0, number_of_rows - 1)
    while completed_rows[random_row] == 1:
        random_row = random.randint(0, number_of_rows - 1)

    return random_row


def get_random_col(completed_cols, number_of_cols):
    if all(col == 1 for col in completed_cols):
        return -1
    random_col = random.randint(0, number_of_cols - 1)
    while completed_cols[random_col] == 1:
        random_col = random.randint(0, number_of_cols - 1)
    return random_col


def get_best_modification(number_of_cols,
                          row_index,
                          col_index,
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
        if VERBOSE:
            print(f'\rRandom value: {random_value}', end="")
        new_board = [row[:] for row in board]
        if col_index == -1:
            col_index = random.randint(0, number_of_cols - 1)
        elif row_index == -1:
            row_index = random.randint(0, number_of_rows - 1)

        new_board[row_index][col_index] = 1 - new_board[row_index][col_index]
        row_result = opt_dist(board[row_index], rows_desc[row_index])
        col_result = opt_dist(get_column(board, col_index), cols_desc[col_index])

        new_row_result = opt_dist(new_board[row_index], rows_desc[row_index])
        new_col_result = opt_dist(get_column(new_board, col_index), cols_desc[col_index])

        if row_result > new_row_result or col_result > new_col_result:
            return best_change, counter + 1

    if counter >= 100:
        new_board = []
        for _ in range(number_of_rows):
            row = [random.choice([0, 1]) for _ in range(number_of_cols)]
            new_board.append(row)
        return new_board, 0

    if col_index == -1:
        for col_index in range(number_of_cols):
            new_board = [row[:] for row in board]
            new_board[row_index][col_index] = 1 - new_board[row_index][col_index]

            row_result = opt_dist(board[row_index], rows_desc[row_index])
            col_result = opt_dist(get_column(board, col_index), cols_desc[col_index])

            new_row_result = opt_dist(new_board[row_index], rows_desc[row_index])
            new_col_result = opt_dist(get_column(new_board, col_index), cols_desc[col_index])

            new_result = (row_result - new_row_result) + (col_result - new_col_result)

            if new_result > best_result:
                if VERBOSE:
                    print(f'Old result: {row_result, col_result}, New result: {new_row_result, new_col_result}')

                best_result = new_result
                best_change = [row[:] for row in new_board]

    elif row_index == -1:
        for row_index in range(number_of_rows):
            new_board = [row[:] for row in board]
            new_board[row_index][col_index] = 1 - new_board[row_index][col_index]

            row_result = opt_dist(board[row_index], rows_desc[row_index])
            col_result = opt_dist(get_column(board, col_index), cols_desc[col_index])

            new_row_result = opt_dist(new_board[row_index], rows_desc[row_index])
            new_col_result = opt_dist(get_column(new_board, col_index), cols_desc[col_index])

            new_result = (row_result - new_row_result) + (col_result - new_col_result)

            if new_result >= best_result:
                if VERBOSE:
                    print(f'Old result: {row_result, col_result}, New result: {new_row_result, new_col_result}')

                best_result = new_result
                best_change = [row[:] for row in new_board]

    return best_change, counter


def update_completion(board, rows_desc, cols_desc, number_of_rows, number_of_cols):
    updated_completed_rows = []
    updated_completed_cols = []
    for i in range(number_of_rows):
        if opt_dist(board[i], rows_desc[i]) == 0:
            updated_completed_rows.append(1)
        else:
            updated_completed_rows.append(0)

    for i in range(number_of_cols):
        if opt_dist(get_column(board, i), cols_desc[i]) == 0:
            updated_completed_cols.append(1)
        else:
            updated_completed_cols.append(0)

    return updated_completed_rows, updated_completed_cols


def solve(completed_rows, completed_cols, board, number_of_rows, number_of_cols, rows_desc, cols_desc):
    counter = 0
    while not is_completed(completed_rows, completed_cols):
        chosen_row = -1
        chosen_col = -1
        chosen_row = get_random_row(completed_rows, number_of_rows)

        if chosen_row == -1:
            chosen_col = get_random_col(completed_cols, number_of_cols)

        best_change, counter = get_best_modification(number_of_cols,
                                                     chosen_row,
                                                     chosen_col,
                                                     board,
                                                     counter,
                                                     rows_desc,
                                                     cols_desc,
                                                     completed_rows,
                                                     completed_cols,
                                                     possibility=1)

        if board == best_change:
            counter += 1
        else:
            board = [row[:] for row in best_change]
            if VERBOSE:
                print(f'Result improved')
                pprint(board)
            counter = 0

        completed_rows, completed_cols = update_completion(board, rows_desc, cols_desc, number_of_rows, number_of_cols)

        if VERBOSE:
            print(f'rows and cols description: {rows_desc, cols_desc}')
            print(f'completed rows and cols: {completed_rows, completed_cols}')

    return board


def find_all_settings(number_of_elements, descriptions):
    def generate_configurations(number_of_elements, descriptions, current_configuration, start_position):
        if not descriptions:
            if len(current_configuration) == number_of_elements:
                configurations.append(current_configuration.copy())
            return

        for block_size in range(descriptions[0], number_of_elements - sum(descriptions[1:]) - len(descriptions) + 1):
            new_configuration = current_configuration + ['#' * block_size]
            next_position = start_position + block_size + 1
            if len(descriptions) > 1:
                new_configuration.append('.')
                next_position += 1
            generate_configurations(number_of_elements, descriptions[1:], new_configuration, next_position)

    configurations = []
    generate_configurations(number_of_elements, descriptions, [], 0)
    print("\n\n\n")
    pprint(configurations)
    return configurations


if __name__ == '__main__':
    input_file_path = "zad1_input.txt"
    output_file_path = "zad1_output.txt"
    input_file = open(input_file_path, 'r', encoding='utf-8')
    output_file = open(output_file_path, 'w', encoding='utf-8')

    first_line = input_file.readline().split()
    number_of_rows = int(first_line[0])
    number_of_cols = int(first_line[1])

    rows_desc = []
    cols_desc = []
    for i in range(number_of_rows):
        rows_desc.append([int(x) for x in input_file.readline().strip().split()])
    for i in range(number_of_cols):
        cols_desc.append([int(x) for x in input_file.readline().strip().split()])

    print(f"rows_desc: {rows_desc}, cols_desc: {cols_desc}")

    initial_board = [[0] * number_of_cols for _ in range(number_of_rows)]

    completed_rows, completed_cols = update_completion(initial_board, rows_desc, cols_desc, number_of_rows,
                                                       number_of_cols)

    rows_combinations = [[]] * number_of_rows
    cols_combinations = [[]] * number_of_cols

    for counter, row_desc in enumerate(rows_desc):
        rows_combinations[counter] = find_all_settings(number_of_cols, row_desc)

    """
    print(f"Completed rows: {completed_rows}, completed cols: {completed_cols}")

    solution_board = solve(completed_rows, completed_cols, initial_board, number_of_rows, number_of_cols,
                           rows_desc, cols_desc)

    pprint(solution_board)

    for row in solution_board:
        output_file.write(''.join(['#' if cell == 1 else '.' for cell in row]) + '\n')
    """
