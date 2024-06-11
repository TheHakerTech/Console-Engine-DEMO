import keyboard

class Keys():
    up = False
    down = False
    right = False
    left = False

def moveRight():
    Keys.right = True

def moveLeft():
    Keys.left = True

def moveUp():
    Keys.up = True

def moveDown():
    Keys.down = True

keyboard.add_hotkey("Right", moveRight)
keyboard.add_hotkey("Left", moveLeft)
keyboard.add_hotkey("Up", moveUp)
keyboard.add_hotkey("Down", moveDown)