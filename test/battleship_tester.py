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

		print(f"Pass {i}")

	return True

def check_ship_hits(test:int = 100) -> bool:
	"""
	Tests hitting ships, and misses.
	"""

	for i in range(tests):
		game = Battleship()

		board = game.return_board_as_array(1)

		for x in range(len(board)):
			for y in range(len(board[1])):
				hit_status = board[y][x] != 0

				game.attack(1, (x, y))

				if not ((game.players[1]["hits board"][y][x] == -1 and not hit_status) or (game.players[1]["hits board"][y][x] == 1 and hit_status)):
					print(f"Game: {game} | Location : {location}")

		print(f"pass{i}")
	return True

print("Board Gen: " + str(check_board_gen()))
