import time
import numpy
import random


memo = {}


def split_text(text: str, polish_words_list: set[str], logs_file, offset: str) -> tuple[int, str]:
    global memo
    print(f'{offset} starting call')
    print(f'{offset} text: {text}')
    if text in memo:
        return memo[text]

    if text in polish_words_list:
        memo[text] = (1, text)
        return 1, text
    elif len(text) <= 1:
        memo[text] = (0, text)
        return 0, text

    current_score = 0
    new_text = ''

    index_set = list()

    for i in range(len(text)):
        index_set.append(i)

    random_index = random.choice(index_set)

    # print(f'{offset} random index: {random_index}, text: {text}, length: {len(text)}')

    while current_score == 0 and index_set:

        left_score, left_text = split_text(text[:random_index], polish_words_list, logs_file, offset + " X")
        right_score, right_text = split_text(text[random_index:], polish_words_list, logs_file, offset + " X")
        new_text = left_text + " " + right_text
        if left_score != 0 and right_score != 0:
            current_score = 1

        # print(f'text: {text}')
        # print(f'{offset} {left_text, right_text}, table: {index_set}, random index : {random_index}, length: {len(text)}')

        index_set.remove(random_index)

        random_index = random.choice(index_set)

        """
        random_offset = numpy.random.randint(-3, 3)
        if random_offset < 0:
            random_index = max(random_index + random_offset, 1)
        else:
            random_index = min(random_index + random_offset, len(text) - 1)
        """

    return current_score, new_text


def reconstruct_text(input_file_path: str, output_file_path: str, logs_file_path: str, polish_words_list: set[str]):
    input_file = open(input_file_path, 'r', encoding='utf-8')
    output_file = open(output_file_path, 'w', encoding='utf-8')
    logs_file = open(logs_file_path, 'w', encoding='utf-8')
    for line in input_file:
        print(line)
        line = line.strip()
        reconstructed_line = split_text(line, polish_words_list, logs_file, "")
        output_file.write(reconstructed_line[1].strip() + '\n')


if __name__ == '__main__':
    start_time = time.time()
    polish_words_file = open('polish_words.txt', 'r', encoding='utf-8')
    polish_words = set(word.strip() for word in polish_words_file)

    reconstruct_text('zad2_input.txt',
                     'zad2_output.txt',
                     'zad2_logs.txt',
                     polish_words)
    print(f"Execution time: {time.time() - start_time} seconds")
