class Battleship:
	def __init__(self):
		self.boards = {
			1: [[0 for y in range(7)] for x in range(7)],
			2: [[0 for y in range(7)] for x in range(7)]
		}

	def __str__(self) -> str:
		string = ""

		for player, board in self.boards.items():
			string += f"{player}:\n"
			for row in board:
				string += f"{row}\n"

		return string
print(Battleship())
