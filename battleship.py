class Battleship:
	class Ship:
		def __check_valid_location__(location:tuple, vertical:bool, length:int) -> bool:
			"""
			Parameters
			----------
			length : int
				The length of the ship
			location : tuple
				(x, y) of the left most/top most space the ship occupies
			vertical : bool
				whether or not the ship is vertical
			"""


		def __init__(self, game:Battleship, length:int, location:tuple, vertical:bool):
			"""
			Parameters
			----------
			game : Battleship
				The game in which the ship exists
			length : int
				The length of the ship
			location : tuple
				(x, y) of the left most/top most space the ship occupies
			vertical : bool
				whether or not the ship is vertical
			"""
			self.length = length
			self.location = location
			self.vertical = vertical

	def __new_ship__(self, location:tuple, vertical:bool, length:int) -> Ship:
		return Ship(self, location, vertical, length)

	def __init__(self):
		# the player board representations
		self.boards = {
			1: [[0 for y in range(7)] for x in range(7)],
			2: [[0 for y in range(7)] for x in range(7)]
		}
		# the ship sizes available
		self.ship_sizes = [2, 3, 3, 4, 5]

	def __str__(self) -> str:
		string = ""

		for player, board in self.boards.items():
			string += f"{player}:\n"
			for row in board:
				string += f"{row}\n"

		return string

	def hit(player:int, coord:tuple) -> bool:
		"""
		Checks if the player shot at was hit, and if so marks it.

		Parameters
		----------
		player : int
			The player being shot at
		coord : tuple
			The (x, y) coordinate where the shot is being aimed at

		Returns
		-------
		bool
			Whether or not the hit landed.

		Extra
		-----
		Positive numbers represent ships, with the number being the length of the ship. (note this was for checking if a ship sinks, but since there's 2 threes that may be a problem)
		0 is an empty space
		Negative numbers represent hit sections, with the magnitude corresponding to ship length.
		"""
		if player not in self.boards:
			raise KeyError("Player does not exist")
		elif coord[0] >= len(self.boards[player]) or coord[1] >= len(self.boards[player][0]):
			return ValueError("Coordinate does not exist")
		else:
			if self.boards[player][coord[0]][coord[1]] != 0:
				self.boards[player][coord[0]][coord[1]] = -self.boards[player][coord[0]][coord[1]]
				return True
			else:
				self.boards[player][coord[0]][coord[1]] = -max(self.ship_sizes) + 1
				return False
print(Battleship())
