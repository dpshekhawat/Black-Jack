import random

#### DECK #####

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

##### CARD class to the suit and rank of cards.

class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

### we now store 52 card objects in a list that can later be shuffled..

class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))  # build Card objects and add them to the list

    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

### TESTING ####

test_deck = Deck()
# To check that the deck has all cards listed remove # before print ...
#print(test_deck)


##############################
 #The Hand class is used to calculate the value of those cards using the values dictionary defined above.
 #It may also need to adjust for the value of Aces when appropriate.
#############################

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':  # just to know how many aces we actually have
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

### chips class just to keep track of a Player's starting chips, bets, and ongoing winnings.

class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

### function for placing bets from the chips that the user have

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips you want to bet: '))
        except:
            print('Please provide an integer!')
        else:
            if chips.bet > chips.total:
                print("Sorry you don't have enough chips for bet, you have {}".format(chips.total))
            else:
                break

### HIT or STAND ###
def hit(deck,hand):

    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop

    while True:

        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")
        if x[0].lower() == 'h':
            hit(deck,hand)  # hit() function defined above

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break

### Displaying Cards ###

def show_some(player,dealer):

    print("Dealer's hand:")
    print("one card is hidden")
    print(dealer.cards[1])
    print('\n')
    print("Players hand:")
    for card in player.cards:
        print(card)

def show_all(player,dealer):

    print("Dealer's hand:")
    for card in dealer.cards:
        print(card)
    print('\n')
    print("Player's hand:")
    for card in player.cards:
        print(card)

### DIFFERENT SCENARIOS OF GAMEPLAY ####

def player_busts(player_hand,dealer_hand,player_chips):
    print('Player busts!')
    Chips.lose_bet()

def player_wins(player_hand,dealer_hand,player_chips):
    print('Player wins!')
    Chips.win_bet()

def dealer_busts(player_hand,dealer_hand,player_chips):
    print('Player wins!, Dealer busts!')
    Chips.win_bet()

def dealer_wins(player_hand,dealer_hand,player_chips):
    print('Dealer wins')
    Chips.lose_bet()

def push(player,dealer):
    print('Player and Dealer tie, PUSH')


### GAMEPLAY ###

while True:
    # Print an opening statement

    print('Welcome to BLACKJACK')
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)

            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 21
    if player_hand.value <=21:

        while dealer_hand.value < player_hand.value:
            hit(deck,dealer_hand)

        # Showing all cards
        show_all(player_hand,dealer_hand)

        # Runnning different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)



    # Informing Player of their chips total
    print('\n Player total chips are at: {}'.format(player_chips.total))

    # Asking to play again
    new_game = input("Would you like to play another hand? y/n")
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thank you for playing!See you again")
        break
