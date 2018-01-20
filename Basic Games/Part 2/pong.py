import random, sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# constants
TIMER_TIME = 33
INSET = 0.1
PADDLE_SPEED = 0.3
BALL_SPEED = 0.4
PADDLE_1_POSITION_X = 0.05
PADDLE_2_POSITION_X = 0.95
PADDLE_SIZE = 0.1
BALL_SIZE = 0.02
direction_options = [-1, 1]

# keep track of which keys are down
keys_down = set()

# game state
paddle_1_score = 0
paddle_2_score = 0
paddle_1_position_y = 0.5
paddle_2_position_y = 0.5
ball_position_x = 0.5
ball_position_y = 0.5
ball_direction_x = None # note: if None, ball needs to be reset
ball_direction_y = None
ball_is_moving = False


# function to draw a rectangle
def drawrect(cx, cy, w2, h2):
    glBegin(GL_QUADS)
    glVertex2f(cx - w2, cy - h2)
    glVertex2f(cx + w2, cy - h2)
    glVertex2f(cx + w2, cy + h2)
    glVertex2f(cx - w2, cy + h2)
    glEnd()


# function to draw a string
def drawstring(x, y, left, s):
    CHAR_SIZE = 104.76
    glPushMatrix()
    glTranslatef(x, y, 0.0)
    if left:
        glTranslatef(-len(s) / 20.0, 0.0, 0.0)
    glScalef(1.0/CHAR_SIZE, 1.0/CHAR_SIZE, 1.0)
    glScalef(1.0/20.0, 1.0/20.0, 1.0)
    for c in s:
        glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(c))
    glPopMatrix()


# normalize ball direction
def normalize_ball_direction():
    global ball_position_x, ball_position_y, ball_direction_x, ball_direction_y
    l = (ball_direction_x ** 2 + ball_direction_y ** 2) ** 0.5
    if l < 0.001:
        ball_position_x = None
    else:
        ball_direction_x /= l
        ball_direction_y /= l


# function for handling key down
def keyboard(c, x, y):
    global keys_down

    keys_down.add(c.lower())


# function for handling key up
def keyboardup(c, x, y):
    global keys_down

    keys_down.discard(c.lower())


# handle state update on timer
def timer(value):
    global keys_down
    global paddle_1_position_y, paddle_2_position_y
    global ball_position_x, ball_position_y, ball_direction_x, ball_direction_y
    global paddle_1_score, paddle_2_score
    global ball_is_moving

    dt = TIMER_TIME / 1000.0

    #moving paddle 1 up
    if ('w' in keys_down):
        paddle_1_position_y += dt * PADDLE_SPEED
        ball_is_moving = True
        if (paddle_1_position_y >= 0.847):
            paddle_1_position_y = 0.847
    #moving paddle 1 down
    if ('s' in keys_down):
        paddle_1_position_y -= dt * PADDLE_SPEED
        ball_is_moving = True
        if (paddle_1_position_y <= 0.151):
            paddle_1_position_y = 0.151
    #moving paddle 2 up
    if ('i' in keys_down):
        ball_is_moving = True
        paddle_2_position_y += dt * PADDLE_SPEED
        if (paddle_2_position_y >= 0.847):
            paddle_2_position_y = 0.847
    #moving paddle 2 down
    if ('k' in keys_down):
        ball_is_moving = True
        paddle_2_position_y -= dt * PADDLE_SPEED
        if (paddle_2_position_y <= 0.151):
            paddle_2_position_y = 0.151
    #initialize ball movement
    if (ball_is_moving == True and ball_direction_x == None and ball_direction_y == None):
        ball_direction_x = random.choice(direction_options)
        ball_direction_y = random.choice(direction_options)

    #move ball
    if (ball_is_moving == True):
        ball_position_x += dt * BALL_SPEED * ball_direction_x
        ball_position_y += dt * BALL_SPEED * ball_direction_y

    #reset ball after score
    if (ball_position_x >= 1.0):
        ball_position_x = 0.5
        ball_position_y = 0.5
        ball_direction_x = None
        ball_direction_y = None
        ball_is_moving = False
        paddle_1_score += 1

    if (ball_position_x <= 0):
        ball_position_x = 0.5
        ball_position_y = 0.5
        ball_direction_x = None
        ball_direction_y = None
        ball_is_moving = False
        paddle_2_score += 1

    #ball can't go through walls
    if (ball_position_y >= 0.88 or ball_position_y <= 0.12):
        ball_direction_y *= -1

    #ball bounces off of paddles
    if (ball_position_x < 0.065 and (ball_position_y <= paddle_1_position_y + 0.1 and ball_position_y >= paddle_1_position_y - 0.1)):
        ball_direction_x = 1

    if (ball_position_x > 0.935 and (ball_position_y <= paddle_2_position_y + 0.1 and ball_position_y >= paddle_2_position_y - 0.1)):
        ball_direction_x = -1
        
    glutPostRedisplay()
    glutTimerFunc(TIMER_TIME, timer, 0)


# function for displaying the game screen
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0.0, 1.0, 0.0, 1.0);
 
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glColor3f(1, 1, 1)

    drawrect(PADDLE_1_POSITION_X, paddle_1_position_y, BALL_SIZE/2, PADDLE_SIZE/2)
    drawrect(PADDLE_2_POSITION_X, paddle_2_position_y, BALL_SIZE/2, PADDLE_SIZE/2)
    drawrect(ball_position_x, ball_position_y, BALL_SIZE/2, BALL_SIZE/2)

    glBegin(GL_LINES)
    glVertex2f(0.0, INSET)
    glVertex2f(1.0, INSET)
    glVertex2f(0.0, 1.0 - INSET)
    glVertex2f(1.0, 1.0 - INSET)
    glEnd()

    drawstring(0.025, 0.925, False, str(paddle_1_score))
    drawstring(0.975, 0.925, True, str(paddle_2_score))

    glutSwapBuffers()


# startup
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(640, 640)
glutCreateWindow('CS3540')
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutKeyboardUpFunc(keyboardup)
glutTimerFunc(TIMER_TIME, timer, 0)
glutMainLoop()
