# main.py
# Enica King and Estefany Gonzalez
# Code for main 1942Game file


import pyxel
import CONSTANTS
from Board import Board

board = Board(CONSTANTS.X, CONSTANTS.Y)

pyxel.run(board.update, board.draw)

