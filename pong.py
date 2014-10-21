# PONG

import simplegui
import random

# globals **************************************

# table
WIDTH = 600
HEIGHT = 400

# ball
BALL_RADIUS = 20

ball_pos = [0, 0]
ball_vel = [0, 0]

# paddle
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

paddle1_pos = 0
paddle1_vel = 0

paddle2_pos = 0
paddle2_vel = 0

# direction
LEFT = False
RIGHT = True

# scores
score1 = 0
score2 = 0


# helpers **************************************
def spawn_ball(direction):
    """
    initializes ball position to the middle of the table
    
    direction - True (RIGHT) or False (LEFT)
    """
    global ball_pos, ball_vel
    
    # set position to middle
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    # set direction
    if direction == RIGHT:
        ball_vel = [random.randrange(60,180) / 60, -random.randrange(120,240) / 60]
    elif direction == LEFT: 
        ball_vel = [-random.randrange(60,180) / 60, -random.randrange(120,240) / 60]
    else:
        print "Error!: Passed wrong type"

# Event Handlers *******************************
def new_game():
    """ 
    sets all the initial values and starts the game 
    """
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, score1, score2 
    
    score1 = 0
    score2 = 0
    
    paddle1_pos = HEIGHT / 2
    paddle1_vel = 0
    
    paddle2_pos = HEIGHT / 2
    paddle2_vel = 0
    
    spawn_ball(RIGHT)   

def draw(canvas):
    """
    draws, updates positions, checks for
    """
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    

    # ball **************************************
    # bounce top wall
    if ball_pos[1] - BALL_RADIUS <= 0:
        ball_vel[1] = ball_vel[1] * -1
    # bounce bottom wall
    if ball_pos[1] + BALL_RADIUS >= HEIGHT - 1:
        ball_vel[1] = ball_vel[1] * -1
   
    # right gutter line    
    if ball_pos[0] + BALL_RADIUS >=  WIDTH - 1 - PAD_WIDTH: 
        # ball on line, so check if paddle 
        if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            # in paddle range, so bounce left and increment speed by 10%
            ball_vel[0] = (ball_vel[0] + (ball_vel[0] * 0.10)) * -1
        else:
            # in gutter
            score1 += 1
            spawn_ball(LEFT) 
            
    # left gutter line        
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH: 
        # ball on line, so check if paddle 
        if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            # in paddle range, so bounce left and increment speed by 10% 
            ball_vel[0] = (ball_vel[0] + (ball_vel[0] * 0.10)) * -1
        else:
            # in gutter
            score2 += 1
            spawn_ball(RIGHT)
        
    # update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # paddles **************************************
    
    # next paddle position
    next_paddle1_pos = paddle1_pos + paddle1_vel
    next_paddle2_pos = paddle2_pos + paddle2_vel
    
    # top and botom walls for paddle1
    if (next_paddle1_pos - HALF_PAD_HEIGHT) <= 0:
        # paddle 1 will go through top wall on next move
        # move paddle to top
        paddle1_pos = HALF_PAD_HEIGHT
    elif (next_paddle1_pos + HALF_PAD_HEIGHT) >= HEIGHT - 1:
        # paddle 1 will go through bottom wall on next move
        # move paddle to bottom
        paddle1_pos = HEIGHT - 1 - HALF_PAD_HEIGHT
    else:
        # no walls on next move, so good to update
        paddle1_pos = next_paddle1_pos
    
    # top and botom walls for paddle2
    if (next_paddle2_pos - HALF_PAD_HEIGHT) <= 0:
        # paddle 2 will go through top wall on next move
        # move paddle to top
        paddle2_pos = HALF_PAD_HEIGHT
    elif (next_paddle2_pos + HALF_PAD_HEIGHT) >= HEIGHT - 1:
        # paddle 2 will go through bottom wall on next move
        # move paddle to bottom
        paddle2_pos = HEIGHT - 1 - HALF_PAD_HEIGHT
    else:
        # no walls on next move, so good to update
        paddle2_pos = next_paddle2_pos

    # draw left paddle
    canvas.draw_line((HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT), 
                     (HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT), 
                     PAD_WIDTH, 'White')

    # draw right paddle
    canvas.draw_line((WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), 
                     (WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT), 
                    PAD_WIDTH, 'White')
    
    # draw scores ****************
    canvas.draw_text(str(score1), (WIDTH/3, 50), 40, 'Red')
    canvas.draw_text(str(score2), (2*WIDTH/3, 50), 40, 'Red')
    
def keydown(key):
    """
    moves paddles up or down
    """
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["up"]: 
        paddle2_vel = -5
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 5

    if chr(key) == 'W': 
        paddle1_vel = -5
    elif chr(key) == 'S':
        paddle1_vel = 5
        
def keyup(key):
    """
    stops paddles
    """
    global paddle1_vel, paddle2_vel

    if chr(key) is 'W' or chr(key) is 'S':
        paddle1_vel  = 0
        
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel  = 0

def restart_button():
    """ button that restarts the game """
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart_button)

# start frame
new_game()
frame.start()
