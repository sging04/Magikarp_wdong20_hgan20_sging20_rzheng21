class Battleship:
	class Ship:
		def check_valid_location(game:Battleship, location:tuple, vertical:bool, length:int, player:int) -> bool:
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

		def __init__(self, game:Battleship, length:int, location:tuple, vertical:bool, player:int):
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

			if check_valid_location(game, location, vertical, length):
				self.game = game
				self.length = length
				self.location = location
				self.vertical = vertical
			else:
				raise InputError(f"The ship placement is invalid because part or all of the ship is off the board.\nLocation:{location} | Game:{game} | Vertical:{vertical} | Length:{length}")

		def hit(self, location:tuple) -> bool:
			if location in self.hits:
				self.hits[location] = True
				return True
			else:
				return False

		def get_locations(self) -> list:
			return list(self.hits.keys())

		def sunk(self) -> bool:
			if False not in self.hits.values():
				return True
			else:
				return False

		def __str__(self):
			return f"Length: {length} | Location: {location} | Vertical: {vertical} | Player: {player}"

	def __new_ship__(self, location:tuple, vertical:bool, length:int, player:int) -> Ship:
		return Ship(self, location, vertical, length, player)

	def __randomize_ship_placement__(self):
		for size in self.ship_sizes:


	def __init__(self, height:int=7, width:int=7):
		# the board stats
		self.height = height
		self.width = width
		# the ship sizes available
		self.ship_sizes = [2, 3, 3, 4, 5]

		player_num = 2
		self.players = {}

		for i in range(player_num):
			self.players{i} = []

		__randomize_ship_placement__()

	def __str__(self) -> str:
		string = ""

		for player, board in self.boards.items():
			string += f"{player}:\n"
			for row in board:
				string += f"{row}\n"

		return string

print(Battleship())
