import random, sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# constants
SIZE = 480
HANDLE_SIZE = 9
FLATNESS_EPSILON = 0.00005

TYPE_BEZIER = 0
TYPE_CATMULLROM = 1

# view state
ctype = TYPE_BEZIER
handles = []
activeHandle = None
showHandles = True


# function for drawing a curve
def drawCurve():
    global ctype, handles

    if ctype == TYPE_BEZIER:
        # TODO: draw Bezier curve from handles
        
        def distance(v0, v1):
            return ((v0[0] - v1[0])**2 + (v0[1] - v1[1])**2)**0.5

        def flat(v0, v1, v2, v3):
            return (distance(v0, v1) + distance(v1, v2) + distance(v2, v3)) / (distance(v0, v3) + FLATNESS_EPSILON**2)

        def drawBeszier(v0, v1, v2, v3):
            x0, y0 = v0
            x1, y1 = v1
            x2, y2 = v2
            x3, y3 = v3
            if flat(v0, v1, v2, v3) < 1.0 + FLATNESS_EPSILON:
                glVertex2f(x0, y0)
                glVertex2f(x3, y3)
            else:
                xi, yi = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
                xj, yj = 0.5 * (x1 + x2), 0.5 * (y1 + y2)
                xk, yk = 0.5 * (x2 + x3), 0.5 * (y2 + y3)
                xl, yl = 0.5 * (xi + xj), 0.5 * (yi + y12)
                xw, yw = 0.5 * (xj + xk), 0.5 * (y12 + y23)
                xz, yz = 0.5 * (xl + xw), 0.5 * (yl + yw)
                drawBeszier((x0, y0), (xi, yi), (xl, yl), (xz, yz))
                drawBeszier((xz, yz), (xw, yw), (xk, y23), (x3, y3))

        for index in xrange(0, len(handles), 3):
            if index + 3 < len(handles):
                drawBeszier(handles[index + 0], handles[index + 1], handles[index + 2], handles[index + 3])

        pass

    else:
        # TODO: draw Catmull-Rom curve from handles
        def drawCatmullRom(v0, v1, v2, v3):
            x0, y0 = v0
            x1, y1 = v1
            x2, y2 = v2
            x3, y3 = v3
            vertices = []
            for index in xrange(11):
                vX = 1 * x1 + (index / 10.0) * (-0.5 * x0 + 0.5 * x2) + (t1**2) * (1 * x0 - 2.5 * x1 + 2 * x2 - 0.5 * x3) + (t1**3) * (-0.5 * x0 + 1.5 * x1 - 1.5 * x2 + 0.5 * x3)
                vY = 1 * y1 + (index / 10.0) * (-0.5 * y0 + 0.5 * y2) + (t1**2) * (1 * y0 - 2.5 * y1 + 2 * y2 - 0.5 * y3) + (t1**3) * (-0.5 * y0 + 1.5 * y1 - 1.5 * y2 + 0.5 * y3)
                vertices.append((vX, vY))

            for (xA, yA), (xB, yB) in zip(vertices, vertices[1:]):
                glVertex2f(xA, yA)
                glVertex2f(xB, yB)

        for index in xrange(len(handles)):
            if index + 3 < len(handles):
                drawCatmullRom(handles[index + 0], handles[index + 1], handles[index + 2], handles[index + 3])

        pass


# mouse button handler
def mouseButton(button, state, mx, my):
    global handles, activeHandle

    if button != GLUT_LEFT_BUTTON:
        return

    if state == GLUT_DOWN:
        closest = 1e100
        for ii, (hx, hy) in enumerate(handles):
            if abs(hx - mx) <= HANDLE_SIZE / 2 and abs(hy - my) <= HANDLE_SIZE / 2:
                distsq = (hx - mx) ** 2 + (hy - my) ** 2
                if distsq < closest:
                    closest = distsq
                    activeHandle = ii

        if activeHandle == None:
            handles.append((mx, my))
            activeHandle = len(handles) - 1

    if state == GLUT_UP:
        activeHandle = None

    glutPostRedisplay()


# mouse motion handler
def mouseMotion(mx, my):
    global handles, activeHandle

    if activeHandle != None:
        handles[activeHandle] = (mx, my)

        glutPostRedisplay()


# function for handling key down
def keyboard(ch, mx, my):
    global ctype, handles, activeHandle, showHandles

    if ch == ' ':
        handles = []
        activeHandle = None

    elif ch.lower() == 't':
        if ctype == TYPE_BEZIER:
            ctype = TYPE_CATMULLROM
        else:
            ctype = TYPE_BEZIER

    elif ch.lower() == 's':
        showHandles = not showHandles

    glutPostRedisplay()


# function for displaying the game screen
def display():
    global handles, activeHandle, showHandles

    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, SIZE, SIZE, 0);
 
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    if showHandles:
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_LINE_STRIP)
        for hx, hy in handles:
            glVertex2f(hx, hy)
        glEnd()

    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINES)
    drawCurve()
    glEnd()

    if showHandles:
        glBegin(GL_QUADS)
        for ii, (hx, hy) in enumerate(handles):
            if activeHandle != None and activeHandle == ii:
                glColor3f(0.5, 0.5, 1.0)
            else:
                glColor3f(0.8, 0.8, 0.8)

            glVertex2f(hx - 0.5 * HANDLE_SIZE, hy - 0.5 * HANDLE_SIZE)
            glVertex2f(hx + 0.5 * HANDLE_SIZE, hy - 0.5 * HANDLE_SIZE)
            glVertex2f(hx + 0.5 * HANDLE_SIZE, hy + 0.5 * HANDLE_SIZE)
            glVertex2f(hx - 0.5 * HANDLE_SIZE, hy + 0.5 * HANDLE_SIZE)
        glEnd()

    glutSwapBuffers()


# startup
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(SIZE, SIZE)
glutCreateWindow('CS3540')
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouseButton)
glutMotionFunc(mouseMotion)
glutPassiveMotionFunc(mouseMotion)
glutMainLoop()
