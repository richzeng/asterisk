import os

def move_up():
    os.system("./crikey '\A\t'")

def move_down():
    os.system("./crikey '\A\S\t'")

def move_right():
    os.system("./crikey '\C\t'")

def move_left():
    os.system("./crikey '\C\S\t'")

def move_together():
    os.system("./crikey '\C-\C-\C-'")

def move_away():
    os.system("./crikey '\C=\C=\C='")
