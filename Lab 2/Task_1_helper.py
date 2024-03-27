VERBOSE = False


def opt_dist(nums: list[int], goal: int) -> int:
    results: list[int] = list()
    if VERBOSE:
        print(f'{nums}\n')
    ones_to_change = 0
    for i in range(len(nums)):
        current_result: int = 0
        current_goal: int = goal
        current_nums: list[int] = [0] * len(nums)

        for j in range(i, len(nums)):

            if nums[j] == 0 and current_goal > current_result:
                current_result += 1
                current_nums[j] = 1
            elif nums[j] == 1 and current_goal > current_result:
                current_goal -= 1
                current_nums[j] = 1
            elif nums[j] == 1 and current_goal <= current_result:
                current_result += 1
                current_nums[j] = 0
        current_result += ones_to_change
        if nums[i] == 1:
            ones_to_change += 1
        if VERBOSE:
            print(current_nums, ones_to_change, current_result, current_goal)

        if current_result >= current_goal:
            results.append(current_result)
    return min(results)


if __name__ == '__main__':
    input_file = open("zad4_input.txt", 'r', encoding='utf-8')
    output_file = open("zad4_output.txt", 'w', encoding='utf-8')
    for line in input_file:
        split_line = line.split(" ")
        input = []
        for char in split_line[0]:
            input.append(int(char))
        result = opt_dist(input, int(split_line[1]))
        output_file.write(str(result) + '\n')
    # print(f'test: {opt_dist([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 5)}')  # 3
    # print(f'test: {opt_dist([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 4)}')  # 4
    # print(f'test: {opt_dist([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 3)}')  # 3
    # print(f'test: {opt_dist([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 2)}')  # 2
    # print(f'test: {opt_dist([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 1)}')  # 1
    # print(f'test: {opt_dist([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 0)}')  # 2
    # print(f'test: {opt_dist([0, 0, 1, 1, 1, 1, 1, 0, 0, 0], 5)}')  # 0
    # print(f'test: {opt_dist([0, 0, 1, 1, 0, 1, 1, 0, 0, 0], 3)}')  # 3
