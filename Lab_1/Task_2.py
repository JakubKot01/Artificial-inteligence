import time


def calculate_score(text):
    words = text.split()
    return sum(pow(len(word), 2) for word in words)


def split_text(text: str, polish_words_list: set[str], logs_file, memo: dict) -> tuple[int, str]:
    if text in memo:
        return memo[text]

    if text in polish_words_list:
        score = calculate_score(text)
        memo[text] = (score, text)
        return score, text
    elif len(text) == 1 and text in polish_words_list:
        memo[text] = (1, text)
        return 1, text
    elif len(text) <= 1:
        memo[text] = (0, text)
        return 0, text

    best_score: int = 0
    best_split: str = ""
    for i in range(1, len(text)):
        left_score, left_text = split_text(text[:i], polish_words_list, logs_file, memo)
        right_score, right_text = split_text(text[i:], polish_words_list, logs_file, memo)
        if left_score + right_score > best_score \
                and left_score != 0 and right_score != 0:
            best_score = left_score + right_score
            best_split = left_text + " " + right_text

    memo[text] = (best_score, best_split)
    return best_score, best_split


def reconstruct_text(input_file_path: str, output_file_path: str, logs_file_path: str, polish_words_list: set[str]):
    input_file = open(input_file_path, 'r', encoding='utf-8')
    output_file = open(output_file_path, 'w', encoding='utf-8')
    logs_file = open(logs_file_path, 'w', encoding='utf-8')
    for line in input_file:
        line = line.strip()
        reconstructed_line = split_text(line, polish_words_list, logs_file, {})
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
