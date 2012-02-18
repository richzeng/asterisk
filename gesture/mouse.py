try:
    from pymouse import PyMouse
    m = PyMouse()

    MOVE_DISTANCE=50

    def move_rel(i,j):
        x,y = m.position()
        x+=i
        y+=j
        m.move(x,y)

    def move_left():
        print "Move left"
        move_rel(-MOVE_DISTANCE, 0)

    def move_right():
        print "Move right"
        move_rel(MOVE_DISTANCE, 0)

    def move_up():
        print "Move up"
        move_rel(0, -MOVE_DISTANCE)

    def move_down():
        print "Move down"
        move_rel(0, MOVE_DISTANCE)

except:
    print "PyMouse not imported"

    def move_left():
        print "Move left"

    def move_right():
        print "Move right"

    def move_up():
        print "Move up"

    def move_down():
        print "Move down"
