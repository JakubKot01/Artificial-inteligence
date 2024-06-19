# Symulator rozgrywek w grę oszust (bullshit) z różnymi agentami

import random
from copy import deepcopy

NUMBER_GAMES = 100
MAX_NUMBER_OF_TURNS = 1000
DEBUG = False
SUITS = ["\u2663", "\u2665", "\u2666", "\u2660"]
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


def less_or_eq(x, y):
    pos_x = VALUES.index(x)
    pos_y = VALUES.index(y)
    return pos_x <= pos_y


def greater_or_eq(x, y):
    pos_x = VALUES.index(x)
    pos_y = VALUES.index(y)
    return pos_x >= pos_y


class Card:
    def __init__(self, val, suit):
        self.suit = suit
        self.val = val

    def to_string(self):
        return f"{self.suit} {self.val}"

    def show(self):
        print(self.suit, self.val)

    def __eq__(self, other):
        return self.val == other.val and self.suit == other.suit


class Deck:
    def __init__(self):
        self.deck = [Card(v, s) for s in SUITS for v in VALUES]

    def show(self):
        result = [c.to_string() for c in self.deck]
        print(result)

    def __getitem__(self, key):
        return self.deck[key]

    def shuffle(self):
        self.deck = random.sample(self.deck, 52)


class Game:
    def __init__(self, players):
        self.players = players
        self.number_of_players = len(self.players)
        self.history = []
        self.player = random.randint(0, self.number_of_players - 1)  # who start the game, and then which one turn it is
        self.pile = []
        self.hands = [[] for _ in range(self.number_of_players)]

        deck = Deck()
        deck.shuffle()

        for i in range(52):
            self.hands[i % self.number_of_players].append(deck[i])

        for i in range(len(self.players)):
            self.players[i].set_number(i)
            self.players[i].send_info(self.number_of_players, self.hands[i])

    def loop(self):
        while True:
            for i in range(self.number_of_players):
                if not self.hands[i]:
                    return i

            if len(self.history) > MAX_NUMBER_OF_TURNS:
                return -1

            self.turn()
            if DEBUG:
                self.show_hands()
                print("")
            self.player = (self.player + 1) % self.number_of_players

    def show_hands(self):
        for i in range(self.number_of_players):
            result = [c.to_string() for c in self.hands[i]]
            print(i, len(result), result)

    def turn(self):
        cards, (amount, value) = self.players[self.player].move(self.history, self.player, self.hands[self.player],
                                                                self.pile)  # cards = [c1, ..., cn]

        for i in range(self.number_of_players):
            self.players[i].inform(self.player, amount, value, self.history, self.pile)

        if DEBUG:
            print(f"player {self.player} declare {amount}, {value} and put {[c.to_string() for c in cards]}")

        # I assume the declarations are in accordance with the rules

        for c in cards:
            self.hands[self.player].remove(c)
            assert c not in self.pile
            self.pile.append(c)

        self.history.append((amount, value))

        for i in range(self.player + 1, self.player + self.number_of_players):
            if self.players[i % self.number_of_players].doubt(self.history, self.player, self.hands):
                if DEBUG:
                    print(f"player {i % self.number_of_players} check")
                self.check(self.player, i % self.number_of_players)
                break

    def check(self, player, checker):

        def checking():
            for c in cards_from_pile:
                if c.val != value:
                    return False
            return True

        amount, value = self.history[-1]
        cards_from_pile = self.pile[-amount:]
        lie = None
        if checking():  # not a lie
            self.hands[checker] += self.pile
            lie = False
        else:
            self.hands[player] += self.pile
            lie = True
        for i in range(self.number_of_players):
            self.players[i].after_check(player, checker, lie, self.history, self.pile, self.hands[i])
        self.pile = []

    @staticmethod
    def finish_game(player):
        if player is None:
            return -1
        else:
            return player.introduce()


class Player():

    def set_number(self, i):
        self.my_number = i

    def send_info(self, number_of_players, hand):
        pass

    def inform(self, player, amount, value, history, pile):
        pass

    def after_check(self, player, checker, lie, history, pile, hand):
        pass

    def move(self, history, player, hand, pile):
        return self.move(self, history, player, hand, pile)

    def doubt(self, history, player, hands):
        return self.doubt(history, player, hands)


class Random(Player):

    def __init__(self, challenging=0.1):
        self.name = "Random"
        self.challenging = challenging

    def introduce(self):
        return f"{self.name} with p = {self.challenging}"

    def move(self, history, player, hand, pile):

        if len(history) == 0 or not pile:
            (amount, last_value) = (-1, '2')
        else:
            (amount, last_value) = history[-1]

        card = random.choice(hand)
        if greater_or_eq(card.val, last_value):  # tell thruth
            return [card], (1, card.val)
        else:  # lie it it last declared value
            return [card], (1, last_value)

    # not really good because player shoudn't get whole hands but I use it only for lengths
    # always when player will end the game otherwise with probability = challenging
    def doubt(self, history, player, hands):
        if len(hands[player]) == 0:
            return True
        return random.random() < self.challenging


class Beginner(Player):

    def __init__(self):
        pass

    @staticmethod
    def introduce():
        return "Beginner"

    def move(self, history, player, hand, pile):

        if len(history) == 0 or not pile:
            (amount, last_value) = (-1, '2')
        else:
            (amount, last_value) = history[-1]
        poss = []
        for card in hand:
            if greater_or_eq(card.val, last_value):
                poss.append(card)

        if DEBUG:
            print("POSS")
            print([c.to_string for c in poss])
        if not poss:  # have to lie - pick random card and declare random legal option
            card = random.choice(hand)
            options = []
            for v in VALUES:
                if greater_or_eq(v, last_value):
                    options.append(v)
            return [card], (1, random.choice(options))

        # don't lie - pick randomly card, pick all cards with same value if they exist and declare thruth
        card = random.choice(poss)
        result = [card]
        for c in poss:
            if c.val == card.val and c != card:
                result.append(c)

        return result, (len(result), card.val)

    # always when somebody will end and when they sure somebody is lying
    def doubt(self, history, player, hands):

        def possible():
            (amount, value) = history[-1]
            in_my_hand = 0
            for c in hands[self.my_number]:
                if c.val == value:
                    in_my_hand += 1
            if in_my_hand + amount > 4:
                return False
            return True

        if len(hands[player]) == 0 or not possible():
            return True
        else:
            return False


class Little_calculator(Player):

    def __init__(self):
        # probability how many card use when cheating - never cheat with four card
        self.prob1 = 0.5
        self.prob2 = 0.4
        self.prob3 = 0.1

    def send_info(self, number_of_players, hand):
        self.number_of_players = number_of_players
        # where given card possible is
        self.poss = [[] for _ in range(number_of_players)]
        self.my_pile = []
        self.poss[self.my_number] = deepcopy(hand)
        deck = [Card(v, s) for s in SUITS for v in VALUES]
        for i in range(number_of_players):
            if i != self.my_number:
                self.poss[i] = [c for c in deck if c not in self.poss[self.my_number]]

        if DEBUG:
            print([c.to_string() for c in self.poss[self.my_number]])

    @staticmethod
    def introduce():
        return "Little calculator"

    def inform(self, player, amount, value, history, pile):
        if player == self.my_number:
            cards = deepcopy(pile[-amount:])
            for c in cards:
                if c not in self.my_pile:
                    self.my_pile.append(c)
        else:
            cards = self.poss[player]
            for c in cards:
                if c not in self.my_pile:
                    self.my_pile.append(c)

        if DEBUG:
            print(f"inform {player}, {amount}, {value}")
            print([c.to_string() for c in self.my_pile])

    def after_check(self, player, checker, lie, history, pile, hand):
        if DEBUG:
            print(f"before check {player}, {checker}, {lie}")
            print([c.to_string() for c in self.poss[player]])
            print([c.to_string() for c in self.poss[checker]])
        if lie:
            for c in self.my_pile:
                if c not in self.poss[player]:
                    self.poss[player].append(c)
        elif checker == self.my_number:
            self.poss[self.my_number] = []
            for c in pile:
                if c not in self.poss[self.my_number]:
                    self.poss[self.my_number].append(c)
            for c in hand:
                if c not in self.poss[self.my_number]:
                    self.poss[self.my_number].append(c)
            # self.poss[checker] = hand + pile
            for c in self.poss[self.my_number]:
                for i in range(self.number_of_players):
                    if i != self.my_number:
                        if c in self.poss[i]:
                            self.poss[i].remove(c)
        else:
            (amount, value) = history[-1]
            cards = [Card(value, s) for s in SUITS]

            count_players = 0
            for c in cards:
                if c in self.poss[player]:
                    count_players += 1
            if count_players == amount:
                for c in cards:
                    if c in self.poss[player]:
                        self.poss[player].remove(c)
                        if c not in self.poss[checker]:
                            self.poss[checker].append(c)
                    else:
                        for c in cards:
                            if c not in self.poss[checker]:
                                self.poss[checker].append(c)

        if DEBUG:
            print(f"after check {player}, {checker}, {lie}")
            print([c.to_string() for c in self.poss[player]])
            print([c.to_string() for c in self.poss[checker]])
        self.my_pile = []

    def move(self, history, player, hand, pile):

        if len(history) == 0 or not pile:
            (amount, last_value) = (-1, '2')
        else:
            (amount, last_value) = history[-1]
        poss = []
        for card in hand:
            if greater_or_eq(card.val, last_value):
                poss.append(card)

        if DEBUG:
            print(poss)
        if not poss:  # have to lie
            # how many cards I declare:
            number_of_cards = 0
            r = random.random()
            if r < self.prob1:
                number_of_cards = 1
            elif r < self.prob1 + self.prob2 and len(hand) >= 2:
                number_of_cards = 2
            elif len(hand) >= 3:
                number_of_cards = 3

            # which cards I will use
            result = random.sample(hand, number_of_cards)

            # which value I declare
            options = []
            for v in VALUES:
                if greater_or_eq(v, last_value):
                    options.append(v)

            best_chaos = 0
            best_value = 'A'
            for v in options:
                cards = [Card(v, s) for s in SUITS]
                chaos = 0
                for c in cards:
                    for i in range(self.number_of_players):
                        if c in self.poss[i]:
                            chaos += 1
                if chaos > best_chaos:
                    best_chaos = chaos
                    best_value = v

            return result, (number_of_cards, best_value)

        # don't lie - pick randomly card, pick all cards with same value if they exist and declare thruth
        card = random.choice(poss)
        result = [card]
        for c in poss:
            if c.val == card.val and c != card:
                result.append(c)

        return result, (len(result), card.val)

    # always when somebody will end and when they sure somebody is lying
    def doubt(self, history, player, hands):

        def possible():
            (amount, value) = history[-1]
            in_my_hand = 0
            for c in hands[self.my_number]:
                if c.val == value:
                    in_my_hand += 1
            if in_my_hand + amount > 4:
                return False

            cards = [Card(value, s) for s in SUITS]
            can_has = 0
            for c in cards:
                if c in self.poss[player]:
                    can_has += 1
            if can_has < amount:
                return False

            return True

        if len(hands[player]) == 0 or not possible():
            return True
        else:
            return False


class Kid(Player):

    def __init__(self):
        self.prob1 = 0.6
        self.prob2 = 0.35
        self.prob3 = 0.05

    @staticmethod
    def introduce():
        return "Kid"

    def move(self, history, player, hand, pile):

        def can_win():
            if len(hand) > 4:
                return False
            for c in hand:
                if c.val != hand[0].val:
                    return False
            if not greater_or_eq(hand[0].val, last_value):
                return False
            return True

        if len(history) == 0 or not pile:
            (amount, last_value) = (-1, '2')
        else:
            (amount, last_value) = history[-1]
        poss = []
        for card in hand:
            if greater_or_eq(card.val, last_value):
                poss.append(card)

        if can_win():
            card = random.choice(poss)
            result = [card]
            for c in poss:
                if c.val == card.val and c != card:
                    result.append(c)

            return result, (len(result), card.val)

        want_to_lie = random.random() < len(hand) / 100

        if want_to_lie or not poss:
            # how many cards I declare:
            number_of_cards = 0
            r = random.random()
            if r < self.prob1:
                number_of_cards = 1
            elif r < self.prob1 + self.prob2 and len(hand) >= 2:
                number_of_cards = 2
            elif len(hand) >= 3:
                number_of_cards = 3

            # which cards I will use
            result = random.sample(hand, number_of_cards)

            # which value I declare
            options = []
            for v in VALUES:
                if greater_or_eq(v, last_value):
                    options.append(v)

            return result, (number_of_cards, random.choice(options))
        else:
            lower_val = 'A'
            card = poss[0]
            for c in poss:
                if not greater_or_eq(c.val, lower_val):
                    lower_val = c.val
                    card = c
            result = [card]
            for c in poss:
                if c.val == card.val and c != card:
                    result.append(c)
            return result, (len(result), card.val)

    # always when somebody will end and when they sure somebody is lying
    def doubt(self, history, player, hands):

        def possible():
            (amount, value) = history[-1]
            in_my_hand = 0
            for c in hands[self.my_number]:
                if c.val == value:
                    in_my_hand += 1
            if in_my_hand + amount > 4:
                return False
            return True

        if len(hands[player]) == 0 or not possible():
            return True
        else:
            return False


if __name__ == '__main__':
    p1 = Random(challenging=0.2)
    p2 = Beginner()
    p3 = Little_calculator()
    p4 = Kid()

    players = [p1, p2, p3, p4]
    result = {-1: 0}
    for i in range(len(players)):
        result[i] = 0

    for i in range(NUMBER_GAMES):
        if i % (NUMBER_GAMES / 10) == 0:
            print(f"{i}/{NUMBER_GAMES} games done")
        game = Game(players)
        winner = game.loop()
        result[winner] += 1

    print("RESULTS")
    print(f"Number of games: {NUMBER_GAMES}")
    print(f"Draws after {MAX_NUMBER_OF_TURNS} moves: {result[-1]}")
    for i in range(len(players)):
        print(f"Wins of player {i} {players[i].introduce()}: {result[i]}, what is {result[i] * 100 / NUMBER_GAMES}%")