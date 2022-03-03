class Battleship:
	def __init__(self):
		self.board1 = [[0 for y in range(7)] for x in range(7)]
		self.board2 = [[0 for y in range(7)] for x in range(7)]

	def __str__(self):
		return "{board1} \n {board2}".format(board1=self.board1, board2=self.board2)

print(Battleship())
