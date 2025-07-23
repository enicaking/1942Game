from Plane import Plane
from Bullets import Bullet
from enemies import Regular
from Background import Background
import pyxel
import CONSTANTS



class Board:
    def __init__(self, w: int, h: int):
        # Initializing the object
        self.width = w
        self.height = h
        pyxel.init(self.width, self.height, title="1942")

        self.background = Background()
        self.score = 0
        # Loading sprites
        pyxel.image(0).load(0, 0, "player 1.png")


        self.bulletsplayer=[]

        self.plane = Plane(self.width / 2, 200)

        # Running the game
        pyxel.run(self.update, self.draw)

    def update_list(self, list):
        for elem in list:
            elem.update()

    def clean_list(self, list1):
        i = 0
        while i < len(list1):
            elem = list1[i]
            if not elem.is_alive:
                list1.pop(i)
            else:
                i += 1

    def update(self):
        self.background.update()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.plane.move('right', self.width)
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.plane.move('left', self.width)
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.plane.move('up', self.height)
        elif pyxel.btn(pyxel.KEY_UP):
            self.plane.move('down', self.height)

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.bulletsplayer.append(Bullet(self.plane.x + (CONSTANTS.PLANE_WIDTH - CONSTANTS.BULLET_WIDTH) /
                                             2, self.plane.y - CONSTANTS.BULLET_HEIGHT / 2))

        for i in range(0, len(self.bulletsplayer)):
            Bullet.update(self.bulletsplayer[i])
            if self.bulletsplayer[i].y == CONSTANTS.Y:
                self.bulletsplayer.pop(i)



    def draw(self):
        pyxel.cls(0)

        self.background.draw()

        for bullet in self.bulletsplayer:
            bullet.draw()

        pyxel.blt(self.plane.x, self.plane.y, *self.plane.sprite)

        pyxel.text(20, 4, f"SCORE {self.score:5}", 7)

