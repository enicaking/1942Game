import CONSTANTS
import pyxel
class Background:
    def __init__(self):
        self.stars = []
        for i in range(CONSTANTS.NUM_STARS):
            self.stars.append(
                (
                    pyxel.rndi(0, pyxel.width - 1),
                    pyxel.rndi(0, pyxel.height - 1),
                    pyxel.rndf(1, 2.5),
                )
            )

    def update(self):
        for i, (x, y, speed) in enumerate(self.stars):
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            self.stars[i] = (x, y, speed)

    def draw(self):
        for (x, y, speed) in self.stars:
            pyxel.pset(x, y, CONSTANTS.STAR_COLOR_HIGH if speed > 1.8 else CONSTANTS.STAR_COLOR_LOW)
