from itertools import combinations

bcards = []
fcards = []
GAMES = 1646701056

for card in range(2, 11):
    for color in range(0, 4):
        bcards.append([card, color])

for card in range(0, 4):
    for color in range(0, 4):
        fcards.append([card, color])


def isRoyalFlush(hand):
    hand.sort()
    card = 10
    for i in range(4):
        if hand[i][0] + 1 != hand[i + 1][0] or hand[i][1] != hand[i + 1][1] or hand[i][0] != card:
            return False
        card += 1
    return hand[4][0] == card


def isStraightFlush(hand):
    hand.sort()
    for i in range(4):
        if hand[i][0] + 1 != hand[i + 1][0] or hand[i][1] != hand[i + 1][1]:
            return False
    return True


def isQuad(hand):
    hand.sort()
    if hand[0][0] == hand[1][0] == hand[2][0] == hand[3][0]:
        return True
    if hand[1][0] == hand[2][0] == hand[3][0] == hand[4][0]:
        return True
    return False


def isFullHouse(hand):
    hand.sort()
    if (hand[0][0] == hand[1][0] == hand[2][0]) and (hand[3][0] == hand[4][0]):
        return True
    if (hand[2][0] == hand[3][0] == hand[4][0]) and (hand[0][0] == hand[1][0]):
        return True
    return False


def isFlush(hand):
    for i in range(4):
        if hand[i][1] != hand[i + 1][1]:
            return False
    return True


def isStraight(hand):
    hand.sort()
    for i in range(4):
        if hand[i][0] + 1 != hand[i + 1][0]:
            return False
    return True


def isTripple(hand):
    hand.sort()
    if hand[0][0] == hand[1][0] == hand[2][0]:
        return True
    if hand[1][0] == hand[2][0] == hand[3][0]:
        return True
    if hand[2][0] == hand[3][0] == hand[4][0]:
        return True
    return False


def isTwoPairs(hand):
    hand.sort()
    if (hand[0][0] == hand[1][0]) and (hand[2][0] == hand[3][0]):
        return True
    if (hand[0][0] == hand[1][0]) and (hand[3][0] == hand[4][0]):
        return True
    if (hand[1][0] == hand[2][0]) and (hand[3][0] == hand[4][0]):
        return True
    return False


def isPair(hand):
    hand.sort()
    for i in range(4):
        if hand[i][0] == hand[i + 1][0]:
            return True
    return False


def assignPoints(hand):
    if isRoyalFlush(hand):
        return 9
    if isStraightFlush(hand):
        return 8
    if isQuad(hand):
        return 7
    if isFullHouse(hand):
        return 6
    if isFlush(hand):
        return 5
    if isStraight(hand):
        return 4
    if isTripple(hand):
        return 3
    if isTwoPairs(hand):
        return 2
    if isPair(hand):
        return 1
    return 0


###########################################################################

"""
bcards = []
fcards = []
GAMES = 1646701056

for card in range(2, 11):
    for color in range(0, 4):
        bcards.append([card, color])

for card in range(0, 4):
    for color in range(0, 4):
        fcards.append([card, color])
"""


if __name__ == '__main__':
    B = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    F = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for hand in combinations(bcards, 5):
        B[assignPoints(list(hand))] += 1

    for hand in combinations(fcards, 5):
        F[assignPoints(list(hand))] += 1

    bWins = 0
    for i in range(2, 10):
        for j in range(1, i):
            bWins += B[i] * F[j]

    print(f'blotkarz: {bWins / GAMES}')
    print(f'figurant: {1 - bWins / GAMES}')