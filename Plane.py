import pyxel
import CONSTANTS

class Plane:
    def __init__(self, x: int, y:int):
        self.x = x
        self.y = y

        self.speed = 5
        self.sprite = (0, 0, 0, CONSTANTS.PLANE_WIDTH , CONSTANTS.PLANE_HEIGHT )
        self.lives = 3

        self.is_alive = True


    def move(self, direction: str, size: int):
        """ This is an example of a method that moves Plane, it receives the
        direction and the size of the board"""

        plane_x_size = self.sprite[3] #32
        plane_y_size = self.sprite[4] #32

        if direction.lower() == 'right' and self.x < size - plane_x_size:
            self.x = self.x + self.speed

        elif direction.lower() == 'left' and self.x > 0:
            self.x -= self.speed

        elif direction.lower() == "up" and self.y < size - plane_y_size:
            self.y = self.y + self.speed

        elif direction.lower() == 'down' and self.y > 0:
            self.y -= self.speed



