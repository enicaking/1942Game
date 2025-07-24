from random import *
import pyxel
import constants
from math import sin, pi
from bullet import Bullet
from player import Player


class Enemy:
    """
    This class will describe the enemy planes and its different types using inheritance
    """
    def __init__(self, x: int, y: int) -> int:
        self.x = x
        self.y = y
        self.alive = True
        constants.enemy_list.append(self)


class Regular(Enemy):
    """
    This subclass will describe the movement and behaviour of the Regular enemy plane
    """
    def __init__(self, x: int, y: int) -> int:
        self.w = constants.REG_ENEMY_WIDTH
        self.h = constants.REG_ENEMY_HEIGHT
        self.__offset = int(random() * 60)
        self.halfway = False
        self.type = "Regular"

        super().__init__(x, y)

    def update(self):
        # Offset and direction randomise flight path downwards
        if (pyxel.frame_count + self.__offset) % 60 < 30:
            self.x += (constants.ENEMY_SPEED/2)
        else:
            self.x -= (constants.ENEMY_SPEED/2)

        # Once halfway, the plane might turn around
        if not self.halfway:
            if self.y == (constants.GAME_HEIGHT/2) and randint(0, 11) < 7:
                self.halfway = True
            else:
                self.y += constants.ENEMY_SPEED

        if self.halfway:
            self.y -= constants.ENEMY_SPEED

        # Random shooting
        if int(random() * 60) < 1:
            Bullet(self.x + (constants.REG_ENEMY_WIDTH - constants.BULLET_WIDTH) / 2,
                   self.y + constants.BULLET_HEIGHT, "enemy")

        # Plane disappears once outside the frame
        if self.y > constants.GAME_HEIGHT - 1:
            self.alive = False

    def draw(self):
        # Generating images
        if self.halfway:
            pyxel.blt(self.x, self.y, 1, 0, 200, self.w, -self.h, colkey=0)
        else:
           pyxel.blt(self.x, self.y, 1, 0, 200, self.w, self.h, colkey=0)


class Red(Enemy):
    """
    This subclass will describe the movement and behaviour of the Red enemy plane
    """
    def __init__(self, x: int, y: int, direction: bool) -> int:
        self.w = constants.RED_ENEMY_WIDTH
        self.h = constants.RED_ENEMY_HEIGHT
        self.aux = direction
        self.type = "Red"
        self.__loops = int(random() * 2) + 2
        self.__angle = pi
        self.killed_red = [[], []]
        super().__init__(x, y)

    def update(self):
        if self.__angle < pyxel.width:
            if self.aux:
                self.y = (75 * sin(self.__angle * (pi/100)))
                self.x = self.__angle
                self.__angle += pi/2
            if not self.aux:
                self.y = (75 * sin(self.__angle * (pi / 100)))
                self.x = pyxel.width - self.__angle
                self.__angle += pi/2

        else:
            self.alive = False

        # First position counts red planes that have appeared
        # Second position will store killed red planes for the bonus
        self.killed_red[0].append(1)

        # Rare shooting
        if int(random() * 300) < 1:
            Bullet(self.x + (constants.RED_ENEMY_WIDTH - constants.BULLET_WIDTH) / 2,
                   self.y + constants.BULLET_HEIGHT, "enemy_red")

        # Keeping plane only when within the frame
        if 0 > self.x > (pyxel.width + constants.RED_ENEMY_WIDTH):
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 100, 100, self.w, self.h, colkey=0)


class Bombardier(Enemy):
    """
    This subclass will describe the movement and behaviour of the Bombardier enemy plane
    """
    def __init__(self, x: int, y: int, position_xplayer: int, position_yplayer: int) -> int:
        self.w = constants.BOMB_ENEMY_WIDTH
        self.h = constants.BOMB_ENEMY_HEIGHT
        self.lives = 5
        self.type = "Bombardier"
        self.__position_xplayer = position_xplayer
        self.__position_yplayer = position_yplayer
        super().__init__(x, y)

    def update(self):
        self.x += constants.ENEMY_SPEED
        aux = int(random() * 400)
        if aux < 200:
            self.y += constants.ENEMY_SPEED
        if aux > 200:
            self.y -= constants.ENEMY_SPEED

        # Bombardier bullets
        if int(random() * 50) < 1:
            Bullet(self.__position_xplayer + 2*(self.x - self.__position_xplayer),
                   self.__position_yplayer + 2*(self.y - self.__position_yplayer), "enemy")

        if 0 > self.x > (pyxel.width - 1):
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 132, 132, self.w, self.h, colkey=0)


class SuperBombardier(Enemy):
    """
    This subclass will describe the movement and behaviour of the Super Bombardier enemy plane
    """
    def __init__(self, x: int, y: int) -> int:
        self.w = 173
        self.h = 100
        self.x = x
        self.y = y
        self.lives = 12
        self.type = "SuperBombardier"
        super().__init__(x, y)

    def update(self):
        self.y -= constants.SBOMB_ENEMY_SPEED

        if int(random() * 50) < 1:
            Bullet(self.x + (self.w - constants.BULLET_WIDTH) / 2,
                   self.y + constants.BULLET_HEIGHT, "enemy")

        if 0 > self.y > (constants.GAME_HEIGHT - 1):
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 1, 0, 0, self.w, self.h, colkey=0)
