#  © 2018 Matt Fan
# http://mattfan.me/

# Fun Fact: Last Summer, I worked on a two-person dev team to build a full-stack web application for Bespoke Investment (https://www.bespokepremium.com/)

from cardobjects import Card, Color, Suit, Hand, Deck
from eleusisobjects import Rule
from functools import reduce

# You can add your own rules here.
# A Rule is initialized with a String describing it, and a function that takes the following parameters and returns a Boolean

# c is the Card being played
# m is a List of the Cards played on the main line (with first card at index zero)
# d is the entire line, as a List of Dictionaries [{'main': Card, 'side':[Card]}]
# h is the player's current Hand

# Some helper functions. To add your own rules, scroll down to the 'rules' list
def threeInARow(c, m, d, h):
    colorCount = 0
    color = None
    for i in range(1,3 +1):
        try:
            if color == None:
                color = m[-i].suit.color()
            elif color != m[-i].suit.color():
                break
            colorCount += 1
        except:
            break
    return c.suit.color() != color if colorCount == 3 else c.suit.color() == color

# I've written some basic rules to start.
# To add your own, simply add the rule to the rules array below.

rules = [
    # Examples:
    # 'Samples of easy secret rules:'
    Rule(
        'If the last card on the MAINLINE was red, play a black card. If the last card on the MAINLINE was black, play a red card.',
        lambda c, m, d, h: m[-1].suit.color() != c.suit.color()
    ),
    Rule(
        'If the last card on THE MAINLINE was a spade, play a heart; if it was a heart, play a diamond; if it was diamond, play club; and if it was club, play a spade.',
        lambda c, m, d, h: { Suit.SPADE: Suit.HEART, Suit.HEART: Suit.DIAMOND, Suit.DIAMOND: Suit.CLUB, Suit.CLUB: Suit.SPADE }[m[-1].suit] == c.suit
    ),
    Rule(
        'The cards on the MAINLINE must follow this pattern: three red cards, then three black, then three red, then three black, etc.',
        threeInARow
    ),
    Rule(
        'If the last card is an odd-numbered card, play an even-numbered card; if the last is even, play an odd. [When numbers are involved, ace is usually 1 (odd), jack is 11 (odd), queen is 12 (even), and king is 13 (odd).',
        lambda c, m, d, h: c.valAsNum() % 2 != m[-1].valAsNum() % 2
    ),
    Rule(
        'If the last card on the MAINLINE is among the cards ace to 7, play a card 8 to king. If it is among 8 to king, play ace to 7.',
        lambda c, m, d, h: (m[-1].valAsNum() <= 7 and c.valAsNum() > 7) or (m[-1].valAsNum() >= 8 and c.valAsNum() < 8)
    ),
    Rule(
        'Play a card with a number that is 1, 2, or 3 higher than the number of the last card on the MAINLINE. The numbers can “turn-the-corner.”',
        lambda c, m, d, h: 1 <= c.valAsNum() - m[-1].valAsNum() <= 3 or -12 <= c.valAsNum() - m[-1].valAsNum() <= -10
    ),
    
    # 'Samples of hard secret rules:'
    Rule(
        'If the last card on the MAINLINE is an odd-numbered card, play a red card. If the last card is even, play a black card.',
        lambda c, m, d, h: c.suit.color() == Color.RED if m[-1].valAsNum() % 2 == 1 else c.suit.color() == Color.BLACK
    ),
    Rule(
        'The card played must be the same suit or the same number as the last card on the MAINLINE.',
        lambda c, m, d, h: c.suit == m[-1].suit or c.valAsNum() == m[-1].valAsNum()
    ),
    Rule(
        'If the last card on the MAINLINE is black, play a card with a number that is equal to or lower than the number of the last card. If the last card on the MAINLINE is red, play a card equal to or higher than the last card.',
        lambda c, m, d, h: c.valAsNum() <= m[-1].valAsNum() if m[-1].suit.color() == Color.BLACK else c.valAsNum() >= m[-1].valAsNum()
    )

]

