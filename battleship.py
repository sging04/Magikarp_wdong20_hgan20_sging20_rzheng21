class Battleship:
	class Ship:
		def __check_valid_location__(game:Battleship, location:tuple, vertical:bool, length:int, player:int) -> bool:
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

			def ship_collision(game:Battleship, location:tuple, vertical:bool, length:int, player:int):
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
				Whether or not the ship overlaps with another ship
				"""

			if location[0] >= game.length or location[1] >= game.width:
				return False # check to see if the starting location is even in the board
			else:
				if vertical == True:
					return location[1] + length < game.height - 1
				else:
					return location[1] + length < game.width - 1

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
			if __check_valid_location__(game, location, vertical, length):
				self.game = game
				self.length = length
				self.location = location
				self.vertical = vertical
				self.player = player

				#keeps track of which ship segments have been hit
				self.hits = {}
				for i in range(length):
					if vertical:
						self.hits[(location[0], location[1] + i)] = False
					else:
						self.hits[(location[0] + i, location[1])] = False
			else:
				raise InputError(f"The ship placement is invalid because part or all of the ship is off the board.\nLocation:{location} | Game:{game} | Vertical:{vertical} | Length:{length}")

		def hit(self, location:tuple) -> bool:
			if location in self.hits:
				self.hits[location] = True
				return True
			else:
				return False

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

	def __str__(self) -> str:
		string = ""

		for player, board in self.boards.items():
			string += f"{player}:\n"
			for row in board:
				string += f"{row}\n"

		return string

print(Battleship())
