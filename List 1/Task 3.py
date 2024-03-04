def opt_dist(nums, D):
    results: list[int] = list()
    for i in range(len(nums)):
        current_result: int = 0
        current_limit: int = D
        print(f'\ncurrent result: {current_result}, current limit: {current_limit}')
        for j in range(i, len(nums)):
            print(f'num: {nums[j]}, j: {j}', end="\t")
            if nums[j] == 0 and current_result <= current_limit:
                current_result += 1
            elif nums[j] == 1:
                current_limit -= 1
        print(f'\ncurrent result: {current_result}, current limit: {current_limit}')
        if current_result == current_limit:
            results.append(current_result)

    return min(results)


if __name__ == '__main__':
    print(f'test: {opt_dist([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 5)}')  # 3
    print(f'test: {opt_dist([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 4)}')  # 4
    print(f'test: {opt_dist([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 3)}')  # 3
    print(f'test: {opt_dist([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 2)}')  # 2
    print(f'test: {opt_dist([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 1)}')  # 1
    print(f'test: {opt_dist([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 0)}')  # 2
