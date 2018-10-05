#  © 2018 Matt Fan
# http://mattfan.me/

# Fun Fact: One of my first jobs was as a marriage counselling intern for the Navy

from random import shuffle, choice as randomChoice
from enum import Enum

# I wrote some classes to help with the representation of objects for this game.
# Many of these can be reused in implementations of other card games.

class Color(Enum):
    RED = 0
    BLACK = 1


class Suit(Enum):
    CLUB = 1
    HEART = 2
    SPADE = 3
    DIAMOND = 4

    def color(self):
        if self.value % 2 == 0:
            return Color.RED
        return Color.BLACK


class Card:
    valueNames = {
        'A': 'Ace',
        2: 'Two',
        3: 'Three',
        4: 'Four',
        5: 'Five',
        6: 'Six',
        7: 'Seven',
        8: 'Eight',
        9: 'Nine',
        10: 'Ten',
        'J': 'Jack',
        'Q': 'Queen',
        'K': 'King',
    }

    suitSymbols = {
        Suit.CLUB: '♣',
        Suit.HEART: '♥',
        Suit.SPADE: '♠',
        Suit.DIAMOND: '♦'
    }

    suitNames = {
        Suit.CLUB: 'Clubs',
        Suit.HEART: 'Hearts',
        Suit.SPADE: 'Spades',
        Suit.DIAMOND: 'Diamonds'
    }

    def __init__(self, value, suit):
        self.suit = suit
        self.value = value
    
    def passesRule(self,rule):
        #Pass in the value and suit.
        #Returns True if the rule is passed, false otherwise
        #takes a function which takes v (a value between 1 and 14), and s(a suit)
        return rule.test(self) #
    
    @classmethod
    def odds(cls, cards, rule):
        # Brute force to figure out odds that a rule will pass for the given cards.
        passes = 0
        for card in cards:
            if card.passesRule(rule): passes += 1
        return passes / len(cards)

    def format(self):
        # String formatting
        return self.valueNames[self.value] + ' of ' + self.suitNames[self.suit]
    def shortFormat(self):
        return '('+str(self.value)+self.suitSymbols[self.suit]+')'
    def fancyFormat(self):
        return f"{self.shortFormat():5}  {self.format()}"

    @classmethod
    def parse(cls, string):
        # Opposite of 'format'
        # Parses a string and returns a new card with the corresponding value if valid.
        valueMap = dict([v.lower(),k] for k, v in cls.valueNames.items())
        suitMap = dict([v.lower(),k] for k, v in cls.suitNames.items())
        args = string.split()
        if len(args) == 3 and args[0].lower() in valueMap and args[2].lower() in suitMap:
            return cls(valueMap[args[0].lower()], suitMap[args[2].lower()])
        # @TODO: raise error if no match found
    

    def __eq__(self, other):
        # Equality method
        return self.value == other.value and self.suit == other.suit
    
    def __ne__(self,other):
        return not self.__eq__(other)

    def __mapToValue(self, map):
        if self.value in map.keys():
            return map[self.value]
        return self.value

    def valAsNum(self):
        return self.__mapToValue({ 'A':1, 'J':11, 'Q':12, 'K':13 })

    def __lt__(self,other):
        f1 = {'A':1,'J':11,'Q':12,'K':13}
        f2 = {'A':14,'J':11,'Q':12,'K':13}
        if self.value == 'A' and other.value == 'A':
            return False
        return self.__mapToValue(f1) < other.__mapToValue(f2)

    def __gt__(self,other):
        f1 = {'A':14,'J':11,'Q':12,'K':13}
        f2 = {'A':1,'J':11,'Q':12,'K':13}
        if self.value == 'A' and other.value == 'A':
            return False
        return self.__mapToValue(f1) > other.__mapToValue(f2)
    
    def __ge__(self,other):
        f1 = {'A':14,'J':11,'Q':12,'K':13}
        f2 = {'A':1,'J':11,'Q':12,'K':13}
        if self.value == 'A' and other.value == 'A':
            return True
        return self.__mapToValue(f1) >= other.__mapToValue(f2)
    
    def __le__(self,other):
        f1 = {'A':1,'J':11,'Q':12,'K':13}
        f2 = {'A':14,'J':11,'Q':12,'K':13}
        if self.value == 'A' and other.value == 'A':
            return True
        return self.__mapToValue(f1) <= other.__mapToValue(f2)


class Hand:
    # Basic Hand Object
    def __init__(self, cards = None):
        self.hand = cards if cards else []
    
    def addCard(self, card):
        self.hand.append(card)
    
    def hasCard(self, card):
        for c in self.hand:
            if c == card: return True
        return False

    def __len__(self):
        return len(self.hand)
    
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        try:
            card = self.hand[self.index]
            self.index += 1
            return card
        except IndexError:
            raise StopIteration

    def removeAPassingCard(self, rule):
        index = -1
        for i, card in enumerate(self.hand):
            if card.passesRule(rule):
                index = i
                break
        if index != -1:
            return self.hand.pop(index) 
        return None

    def odds(self, rule):
        # Brute force to figure out odds that a rule will pass for the given cards.
        passes = 0
        for card in self.hand:
            if card.passesRule(rule): passes += 1
        return passes / len(self.hand)

    def removeCard(self, card):
        index = -1
        for i, c in enumerate(self.hand):
            if c == card:
                index = i
                break
        if index != -1:
            return self.hand.pop(index)
        return None

    def numberOfCards(self):
        return len(self.hand)

class Deck:
    # Basic Deck Object
    suits = [Suit.HEART, Suit.CLUB, Suit.DIAMOND, Suit.SPADE]
    values = ['A',2,3,4,5,6,7,8,9,10,'J','Q','K']
    
    def shuffle(self):
        # Shuffles the cards
        return shuffle(self.cards)
    
    def foldInDeck(self):
        # Adds a new deck of cards (52 cards) to the existing deck object
        for s in self.suits:
            for v in self.values:
                self.cards.append(Card(v,s))
        self.shuffle()
    
    def __init__(self, numOfDecks = 1):
        self.cards = []
        #initialize with numOfDecks decks
        for k in range (0, numOfDecks):
            self.foldInDeck()

    def deal(self):
        # Deal a card from the deck.
        try:
            return self.cards.pop()
        except:
            # If the deck is out of cards, add and shuffle a new deck and deal from that.
            print('* No more cards in deck. Folding in a new deck now. *')
            self.foldInDeck()
            return self.cards.pop()
    
    def getCards(self):
        return self.cards