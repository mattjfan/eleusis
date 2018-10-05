#  © 2018 Matt Fan
# http://mattfan.me/

# Fun Fact: Last Spring, I designed and built an image-projecting drone from scratch (http://mattfan.me/portfolio/hovar/)

from itertools import cycle
from functools import reduce
from cardobjects import Card, Color, Suit, Hand, Deck

class Player:
    def __init__(self, name, hand=Hand()):
        self.name =  name
        self.hand = hand
        self.score = 0 


class Players:
    def __init__(self, players):
        self.players = {}
        for player in players:
            self.players[player] = Player(player)
        self.player_names = cycle(players)
    
    def nextPlayer(self):
        return self.players[next(self.player_names)]
    
    # Apply some callback that modifies each player
    # Callback takes a Player object, and returns nothing 
    def mapPlayers(self, callback): #deprecated. Use for ... in loop instead
        for player in self.players.values():
            callback(player)
    
    def getPlayers(self):
        return self.players.values()

    def __iter__(self):
        self.__iterable = iter(self.players.values())
        return self
    
    def __next__(self):
        return self.__iterable.__next__()

    def __len__(self):
        return len(self.players)
    

class Line:
    def __init__(self):
        self.line = []
    
    def addToMain(self, card):
        self.line.append({'main': card, 'side':[]})
    
    def addToSide(self, card):
        self.line[-1]['side'].append(card)

    def getMainLine(self):
        return list(map(lambda x: x['main'], self.line))
    
    def getFullLine(self):
        return reduce(lambda acc, curr: acc + [curr['main']] + curr['side'], self.line, [])

    # Confusing nomenclature- prints out the LINE object, but takes more than one line on the terminal
    def printLine(self):
        print(f"   {'MAIN LINE:':27}   SIDE LINE:")
        for row in reversed(self.line):
            sideLine = ''
            for card in row['side']:
                sideLine += f' {card.shortFormat()}'
            print(f"    {row['main'].fancyFormat():27}| {sideLine}")


class Rule:
    hand = None
    line = None
    # Rule object for Eleusis
    @classmethod
    def setLine(cls, line):
        cls.line = line

    @classmethod
    def setHand(cls, hand): #Set the fourth arg for callback f (player hand)
        cls.hand = hand

    def __init__(self, name, callback):
        self.name = name
        self.f = callback

    def test(self, card): # Dependent on mainline implementation in eleusis.py file :(. Potential refactor
        return self.f(card, self.line.getMainLine(), self.line.getFullLine(), self.hand)
    
    def merge(self, other): # Creates a stricter composite rule from logical and of two other rules
        return Rule(f"({self.name} and {other.name})", lambda c, m, d, h: self.f(c,m,d,h) and other.f(c,m,d,h))

    def overlay(self, other): # Creates a more lenient rule from logical or of two other
        return Rule(f"({self.name} or {other.name})", lambda c, m, d, h: self.f(c,m,d,h) or other.f(c,m,d,h))

    # def odds(self): # Tests the odds of a rule against a new deck of cards
    #     try:
    #         return Card.odds(Deck(1).getCards(), self) # TODO: write tests
    #     except:
    #         return -1
