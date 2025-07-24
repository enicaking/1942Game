import pyxel
import constants


class Bullet:
    """
    This class will describe the mechanism of shooting within the game
    """
    def __init__(self, x: int, y: int, entity: str) -> None:
        self.x = x
        self.y = y
        self.w = constants.BULLET_WIDTH
        self.h = constants.BULLET_HEIGHT
        self.alive = True
        self.entity = entity

        constants.bullet_list.append(self)

    def update(self):
        # Player bullets rise and enemy bullets fall
        if self.entity == "player":
            self.y -= constants.BULLET_SPEED
        elif self.entity == "enemy" or self.entity == "enemy_red":
            self.y += constants.BULLET_SPEED
        # Limited to game frame
        if self.y + self.h - 1 < 0:
            self.alive = False

    def draw(self):
        # Differentiating between double player shot and enemy pellets
        if self.entity == "player":
            pyxel.rect(self.x - 5, self.y, self.w, self.h, constants.BULLET_COLOR_PLAYER)
            pyxel.rect(self.x + 5, self.y, self.w, self.h, constants.BULLET_COLOR_PLAYER)
        elif self.entity == "enemy":
            pyxel.rect(self.x, self.y, self.w, self.h, constants.BULLET_COLOR_ENEMY)
        elif self.entity == "enemy_red":
            pyxel.blt(self.x, self.y, 2, 75, 90, 4, 4, colkey=0)
