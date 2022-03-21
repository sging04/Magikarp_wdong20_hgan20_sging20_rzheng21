import sys
import time
from os import path
#adds the repo to the sys paths. Gets abs path, gets parent directory, then the parent directory of that to get repo directory.
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))+ "/app")
#imports from ../app/battleship.py
from app.battleship import Battleship
import math
import random
# seeds battleship
Battleship.random = random

print(Battleship())
DEBUG_MODES = (
	'AI-off', #AI does not make moves
	'TESTPLAYER' # does not check player 1
)

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
		game = Battleship(DEBUG = ('TESTPLAYER', 'AI-off'))
		# print(game)
		board = str(game.return_board_as_array(1)) # gets board for the AI

		for ship, segments in expected_ships.items():
			if board.count(str(ship)) != segments:
				return False

		# print(f"Pass {i}")

	return True

def check_ship_hits(tests:int = 100) -> bool:
	"""
	Tests hitting ships, and misses.
	"""

	for i in range(tests):
		game = Battleship(DEBUG = ('TESTPLAYER', 'AI-off'))

		board = game.return_board_as_array(1)

		for x in range(len(board)):
			for y in range(len(board[1])):
				hit_status = board[y][x] != 0
				# print(hit_status)

				game.attack(1, (x, y))
				hit_value = game.players[0]["hits board"][y][x]

				if not ((hit_value == -1 and not hit_status) or (hit_value == 1 and hit_status)):
					print(f"Game: {game} | Location : ({x}, {y})")
					return False

				game.attack(0, (x, y)) # just to pass the turn back
		# print(f"pass{i} | Game: {game}")
	return True

def check_ship_sinks(tests:int = 100) -> bool:
	"""
	Tests hitting ships, and sinks.
	"""

	for n in range(tests):
		game = Battleship(DEBUG = ('TESTPLAYER', 'AI-off'))

		board = game.return_board_as_array(1)

		for ship in game.players[1]["ships"]:
			for i in range(len(ship.get_locations())-1):
				if game.attack(1, ship.get_locations()[i]): #THIS SHOULD ALWAYS BE FALSE IF THE SHIP ISNT SUNK, AND IT ISNT SUNK IF WE DONT HIT THE LAST BIT
					return False
				game.attack(0, ship.get_locations()[i]) # passes the turn back
			if not game.attack(1, ship.get_locations()[-1]): #THIS SHOULD ALWAYS BE FALSE IF THE SHIP IS SUNK
				return False
			game.attack(0, ship.get_locations()[-1])#passes the turn back

		# print(n, f"{game}")
	return True

def check_check_winner(tests:int = 100) -> bool:
	"""
	Tests the winner function
	"""
	for n in range(tests):
		game = Battleship(DEBUG = ('TESTPLAYER', 'AI-off'))

		board = game.return_board_as_array(1)

		for ship in game.players[1]["ships"]:
			for i in range(len(ship.get_locations())-1):
				if game.attack(1, ship.get_locations()[i]): #THIS SHOULD ALWAYS BE FALSE IF THE SHIP ISNT SUNK, AND IT ISNT SUNK IF WE DONT HIT THE LAST BIT
					return False
				game.attack(0, ship.get_locations()[i]) # passes the turn back
			if not game.attack(1, ship.get_locations()[-1]): #THIS SHOULD ALWAYS BE FALSE IF THE SHIP IS SUNK
				return False
			game.attack(0, ship.get_locations()[-1])#passes the turn back

		if game.check_winner() != 0:
			return False

		# print(n)

	return True

def check_random_ai(tests:int = 100) -> bool:
	"""
	Tests the random AI
	"""

	for i in range(tests):
		game = Battleship(DEBUG = ('DOUBLEHITS',))
		game.__randomize_ship_placement__(0)

		for x in range(game.width):
			for y in range(game.height):
				if game.check_winner() != -1:
					break

				game.attack(1, (0,0))
				# print(game) # Visual spot check: passed

		if game.check_winner() == -1:
			return False # you should've won

	return True

def check_move_history(tests:int = 100) -> bool:
	"""
	Checks move history tracker
	"""

	for n in range(tests):
		game = Battleship(DEBUG = ('AI-off'))
		game.__randomize_ship_placement__(0)

		individual_moves = {
			0 : [],
			1 : []
		}


		for x in range(game.width * game.height * 2):
			# random move
			location = (random.randint(0, game.width - 1), random.randint(0, game.height - 1))

			while location in individual_moves[x % 2]:
				location = (random.randint(0, game.width - 1), random.randint(0, game.height - 1))

			individual_moves[x % 2].append(location)
			game.attack((x + 1) % 2, location)

		# merges individual move history for complete move history
		history = []

		game_length = sum([len(moves) for moves in individual_moves.values()])
		for i in range(game_length):
			player = i % len(individual_moves)
			history.append((player, individual_moves[player][math.floor(i / len(individual_moves))]))

		if tuple(history) != game.get_move_history():
			print(history, game.get_move_history())
			return False

		print(f"{n} --------------\n{game}")

	return True

print("Board Gen: " + str(check_board_gen()))
print("Hits: " + str(check_ship_hits()))
print("Sinks: " + str(check_ship_sinks()))
print("Check win: " + str(check_check_winner()))
print("Random: " + str(check_random_ai()))
print("Move history: " + str(check_move_history()))
