import sys
if sys.platform == 'linux2':
    import os

    def move_up():
        print "Move Up"
        os.system("./crikey '\A\t'")

    def move_down():
        print "Move Down"
        os.system("./crikey '\A\S\t'")

    def move_right():
        print "Move Right"
        os.system("./crikey '\C\t'")

    def move_left():
        print "Move Left"
        os.system("./crikey '\C\S\t'")

    def move_together():
        print "Zoom In"
        os.system("./crikey '\C-\C-\C-'")

    def move_away():
        print "Zoom Out"
        os.system("./crikey '\C=\C=\C='")

elif sys.platform == 'win32':
    import win32api, win32con
    def move_up():
        print "Move Up"
        win32api.keybd_event(win32con.VK_MENU, 0, 0)
        win32api.keybd_event(win32con.VK_TAB, 0, 0)
        win32api.keybd_event(win32con.VK_TAB, 0, win32con.KEYEVENTF_KEYUP)
        win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP)

    def move_down():
        print "Move Down"
        win32api.keybd_event(win32con.VK_MENU, 0, 0)
        win32api.keybd_event(win32con.VK_SHIFT, 0, 0)
        win32api.keybd_event(win32con.VK_TAB, 0, 0)
        win32api.keybd_event(win32con.VK_TAB, 0, win32con.KEYEVENTF_KEYUP)
        win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP)
        win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP)

    def move_right():
        print "Move Right"
        win32api.keybd_event(win32con.VK_LCONTROL, 0, 0)
        win32api.keybd_event(win32con.VK_TAB, 0, 0)
        win32api.keybd_event(win32con.VK_TAB, 0, win32con.KEYEVENTF_KEYUP)
        win32api.keybd_event(win32con.VK_LCONTROL, 0, win32con.KEYEVENTF_KEYUP)

    def move_left():
        print "Move Left"
        win32api.keybd_event(win32con.VK_LCONTROL, 0, 0)
        win32api.keybd_event(win32con.VK_SHIFT, 0, 0)
        win32api.keybd_event(win32con.VK_TAB, 0, 0)
        win32api.keybd_event(win32con.VK_TAB, 0, win32con.KEYEVENTF_KEYUP)
        win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP)
        win32api.keybd_event(win32con.VK_LCONTROL, 0, win32con.KEYEVENTF_KEYUP)

    def move_together():
        print "Zoom In"

    def move_away():
        print "Zoom Out"
