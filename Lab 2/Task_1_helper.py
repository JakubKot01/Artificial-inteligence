VERBOSE = False


def opt_dist(nums: list[int], goal: list[int]) -> int:
    results: list[int] = []

    for start_index in range(len(nums)):
        current_result: int = 0
        current_goal: list[int] = goal.copy()
        current_nums: list[int] = [0] * len(nums)
        ones_to_change = 0

        for i in range(start_index, len(nums)):
            if nums[i] == 0 and sum(current_goal) > 0:
                current_result += 1
                current_nums[i] = 1
                if len(current_goal) > 1:
                    current_goal[0] -= 1
            elif nums[i] == 1 and sum(current_goal) > 0:
                current_goal[0] -= 1
                current_nums[i] = 1
            elif nums[i] == 1 and sum(current_goal) == 0:
                current_result += 1
                current_nums[i] = 0
            elif nums[i] == 0 and sum(current_goal) == 0:
                current_result += 1

        current_result += ones_to_change
        ones_to_change += nums[start_index]

        if sum(current_goal) == 0:
            results.append(current_result)

    if results:
        return min(results)
    else:
        return float('inf')  # Zwróć nieskończoność, jeśli lista wyników jest pusta


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
