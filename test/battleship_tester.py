import sys
import time
from os import path
#adds the repo to the sys paths. Gets abs path, gets parent directory, then the parent directory of that to get repo directory.
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))+ "/app")
#imports from ../app/battleship.py
from app.battleship import Battleship
import random
# seeds battleship
Battleship.random = random

print(Battleship())

def check_board_gen(tests:int = 100) -> bool:
	"""
	Tests the AI board generation. Gets collisions as well, making sure there's no overlap.
	"""
	tests = 100
	expected_ships = {
		2 : 2,
		3 : 6,
		4 : 4,
		5 : 5
	} #expected amount of each ship segment

	for i in range(tests):
		game = Battleship()
		# print(game)
		board = str(game.return_board_as_array(1)) # gets board for the AI

		for ship, segments in expected_ships.items():
			if board.count(str(ship)) != segments:
				return False

	return True

print("Board Gen: " + str(check_board_gen()))
