import random
import CONSTANTS


class Enemies:
    def _init_(self, x: int, y: int):
        self.x = x
        self.y = y

    #def loop(self):


class Regular:
    def _init_(self, x, y):
        self.speed = 5  # same as player
        self.sprite = pyxel.image(0).load(2, 0, "regular.png")
        self.health = 1
        self.power = 500
        self.amount = random.randint(3, 5)
        self.bullet = 1
        self.sprite = None

