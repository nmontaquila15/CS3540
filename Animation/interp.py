import math, random, sys, time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# constants
TIMER_TIME = 33
SIZE = 480
INTERP_TIME = 1.5
CIRCLE_SIZE = 20
START_XY = 150
END_XY = 330

INTERP_LINEAR = 1
INTERP_CUBIC = 2
INTERP_CARTOON = 3

# state
start_time = None
interp_mode = None


# function for drawing a circle
def drawCircle():
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0.0, 0.0)
    for ii in xrange(32):
        theta = 2. * math.pi * ii / 31.
        glVertex2f(math.cos(theta), math.sin(theta))
    glEnd()


# draws state based on animation time
def drawAnimation(t, swap, mode):
    if swap:
        src, dst = END_XY, START_XY
    else:
        src, dst = START_XY, END_XY

    xy = src

    # TODO: implement interpolations based on mode
    if mode == INTERP_LINEAR:
        t1 = t

    elif mode == INTERP_CUBIC:
        t1 = 3 * t**2 - 2 * t**3

    elif mode == INTERP_CARTOON:
        t1 = -0.6 * math.sin(1.4 * math.pi * t + 0.9) + 0.5

    xy = src * (1 - t1) + t1 * dst

    glPushMatrix()
    glTranslatef(xy, xy, 0)
    glScalef(CIRCLE_SIZE, CIRCLE_SIZE, 1)
    drawCircle()
    glPopMatrix()


# function for handling key down
def keyboard(c, x, y):
    global start_time, interp_mode

    if c.lower() == '1':
        interp_mode = INTERP_LINEAR
    elif c.lower() == '2':
        interp_mode = INTERP_CUBIC
    elif c.lower() == '3':
        interp_mode = INTERP_CARTOON
    else:
        return

    start_time = time.time()


# handle state update on timer
def timer(value):
    glutPostRedisplay()
    glutTimerFunc(TIMER_TIME, timer, 0)


# function for displaying the game screen
def display():
    global start_time, interp_mode

    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, SIZE, 0, SIZE);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glColor3f(0.8, 0.9, 0.9)
    if start_time == None:
        drawAnimation(0.0, False, INTERP_LINEAR)
    else:
        part = int((time.time() - start_time) / INTERP_TIME)
        t = max(0.0, min(1.0, (time.time() - (start_time + INTERP_TIME * part)) / INTERP_TIME))
        if part % 4 == 0:
            drawAnimation(t, False, interp_mode)
        elif part % 4 == 1:
            drawAnimation(1, False, interp_mode)
        elif part % 4 == 2:
            drawAnimation(t, True, interp_mode)
        else:
            drawAnimation(1, True, interp_mode)

    glutSwapBuffers()


# startup
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(SIZE, SIZE)
glutCreateWindow('CS3540')
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutTimerFunc(TIMER_TIME, timer, 0)
glutMainLoop()