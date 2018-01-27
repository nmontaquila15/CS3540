import random, sys, math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# constants
TIMER_TIME = 33
SIZE = 480
ROTATE_SPEED = 50
TRANSLATE_SPEED = 100

# keep track of which keys are down
keys_down = set()

# state / constants
root_translate = 240.
root_rotate = 45.
ROOT_LENGTH = 200.
ROOT_WIDTH = 20.

seg_rotate = 45.
seg_length = 100.
SEG_WIDTH = 15.

finger_rotate = 45.
FINGER_ROTATE_OFFSET = 45.
FINGER_LENGTH = 25.
FINGER_WIDTH = 5.


# function for drawing a square whose left edge is the y-axis and centered along the y-axis
def drawSquare():
    glBegin(GL_QUADS)
    glVertex2f(0.0, -0.5)
    glVertex2f(1.0, -0.5)
    glVertex2f(1.0,  0.5)
    glVertex2f(0.0,  0.5)
    glEnd()


# function for drawing robot arm
def drawArm():
    global root_translate, root_rotate, seg_rotate, seg_length, finger_rotate

    # TODO: draw the robot arm
    glPushMatrix()
    glTranslatef(root_translate, 0, 0)
    glRotatef(root_rotate, 0, 0, 1)
    glPushMatrix()
    glScalef(ROOT_LENGTH, ROOT_WIDTH, 1)
    drawSquare()
    glPopMatrix()
    glTranslatef(ROOT_LENGTH, 0, 0)
    glRotatef(seg_rotate, 0, 0, 1)
    glPushMatrix()
    glScalef(seg_length, SEG_WIDTH, 1)
    drawSquare()
    glPopMatrix()
    glTranslatef(seg_length, 0, 0)
    glPushMatrix()
    glTranslatef(0, SEG_WIDTH / 2.0, 0)
    glRotatef(finger_rotate, 0, 0, 1)
    glPushMatrix()
    glScalef(FINGER_LENGTH, FINGER_WIDTH, 1)
    drawSquare()
    glPopMatrix()
    glTranslatef(FINGER_LENGTH, 0, 0)
    glRotatef(-finger_rotate, 0, 0, 1)
    glScalef(FINGER_LENGTH, FINGER_WIDTH, 1)
    drawSquare()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, -SEG_WIDTH / 2.0, 0)
    glRotatef(-finger_rotate, 0, 0, 1)
    glPushMatrix()
    glScalef(FINGER_LENGTH, FINGER_WIDTH, 1)
    drawSquare()
    glPopMatrix()
    glTranslatef(FINGER_LENGTH, 0, 0)
    glRotatef(finger_rotate, 0, 0, 1)
    glScalef(FINGER_LENGTH, FINGER_WIDTH, 1)
    drawSquare()
    glPopMatrix()
    glPopMatrix()

# mouse button handler
def mouseButton(button, state, mx, my):
    global root_translate, root_rotate, seg_rotate, seg_length, finger_rotate

    if button != GLUT_LEFT_BUTTON:
        return

    if state != GLUT_DOWN:
        return

    # TODO: inverse kinematics for robot arm to reach clicked point


    inv = False
    move = (mx - root_translate)
    
    if move < 0:
        move = -move
        inv = True

    click = move **2 + (SIZE - my - 1)**2
    if click < (ROOT_LENGTH - seg_length)**2:
        return

    if click > (seg_length + ROOT_LENGTH)**2:
        return

    if inv:
        r = (move ** 2 + (SIZE - my - 1) ** 2 - ROOT_LENGTH ** 2 - seg_length ** 2)
        root_rotate = 180 - (math.atan2((SIZE - my - 1) , move) - math.atan2(seg_length * math.sin(math.acos(max(-1, min(1, r / (2 * ROOT_LENGTH * seg_length))))), ROOT_LENGTH + seg_length * math.cos(math.acos(max(-1, min(1, r / (2 * ROOT_LENGTH * seg_length))))))) * 180 / 3.14
        seg_rotate = -(math.acos(max(-1, min(1, r / (2 * ROOT_LENGTH * seg_length))))) * 180 / 3.14
    else:
        r = (move ** 2 + (SIZE - my - 1) ** 2 - ROOT_LENGTH ** 2 - seg_length ** 2)
        root_rotate = (math.atan2((SIZE - my - 1) , move) - math.atan2(seg_length * math.sin(math.acos(max(-1, min(1, r / (2 * ROOT_LENGTH * seg_length))))), ROOT_LENGTH + seg_length * math.cos(math.acos(max(-1, min(1, r / (2 * ROOT_LENGTH * seg_length))))))) * 180 / 3.14
        seg_rotate = (math.acos(max(-1, min(1, r / (2 * ROOT_LENGTH * seg_length))))) * 180 / 3.14

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
    global root_translate, root_rotate, seg_rotate, seg_length, finger_rotate

    dt = TIMER_TIME / 1000.0

    if 'q' in keys_down:
        root_rotate += ROTATE_SPEED * dt
    if 'w' in keys_down:
        root_rotate -= ROTATE_SPEED * dt

    if 'e' in keys_down:
        seg_rotate += ROTATE_SPEED * dt
    if 'r' in keys_down:
        seg_rotate -= ROTATE_SPEED * dt

    if 't' in keys_down:
        finger_rotate += ROTATE_SPEED * dt
    if 'y' in keys_down:
        finger_rotate -= ROTATE_SPEED * dt

    if 'a' in keys_down:
        root_translate -= TRANSLATE_SPEED * dt
    if 's' in keys_down:
        root_translate += TRANSLATE_SPEED * dt

    if 'd' in keys_down:
        seg_length -= TRANSLATE_SPEED * dt
    if 'f' in keys_down:
        seg_length += TRANSLATE_SPEED * dt


    glutPostRedisplay()
    glutTimerFunc(TIMER_TIME, timer, 0)


# function for displaying the game screen
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, SIZE, 0, SIZE);
 
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glColor3f(0.5, 0.5, 0.5)
    drawArm()

    glutSwapBuffers()


# startup
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(SIZE, SIZE)
glutCreateWindow('CS3540')
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutKeyboardUpFunc(keyboardup)
glutMouseFunc(mouseButton)
glutTimerFunc(TIMER_TIME, timer, 0)
glutMainLoop()
