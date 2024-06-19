"""
Gracze:
    - Losowy:
        - Pamięć:
            - Brak
        - Ruch:
            Bierze losową kartę z ręki, jeśli może ją zadeklarować - robi to, w przeciwnym wypadku - deklaruje ostatnią zadeklarowaną wartość
        - Sprawdzanie:
            - Sprawdza zawsze gdy przeciwnik pozbędzie się wszystkich kart
            - Sprawdza z prawdopodobieństwem x
    - Początkujący:
        - Pamięć:
            - Brak
        - Ruch:
            - Jeśli może - losuje kartę o dozwolonej wartości i wyrzuca wszystkie o tej samej wartości
            - Jeśli nie ma takiej karty - bierze losową kartę i deklaruje kartę o losowej dozwolonej wartości
        - Sprawdzanie:
            - Sprawdza zawsze gdy przeciwnik może wygrać
            - Sprawdza jeśli karty w ręce ewidetnie wskazują na oszustwo
    - Naiwny:
        - Pamięć:
            - Brak
        - Ruch:
            - Im mniej kart w dłoni, tym mniej oszukuje
            - Nie oszukuje jeśli może wygrać
            - Jeśli oszukuje - Bierze losowe x kart i deklaruje losową dozwoloną wartość
            - Jeśli nie oszukuje - Pozbywa się jak najmniejszych kart
        - Sprawdzanie:
            - Tak jak gracz początkujący
    - Wyrachowany:
        - Pamięć:
            - Trzyma listę możliwych kart w posiadaniu każdego gracza
        - Ruch:
            - Stara się grać uczciwie
            - Jeśli oszukuje - deklaruje x kart i wybiera karty, o których ma najmniejszą wiedzę
                (Im więcej graczy może ją posiadać tym lepiej)
        - Sprawdzanie:
            - Sprawdza gdy gracz może wygrać lub gdy ma pewność, że oszukuje
"""

import random
from copy import deepcopy

NUMBER_GAMES = 100
MAX_NUMBER_OF_TURNS = 1000
SUITS = ["CLUBS", "HEARTS", "DIAMOND", "SPADE"]
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

    def __eq__(self, other):
        return self.val == other.val and self.suit == other.suit


class Deck:
    def __init__(self):
        self.deck = [Card(v, s) for s in SUITS for v in VALUES]

    def __getitem__(self, key):
        return self.deck[key]

    def shuffle(self):
        self.deck = random.sample(self.deck, 52)


class Game:
    def __init__(self, players_list):
        self.players = players_list
        self.number_of_players = len(self.players)
        self.history = []
        self.player = random.randint(0, self.number_of_players - 1)  # who start the game, and then which one turn it is
        self.pile = []
        self.hands = [[] for _ in range(self.number_of_players)]

        deck = Deck()
        deck.shuffle()

        for card_index in range(52):
            self.hands[card_index % self.number_of_players].append(deck[card_index])

        for player_index in range(len(self.players)):
            self.players[player_index].set_number(player_index)
            self.players[player_index].send_info(self.number_of_players, self.hands[player_index])

    def loop(self):
        while True:
            for player_index in range(self.number_of_players):
                if not self.hands[player_index]:
                    return player_index

            if len(self.history) > MAX_NUMBER_OF_TURNS:
                return -1

            self.turn()
            self.player = (self.player + 1) % self.number_of_players

    def turn(self):
        cards, (amount, value) = self.players[self.player].move(self.history, self.player, self.hands[self.player],
                                                                self.pile)  # cards = [c1, ..., cn]

        for player_index in range(self.number_of_players):
            self.players[player_index].inform(self.player, amount, value, self.history, self.pile)

        for card in cards:
            self.hands[self.player].remove(card)
            assert card not in self.pile
            self.pile.append(card)

        self.history.append((amount, value))

        for player_index in range(self.player + 1, self.player + self.number_of_players):
            if self.players[player_index % self.number_of_players].doubt(self.history, self.player, self.hands):
                self.check(self.player, player_index % self.number_of_players)
                break

    def check(self, player, checker):

        def checking():
            for card in cards_from_pile:
                if card.val != value:
                    return False
            return True

        amount, value = self.history[-1]
        cards_from_pile = self.pile[-amount:]
        lie = False
        if checking():  # not a lie
            self.hands[checker] += self.pile
            lie = False
        else:
            self.hands[player] += self.pile
            lie = True
        for player_index in range(self.number_of_players):
            (self.players[player_index]
                .after_check(player, checker, lie, self.history, self.pile, self.hands[player_index]))
        self.pile = []

    @staticmethod
    def finish_game(player):
        if player is None:
            return -1
        else:
            return player.whoAmI()


class Player:

    def set_number(self, player_number):
        self.my_number = player_number

    def send_info(self, number_of_players, hand):
        pass

    def inform(self, player, amount, value, history, pile):
        pass

    def after_check(self, player, checker, lie, history, pile, hand):
        pass

    def move(self, history, player, hand, pile):
        return self.move(history, player, hand, pile)

    def doubt(self, history, player, hands):
        return self.doubt(history, player, hands)


class Random(Player):

    def __init__(self, challenging=0.1):
        self.name = "Random"
        self.challenging = challenging

    def whoAmI(self):
        return f"{self.name} with p = {self.challenging}"

    def move(self, history, player, hand, pile):

        if len(history) == 0 or not pile:
            (amount, last_value) = (-1, '2')
        else:
            (amount, last_value) = history[-1]

        card = random.choice(hand)
        if greater_or_eq(card.val, last_value):  # tell truth
            return [card], (1, card.val)
        else:  # lie: last declared value
            return [card], (1, last_value)

    # not really good because player shouldn't get whole hands, but I use it only for lengths
    # always when player will end the game otherwise with probability = challenging
    def doubt(self, history, player, hands):
        if len(hands[player]) == 0:
            return True
        return random.random() < self.challenging


class Beginner(Player):

    def __init__(self):
        pass

    @staticmethod
    def whoAmI():
        return "Beginner"

    def move(self, history, player, hand, pile):

        if len(history) == 0 or not pile:
            (amount, last_value) = (-1, '2')
        else:
            (amount, last_value) = history[-1]
        possession = []
        for card in hand:
            if greater_or_eq(card.val, last_value):
                possession.append(card)

        if not possession:  # have to lie - pick random card and declare random legal value
            card = random.choice(hand)
            possible_values = []
            for v in VALUES:
                if greater_or_eq(v, last_value):
                    possible_values.append(v)
            return [card], (1, random.choice(possible_values))

        # don't lie - pick randomly card, pick all cards with same value if they exist and declare truth
        card = random.choice(possession)
        chosen_cards = [card]
        for card in possession:
            if card.val == card.val and card != card:
                chosen_cards.append(card)

        return chosen_cards, (len(chosen_cards), card.val)

    # always when somebody will end and when they sure somebody is lying
    def doubt(self, history, player, hands):

        def possible():
            (amount, value) = history[-1]
            in_my_hand = 0
            for card in hands[self.my_number]:
                if card.val == value:
                    in_my_hand += 1
            if in_my_hand + amount > 4:
                return False
            return True

        if len(hands[player]) == 0 or not possible():
            return True
        else:
            return False


class Calculated(Player):

    def __init__(self):
        # probability how many card use when cheating - never cheat with four card
        self.my_pile = None
        self.number_of_players = None
        self.possession = None
        self.prob1 = 0.5
        self.prob2 = 0.4
        self.prob3 = 0.1

    def send_info(self, number_of_players, hand):
        self.number_of_players = number_of_players
        # where given card possible is
        self.possession = [[] for _ in range(number_of_players)]
        self.my_pile = []
        self.possession[self.my_number] = deepcopy(hand)
        deck = [Card(v, s) for s in SUITS for v in VALUES]
        for player_index in range(number_of_players):
            if player_index != self.my_number:
                self.possession[player_index] = [card for card in deck if card not in self.possession[self.my_number]]

    @staticmethod
    def whoAmI():
        return "Calculated"

    def inform(self, player, amount, value, history, pile):
        if player == self.my_number:
            cards = deepcopy(pile[-amount:])
            for card in cards:
                if card not in self.my_pile:
                    self.my_pile.append(card)
        else:
            cards = self.possession[player]
            for card in cards:
                if card not in self.my_pile:
                    self.my_pile.append(card)

    def after_check(self, player, checker, lie, history, pile, hand):
        if lie:
            for card in self.my_pile:
                if card not in self.possession[player]:
                    self.possession[player].append(card)
        elif checker == self.my_number:
            self.possession[self.my_number] = []
            for card in pile:
                if card not in self.possession[self.my_number]:
                    self.possession[self.my_number].append(card)
            for card in hand:
                if card not in self.possession[self.my_number]:
                    self.possession[self.my_number].append(card)
            for card in self.possession[self.my_number]:
                for player_index in range(self.number_of_players):
                    if player_index != self.my_number:
                        if card in self.possession[player_index]:
                            self.possession[player_index].remove(card)
        else:
            (amount, value) = history[-1]
            cards = [Card(value, s) for s in SUITS]

            count_players = 0
            for card in cards:
                if card in self.possession[player]:
                    count_players += 1
            if count_players == amount:
                for card in cards:
                    if card in self.possession[player]:
                        self.possession[player].remove(card)
                        if card not in self.possession[checker]:
                            self.possession[checker].append(card)
            else:
                for card in cards:
                    if card not in self.possession[checker]:
                        self.possession[checker].append(card)
        self.my_pile = []

    def move(self, history, player, hand, pile):

        if len(history) == 0 or not pile:
            (amount, last_value) = (-1, '2')
        else:
            (amount, last_value) = history[-1]
        possession = []
        for card in hand:
            if greater_or_eq(card.val, last_value):
                possession.append(card)

        if not possession:  # have to lie
            # how many cards I declare:
            number_of_cards = 0
            r = random.random()
            if r < self.prob1:
                number_of_cards = 1
            elif r < self.prob2 and len(hand) >= 2:
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
                for card in cards:
                    for player_index in range(self.number_of_players):
                        if player_index != self.my_number:
                            if card in self.possession[player_index]:
                                chaos += 1
                if chaos > best_chaos:
                    best_chaos = chaos
                    best_value = v

            return result, (number_of_cards, best_value)

        # don't lie - pick randomly card, pick all cards with same value if they exist and declare truth
        possession.sort(key=lambda x: x.val)
        # card = random.choice(possession)
        card = possession[0]
        result = [card]
        for card in possession:
            if card.val == card.val and card != card:
                result.append(card)

        return result, (len(result), card.val)

    # always when somebody will end and when they sure somebody is lying
    def doubt(self, history, player, hands):

        def possible():
            (amount, value) = history[-1]
            in_my_hand = 0
            for card in hands[self.my_number]:
                if card.val == value:
                    in_my_hand += 1
            if in_my_hand + amount > 4:
                return False

            cards = [Card(value, s) for s in SUITS]
            can_have = 0
            for card in cards:
                if card in self.possession[player]:
                    can_have += 1
            if can_have < amount:
                return False

            return True

        if len(hands[player]) == 0 or not possible():
            return True
        else:
            return False


class Naive(Player):

    def __init__(self):
        self.prob1 = 0.6
        self.prob2 = 0.35
        self.prob3 = 0.05

    @staticmethod
    def whoAmI():
        return "Naive"

    def move(self, history, player, hand, pile):

        def can_win():
            if len(hand) > 4:
                return False
            for card in hand:
                if card.val != hand[0].val:
                    return False
            if not greater_or_eq(hand[0].val, last_value):
                return False
            return True

        if len(history) == 0 or not pile:
            (amount, last_value) = (-1, '2')
        else:
            (amount, last_value) = history[-1]
        options = []
        for card in hand:
            if greater_or_eq(card.val, last_value):
                options.append(card)

        if can_win():
            card = random.choice(options)
            result = [card]
            for card in options:
                if card.val == card.val and card != card:
                    result.append(card)

            return result, (len(result), card.val)

        want_to_lie = random.random() < len(hand) / 100

        if want_to_lie or not options:
            # how many cards I declare:
            number_of_cards = 0
            r = random.random()
            if r < self.prob1:
                number_of_cards = 1
            elif r < self.prob2 and len(hand) >= 2:
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
            card = options[0]
            for card in options:
                if not greater_or_eq(card.val, lower_val):
                    lower_val = card.val
                    card = card
            result = [card]
            for card in options:
                if card.val == card.val and card != card:
                    result.append(card)
            return result, (len(result), card.val)

    # always when somebody will win and when they sure somebody is lying
    def doubt(self, history, player, hands):

        def possible():
            (amount, value) = history[-1]
            in_my_hand = 0
            for card in hands[self.my_number]:
                if card.val == value:
                    in_my_hand += 1
            if in_my_hand + amount > 4:
                return False
            return True

        if len(hands[player]) == 0 or not possible():
            return True
        else:
            return False


if __name__ == '__main__':
    random1 = Random(challenging=0.2)
    random2 = Random(challenging=0.2)
    random3 = Random(challenging=0.2)
    random4 = Random(challenging=0.2)

    beginner1 = Beginner()
    beginner2 = Beginner()
    beginner3 = Beginner()
    beginner4 = Beginner()

    naive1 = Naive()
    naive2 = Naive()
    naive3 = Naive()
    naive4 = Naive()

    calculated1 = Calculated()
    calculated2 = Calculated()
    calculated3 = Calculated()
    calculated4 = Calculated()

    players_list = [
        random1, random2, random3, random4,
        beginner1, beginner2, beginner3, beginner4,
        naive1, naive2, naive3, naive4,
        calculated1, calculated2, calculated3, calculated4
    ]

    for game in range(10):
        print(f"Players set number: {game}")
        players = random.sample(players_list, 4)
        result = {-1: 0}
        for index in range(len(players)):
            result[index] = 0

        for index in range(NUMBER_GAMES):
            # if index % (NUMBER_GAMES / 10) == 0:
            #     print(f"{index}/{NUMBER_GAMES} games done")
            game = Game(players)
            winner = game.loop()
            result[winner] += 1

        # print("RESULTS")
        # print(f"Number of games: {NUMBER_GAMES}")
        # print(f"Draws after {MAX_NUMBER_OF_TURNS} moves: {result[-1]}")
        for index in range(len(players)):
            print(f"Wins of player {index} {players[index].whoAmI()}: {result[index]}, "
                  f"what is {result[index] * 100 / NUMBER_GAMES}%")
