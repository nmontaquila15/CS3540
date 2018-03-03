import random, sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# constants
PIXEL_SIZE = 10
SIZE = 40
LINE_COLOR = 128

# view state
pixels = [[(0, 0, 0) for i in xrange(SIZE)] for i in xrange(SIZE)] # grid of pixels to be displayed
currMouse = None # current position of mouse
lastMouse = None # previous position of mouse click

# function to draw a line into pixels
def drawline(p0, p1):
    global pixels

    line_color = (LINE_COLOR, LINE_COLOR, LINE_COLOR)

    x0,y0 = p0
    x1,y1 = p1

    if y0 == y1:
        if x0 > x1:
           x0,x1 = x1,x0
        for x in xrange(x0, x1+1):
            pixels[x][y0] = line_color
        return
    
    if x0 == x1:
        if y0 > y1:
           y0,y1 = y1,y0
        for y in xrange(y0, y1+1):
            pixels[x0][y] = line_color
        return
    
    deltaX = x1 - x0
    deltaY = y1 - y0

    if abs(deltaX) >= abs(deltaY):
        if x0 > x1:
            x0,x1 = x1, x0
            y0,y1 = y1, y0
        deltaX = x1 - x0
        deltaY = y1 - y0
        slope = abs(float(deltaY) / deltaX)
        subSlope = 0.0
        y = y0
        for x in xrange(x0, x1 + 1):
            pixels[x][y] = line_color
            subSlope += slope
            while subSlope >= 0.5:
                if deltaY > 0:
                    y += 1
                else:
                    y -= 1
                subSlope -= 1.0

    else:
        if y0 > y1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        deltaX = x1 - x0
        deltaY = y1 - y0
        slope = abs(float(deltaX) / deltaY)
        subSlope = 0.0
        x = x0
        for y in xrange(y0, y1 + 1):
            pixels[x][y] = line_color
            subSlope += slope
            while subSlope >= 0.5:
                if deltaX > 0:
                    x += 1
                else:
                    x -= 1
                subSlope -= 1.0


# update current mouse position
def updateCurrMouse(xx, yy):
    global currMouse

    currMouse = (max(0, min(SIZE - 1, xx / PIXEL_SIZE)),
                 max(0, min(SIZE - 1, SIZE - (yy / PIXEL_SIZE) - 1)))


# mouse button handler
def mouseButton(button, state, xx, yy):
    global currMouse, lastMouse

    if button != GLUT_LEFT_BUTTON:
        return

    if state != GLUT_DOWN:
        return

    updateCurrMouse(xx, yy)

    if lastMouse != None and lastMouse != currMouse:
        drawline(lastMouse, currMouse)

    lastMouse = currMouse

    glutPostRedisplay()


# mouse motion handler
def mouseMotion(xx, yy):
    updateCurrMouse(xx, yy)

    glutPostRedisplay()


# function for handling key down
def keyboard(c, x, y):
    global currMouse, lastMouse
    global pixels

    if c == ' ':
        lastMouse = None
        for xx in xrange(SIZE):
            for yy in xrange(SIZE):
                pixels[xx][yy] = (0, 0, 0)
        glutPostRedisplay()


# function for displaying a pixel
def displayPixel(xx, yy):
    glVertex2f((xx + 0) * PIXEL_SIZE, (yy + 0) * PIXEL_SIZE)
    glVertex2f((xx + 1) * PIXEL_SIZE, (yy + 0) * PIXEL_SIZE)
    glVertex2f((xx + 1) * PIXEL_SIZE, (yy + 1) * PIXEL_SIZE)
    glVertex2f((xx + 0) * PIXEL_SIZE, (yy + 1) * PIXEL_SIZE)


# function for displaying the game screen
def display():
    global currMouse, lastMouse
    global pixels

    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, PIXEL_SIZE * SIZE, 0, PIXEL_SIZE * SIZE);
 
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glBegin(GL_QUADS)
    for xx in xrange(SIZE):
        for yy in xrange(SIZE):
            rr, gg, bb = pixels[xx][yy]
            glColor3f(rr / 255., gg / 255., bb / 255.)
            displayPixel(xx, yy)
    glEnd()

    if lastMouse != None:
        glColor3f(1, 1, 1)
        glBegin(GL_LINE_LOOP)
        displayPixel(lastMouse[0], lastMouse[1])
        glEnd()

    if currMouse != None:
        glColor3f(1, 1, 1)
        glBegin(GL_LINE_LOOP)
        displayPixel(currMouse[0], currMouse[1])
        glEnd()

    glutSwapBuffers()


# startup
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(PIXEL_SIZE * SIZE, PIXEL_SIZE * SIZE)
glutCreateWindow('CS3540')
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouseButton)
glutMotionFunc(mouseMotion)
glutPassiveMotionFunc(mouseMotion)
glutMainLoop()
