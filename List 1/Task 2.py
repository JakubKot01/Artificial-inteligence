def calculate_score(text):
    words = text.split()
    return sum(pow(len(word), 2) for word in words)


def split_text(text: str, polish_words_list: set[str], logs_file) -> tuple[int, str]:
    if text in polish_words_list:
        score = pow(len(text), 2)
        return score, text

    if len(text) == 1:
        return 0, ""

    best_score = 0
    best_partition = ""

    for i in range(1, len(text)):
        left_part = text[:i]
        right_part = text[i:]

        if left_part in polish_words_list:
            left_score, left_partition = split_text(right_part, polish_words_list, logs_file)
            current_score = pow(len(left_part), 2) + left_score

            if current_score > best_score:
                best_score = current_score
                best_partition = left_part + " " + left_partition

        if right_part in polish_words_list:
            right_score, right_partition = split_text(left_part, polish_words_list, logs_file)
            current_score = pow(len(right_part), 2) + right_score

            if current_score > best_score:
                best_score = current_score
                best_partition = right_partition + " " + right_part

    return best_score, best_partition


def reconstruct_text(input_file_path: str, output_file_path: str, logs_file_path: str, polish_words_list: set[str]):
    input_file = open(input_file_path, 'r', encoding='utf-8')
    output_file = open(output_file_path, 'w', encoding='utf-8')
    logs_file = open(logs_file_path, 'w', encoding='utf-8')
    for line in input_file:
        print(line)
        line = line.strip()
        reconstructed_line = split_text(line, polish_words_list, logs_file)
        output_file.write(reconstructed_line[1].strip() + '\n')


if __name__ == '__main__':
    polish_words_file = open('polish_words.txt', 'r', encoding='utf-8')
    polish_words = set(word.strip() for word in polish_words_file)

    reconstruct_text('zad2_input.txt',
                     'zad2_output.txt',
                     'zad2_logs.txt',
                     polish_words)
