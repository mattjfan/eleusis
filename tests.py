#  © 2018 Matt Fan
# http://mattfan.me/

# Fun Fact: I built a writing habits website that reached #3 on Product Hunt's Product of the Day (https://www.producthunt.com/posts/writedaily)

from cardobjects import Card, Color, Suit, Hand, Deck
from eleusisobjects import Rule, Line, Players, Player
from rules import rules as myRules
from eleusis import *
import unittest
import itertools
from functools import reduce

class TestCard(unittest.TestCase):
    ace = Card('A', Suit.HEART)
    two = Card(2, Suit.SPADE)
    ten = Card(10, Suit.CLUB)
    king = Card('K', Suit.DIAMOND)
    def test_equals(self):
        self.assertTrue(Card('A', Suit.HEART) == Card('A', Suit.HEART))
        self.assertTrue(Card(6, Suit.SPADE) == Card(6, Suit.SPADE))
        self.assertFalse(Card(6, Suit.SPADE) == Card(6, Suit.HEART))
        self.assertFalse(Card('A', Suit.HEART) == Card('K', Suit.HEART))
        self.assertFalse(Card('A', Suit.HEART) == Card(3, Suit.HEART))
    def test_gt(self):
        self.assertFalse(Card('A', Suit.HEART) > Card('A', Suit.HEART))
        self.assertFalse(Card('A', Suit.HEART) > Card('A', Suit.SPADE))
        self.assertTrue(Card('A', Suit.HEART) > Card(2, Suit.HEART))
        self.assertTrue(Card('A', Suit.HEART) > Card('K', Suit.HEART))
        self.assertFalse(Card(2, Suit.HEART) > Card(3, Suit.HEART))
        self.assertFalse(Card(3, Suit.HEART) > Card(3, Suit.HEART))
    def test_ge(self):
        self.assertTrue(self.ace >= self.ace)
        self.assertTrue(self.ace >= self.two)
        self.assertTrue(self.ace >= self.king)
        self.assertTrue(self.king >= self.ten)
        self.assertTrue(self.two >= self.ace) #Ace can be low or high
        self.assertFalse(self.two >= self.king)
        self.assertFalse(self.two >= self.ten)
    def test_lt_le_ne(self):
        a1 = Card('A', Suit.HEART)
        a2 = Card('A', Suit.HEART)
        a3 = Card('A', Suit.SPADE)
        self.assertTrue(a1 == a2)
        self.assertFalse(a1 < a2) #Aces can be high or low, but are equal to other aces
        self.assertFalse(a1 > a2) 
        self.assertFalse(a2 == a3)
        self.assertTrue(a2 != a3)
        self.assertTrue(self.ace < self.king)
        self.assertTrue(a1 <= a3)
    def test_parse1(self):
        # Note: parse only works for exact strings, but more lenient parsing may be preferable
        # As such, strictness won't be tested, only validity on well-formed strings
        self.assertTrue(Card('A', Suit.HEART) == Card.parse('Ace of Hearts'))
        self.assertFalse(Card('A', Suit.HEART) == Card.parse('Ace of Spades'))
        self.assertTrue(None == Card.parse('Mumbo Jumbo'))
        self.assertTrue(Card(3, Suit.SPADE) == Card.parse('Three of Spades'))
        self.assertTrue(Card('K', Suit.DIAMOND) == Card.parse('King of Diamonds'))
        self.assertTrue(Card(4, Suit.CLUB) == Card.parse('Four of Clubs'))
        self.assertTrue(Card('A', Suit.HEART) == Card.parse('Ace of hearts'))
        # added handling for these cases:
        self.assertFalse(Card('A', Suit.HEART) == Card.parse(' Ace of  Spades'))
        self.assertTrue(Card(3, Suit.SPADE) == Card.parse('three OF spades'))
        self.assertTrue(Card(3, Suit.SPADE) == Card.parse('three of spades'))
        self.assertTrue(Card('K', Suit.DIAMOND) == Card.parse('King of Diamonds   '))

class TestPlayer(unittest.TestCase):
    pass

class TestPlayers(unittest.TestCase):
    pass

class TestHand(unittest.TestCase):
    def testHandBasics(self):
        h1 = Hand()
        h1.addCard(Card('A',Suit.HEART))
        h1.addCard(Card('A',Suit.SPADE))
        h1.addCard(Card(3,Suit.CLUB))
        h1.addCard(Card(5,Suit.CLUB))
        h1.addCard(Card('Q',Suit.CLUB))
        self.assertTrue(h1.hasCard(Card('A', Suit.HEART)))
        self.assertFalse(h1.hasCard(Card('A', Suit.CLUB)))
    
    def testDuplicateCardsInHand(self):
        h2 = Hand([Card('Q',Suit.CLUB),Card('Q',Suit.CLUB),Card('3',Suit.DIAMOND)]) #optional initialization test
        self.assertTrue(h2.hasCard(Card('Q', Suit.CLUB)))  
        h2.removeCard(Card('Q', Suit.CLUB))
        self.assertTrue(h2.hasCard(Card('Q', Suit.CLUB))) 
        h2.removeCard(Card('Q', Suit.CLUB)) 
        self.assertFalse(h2.hasCard(Card('Q', Suit.CLUB))) 
        self.assertTrue(len(h2) == 1)
    
    def testHandRuleMethods(self):
        Rule.setLine(Line())
        hasHeart = Rule('has heart', lambda c, m, d, h: c.suit == Suit.HEART)
        hasClub = Rule('has club', lambda c, m, d, h: c.suit == Suit.CLUB)
        h2 = Hand([Card('Q',Suit.CLUB),Card('Q',Suit.CLUB),Card('3',Suit.DIAMOND)])
        self.assertTrue(h2.odds(hasHeart) == 0) #testing odds work properly
        self.assertTrue(h2.odds(hasClub) > 0)
        self.assertTrue(h2.removeAPassingCard(hasClub) == Card('Q',Suit.CLUB)) #testing passing card removal
        self.assertTrue(len(h2) == 2)
        self.assertTrue(h2.removeAPassingCard(hasHeart) == None)


class TestDeck(unittest.TestCase):
    pass

class TestLine(unittest.TestCase):
    def testLineBasics(self):
        line = Line()
        self.assertTrue(line.getMainLine() == [])
        line.addToMain(Card('Q', Suit.CLUB))
        self.assertTrue(line.getMainLine()[-1] == Card('Q', Suit.CLUB))
        line.addToMain(Card('K', Suit.SPADE))
        line.addToSide(Card('Q', Suit.CLUB))
        line.addToSide(Card(3, Suit.HEART))
        self.assertTrue(line.getMainLine()[-1] == Card('K', Suit.SPADE))
        self.assertTrue(line.getFullLine()[-1] == Card(3, Suit.HEART))
        self.assertTrue(line.getFullLine()[0] == Card('Q', Suit.CLUB))
        self.assertTrue(line.getMainLine()[0] == Card('Q', Suit.CLUB))

class TestRule(unittest.TestCase):
    def testRuleBasics(self):
        line = Line()
        line.addToMain(Card('Q', Suit.CLUB))
        line.addToMain(Card(5, Suit.SPADE))
        line.addToSide(Card('Q', Suit.CLUB))
        line.addToSide(Card('K', Suit.HEART))
        hand = Hand([Card(3,Suit.SPADE), Card(7,Suit.CLUB)])
        Rule.setLine(line)
        Rule.setHand(hand)
        r1 = Rule('red cards', lambda c,m,d,h: c.suit.color() == Color.RED)
        r2 = Rule('less than 5', lambda c,m,d,h: c.valAsNum() < 5 )
        r3 = Rule('Greater than last card on MAINLINE', lambda c,m,d,h: c > m[-1])
        r4 = Rule('Same color as ACTUAL last card play', lambda c,m,d,h: c.suit.color() == d[-1].suit.color())
        r5 = Rule('Greater than or equal to highest card in hand', lambda c,m,d,h: reduce(lambda acc, card: acc and c >= card, h, True))

        self.assertTrue(Card('Q', Suit.HEART).passesRule(r1)) #test c
        self.assertTrue(r1.test(Card('Q', Suit.HEART))) # test card and rule methods
        self.assertFalse(r1.test(Card(3, Suit.SPADE)))
        self.assertTrue(r5.test(Card(7, Suit.SPADE))) # test h
        self.assertTrue(r5.test(Card('J', Suit.SPADE)))
        self.assertFalse(r5.test(Card(5, Suit.CLUB)))
        self.assertTrue(r4.test(Card('J', Suit.DIAMOND))) #test d
        self.assertFalse(r4.test(Card(5, Suit.CLUB)))
        self.assertTrue(r3.test(Card('J', Suit.DIAMOND))) #test m
        self.assertFalse(r3.test(Card(5, Suit.CLUB)))

    def testRuleComposition(self):
        line = Line()
        line.addToMain(Card('Q', Suit.CLUB))
        line.addToMain(Card(5, Suit.SPADE))
        line.addToSide(Card('Q', Suit.CLUB))
        line.addToSide(Card('K', Suit.HEART))
        hand = Hand([Card(3,Suit.SPADE), Card(7,Suit.CLUB)])
        Rule.setLine(line)
        Rule.setHand(hand)
        r1 = Rule('red cards', lambda c,m,d,h: c.suit.color() == Color.RED)
        r2 = Rule('less than 5', lambda c,m,d,h: c.valAsNum() < 5 )
        r3 = Rule('Greater than last card on MAINLINE', lambda c,m,d,h: c > m[-1])
        r4 = Rule('Same color as ACTUAL last card play', lambda c,m,d,h: c.suit.color() == d[-1].suit.color())
        r5 = Rule('Greater than or equal to highest card in hand', lambda c,m,d,h: reduce(lambda acc, card: acc and c >= card, h, True))

        r6 = r1.merge(r2) # merging simple rules
        self.assertTrue('(red cards and less than 5)' == r6.name)
        self.assertFalse(r6.test(Card('J', Suit.HEART)))
        self.assertTrue(r6.test(Card(3, Suit.HEART)))
        self.assertFalse(r6.test(Card(3, Suit.SPADE)))
        r7 = r3.merge(r5) # merging more complicated rules
        self.assertTrue(hand.odds(r7) == .5)
        r8 = r1.overlay(r2) # overlay test
        self.assertTrue(r8.test(Card(4,Suit.SPADE)))
        self.assertTrue(r8.test(Card(4,Suit.HEART)))
        self.assertFalse(r8.test(Card('K',Suit.SPADE)))
        self.assertTrue(r8.test(Card('K',Suit.HEART)))

class TestEleusis(unittest.TestCase):
    # pain to test because of all the terminal i/o.
    # decided to play test instead
    pass

if __name__ == '__main__':
    unittest.main()


# print (Suit.color(Suit.HEART) == Color.RED)
# myCard = (Card.parse('Ace of Hearts'))
# print(myCard.format())
# print(myCard.equals(Card('A', Suit.HEART)))
# myDeck = Deck()
# for n in range(0,53):
#     print(myDeck.deal().format())
# rule = rules[0]['rule']
# print(myCard.passesRule(rule))

# print(myRules[4].test(Card('A',Suit.HEART)))
# print(Card('A', Suit.HEART).passesRule(myRules[4]))

# class TestRuleOdds(unittest.TestCase):
#     def test_even_odds(self):
#         rule = Rule('Only Red Cards', lambda c, m , d, h: c.suit == Suit.HEART or c.suit == Suit.DIAMOND)
#         self.assertTrue(rule.odds() == .5)

# cycle = itertools.cycle(['a','b','c'])
# for n in range (0,20):
#     print(next(cycle))