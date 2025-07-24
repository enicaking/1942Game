import pyxel
import constants
from bullet import Bullet


class Player:
    """
    This class will describe the player sprite and its movement within the game
    """
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.w = constants.PLAYER_WIDTH
        self.h = constants.PLAYER_HEIGHT
        self.lives = constants.PLAYER_LIVES
        self.alive = True
        self.loop = False
        # Alternating helices
        self.__spritehelix1 = (0, 0, 0, 30, 22)
        self.__spritehelix2 = (0, 30, 0, 30, 22)
        # Loop sequence
        self.__sprite_loop1 = (2, 0, 20, 32, 20)
        self.__sprite_loop2 = (2, 128, 20, 32, 20)
        self.__sprite_loop3 = (2, 30, 22, 32, 20)
        self.__sprite_loop4 = (2, 158, 24, 30, 14)
        self.__sprite_loop5 = (2, 158, 24, 30, 14)
        self.__sprite_loop6 = (2, 64, 24, 30, 16)
        self.__sprite_loop7 = (2, 32, 48, 32, 24)
        self.__sprite_loop8 = (2, 65, 45, 32, 28)
        self.__sprite_loop9 = (2, 128, 45, 34, 28)
        self.__sprite_loop10 = (2, 164, 45, 32, 26)
        self.__sprite_loop11 = (2, 196, 45, 32, 26)
        self.__sprite_loop12 = (2, 92, 26, 32, 14)
        self.__sprite_loop13 = (2, 98, 28, 32, 10)
        self.__sprite_loop14 = (2, 30, 22, 32, 20)
        self.__sprite_loop15 = (2, 128, 20, 32, 20)
        self.__sprite_loop16 = (2, 0, 20, 32, 20)
        self.__loop_counter = 0
        self.loops_allowed = 3

    def update(self):
        # Arrow buttons move the plane
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= constants.PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += constants.PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= constants.PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += constants.PLAYER_SPEED

        # Limiting plane movement to the game frame
        self.x = max(self.x, 0)
        self.x = min(self.x, constants.GAME_WIDTH - self.w)
        self.y = max(self.y, 0)
        self.y = min(self.y, constants.GAME_HEIGHT - self.h)

        # Shoot button
        if pyxel.btnp(pyxel.KEY_SPACE):
            Bullet(self.x + (constants.PLAYER_WIDTH - constants.BULLET_WIDTH) / 2,
                   self.y - constants.BULLET_HEIGHT, "player")
            pyxel.play(0, 0)

        # Loop button works only if the player can still turn
        if pyxel.btnp(pyxel.KEY_Z) and self.loops_allowed > 0:
            self.loop = True

    def draw(self):
        # Loop animation
        if self.loop:
            if self.__loop_counter < 30:
                if self.__loop_counter in [0, 1]:
                    pyxel.blt(self.x, self.y - 10, *self.__sprite_loop1, colkey=0)
                elif self.__loop_counter in [2, 3]:
                    pyxel.blt(self.x, self.y - 15, *self.__sprite_loop2, colkey=0)
                elif self.__loop_counter in [4, 5]:
                    pyxel.blt(self.x, self.y - 10, *self.__sprite_loop3, colkey=0)
                elif self.__loop_counter in [6, 7]:
                    pyxel.blt(self.x, self.y, *self.__sprite_loop4, colkey=0)
                elif self.__loop_counter in [8, 9]:
                    pyxel.blt(self.x, self.y - 40, *self.__sprite_loop5, colkey=0)
                elif self.__loop_counter in [10, 11]:
                    pyxel.blt(self.x, self.y + 20, *self.__sprite_loop6, colkey=0)
                elif self.__loop_counter in [12, 13]:
                    pyxel.blt(self.x, self.y + 40, *self.__sprite_loop7, colkey=0)
                elif self.__loop_counter in [14, 15]:
                    pyxel.blt(self.x, self.y + 60, *self.__sprite_loop8, colkey=0)
                elif self.__loop_counter in [16, 17]:
                    pyxel.blt(self.x, self.y + 60, *self.__sprite_loop9, colkey=0)
                elif self.__loop_counter in [16, 17]:
                    pyxel.blt(self.x, self.y + 60, *self.__sprite_loop10, colkey=0)
                elif self.__loop_counter in [18, 19]:
                    pyxel.blt(self.x, self.y + 60, *self.__sprite_loop11, colkey=0)
                elif self.__loop_counter in [20, 21]:
                    pyxel.blt(self.x, self.y + 50, *self.__sprite_loop12, colkey=0)
                elif self.__loop_counter in [22, 23]:
                    pyxel.blt(self.x, self.y + 40, *self.__sprite_loop13, colkey=0)
                elif self.__loop_counter in [24, 25]:
                    pyxel.blt(self.x, self.y + 30, *self.__sprite_loop14, colkey=0)
                elif self.__loop_counter in [26, 27]:
                    pyxel.blt(self.x, self.y + 20, *self.__sprite_loop15, colkey=0)
                elif self.__loop_counter in [28, 29]:
                    pyxel.blt(self.x, self.y, *self.__sprite_loop16, colkey=0)
                self.__loop_counter += 1
            else:
                self.loop = False
                self.__loop_counter = 0
                self.loops_allowed -= 1
        # Helix animation
        else:
            if pyxel.frame_count % 5 != 0:
                pyxel.blt(self.x, self.y, *self.__spritehelix1)
            if pyxel.frame_count % 5 == 0:
                pyxel.blt(self.x, self.y, *self.__spritehelix2)
