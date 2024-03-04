from collections import deque

DEBUG: bool = True
IS_IN_CHECK: bool = False

INF: int = 256

OCCUPIED_POSITIONS: dict[str, list[int]] = {"WHITE_KING": [0, 0], "WHITE_TOWER": [0, 0], "BLACK_KING": [0, 0]}

moves_dict = {
    "left": [-1, 0],
    "left-up": [-1, 1],
    "up": [0, 1],
    "right-up": [1, 1],
    "right": [1, 0],
    "right-down": [1, -1],
    "down": [0, -1],
    "left-down": [-1, -1],
}

king_moves = ["left", "left-up", "up", "right-up", "right", "right-down", "down", "left-down"]
tower_moves = ["left", "up", "right", "down"]


class Figure:
    def __init__(self, position, moves):
        self.position: list[int] = position
        self.moves: list[str] = moves


class King(Figure):
    def __init__(self, position):
        Figure.__init__(self, position, king_moves)


class Tower(Figure):
    def __init__(self, position):
        Figure.__init__(self, position, tower_moves)


def read_input(path="zad1_input.txt"):
    return open(path, "r").read().split(" ")


def convert_position(position: str) -> list[int]:
    x = ord(position[0]) - 97
    y = int(position[1]) - 1
    return [x, y]


def print_board(white_king_position: list[int],
                white_tower_position: list[int],
                black_king_position: list[int]):
    white_king_written = False
    white_tower_written = False
    black_king_written = False

    print("\n\n")

    last = ""

    current_x = -1
    current_y = -1

    for y in range(17):
        current_x = -1
        if y == 16:
            print("\n     A    B    C    D    E    F    G    H")
            break
        elif y % 2 == 1:
            print("\n", y // 2 + 1, end=" ")
        else:
            print("\n   | -- | -- | -- | -- | -- | -- | -- | -- |", end="")
            current_y += 1
            continue
        last = " "
        for x in range(40):
            if x % 5 == 0:
                print("|", end="")
                current_x += 1
                last = "|"
            elif current_x == black_king_position[0] and current_y == black_king_position[1] and not black_king_written:
                print(" bK ", end="")
                last = "K"
                black_king_written = True
            elif current_x == white_king_position[0] and current_y == white_king_position[1] and not white_king_written:
                print(" wK ", end="")
                last = "K"
                white_king_written = True
            elif current_x == white_tower_position[0] and current_y == white_tower_position[1] \
                    and not white_tower_written:
                print(" wT ", end="")
                last = "T"
                white_tower_written = True
            elif last == "K" or last == "T":
                print("", end="")
            else:
                print(" ", end="")


def is_move_available(white_turn, move_name, position, i=1):
    global OCCUPIED_POSITIONS

    move = moves_dict[move_name]
    new_x = position[0] + move[0] * i
    new_y = position[1] + move[1] * i

    if white_turn:
        if abs(new_x - OCCUPIED_POSITIONS["BLACK_KING"][0]) == 1 \
                or abs(new_y - OCCUPIED_POSITIONS["BLACK_KING"][1]) == 1:
            return False
    if not white_turn:
        if new_x == OCCUPIED_POSITIONS["WHITE_TOWER"][0] or new_y == OCCUPIED_POSITIONS["WHITE_TOWER"][1]:
            return False
        if abs(new_x - OCCUPIED_POSITIONS["WHITE_KING"][0]) == 1 \
                or abs(new_y - OCCUPIED_POSITIONS["WHITE_KING"][1]) == 1:
            return False

    if new_x < 0 or new_x > 7:
        return False
    if new_y < 0 or new_y > 7:
        return False
    return True


def find_solution(white_king_position: list[int],
                  white_tower_position: list[int],
                  black_king_position: list[int],
                  white_turn: bool):
    global INF, OCCUPIED_POSITIONS, DEBUG, IS_IN_CHECK

    queue = deque([(1, white_king_position, white_tower_position, black_king_position, white_turn)])
    best_result = INF

    while queue:
        depth, white_king_position, white_tower_position, black_king_position, white_turn = queue.popleft()

        if DEBUG:
            print_board(white_king_position, white_tower_position, black_king_position)

        OCCUPIED_POSITIONS["WHITE_KING"] = white_king_position
        OCCUPIED_POSITIONS["WHITE_TOWER"] = white_tower_position
        OCCUPIED_POSITIONS["BLACK_KING"] = black_king_position

        no_moves = True

        if white_turn:
            for figure in ['Tower', 'King']:
                if figure == 'King':
                    for move in king_moves:
                        if is_move_available(white_turn, move, white_king_position):
                            new_white_king_position = [white_king_position[0] + moves_dict[move][0],
                                                      white_king_position[1] + moves_dict[move][1]]
                            queue.append((depth + 1, new_white_king_position, white_tower_position,
                                          black_king_position, False))
                if figure == 'Tower':
                    for move in king_moves:
                        for i in range(1, 9):
                            if is_move_available(white_turn, move, white_tower_position, i=i):
                                new_white_tower_position = [white_tower_position[0] + moves_dict[move][0] * i,
                                                            white_tower_position[1] + moves_dict[move][1] * i]
                                queue.append((depth + 1, white_king_position, new_white_tower_position,
                                              black_king_position, False))
        else:
            for move in king_moves:
                if is_move_available(white_turn, move, black_king_position):
                    new_black_king_position = [black_king_position[0] + moves_dict[move][0],
                                               black_king_position[1] + moves_dict[move][1]]
                    queue.append((depth + 1, white_king_position, white_tower_position,
                                  new_black_king_position, True))
                    no_moves = False
            if no_moves and IS_IN_CHECK:
                return depth
            elif no_moves:
                return INF

    return best_result


if __name__ == "__main__":
    '''
    input format: color, white king, white tower, black king
    '''
    current_situation = read_input()
    white_turn = current_situation[0] == "white"

    print(f'Is white turn?: {white_turn}')
    print(f'current_situation: {current_situation}')

    white_king_position: list[int] = convert_position(current_situation[1])
    white_tower_position: list[int] = convert_position(current_situation[2])
    black_king_position: list[int] = convert_position(current_situation[3])

    print(f'white_king_position: {white_king_position}')
    print(f'white_tower_position: {white_tower_position}')
    print(f'black_king_position: {black_king_position}')

    available_moves = king_moves + king_moves + king_moves

    result = find_solution(white_king_position, white_tower_position, black_king_position, white_turn)
    if result == INF:
        print("INF")
    else:
        print(str(result))
