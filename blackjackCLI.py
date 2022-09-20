import random
from os import system, name

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

#clear console method
def clear():
    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')

#creating card class#
class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

#creating Deck, shuffle function and single dealing#
class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list#
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = '' #starting competition deck empty#
        for card in self.deck:
            deck_comp += '\n' + card.__str__() #add each card object's string
        return 'The deck has' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

#creating a hand#
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

#creating Chips balance
class Chips:

    def __init__(self):
        self.total = 5000  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

#Taking bets#
def take_bet(chips):
    while True:
        print("You have %d dollars in the bank " %(chips.total))
        try:
            chips.bet = int(input('How much would you like to bet?  '))
        except ValueError:
            print("Sorry, a bet must be an integer!")
        else:
            if chips.bet > chips.total:
                print('Sorry, your bet cannot exceed {} '.format(chips.total))
            else:
                break

# taking hits#
def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

#player to take hits or stand
def hit_or_stand(deck,hand,chips):
    global playing
    global firstRound

    while True:

        if firstRound:
            x = input("\nWould you like to Hit or Stand or Double Down (h/s/d) ?: ")
            clear()
            firstRound = False
        else:
            x = input("\nWould you like to Hit or Stand (h/s) ?: ")
            clear()

        if x[0].lower() == 'h':
            hit(deck,hand)  # hit() function defined above

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        elif x[0].lower() == 'd':
            print("Player double downs.")
            if (chips.bet * 2) > chips.total:
                a = input("You don't have enough chips. All in? (y/n) : ")
                if a[0].lower() == 'y':
                    chips.bet = chips.total
                    hit(deck,hand)
                    playing = False
                else:
                    print("Continuing regular play without increasing your bet.")
                    continue
            else:
                chips.bet *= 2
                hit(deck,hand)
                playing = False

        else:
            print("Sorry, please try again.")
            continue
        # firstRound = False
        break

#player to take hits or stand on split hands
def hit_or_stand_on_split(deck,firstHand,secondHand,chips1,chips2):
        global playing
        global onFirstHand
        global onSecondHand

        global bustFirstHand
        global bustSecondHand
        global firstHand_chips
        global secondHand_chips
        global firstRound

        while True:
            if onFirstHand:

                if bustFirstHand:
                    print("\nPlayer busts on first hand!")
                    onFirstHand = False
                    onSecondHand = True

                else:

                    if firstRound:
                        x = input("\n1st HAND: Would you like to Hit or Stand or Double Down (h/s/d) ?: ")
                        firstRound = False
                    else:
                        x = input("\n1st HAND: Would you like to Hit or Stand (h/s) ?: ")

                    if x[0].lower() == 'h':
                        hit(deck,firstHand)

                    elif x[0].lower() == 's':
                        print("Player stands on 1st hand.")
                        onFirstHand = False
                        onSecondHand = True
                        firstRound = True   #sets up first round for second hand

                    elif x[0].lower() == 'd':
                        print("Player double downs on 1st hand.")
                        if (chips1.bet * 2) > chips1.total:
                            a = input("You don't have enough chips. All in? (y/n) : ")
                            if a[0].lower() == 'y':
                                chips1.bet = chips1.total
                                hit(deck,firstHand)
                                onFirstHand = False
                                onSecondHand = True
                                firstRound = True
                            else:
                                print("Continuing regular play without increasing your bet.")
                                continue
                        else:
                            chips1.bet *= 2
                            hit(deck,firstHand)
                            onFirstHand = False
                            onSecondHand = True
                            firstRound = True

                    else:
                        print("Sorry, please try again.")
                        continue
                    break

            # firstRound = True
            if onSecondHand:

                if firstRound:
                    x = input("\n2nd HAND: Would you like to Hit or Stand or Double Down (h/s/d) ?: ")
                    clear()
                    firstRound = False
                else:
                    x = input("\n2nd HAND: Would you like to Hit or Stand (h/s) ?: ")
                    clear()

                if x[0].lower() == 'h':
                    hit(deck,secondHand)

                elif x[0].lower() == 's':
                    print("Player stands. Dealer is playing.")
                    playing = False

                elif x[0].lower() == 'd':
                    print("Player double downs on 2nd hand.")
                    if (chips2.bet * 2) > chips2.total:
                        a = input("You don't have enough chips. All in? (y/n) : ")
                        if a[0].lower() == 'y':
                            chips2.bet = chips2.total
                            hit(deck,secondHand)
                            playing = False
                        else:
                            print("Continuing regular play without increasing your bet.")
                            continue
                    else:
                        chips2.bet *= 2
                        hit(deck,secondHand)
                        playing = False

                else:
                    print("Sorry, please try again.")
                    continue
                break


#player to split
def split(deck,hand):

    playerCards = getattr(hand, "cards")
    card1 = playerCards[0]
    card2 = playerCards[1]

    hand1 = Hand()
    hand1.add_card(card1)
    hand1.add_card(deck.deal())

    hand2 = Hand()
    hand2.add_card(card2)
    hand2.add_card(deck.deal())

    return hand1, hand2


#functions to display cards#
def show_some(player,dealer):
    clear()
    print("\nDealer's Hand:")
    print(" "*3 + "<HIDDEN CARD>")
    print(" "*2, dealer.cards[1])
    print("\nPlayer's Hand: ", *player.cards, sep= '\n' + " "*3)
    print("Player's Hand = ", player.value)

def show_all(player,dealer):
    clear()
    print("\nDealer's Hand:", *dealer.cards, sep='\n' + " "*3)
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand: ", *player.cards, sep= '\n' + " "*3)
    print("Player's Hand = ", player.value)

def show_some_with_split(player1st,player2nd,dealer):
    clear()
    print("\nDealer's Hand:")
    print("<card hidden>")
    print(dealer.cards[1])
    print("\nPlayer's 1st Hand: ", *player1st.cards, sep= '\n' + " "*3)
    print("Player's 1st Hand = ", player1st.value)
    print("\nPlayer's 2nd Hand: ", *player2nd.cards, sep= '\n' + " "*3)
    print("Player's 2nd Hand = ", player2nd.value)

def show_all_with_split(player1st,player2nd,dealer):
    clear()
    print("\nDealer's Hand:", *dealer.cards, sep='\n' + " "*3)
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's 1st Hand: ", *player1st.cards, sep= '\n' + " "*3)
    print("Player's 1st Hand = ", player1st.value)
    print("\nPlayer's 2nd Hand: ", *player2nd.cards, sep= '\n' + " "*3)
    print("Player's 2nd Hand = ", player2nd.value)

#function to compare player's first 2 cards for split
def compare_cards(player):
    playerCards = getattr(player, "cards")
    card1 = str(playerCards[0])
    card2 = str(playerCards[1])

    #get number or face of card
    card1 = card1.split()[0]
    card2 = card2.split()[0]

    if card1 == card2:
        return True
    else:
        return False

#functions to handle game scenarios#
def player_busts(player,dealer,chips):
    # player = str(player)
    if player[0] == 'f':
        print("\nPlayer busts on first hand!")
        chips.lose_bet()
    elif player[0] == 's':
        print("\nPlayer busts on second hand!")
        chips.lose_bet()
    else:
        print("\nPlayer busts!")
        chips.lose_bet()

def player_wins(player,dealer,chips):
    if player[0] == 'f':
        print("\nPlayer wins first hand!")
        chips.win_bet()
    elif player[0] == 's':
        print("\nPlayer wins second hand!")
        chips.win_bet()
    else:
        print("\nPlayer wins!")
        chips.win_bet()

def dealer_busts(player,dealer,chips):
    if player[0] == 'f':
        print("\nDealer busts! Player wins first hand!")
        chips.win_bet()
    elif player[0] == 's':
        print("\nDealer busts! Player wins second hand!")
        chips.win_bet()
    else:
        print("\nDealer busts!")
        chips.win_bet()

def dealer_wins(player,dealer,chips):
    if player[0] == 'f':
        print("\nDealer wins first hand!")
        chips.lose_bet()
    elif player[0] == 's':
        print("\nDealer wins second hand!")
        chips.lose_bet()
    else:
        print("\nDealer wins!")
        chips.lose_bet()

def push(player,dealer):
    if player[0] == 'f':
        print("\nDealer and Player tie first hand!")
    elif player[0] == 's':
        print("\nDealer and Player tie second hand!")
    else:
        print("\nDealer and Player tie! It's a push.")

def push_both(player1st,player2nd,dealer):
    print("\nDealer and Player tie both hands! It's a push.")



#NOW FOR THE GAME
# added to take care of hand object:
player = "player"
first = "first"
second = "second"

firstRound = True

player_chips = Chips()

firstHand_chips = Chips()
secondHand_chips = Chips()
while True:
    # Print an opening statement
    print("Let's play BlackJack!\n")

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    #hands for if player splits
    firstHand = Hand()
    secondHand = Hand()

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    splitting = False

    firstRound = True

    #prompt for split
    if compare_cards(player_hand):
        while True:
            choice = input("\nWould you like to split your cards (y/n) ?: ")

            if choice[0].lower() == 'y':
                new_player_hand = split(deck,player_hand)
                firstHand = new_player_hand[0]
                secondHand = new_player_hand[1]
                clear()
                show_some_with_split(firstHand,secondHand,dealer_hand)
                splitting = True

                # create separate bets on each hand
                firstHand_chips.total = player_chips.total
                firstHand_chips.bet = player_chips.bet
                secondHand_chips.total = player_chips.total
                secondHand_chips.bet = player_chips.bet
                # print(firstHand_chips.total, firstHand_chips.bet)
                # print(secondHand_chips.total, secondHand_chips.bet)

                # keep track of which hand playing on
                onFirstHand = True
                onSecondHand = False

                # noting hands player busts on
                bustFirstHand = False
                bustSecondHand = False

                break

            elif choice[0].lower() == 'n':
                splitting = False
                break

            # Reruns loop if player didn't choose y or n
            else:
                print("Sorry, please try again")
                continue


    while playing:  # recall this variable from our hit_or_stand function

        #play on both player hands
        if splitting:

            hit_or_stand_on_split(deck,firstHand,secondHand,firstHand_chips,secondHand_chips)

            # Show both hands but keep one dealer card hidden
            show_some_with_split(firstHand,secondHand,dealer_hand)

            if firstHand.value > 21:
                bustFirstHand = True

            if secondHand.value > 21:
                bustSecondHand = True

                break


        #hit or stand on one hand
        else:
            # Prompt for Player to Hit or Stand
            hit_or_stand(deck, player_hand, player_chips)

            # Show cards (but keep one dealer card hidden)
            show_some(player_hand,dealer_hand)

            # If player's hand exceeds 21, run player_busts() and break out of loop
            if player_hand.value >21:
                player_busts(player, dealer_hand, player_chips)

                break


    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    # if player didn't split
    if player_hand.value <= 21 and splitting == False:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand,dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player,dealer_hand,player_chips)

        else:
            push(player,dealer_hand)

    # If Player split
    elif splitting:

        # player busts both hands - dealer doesn't draw
        if bustFirstHand and bustSecondHand:
            player_busts(first,dealer_hand,firstHand_chips)
            player_busts(second,dealer_hand,secondHand_chips)

        else:
            while dealer_hand.value <17:
                hit(deck, dealer_hand)

            show_all_with_split(firstHand,secondHand,dealer_hand)

            # player bust first hand win second hand
            if bustFirstHand and dealer_hand.value < secondHand.value:
                player_busts(first,dealer_hand,firstHand_chips)
                player_wins(second,dealer_hand,secondHand_chips)

            # player bust first hand lose second hand
            elif bustFirstHand and dealer_hand.value > secondHand.value:
                player_busts(first,dealer_hand,firstHand_chips)
                dealer_wins(second,dealer_hand,secondHand_chips)

            # player bust first hand tie second hand
            elif bustFirstHand and dealer_hand.value == secondHand.value:
                player_busts(first,dealer_hand,firstHand_chips)
                push(second,dealer_hand)

            # player bust first hand dealer bust second hand
            elif bustFirstHand and dealer_hand.value > 21:
                player_busts(first,dealer_hand,firstHand_chips)
                dealer_busts(second,dealer_hand,secondHand_chips)

            # player wins first hand busts second hand
            elif dealer_hand.value < firstHand.value and bustSecondHand:
                player_wins(first,dealer_hand,firstHand_chips)
                player_busts(second,dealer_hand,secondHand_chips)

            # player loses first hand busts second hand
            elif dealer_hand.value > firstHand.value and bustSecondHand:
                dealer_wins(first,dealer_hand,firstHand_chips)
                player_busts(second,dealer_hand,secondHand_chips)

            # player ties first hand busts second hand
            elif dealer_hand.value == firstHand.value and bustSecondHand:
                push(first,dealer_hand)
                player_busts(second,dealer_hand,secondHand_chips)

            # dealer busts first hand player busts second hand
            elif dealer_hand.value > 21 and bustSecondHand:
                dealer_busts(first,dealer_hand,firstHand_chips)
                player_busts(second,dealer_hand,secondHand_chips)

            # dealer busts and player didn't bust either hand
            elif dealer_hand.value > 21 and bustFirstHand == False and bustSecondHand == False:
                dealer_busts(first,dealer_hand,firstHand_chips)
                dealer_busts(second,dealer_hand,secondHand_chips)

            # dealer wins both hands
            elif dealer_hand.value > firstHand.value and dealer_hand.value > secondHand.value:
                dealer_wins(first,dealer_hand,firstHand_chips)
                dealer_wins(second,dealer_hand,secondHand_chips)

            # player wins both hands
            elif dealer_hand.value < firstHand.value and dealer_hand.value < secondHand.value:
                player_wins(first,dealer_hand,firstHand_chips)
                player_wins(second,dealer_hand,secondHand_chips)

            # player wins first hand, dealer wins second
            elif dealer_hand.value < firstHand.value and dealer_hand.value > secondHand.value:
                player_wins(first,dealer_hand,firstHand_chips)
                dealer_wins(second,dealer_hand,secondHand_chips)
                print("\nNo money exchanged!")

            # player wins first hand, player and dealer tie second
            elif dealer_hand.value < firstHand.value and dealer_hand.value == secondHand.value:
                player_wins(first,dealer_hand,firstHand_chips)
                push(second,dealer_hand)

            # player and dealer tie first hand, player wins second
            elif dealer_hand.value == firstHand.value and dealer_hand.value < secondHand.value:
                push(first,dealer_hand)
                player_wins(second,dealer_hand,secondHand_chips)

            # dealer wins first hand, player wins second
            elif dealer_hand.value > firstHand.value and dealer_hand.value < secondHand.value:
                dealer_wins(first,dealer_hand,firstHand_chips)
                player_wins(second,dealer_hand,secondHand_chips)
                print("\nNo money exchanged!")

            # dealer wins first hand, player and dealer tie second
            elif dealer_hand.value > firstHand.value and dealer_hand.value == secondHand.value:
                dealer_wins(first,dealer_hand,firstHand_chips)
                push(second,dealer_hand)

            # player and dealer tie first hand, dealer wins second
            elif dealer_hand.value == firstHand.value and dealer_hand.value > secondHand.value:
                push(first,firstHand_chips)
                dealer_wins(second,dealer_hand,secondHand_chips)

            # tie on first hand, tie on second hand
            else:
                push_both(firstHand,secondHand,dealer_hand)

        player_chips.total = (firstHand_chips.total + secondHand_chips.total) - player_chips.total


    # Inform Player of their chips total
    print("\nUpdated amount in bank: ", player_chips.total)

    # Ask to play again
    new_game = input("Would you like to play again (y/n) ?: ")
    clear()

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Total amount left in the bank: $", player_chips.total)
        if player_chips.total <= 5000:
            print("\nMoney lost: $", 5000-player_chips.total)
        else:
            print("\nMoney gained: $", player_chips.total-5000)
        print("\nThanks for playing!")

        break

    
