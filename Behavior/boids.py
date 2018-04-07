import math, random, sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# constants
TIMER_TIME = 33
SIZE = 480
BOID_SPEED = 100
BOID_ACCEL = 10.0 # maximum accelleration of boid
WEIGHT_SEPARATION = 0.4
WEIGHT_ALIGNMENT = 0.1
WEIGHT_COHESION = 0.2
NBR_RADIUS = 80 # distance at which another boid is considered a neighbor
BOID_SIZE = 10


# state / constants
boids = [] # list of boids as [x position, y position, x velocity, y velocity] lists
boid_sel = None # index of selected boid, if any
use_separation = True
use_alignment = True
use_cohesion = True


# return a list containing the indices, positions, and velocities of neighboring boids for the given boid index
def get_neighbors_for_boid(ii):
    global boids, boid_sel

    nbr_ids = set() # set of indices of neighbors
    nbr_data = [] # a list of 4-tuples (x, y, vx, vy) for position and velocity of neighbors

    # TODO: find neighbors (considering wrapping around edges)
    x0, y0, vx0, vy0 = boids[ii]
    for sub, (px, py, vx, vy) in enumerate(boids):
        if sub == ii:
            continue
        closest = None
        closest_dist = 1e+100
        for dx, dy in [(0, 0),(SIZE, 0),(-SIZE, 0),(0, SIZE),(0, -SIZE)]:
            x1 = px + dx
            y1 = py + dy
            dist = ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5
            if dist < NBR_RADIUS and dist < closest_dist:
                closest = (x1,y1,vx,vy)
                closest_dist = dist
        if closest:
            nbr_ids.add(sub)
            nbr_data.append(closest)

    return nbr_ids, nbr_data


# get desired separation acceleration
def boid_separation_accel(boid, nbr_data):
    accel = [0.0, 0.0]

    # TODO: compute desired acceleration
    px, py, vx, vy = boid
    for prev_x, prev_y, prev_vx, prev_vy in nbr_data:
        dx = px - prev_x
        dy = py - prev_y
        ll = (dx ** 2 + dy ** 2) ** 0.5
        if ll < 0.0001:
            accel[0] += 0.1 * NBR_RADIUS * 1
            accel[1] += 0.1 * NBR_RADIUS * 0
        else:
            accel[0] += 0.1 * NBR_RADIUS * dx / ll
            accel[1] += 0.1 * NBR_RADIUS * dy / ll
    
    return accel


# get desired alignment acceleration
def boid_alignment_accel(boid, nbr_data):
    accel = [0.0, 0.0]

    # TODO: compute desired acceleration
    px, py, vx, vy = boid
    new_vx, new_vy = (0.0, 0.0)
    for prev_x, prev_y, prev_vx, prev_vy in nbr_data:
        new_vx += prev_vx
        new_vy += prev_vy

    new_vx /= len(nbr_data)
    new_vy /= len(nbr_data)
    accel[0] = new_vx - vx
    accel[1] = new_vy - vy
    
    return accel


# get desired cohesion acceleration
def boid_cohesion_accel(boid, nbr_data):
    accel = [0.0, 0.0]

    # TODO: compute desired acceleration
    accel = [0.0, 0.0]
    px, py, vx, vy = boid
    new_x, new_y = (0.0, 0.0)
    for prev_x, prev_y, prev_vx, prev_vy in nbr_data:
        new_x += prev_x
        new_y += prev_y

    new_x /= len(nbr_data)
    new_y /= len(nbr_data)
    accel[0] = new_x - px
    accel[1] = new_y - py
    
    return accel


# truncate vector to given magnitude and return magnitude
def truncate(vec, ml):
    ll = (vec[0] ** 2 + vec[1] ** 2) ** 0.5
    if ll > ml:
        vec[0] *= ml / ll
        vec[1] *= ml / ll
        return ml
    else:
        return ll


# steer a boid based on desired accelerations
def steer_boid(ii, nbr_data, dt):
    global boids, boid_se
    global use_separation, use_alignment, use_cohesion

    if len(nbr_data) != 0:
        separation_accel = [0, 0]
        if use_separation:
            separation_accel = boid_separation_accel(boids[ii], nbr_data)

        alignment_accel = [0, 0]
        if use_alignment:
            alignment_accel = boid_alignment_accel(boids[ii], nbr_data)

        cohesion_accel = [0, 0]
        if use_cohesion:
            cohesion_accel = boid_cohesion_accel(boids[ii], nbr_data)

        dvx, dvy = 0.0, 0.0
        accel_left = BOID_ACCEL
        for scale, accel in [(WEIGHT_SEPARATION, separation_accel), (WEIGHT_ALIGNMENT, alignment_accel), (WEIGHT_COHESION, cohesion_accel)]:
            accel[0] *= scale
            accel[1] *= scale
            ll = truncate(accel, accel_left)
            dvx += accel[0]
            dvy += accel[1]
            accel_left -= ll
            if accel_left <= 0.0:
                break
            
        boids[ii][2] += dvx
        boids[ii][3] += dvy

        spd = (boids[ii][2] ** 2 + boids[ii][3] ** 2) ** 0.5
        if spd > BOID_SPEED:
            boids[ii][2] *= BOID_SPEED / spd
            boids[ii][3] *= BOID_SPEED / spd
        elif spd < 0.7 * BOID_SPEED:
            boids[ii][2] *= 0.7 * BOID_SPEED / spd
            boids[ii][3] *= 0.7 * BOID_SPEED / spd


# function for drawing a single boid
def drawBoid():
    glBegin(GL_POLYGON)
    glVertex2f( 1.0,  0.0)
    glVertex2f(-0.5,  0.5)
    glVertex2f(-0.5, -0.5)
    glEnd()


# function for drawing all boids
def drawBoids():
    global boids, boid_sel

    nbr_ids, nbr_data = set(), []
    if boid_sel != None:
        nbr_ids, nbr_data = get_neighbors_for_boid(boid_sel)

    for ii, (px, py, vx, vy) in enumerate(boids):
        if ii == boid_sel:
            glColor3f(0.0, 1.0, 1.0)
        elif ii in nbr_ids:
            glColor3f(0.0, 0.2, 0.8)
        else:
            glColor3f(0.5, 0.5, 0.5)

        for dx, dy in [(0, 0), (SIZE, 0), (-SIZE, 0), (0, SIZE), (0, -SIZE)]:
            glPushMatrix()
            glTranslatef(px + dx, py + dy, 0)
            glRotatef(180.0 / math.pi * math.atan2(vy, vx), 0, 0, 1)
            glScalef(BOID_SIZE, BOID_SIZE, 1)
            drawBoid()
            glPopMatrix()


# mouse button handler
def mouseButton(button, state, mx, my):
    global boids, boid_sel

    if button != GLUT_LEFT_BUTTON:
        return

    if state != GLUT_DOWN:
        return

    wx = mx
    wy = SIZE - my - 1

    if glutGetModifiers() & GLUT_ACTIVE_SHIFT:
        sel_dist_sq = (2 * BOID_SIZE) ** 2
        boid_sel = None
        closest_sq = 1e100
        for ii, (px, py, vx, vy) in enumerate(boids):
            dist_sq = ((wx - px) ** 2 + (wy - py) ** 2)
            if dist_sq < sel_dist_sq and dist_sq < closest_sq:
                boid_sel = ii
                closest_sq = dist_sq
    else:
        angle = random.random() * math.pi * 2.0
        boids.append([wx, wy, BOID_SPEED * math.cos(angle), BOID_SPEED * math.sin(angle)])

    glutPostRedisplay()


# function for handling key down
def keyboard(c, x, y):
    global boids, boid_sel
    global use_separation, use_alignment, use_cohesion

    if c == ' ':
        boids = []
        boid_sel = None

    elif c == '1':
        use_separation = not use_separation

    elif c == '2':
        use_alignment = not use_alignment

    elif c == '3':
        use_cohesion = not use_cohesion

    glutPostRedisplay()


# handle state update on timer
def timer(value):
    global boids, boid_sel

    dt = TIMER_TIME / 1000.0

    for ii in xrange(len(boids)):
        nbr_ids, nbr_data = get_neighbors_for_boid(ii)
        steer_boid(ii, nbr_data, dt)

    for boid in boids:
        boid[0] += dt * boid[2]
        boid[1] += dt * boid[3]
        while boid[0] < 0.0:
            boid[0] += SIZE
        while boid[0] >= SIZE:
            boid[0] -= SIZE
        while boid[1] < 0.0:
            boid[1] += SIZE
        while boid[1] >= SIZE:
            boid[1] -= SIZE
    
    glutPostRedisplay()
    glutTimerFunc(TIMER_TIME, timer, 0)


# function to draw a string
def drawstring(x, y, j, s):
    CHAR_SIZE = 104.76
    NEW_SIZE = 10.0
    glPushMatrix()
    glTranslatef(x, y, 0.0)
    if j > 0:
        glTranslatef(-NEW_SIZE * len(s), 0.0, 0.0)
    elif j == 0:
        glTranslatef(-0.5 * NEW_SIZE * len(s), 0.0, 0.0)
    glScalef(1.0/CHAR_SIZE, 1.0/CHAR_SIZE, 1.0)
    glScalef(NEW_SIZE, NEW_SIZE, 1.0)
    for c in s:
        glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(c))
    glPopMatrix()


# function for displaying the game screen
def display():
    global boids, boid_se
    global use_separation, use_alignment, use_cohesion

    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, SIZE, 0, SIZE);
 
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    drawBoids()

    glColor3f(0.3, 0.3, 0.3)

    if use_separation:
        drawstring(10, 10, -1, 'separation')
    if use_alignment:
        drawstring(SIZE / 2.0, 10, 0, 'alignment')
    if use_cohesion:
        drawstring(SIZE - 10, 10, 1, 'cohesion')

    glutSwapBuffers()


# startup
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(SIZE, SIZE)
glutCreateWindow('CS3540')
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouseButton)
glutTimerFunc(TIMER_TIME, timer, 0)
glutMainLoop()
