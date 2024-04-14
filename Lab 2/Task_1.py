import random
from pprint import pprint
from Task_1_helper import opt_dist


VERBOSE = False

class Setting:
    def __init__(self, elements, breaks):
        self.elements = elements
        self.breaks = breaks


def find_all_settings(number_of_elements, descriptions):
    result = []
    number_of_blocks = len(descriptions)
    number_of_breaks = len(descriptions) - 1
    summary_number_of_filled_fields = 0
    index = 0
    table = []
    breaks_indexes = [0]
    for counter in range(number_of_breaks + number_of_blocks):
        if counter % 2 == 0:
            for i in range(descriptions[counter // 2]):
                summary_number_of_filled_fields += 1
                table.append("#")
                index += 1
        else:
            breaks_indexes.append(index)
            table.append(".")
            index += 1

    result.append(table)

    number_of_left_fields = number_of_elements - (summary_number_of_filled_fields + number_of_breaks)
    if number_of_left_fields != 0:
        for i in range(number_of_left_fields):
            table.append(".")

    for cut_items in range(1, number_of_left_fields + 1):
        print("\n", cut_items, "\n")
        current_table = table[:-cut_items].copy()
        for break_number, add_index in enumerate(breaks_indexes):
            for i in range(cut_items):
                current_add_table = current_table.copy()
                current_add_table.insert(add_index, ".")
                for j in range(cut_items):
                    current_added_items = i + j
                    print(current_added_items, end=" ")
                    for k in range(break_number + 1, len(breaks_indexes)):
                        if cut_items - current_added_items > 0:
                            print(f'adding in : {breaks_indexes[k] + current_added_items}')
                            current_add_table.insert(breaks_indexes[k] + current_added_items, ".")
                print(current_add_table)
                result.append(current_add_table)

    print("\n\n\n")
    for table in result:
        print(table)
    return result


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

    rows_combinations = [[]] * number_of_rows
    cols_combinations = [[]] * number_of_cols

    rows_combinations[4] = find_all_settings(number_of_cols, rows_desc[4])

    # for counter, row_desc in enumerate(rows_desc):
    #     rows_combinations[counter] = find_all_settings(number_of_cols, row_desc)

    """
    print(f"Completed rows: {completed_rows}, completed cols: {completed_cols}")

    solution_board = solve(completed_rows, completed_cols, initial_board, number_of_rows, number_of_cols,
                           rows_desc, cols_desc)

    pprint(solution_board)

    for row in solution_board:
        output_file.write(''.join(['#' if cell == 1 else '.' for cell in row]) + '\n')
    """
