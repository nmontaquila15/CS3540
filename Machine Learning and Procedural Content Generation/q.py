import random, sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# constants
TIMER_TIME = 33
CELL_SIZE = 50
SIZE = 7
AGENT_OFF       = 0
AGENT_LEARNING  = 1
AGENT_RUNNING   = 2


# view state
start = (SIZE / 2, 0) # starting position
goal = (SIZE / 2, SIZE - 1) # ending position
bonus = None # location of bonus, if any
bonus_present = False # if there is a bonus, it it still there (as opposed to having been collected)?
hazard1 = (SIZE / 2, SIZE / 2) # hazard position
hazard2 = (SIZE / 2 + 1, SIZE - 1) # hazard position
agent = start # agent current position
agent_mode = AGENT_OFF
reset_on_next = False # reset the agent on the next step?
step_delay = 0
Q = None # Q table: map from (agent position, bonus present, action) to expected reward


# get the actions possible for a given cell
def actions_for_cell(cell):
    xx, yy = cell
    actions = ['N', 'S', 'E', 'W']
    if xx == 0:
        actions.remove('W')
    if xx == SIZE - 1:
        actions.remove('E')
    if yy == 0:
        actions.remove('S')
    if yy == SIZE - 1:
        actions.remove('N')
    return actions


# state transition function
def transition(cell, bonus_present, act):
    actions = actions_for_cell(cell)

    if act not in actions:
        raise RuntimeError('Action not allowed')

    xx, yy = cell
    if act == 'N':
        new_cell = (xx, yy + 1)
    if act == 'S':
        new_cell = (xx, yy - 1)
    if act == 'E':
        new_cell = (xx + 1, yy)
    if act == 'W':
        new_cell = (xx - 1, yy)

    if new_cell == bonus:
        new_bonus_present = False
    else:
        new_bonus_present = bonus_present

    reset = new_cell in [goal, hazard1, hazard2]

    return new_cell, new_bonus_present, reset


# reward function for the cell the agent is moving into, and if there was a bonus before the move
def reward(next_cell, bonus_present):
    if next_cell == goal:
        return 1.0
    if next_cell == bonus and bonus_present:
        return 4.0
    if next_cell in [hazard1, hazard2]:
        return -5.0
    return 0.0


# reset q table
def reset_Q():
    global Q

    Q = {}
    for xx in xrange(SIZE):
        for yy in xrange(SIZE):
            cell = (xx, yy)
            for bb in [True, False]:
                for aa in actions_for_cell(cell):
                    Q[(cell, bb, aa)] = 0.0


# reset state
def reset_state():
    global start, goal, bonus, bonus_present, hazard1, hazard2, agent, agent_mode, reset_on_next

    agent = start
    bonus_present = (bonus != None)
    reset_on_next = False


# find best action to take; if there is more that one with equal expected reward, return a random one
def find_best_action(actions):
    # TODO: find the actions with the best Q and return one randomly
    best_actions, max_qValue = [], None
    for action in actions:
        qValue = Q[agent, bonus_present, action]
        if max_qValue == None or qValue > max_qValue:
            best_actions, max_qValue = [action], qValue
        elif qValue == max_qValue:
            best_actions.append(action)

    return random.choice(best_actions)


# handle stepping of agent
def step_agent(is_learning):
    global start, goal, bonus, bonus_present, hazard1, hazard2, agent, agent_mode, reset_on_next

    if reset_on_next:
        reset_state()
        return
    
    next_agent = agent
    next_bonus_present = bonus_present
    reset = False
    
    actions = actions_for_cell(agent)

    if is_learning:
        ALPHA = 0.8
        GAMMA = 0.8
        EPSILON = 0.75

        # TODO: step the agent by setting next_agent, next_bonus_present, and reset; update Q table
        if random.random() > EPSILON:
            next_action = find_best_action(actions)
        else:
            next_action = random.choice(actions)
        next_agent, next_bonus_present, reset = transition(agent, bonus_present, next_action)
        r = reward(next_agent, bonus_present)
        max_qValue = -1e+100
        for action in actions_for_cell(next_agent):
            max_qValue = max(max_qValue, Q[next_agent, next_bonus_present, action])

        prev_qValue = Q[agent, bonus_present, next_action]
        new_qValue = (1 - ALPHA) * prev_qValue + ALPHA * (r + GAMMA * max_qValue)
        Q[agent, bonus_present, next_action] = new_qValue

    else:
        best_action = find_best_action(actions)
        next_agent, next_bonus_present, reset = transition(agent, bonus_present, random.choice(best_action))

    agent = next_agent
    bonus_present = next_bonus_present

    reset_on_next = reset


# function for handling key down
def keyboard(c, x, y):
    global start, goal, bonus, bonus_present, hazard1, hazard2, agent, agent_mode

    if c == '1':
        reset_state()
        agent_mode = AGENT_OFF
    elif c == '2':
        reset_state()
        agent_mode = AGENT_LEARNING
    elif c == '3':
        reset_state()
        agent_mode = AGENT_RUNNING

    if c in ['s', 'g', 'h', 'j', 'k', 'b', ' ']:
        xx = max(0, min(SIZE - 1, int(x / CELL_SIZE)))
        yy = max(0, min(SIZE - 1, int((CELL_SIZE * SIZE - y - 1) / CELL_SIZE)))
        cell = (xx, yy)
        if c == 's':
            start = cell
        elif c == 'g':
            goal = cell
        elif c == 'h':
            hazard1 = cell
        elif c == 'j':
            hazard2 = cell
        elif c == 'b':
            if bonus == None or bonus != cell:
                bonus = cell
            else:
                bonus = None

        reset_Q()
        reset_state()
        agent_mode = AGENT_OFF

    glutPostRedisplay()


# handle state update on timer
def timer(value):
    global start, goal, bonus, bonus_present, hazard1, hazard2, agent, agent_mode, step_delay

    dt = TIMER_TIME / 1000.0

    if agent_mode != AGENT_OFF:
        is_learning = (agent_mode == AGENT_LEARNING)
        if not is_learning and step_delay > 0:
            step_delay -= 1
        else:
            step_agent(is_learning)
            step_delay = 8

    glutPostRedisplay()
    glutTimerFunc(TIMER_TIME, timer, 0)


# function for displaying a pixel
def displayPixel(xx, yy, inset):
    glVertex2f((xx + 0) * CELL_SIZE + inset, (yy + 0) * CELL_SIZE + inset)
    glVertex2f((xx + 1) * CELL_SIZE - inset, (yy + 0) * CELL_SIZE + inset)
    glVertex2f((xx + 1) * CELL_SIZE - inset, (yy + 1) * CELL_SIZE - inset)
    glVertex2f((xx + 0) * CELL_SIZE + inset, (yy + 1) * CELL_SIZE - inset)


# function for displaying an action
def displayAction(xx, yy, aa, inset):
    glPushMatrix()
    glTranslatef((xx + 0.5) * CELL_SIZE, (yy + 0.5) * CELL_SIZE, 0.0)
    if aa == 'N':
        glRotate(90, 0, 0, 1)
    elif aa == 'S':
        glRotate(270, 0, 0, 1)
    elif aa == 'E':
        pass
    elif aa == 'W':
        glRotate(180, 0, 0, 1)
    glBegin(GL_QUADS)
    glVertex2f(CELL_SIZE/2.0 - inset,  inset/2.0)
    glVertex2f(CELL_SIZE/2.0 - inset, -inset/2.0)
    glVertex2f(CELL_SIZE/2.0, -inset/8.0)
    glVertex2f(CELL_SIZE/2.0,  inset/8.0)
    glEnd()
    glPopMatrix()


# function for displaying the game screen
def display():
    global start, goal, bonus, bonus_present, hazard1, hazard2, agent, agent_mode
    global Q

    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, CELL_SIZE * SIZE, 0, CELL_SIZE * SIZE);
 
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    inset = CELL_SIZE / 5.0

    glBegin(GL_QUADS)
    glColor3f(0.0, 0.8, 0.0)
    displayPixel(goal[0], goal[1], inset)
    if bonus != None:
        if bonus_present:
            glColor3f(0.8, 0.8, 0.0)
        else:
            glColor3f(0.4, 0.4, 0.0)
        displayPixel(bonus[0], bonus[1], inset)
    glColor3f(0.8, 0.0, 0.0)
    displayPixel(hazard1[0], hazard1[1], inset)
    glColor3f(0.8, 0.0, 0.0)
    displayPixel(hazard2[0], hazard2[1], inset)
    glColor3f(0.0, 0.4, 0.4)
    displayPixel(start[0], start[1], inset)
    glColor3f(0.0, 0.0, 0.9)
    displayPixel(agent[0], agent[1], inset)
    glEnd()

    for xx in xrange(SIZE):
        for yy in xrange(SIZE):
            cell = (xx, yy)
            actions = actions_for_cell(cell)
            for aa in actions:
                Q_at = Q[(cell, bonus_present, aa)]
                if Q_at == 0.0:
                    clr = 0.1
                    glColor3f(clr, clr, clr)
                elif Q_at >= 0.0:
                    if bonus != None and bonus_present:
                        Q_at /= 5.0
                    clr = 0.1 + 0.6 * Q_at
                    glColor3f(0, clr, 0)
                else:
                    Q_at /= 5.0
                    clr = 0.1 + 0.6 * -Q_at
                    glColor3f(clr, 0, 0)
                displayAction(xx, yy, aa, inset)

    glColor3f(0.5, 0.5, 0.5)
    for xx in xrange(SIZE):
        for yy in xrange(SIZE):
            glBegin(GL_LINE_LOOP)
            displayPixel(xx, yy, 0)
            glEnd()

    glutSwapBuffers()


# startup
random.seed(12345)
reset_Q()
reset_state()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(CELL_SIZE * SIZE, CELL_SIZE * SIZE)
glutCreateWindow('CS3540')
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutTimerFunc(TIMER_TIME, timer, 0)
glutMainLoop()
