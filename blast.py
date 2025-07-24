import pyxel
import constants


class Blast:
    """
    This class will describe the mechanism of the blast effect from collisions within the game
    """
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.__radius = constants.BLAST_START_RADIUS
        self.alive = True

        constants.blast_list.append(self)

    def update(self):
        # Radius expands until it gets big enough to dissipate
        self.__radius += 1
        if self.__radius > constants.BLAST_END_RADIUS:
            self.alive = False

    def draw(self):
        # Two circles to create dimension within the blast
        pyxel.circ(self.x, self.y, self.__radius, constants.BLAST_COLOR_IN)
        pyxel.circb(self.x, self.y, self.__radius, constants.BLAST_COLOR_OUT)
