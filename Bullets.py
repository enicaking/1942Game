# Bullets.py
# Enica King and Estefany Gonzalez
# Code for 1942Game Bullet class


import pyxel
import CONSTANTS


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = CONSTANTS.BULLET_WIDTH
        self.h = CONSTANTS.BULLET_HEIGHT
        self.sprite = pyxel.image(0).load(1, 0, "bulletsplayer.png")
        self.is_alive = True


    def update(self):
        self.y -= CONSTANTS.BULLET_SPEED
        if self.y + self.h - 1 < 0:
            self.is_alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0,1,0, self.w, self.h, colkey=0)

