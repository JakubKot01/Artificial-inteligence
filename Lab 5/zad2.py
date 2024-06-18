board = [[0] * 72 for _ in range(72)]
for i in range(72):
    board[0][i] = 25
    board[i][0] = 25
    board[71][i] = 25
    board[i][71] = 25

corners = [[] for _ in range(25)]
corners[24] = [(1, 1), (1, 70), (70, 70), (70, 1)]
letters = 'ABCDEFGHIJKLMNOPQRSTUVWX'

goal = 100


def print_board(b):
    small_sq_added = False
    for i in range(1, 71, 1):
        expand = False
        prev = 0
        for j in range(1, 71, 1):
            v = b[i][j]
            if v == 0 and not expand:
                if not small_sq_added:
                    print("A", end="")
                    small_sq_added = True
                else:
                    print(".", end="")
            elif v == 0 and expand:
                print(letters[prev - 1], end="")
            elif v != 0 and not expand:
                expand = True
                prev = v
                print(letters[v - 1], end="")
            elif v != 0 and expand:
                print(letters[v - 1], end="")
                if b[i][j + 1] != prev:
                    expand = False
        print()


def is_corner(y, x):
    if y == 0 or y == 71 or x == 0 or x == 71:
        return False
    if board[y][x] != 0:
        return False
    if board[y - 1][x] > 0 and board[y][x - 1] > 0:
        return True
    if board[y - 1][x] > 0 and board[y][x + 1] > 0:
        return True
    if board[y + 1][x] > 0 and board[y][x - 1] > 0:
        return True
    if board[y + 1][x] > 0 and board[y][x + 1] > 0:
        return True
    return False


def count_frees():
    s = 0
    for i in range(1, 71, 1):
        expand = False
        prev = 0
        for j in range(1, 71, 1):
            v = board[i][j]
            if v == 0 and not expand:
                s += 1
            elif v != 0 and not expand:
                expand = True
                prev = v
            elif v != 0 and expand:
                if board[i][j + 1] != prev:
                    expand = False
    return s


def horizon_cor(y, x):
    if board[y][x - 1] != 0:
        return 1
    return -1


def vertic_cor(y, x):
    if board[y - 1][x] != 0:
        return 1
    return -1


def place_square(s, c):
    corners[s - 1].clear()
    for cr in corners[s]:
        if cr != c:
            corners[s - 1].append(cr)
    cy, cx = c
    hor = horizon_cor(cy, cx)
    ver = vertic_cor(cy, cx)

    for i in range(s):
        if board[cy + i * ver][cx] != 0:
            corners[s - 1].append(c)
            return False
    for i in range(s):
        if board[cy][cx + i * hor] != 0:
            corners[s - 1].append(c)
            return False
    for i in range(s):
        if board[cy + i * ver][cx + (s - 1) * hor] != 0:
            corners[s - 1].append(c)
            return False
    for i in range(s):
        if board[cy + (s - 1) * ver][cx + i * hor] != 0:
            corners[s - 1].append(c)
            return False

    for i in range(s):
        board[cy + i * ver][cx] = s
        board[cy + i * ver][cx + (s - 1) * hor] = s
        board[cy][cx + i * hor] = s
        board[cy + (s - 1) * ver][cx + i * hor] = s

    up = cy + s
    down = cy - 1
    if ver == -1:
        up = cy + 1
        down = cy - s
    right = cx + s
    left = cx - 1
    if hor == -1:
        right = cx + 1
        left = cx - s
    for i in range(-1, s + 1, 1):
        if is_corner(up, cx + i * hor) and (up, cx + i * hor) not in corners[s - 1]:
            corners[s - 1].append((up, cx + i * hor))
    for i in range(-1, s + 1, 1):
        if is_corner(down, cx + i * hor) and (down, cx + i * hor) not in corners[s - 1]:
            corners[s - 1].append((down, cx + i * hor))
    for i in range(-1, s + 1, 1):
        if is_corner(cy + i * ver, right) and (cy + i * ver, right) not in corners[s - 1]:
            corners[s - 1].append((cy + i * ver, right))
    for i in range(-1, s + 1, 1):
        if is_corner(cy + i * ver, left) and (cy + i * ver, left) not in corners[s - 1]:
            corners[s - 1].append((cy + i * ver, left))
    return True


def unplace_square(s, c):
    cy, cx = c
    hor = 1
    ver = 1
    if board[cy][cx - 1] == s:
        hor = -1
    if board[cy - 1][cx] == s:
        ver = -1

    for i in range(s):
        board[cy + i * ver][cx] = 0
        board[cy + i * ver][cx + (s - 1) * hor] = 0
        board[cy][cx + i * hor] = 0
        board[cy + (s - 1) * ver][cx + i * hor] = 0


def solve(s):
    if s == 1:
        n = count_frees() - 1
        if n <= goal:
            print(n)
            print_board(board)
            exit()
        return True

    chosen_any = False
    for c in corners[s]:
        placed = place_square(s, c)
        if not placed:
            continue
        chosen_any = True
        res = solve(s - 1)
        unplace_square(s, c)
        if res:
            return True

    if not chosen_any:
        if s > 10:
            return False
        solve(s - 1)
        return False


solve(24)
