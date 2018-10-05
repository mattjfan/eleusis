#  © 2018 Matt Fan
# http://mattfan.me/

# Fun Fact: In my sophomore year in college, I ran an incubator (https://startupshell.org/) 

from random import choice as randomChoice
from os import system, name
from time import sleep
from rules import rules as myRules
from cardobjects import Card, Color, Suit, Hand, Deck
from eleusisobjects import Rule, Line, Players, Player

# This file includes main game logic.

class Game:
    def __init__(self, rules = myRules, options = {}):
        self.rules = rules
        self.options = options
        self.STARTING_HAND_SIZE = 12 if 'starting_hand_size' not in self.options else self.options['starting_hand_size']

    @classmethod
    def clearScreen(cls):
        # Clears the screen. Keeps players from seeing each other's hands, looks nice. 
        _ = system('cls') if name == 'nt' else system('clear') 
    
    def initializeRound(self, rule):
        self.roundActive = True
        self.winner = None
        self.rule = rule
        self.deck = Deck(int(len(self.players)*self.STARTING_HAND_SIZE/40) + 1) # Determine how many decks to fold in to start
        self.line = Line()
        Rule.setLine(self.line)
        for player in self.players:
            player.hand = Hand()
            for n in range(0, self.STARTING_HAND_SIZE ):
                player.hand.addCard(self.deck.deal())
        self.line.addToMain(self.deck.deal())
        while True: # Keep cycling player turns until someone wins
            self.playTurn(self.players.nextPlayer())
            if self.roundActive == False:
                self.clearScreen()
                print(f"\n{self.winner.name} has WON this round!\nThe rule was {self.rule.name}\n")
                print('Cumulative scores for the entire game:')
                ranked = sorted(self.players.getPlayers(), key=lambda k: k.score, reverse=True)
                for player in ranked:
                    print(f"    {player.name}    :   {player.score}")
                print(f"\n{ranked[0].name} is leading for the game, with {ranked[0].score} points\n")
                makingChoice = True
                while makingChoice:
                    choice = input('Do you want to play another round? (y/n)')
                    if choice == 'y' or choice == 'Y':
                        self.initializeRound(randomChoice(self.rules)) # Call a new round.
                        makingChoice = False # Otherwise, exit.
                    elif choice == 'n' or choice =='N': 
                        return None
                    else:
                        print("I didn't recognize that command.")
                return None
    
    def start(self):
        # Starts the Game
        self.clearScreen()
        print("""
█▀▀ █░░ █▀▀ █░░█ █▀▀ ░▀░ █▀▀   █▀▀ █░█ █▀▀█ █▀▀█ █▀▀ █▀▀ █▀▀
█▀▀ █░░ █▀▀ █░░█ ▀▀█ ▀█▀ ▀▀█   █▀▀ ▄▀▄ █░░█ █▄▄▀ █▀▀ ▀▀█ ▀▀█
▀▀▀ ▀▀▀ ▀▀▀ ░▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀   ▀▀▀ ▀░▀ █▀▀▀ ▀░▀▀ ▀▀▀ ▀▀▀ ▀▀▀
        """)
        print("©2018 Matt Fan")
        print("\nThanks for playing my game! Eleusis is a game designed by Robert Abbott in 1956, where there's a secret rule, and players take turns placing cards onto a MAIN LINE that they think obey that rule.")
        print("My implementation is a streamlined, multi-player version (based on Eleusis Express variant) where players take turns placing cards to match a rule that's procedurally generated at the beginning of the round.")
        print("More info in the README. Enjoy!\n")
        print("First, let's figure out who's playing. One at a time, have each player type their name below.")
        players = []
        addingPlayers = True
        while addingPlayers:
            playerName = input("Name: ")
            if playerName not in players:
                players.append(playerName)
            else:
                print('Sorry, that name is already taken.')
            makingChoice = True
            while makingChoice:
                choice = input('Do you want to add another player? (y/n)')
                if choice == 'y' or choice == 'Y':
                    makingChoice = False
                elif choice == 'n' or choice =='N':
                    makingChoice = False
                    addingPlayers = False
                else:
                    print("I didn't recognize that command.")
        print("Great! Let's get started!")

        self.players = Players(players)

        self.initializeRound(randomChoice(self.rules)) # recursively calls new rounds until players quit
        self.clearScreen()
        print('\nThanks for playing Eleusis!') # exit program
        sleep(2)

    def playerWins(self, player):
        # Called when a player wins! Update scores and break out of player turns loop
        player.hand = Hand()
        print(f"Congrats {player.name}! You've won this round!")
        self.winner = player
        for p in self.players:
            p.score += self.STARTING_HAND_SIZE - p.hand.numberOfCards()
        self.roundActive = False
        sleep(1)

    def playTurn(self, player):
        # Play a single turn
        self.clearScreen()
        self.rule.setHand(player.hand)
        input(f"\nHi {player.name}, it's your turn! Press ENTER to continue.")
        self.clearScreen()
        print(f"\n--- It's {player.name}'s Turn! ---\nPlayer Cards:")
        cardCountString = "    |"
        for p in self.players:
            cardCountString += f"    {p.name}: {p.hand.numberOfCards()}    |" 
        print(cardCountString)
        print('\nTHE LINE (most recent at top): ')
        self.line.printLine();
        print('\nYOUR HAND: ')
        for card in player.hand:
            print(f"    {card.fancyFormat()}")     
        print('')
        while (True):
            choice = input('> Type the card you want to play (or NO PLAY): ') 
            chosenCard = Card.parse(choice) #If invalid parse, this just evaluates to None
            if choice == 'NO PLAY':
                if player.hand.odds(self.rule) == 0:
                    if player.hand.numberOfCards() == 1:
                        self.playerWins(player)
                        break
                    cardsToReplace = len(player.hand)
                    for c in player.hand:
                        self.line.addToSide(c)
                    player.hand = Hand()
                    for i in range(1, cardsToReplace):
                        player.hand.addCard(self.deck.deal())
                    print("Correct! The DEALER moves your cards onto the SIDE LINE, and replaces your hand sans one card.")
                    break
                else:
                    correctCard = player.hand.removeAPassingCard(self.rule)
                    self.line.addToMain(correctCard)
                    player.hand.addCard(self.deck.deal())
                    print('Sorry, you could have played something.')
                    print(f'The dealer moves the {correctCard.format()} from your hand to the MAIN LINE, and replaces it.')
                    break
            elif chosenCard and player.hand.hasCard(chosenCard) and chosenCard.passesRule(self.rule):
                if player.hand.numberOfCards() == 1:
                    self.playerWins(player)
                    break
                self.line.addToMain(player.hand.removeCard(chosenCard))
                print(f'Correct! You move the {chosenCard.format()} onto the MAIN LINE.')
                break
            elif chosenCard and player.hand.hasCard(chosenCard):
                self.line.addToSide(player.hand.removeCard(chosenCard))
                player.hand.addCard(self.deck.deal())
                print(f'Sorry, that selection fails the rule. The {chosenCard.format()} is moved to the SIDE LINE and replaced.')
                break
            elif chosenCard:
                print("    You don't have that card in your hand! Please choose a valid card.")
            else:
                print("    Which card is that? Please type the card exactly as it appears in YOUR HAND.")
                print("    You could also type 'NO PLAY' if you think there aren't any legal moves left.")  
        print('')
        if self.roundActive:
            input("That ends your turn! Press ENTER once you're done, then pass it over to the next player\n>")
    # Face cards

if __name__ == "__main__":
    
    # Initialize Standard Game
    myGame = Game(myRules)

    # Initialize Speed Round Variant:
    # myGame = Game(myRules, {'starting_hand_size': 5})
    
    # Start the Game
    myGame.start()

