from random import *
import pyxel
import constants


class Background:
    """
    This class will resemble the appearance of the space
    """
    # No properties and setters since there are no attributes

    def __init__(self):
        # Randomising a set number of stars
        self.__star_list = []
        for i in range(constants.STAR_COUNT):
            self.__star_list.append((random() * pyxel.width, random() * pyxel.height, random() * 1.5 + 1))

    def update(self):
        for i, (x, y, speed) in enumerate(self.__star_list):
            # Stars move downwards to create illusion of player moving forwards
            y += speed
            # Infinite loop
            if y >= pyxel.height:
                y -= pyxel.height
            # Updating
            self.__star_list[i] = (x, y, speed)

    def draw(self):
        for (x, y, speed) in self.__star_list:
            # Drawing each star as a different colored dot to create depth
            pyxel.pset(x, y, constants.STAR_COLOR_HIGH if speed > 1.8 else constants.STAR_COLOR_LOW)
