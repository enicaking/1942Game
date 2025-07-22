import pyxel



import pyxel

def update_0():
    ''' This function is executed every frame. Now it only checks if the user
    pressed Q to finish'''
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()


def move(x, y):
    ''' This function checks if the arrows of the keyboard are pressed and
    updates the x and y accordingly.'''
    if pyxel.btn(pyxel.KEY_RIGHT):
        x = x + 1
    elif pyxel.btn(pyxel.KEY_LEFT):
        x = x - 1
    elif pyxel.btn(pyxel.KEY_UP):
        y = y - 1
    elif pyxel.btn(pyxel.KEY_DOWN):
        y = y + 1

    return x, y


def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    else:
        position[0], position[1] = move(position[0], position[1])



def draw():
    ''' This function draws graphics from the image bank'''
    pyxel.cls(3)
    pyxel.blt(position[0], position[1], 0, 0, 0, 16, 16,colkey=0)
    x = pyxel.frame_count % pyxel.width
    pyxel.blt(x, 10, 1, 17, 0,16,16, colkey=0)

position = [10, 10]


################## main program ##################

WIDTH = 160
HEIGHT = 120
CAPTION = "This is an example of images in pyxel"

pyxel.init(WIDTH, HEIGHT, title=CAPTION)

pyxel.image(1).load(17, 0, "/Users/estefanygonzalez/Desktop/UNI/Programming classes/PYXEL/pyxel-examples/418-4184613_"
                           "mario-mushroom-pixil-super-mario-world-1-up.png")
pyxel.load("assets1234.pyxres")

pyxel.run(update, draw)
