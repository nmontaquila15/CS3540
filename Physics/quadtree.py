import random, sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# constants
WORLD_SIZE = 480
OBJECT_SIZE = 20 # size of each object
MAX_TREE_DEPTH = 4 # max depth to subdivide quadtree to

# view state
objects = [] # all objects in world
objects_selected = None # list of object selected after click
quadtree = None # the quadtree


# class representing a quadtree node
class Node:
    # initialize node
    def __init__(self, bounds, depth):
        self._bounds = bounds # bounds of this node as ((x0, y0), (x1, y1))
        self._depth = depth # depth of this node
        self._objects = [] # objects in this node
        self._children = None # child nodes: None or four
        self._visited = False # use this to determine if a node was visited during traversal

    # clear all visited flags
    def clearVisited(self):
        self._visited = False
        if self._children:
            for child in self._children:
                child.clearVisited()

    # do some basic checks of the tree structure
    def checkStructure(self):
        if self._objects and self._children:
            raise RuntimeError("Node has objects and children.")
        if self._depth > MAX_TREE_DEPTH:
            raise RuntimeError("Node depth greater than max depth.")

        if self._children:
            for child in self._children:
                child.checkStructure()

    # recursively display a node
    def display(self, showVisited):
        (x0, y0), (x1, y1) = self._bounds

        if showVisited:
            if self._visited:
                glColor(0.0, 0.0, float(self._depth + 1) / (MAX_TREE_DEPTH + 2))
                glBegin(GL_QUADS)
                glVertex2f(x0, y0)
                glVertex2f(x1, y0)
                glVertex2f(x1, y1)
                glVertex2f(x0, y1)
                glEnd()
        else:
            if self._objects != None and len(self._objects) != 0:
                glColor(0.2, 0.2, 0.2)
                glBegin(GL_QUADS)
                glVertex2f(x0, y0)
                glVertex2f(x1, y0)
                glVertex2f(x1, y1)
                glVertex2f(x0, y1)
                glEnd()

        glColor(0.5, 0.5, 0.5)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x0, y0)
        glVertex2f(x1, y0)
        glVertex2f(x1, y1)
        glVertex2f(x0, y1)
        glEnd()

        if self._children:
            for child in self._children:
                child.display(showVisited)

    # insert an object into the quadtree, changing the tree structure as needed
    def insertObject(self, object):
        # TODO: put object into quadtree

        half_object_size = OBJECT_SIZE/2
        bounds = self._bounds
        
        if self._depth >= MAX_TREE_DEPTH:
            self._objects.append(object)
            return
        
        elif object[1] + half_object_size < bounds[0][1] or object[0] + half_object_size < bounds[0][0] or object[1] - half_object_size >= bounds[1][1] or object[0] - half_object_size >= bounds[1][0]:
            return
        
        else:
            if self._children == None:
                if len(self._objects) == 0:
                    self._objects.append(object)
                    return
                
                (x0, y0), (x1, y1) = bounds
                mid_y = (y0 + y1)/2
                mid_x = (x0 + x1)/2
                self._children = [Node(((x0, y0), (mid_x, mid_y)), self._depth + 1), Node(((mid_x, y0), (x1, mid_y)), self._depth + 1), Node(((x0, mid_y), (mid_x, y1)), self._depth + 1), Node(((mid_x, mid_y), (x1, y1)), self._depth + 1)]

                for obj in self._objects + [object]:
                    for child in self._children:
                        child.insertObject(obj)
                self._objects = None
            else:
                for child in self._children:
                    child.insertObject(object)
            return   

    # find any objects in the tree that contain the given point
    def findObjects(self, pt):
        # TODO: traverse tree to see if any objects were selected, return empty list if not found

        half_object_size = OBJECT_SIZE/2
        bounds = self._bounds
        
        if pt[0] < bounds[0][0] or pt[1] < bounds[0][1] or pt[0] >= bounds[1][0] or pt[1] >= bounds[1][1]:
            return []
        else:
            object_list = []
            self._visited = True
            
            if self._children == None:
                for object in self._objects:
                    if abs(object[0] - pt[0]) < half_object_size and abs(object[1] - pt[1]) < half_object_size:
                        object_list.append(object)

            else:
                for child in self._children:
                    object_list = object_list + child.findObjects(pt)

            return object_list

# generate new world
def newWorld():
    global objects, objects_selected, quadtree

    objects = []
    objects_selected = None
    quadtree = Node(((0, 0), (WORLD_SIZE, WORLD_SIZE)), 0)

    n = random.randint(5, 15)

    for i in xrange(n):
        x = random.randint(OBJECT_SIZE, WORLD_SIZE - OBJECT_SIZE - 1)
        y = random.randint(OBJECT_SIZE, WORLD_SIZE - OBJECT_SIZE - 1)
        object = (x, y)
        objects.append(object)
        quadtree.insertObject(object)

    quadtree.checkStructure()


# mouse button handler
def mouseButton(button, state, xx, yy):
    global objects, objects_selected, quadtree

    if button != GLUT_LEFT_BUTTON:
        return

    if state != GLUT_DOWN:
        return

    quadtree.clearVisited()
    objects_selected = quadtree.findObjects((xx, WORLD_SIZE - yy - 1))

    glutPostRedisplay()


# function for handling key down
def keyboard(c, x, y):
    if c == ' ':
        newWorld()
        glutPostRedisplay()


# function for displaying the game screen
def display():
    global objects, objects_selected, quadtree

    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, WORLD_SIZE, 0, WORLD_SIZE)
 
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    quadtree.display(objects_selected != None)

    glBegin(GL_QUADS)
    for obj in objects:
        if objects_selected and obj in objects_selected:
            glColor3f(1, 1, 0)
        else:
            glColor3f(1, 1, 1)
        xx, yy = obj
        glVertex2f(xx - OBJECT_SIZE / 2, yy - OBJECT_SIZE / 2)
        glVertex2f(xx + OBJECT_SIZE / 2, yy - OBJECT_SIZE / 2)
        glVertex2f(xx + OBJECT_SIZE / 2, yy + OBJECT_SIZE / 2)
        glVertex2f(xx - OBJECT_SIZE / 2, yy + OBJECT_SIZE / 2)
    glEnd()

    glutSwapBuffers()


# startup
random.seed(12345)
newWorld()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(WORLD_SIZE, WORLD_SIZE)
glutCreateWindow('CS3540')
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouseButton)
glutMainLoop()
