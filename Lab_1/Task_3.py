import random


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


def isTriple(hand):
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
        return 10
    if isStraightFlush(hand):
        return 9
    if isQuad(hand):
        return 8
    if isFullHouse(hand):
        return 7
    if isFlush(hand):
        return 6
    if isStraight(hand):
        return 5
    if isTriple(hand):
        return 4
    if isTwoPairs(hand):
        return 3
    if isPair(hand):
        return 2
    return 0


################################################################################

def allCards():
    figurantCards = [11, 12, 13, 14]
    blotkarzCards = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    fc = [(i, j) for i in figurantCards for j in range(1, 5)]
    bc = [(i, j) for i in blotkarzCards for j in range(1, 5)]

    return fc, bc


# zwraca 1 jeśli wygra blotkarz, 0 jeśli figurant
def test(figurantCards, blotkarzCards):
    figurantHand = random.sample(figurantCards, 5)
    blotkarzHand = random.sample(blotkarzCards, 5)

    return assignPoints(figurantHand) < assignPoints(blotkarzHand)


def make_test(n, figurantCards, blotkarzCards):
    counter = 0
    for _ in range(n):
        counter += test(figurantCards, blotkarzCards)

    print(f'Blotkarz ma {counter / n * 100: .2f}% szans na wygraną przy {n} grach.')


F, B = allCards()
make_test(1000000, F, B)