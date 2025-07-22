import pyxel

from Board import Board
from Background import Background
from Bullets import Bullet
import CONSTANTS

board = Board(CONSTANTS.X,CONSTANTS.Y)

pyxel.run(board.update, board.draw)