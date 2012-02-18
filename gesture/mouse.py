from pymouse import PyMouse
m = PyMouse()
MOVE_DISTANCE=5

def move_rel(i,j):
    x,y = m.position()
    x+=i
    y+=j
    m.move(x,y)

def move_left():
    move_rel(-MOVE_DISTANCE, 0)

def move_right():
    move_rel(MOVE_DISTANCE, 0)

def move_up():
    move_rel(0, -MOVE_DISTANCE)

def move_down():
    move_rel(0, MOVE_DISTANCE)