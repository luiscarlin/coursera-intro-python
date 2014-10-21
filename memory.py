# Memory Game

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import pygame
import random

CANVAS_HEIGHT = 100
CANVAS_WIDTH = 800
CARD_WIDTH = CANVAS_WIDTH/16

# helpers 
def new_game():
    """
    resets the game 
    """
    global cards, exposed, state, first_card_index
    global second_card_index, turns
    
    cards = range(0,8)
    cards += cards
    random.shuffle(cards)

    exposed = [False] * 16
    
    state = 0
    first_card_index = None
    second_card_index = None
    turns = 0
     
# event handlers
def mouseclick(pos):
    """
    determines the state of the game and logic
    state 0 = game just started and person clicked on 1st card
    state 1 = person clicked on 2nd card
    state 2 = person clicked on 1st card for next match
                - if previous 2 cards same -> leave shown
                - if previous 2 cards not same -> flip
                
    pos - tuple (x, y) for location of click
    """
    global state, first_card_index, second_card_index, turns
    
    card_index_clicked = pos[0] / CARD_WIDTH

    if state == 0:
        # show 1st card selected
        exposed[card_index_clicked] = True
        
        # save the first card index
        first_card_index = card_index_clicked;
        turns += 1
        
        # next state
        state = 1
        
    elif state == 1:
        # show 2nd card selected if clicked on unexposed card
        if (not exposed[card_index_clicked]):
            exposed[card_index_clicked] = True
            
            # save the second card index
            second_card_index = card_index_clicked
            
            # next state
            state = 2
    else:
        # continue if clicked on unexposed card
        if (exposed[card_index_clicked] == False):   
            # did the other 2 match?
            if (cards[first_card_index] != cards[second_card_index]): 
                # did not match, so flip them
                exposed[first_card_index] = False
                exposed[second_card_index] = False
         
           # expose the first for a new match
            exposed[card_index_clicked] = True
            first_card_index = card_index_clicked
            
            turns += 1
            # next state
            state = 1
                    
def draw(canvas):
    """
    draws all the cards based on exposed list
    """
    for index in range(0, 16): 
        num_pos = [CARD_WIDTH/2 + index * CARD_WIDTH - 15, CANVAS_HEIGHT/2 + 20]
        card_pos = CARD_WIDTH * index
        
        if (not exposed[index]):
            # green squares
            canvas.draw_polygon([(card_pos, 0), (card_pos, CANVAS_HEIGHT), 
                                 (card_pos + CARD_WIDTH, CANVAS_HEIGHT), 
                                 (card_pos + CARD_WIDTH, 0)], 2, "Black", "Green")
        else:
            # exposed, so print number
            canvas.draw_text(str(cards[index]), num_pos, 60, 'White')

    # show turns so far
    label.set_text('Turns = ' + str(turns))
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory Game", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()