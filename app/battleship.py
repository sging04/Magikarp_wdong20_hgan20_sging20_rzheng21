import random

def debug_print(input:str, DEBUG=False):
	if DEBUG:
		print(input)

class Battleship:
	class Ship:
		def check_valid_location(self, game:'Battleship', location:tuple, vertical:bool, length:int, player:int) -> bool:
			"""
			Parameters
			----------
			game : Battleship
				The game in which the ship exists
			length : int
				The length of the ship
			location : tuple
				(x, y) of the left most/top most space the ship occupies. 0 indexed.
			vertical : bool
				whether or not the ship is vertical
			player : int
				which player's board it's on

			Returns
			-------
			Whether or not the ship is placed in a valid location
			"""
			# this is a very naive solution but it works (other solution would be checking line overlaps but I don't want to do that + this is more generalizable)
			for ship in game.players[player]:
				locations = ship.get_locations()

				for location in self.hits.keys():
					if location in locations:
						return False

			for location in self.hits.keys():
				if (location[0] >= game.width or location[0] < 0) or (location[1] >= game.height or location[0] < 0):
					return False

			return True

		def __init__(self, game:'Battleship', location:tuple, vertical:bool, length:int, player:int):
			"""
			Parameters
			----------
			game : Battleship
				The game in which the ship exists
			length : int
				The length of the ship
			location : tuple
				(x, y) of the left most/top most space the ship occupies. 0 indexed.
			vertical : bool
				whether or not the ship is vertical
			"""
			self.hits = {}
			for i in range(length):
				if vertical:
					self.hits[(location[0], location[1] + i)] = False
				else:
					self.hits[(location[0] + i, location[1])] = False

			if self.check_valid_location(game, location, vertical, length, player):
				self.game = game
				self.length = length
				self.location = location
				self.vertical = vertical
			else:
				raise ValueError(f"The ship placement is invalid because part or all of the ship is off the board.\nLocation:{location} | Game:{game} | Vertical:{vertical} | Length:{length}")

		def hit(self, location:tuple) -> bool:
			"""
			Tells you if you've hit a location or not. If you do, it also marks the hit on the ship itself.

			Parameters
			----------
			location : tuple
				(x, y) of where you're trying to hit

			Returns
			-------
			A boolean if you hit something.
			"""
			if location in self.hits:
				self.hits[location] = True
				return True
			else:
				return False

		def get_locations(self) -> list:
			"""
			Returns
			-------
			A list of locations where the ship is located.
			"""
			return list(self.hits.keys())

		def sunk(self) -> bool:
			"""
			Returns
			-------
			If all the ship sections have been sunk.
			"""
			if False not in self.hits.values():
				return True
			else:
				return False

		def __str__(self):
			return f"Length: {length} | Location: {location} | Vertical: {vertical} | Player: {player}"

	def __randomize_ship_placement__(self, player:int = 1):
		"""
		Fills a playerboard with all the ships needed.

		Parameters
		----------
		player : int
			Which player's board are we updating?
		"""
		for size in self.ship_sizes:
			location = (random.randint(0, self.width), random.randint(0, self.height))
			vertical = (random.randint(0, 1) == 1)
			ship = None

			while ship == None:
				try:
					ship = self.Ship(self, location, vertical, size, player)
				except ValueError as e:
					debug_print(e)
					location = (random.randint(0, self.width), random.randint(0, self.height))
					vertical = (random.randint(0, 1) == 1)

			self.players[player]["ships"].append(ship)

	def __init__(self, height:int=7, width:int=7):
		"""
		Parameters
		----------
		height : int
			number of rows in the board (max y)
		width : int
			number of rows in the board (max x)
		"""
		# the board stats
		self.height = height
		self.width = width
		# the ship sizes available
		self.ship_sizes = [2, 3, 3, 4, 5]

		player_num = 2
		self.players = {}

		for i in range(player_num):
			self.players[i] = {
				"ships":[],
				"hits board":[[False for x in range(self.width)] for y in range(self.height)]
			}

		self.__randomize_ship_placement__()
		self.current_player = 0

	def return_board_as_array(self, player:int) -> list:
		board = [[0 for x in range(self.width)] for y in range(self.height)]

		for ship in self.players[player]["ships"]:
			locations = ship.get_locations()

			for location in locations:
				board[location[1]][location[0]] = ship.length

		return board

	def attack(self, player:int, location:tuple):
		"""
		Changes hit board and ships hit status based on attacks.

		Parameters
		----------
		player : int
			The player being attacked
		location : tuple
			(x, y) of where you're hitting
		"""

	def __str__(self) -> str:
		string = ""

		for player in self.players:
			string += f"{player}:\n"
			board = self.return_board_as_array(player)

			for row in board:
				string += f"{row}\n"

		return string

print(Battleship())
