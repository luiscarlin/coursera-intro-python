# Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# Classes #############################################
class Card:
    """ represents 1 card """
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
class Hand:
    """ represents a collection of Cards """
    def __init__(self):
        self.hand = []

    def __str__(self):
        """ returns a string representation of a hand """
        to_return = "Value: " + str(self.get_value()) + "\n"
        to_return += "Cards: " + str(len(self.hand)) + " card(s)\n"
                
        for card in self.hand:
            to_return += str(card) + "\n"   
            
        return to_return
        
    def add_card(self, card):
        """ adds a card object to a hand """
        self.hand.append(card)

    def get_value(self):
        """ sums the value of the hand. Only adds aces if less than 21 """
        score = 0
        
        # add all values (ace = 1)
        for card in self.hand: 
            score +=  VALUES[card.get_rank()]
            
        # add 10 to ace if we can      
        if (score != 0 and self.contains_ace() and (score + 10 <= 21)):
            score += 10
        
        return score
    
    def contains_ace(self):
        """ true if hand contains ace """ 
        found = False
        
        for card in self.hand:
            if card.get_rank() == 'A':
                found = True
                break
        return found
    
    def draw(self, canvas, pos):
        """ draws a hand of cards starting at pos """
        for index in range(len(self.hand)):
            self.hand[index].draw(canvas, [pos[0] + index * 100, pos[1]])
        
class Deck:
    """ collection of cards """
    def __init__(self):
        self.deck = []
        
        # populate the deck 
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        """ shuffles deck of cards """ 
        random.shuffle(self.deck)

    def deal_card(self):
        """ deals a card object from the deck """
        return self.deck.pop()
    
    def __str__(self):
        """ string representation of a deck """
        to_return = "# cards: " + str(len(self.deck)) + "\n"
        
        if (len(self.deck) > 0):
           for card in self.deck:
                to_return += str(card) + " "
        return to_return

# Event handlers ###################################################
def deal():
    """ start a new game """
    global outcome, in_play, deck, player_hand, dealer_hand, score
    
    if in_play: 
        outcome = "Forfeit. You lose!"
        score -= 1
    else:
        outcome = ""

    deck = Deck()
    deck.shuffle()
    
    dealer_hand = Hand()
    player_hand = Hand()
    
    # deal 2 cards to dealer and player
    for i in range(0,2):
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
    
    in_play = True

def hit():
    """ add card to player's hand. Check if bust """
    global in_play, player_hand, outcome, score
 
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
        
        if player_hand.get_value() > 21:
            # player went bust
            outcome = "You went bust. You lose!"
            in_play = False
            score -= 1
       
def stand():
    """ add cards to dealer. Check who won """
    global in_play, dealer_hand, outcome, score, player_hand
   
    if in_play: 
        while (dealer_hand.get_value() < 17):
            # hit dealer 
            dealer_hand.add_card(deck.deal_card())
            
        # check if the dealer busted
        if dealer_hand.get_value() > 21:
            outcome = "Dealer went bust. You win!"
            score += 1
        else:
            # at this point, both are under 21, so compare (dealer wins ties)
            if dealer_hand.get_value() < player_hand.get_value():
                # player wins
                outcome = "You win!"
                score += 1
            else:
                # dealer wins
                outcome = "You lose!"
                score -= 1     
        in_play = False
    
def draw(canvas):
    global player_hand, dealer_hand, outcome

    # draw hands
    dealer_hand.draw(canvas, [50, 150])
    player_hand.draw(canvas, [50, 350])   
    
    # cover dealer's hole card if in play
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [50 + CARD_BACK_CENTER[0], 150 + CARD_BACK_CENTER[1]], 
                          CARD_BACK_SIZE)   
  
    # print text
    canvas.draw_text('Dealer', (50, 130), 20, 'Black', "monospace")
    canvas.draw_text('Player', (50, 330), 20, 'Black', "monospace")
    canvas.draw_text('Blackjack', (170, 50), 50, 'Black', "monospace")
    canvas.draw_text('Score: ' + str(score), (250, 100), 20, 'white', "monospace")
    canvas.draw_text(outcome, (250, 130), 20, 'Black', "monospace")
    
    if in_play:
        canvas.draw_text("Hit or Stand?", (250, 330), 20, 'Black', "monospace")
    else:
        canvas.draw_text("New Deal?", (250, 330), 20, 'Black', "monospace")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()