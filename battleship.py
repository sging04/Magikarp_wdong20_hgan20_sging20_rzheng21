class Battleship:
	def __init__(self):
		self.boards = {
			1: [[0 for y in range(7)] for x in range(7)],
			2: [[0 for y in range(7)] for x in range(7)]
		}

		self.ship_sizes = [2, 3, 3, 4, 5]

	def __str__(self) -> str:
		string = ""

		for player, board in self.boards.items():
			string += f"{player}:\n"
			for row in board:
				string += f"{row}\n"

		return string

	def hit(player:int, coord:tuple) -> bool:
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
