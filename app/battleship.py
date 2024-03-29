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
			for ship in game.players[player]["ships"]:
				locations = ship.get_locations()

				for location in self.hits.keys():
					if location in locations:
						return False
			# checks if the ship locations are still on the board
			for location in self.hits.keys():
				if game.not_in_board(location):
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
			# creates dict of which location on the ship has been hit and not hit
			self.hits = {}
			for i in range(length):
				if vertical:
					self.hits[(location[0], location[1] + i)] = False
				else:
					self.hits[(location[0] + i, location[1])] = False
			# checks if the locations are valid, if so initialize, if not, throw an error
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
			# determines spawn location
			location = (random.randint(0, self.width), random.randint(0, self.height))
			# determines verticality
			vertical = (random.randint(0, 1) == 1)
			ship = None
			# tries to create ships until a valid one is created
			while ship == None:
				try:
					ship = self.Ship(self, location, vertical, size, player)
				except ValueError as e:
					debug_print(e)
					location = (random.randint(0, self.width), random.randint(0, self.height))
					vertical = (random.randint(0, 1) == 1)
			# adds valid ship to player ships when created
			self.players[player]["ships"].append(ship)

	def __init__(self, height:int=10, width:int=10, DEBUG:tuple = ()):
		"""
		Parameters
		----------
		height : int
			number of rows in the board (max y)
		width : int
			number of rows in the board (max x)
		DEBUG : bool
			whether or not AI move
		"""
		# DEBUG mode
		self.DEBUG = DEBUG
		# the board stats
		self.height = height
		self.width = width
		# the ship sizes available
		self.ship_sizes = [2, 3, 3, 4, 5]

		# player initialization
		player_num = 2
		self.players = {}

		# creates the items needed to be tracked for each player
		for i in range(player_num):
			self.players[i] = {
				"ships":[],
				"hits board":[[0 for x in range(self.width)] for y in range(self.height)]
			}

		for i in range(1, player_num):
			self.players[i]["AI"] = AI(self)

		# places random ship for the ai
		self.__randomize_ship_placement__()
		# starts with player 0
		self.current_player = 0
		self.winner = -1
		# move history recorder
		self.move_history = [] # tuple of (player:int, location:tuple(x,y))

	def return_board_as_array(self, player:int) -> list:
		# creates an array representation of the board. goes board[y][x] like in matrix notation.
		board = [[0 for x in range(self.width)] for y in range(self.height)]

		for ship in self.players[player]["ships"]:
			locations = ship.get_locations()
			# places the ship length on the corresponding ship location on the board
			for location in locations:
				debug_print(locations)
				board[location[1]][location[0]] = ship.length

		return board

	def not_in_board(self, location:tuple) -> bool:
		"""
		Parameters
		----------
		location : tuple
			(x, y) of location being checked

		Returns
		-------
		Whether or not the location is in the board.
		"""
		return (location[0] >= self.width or location[0] < 0) or (location[1] >= self.height or location[1] < 0)

	def advance_turn(self, latest_player:int, last_shot:tuple):
		"""
		Changes whose turn it is. And adds to latest move to history.

		latest_player : int
			the last player to make a move (who's turn are we advancing from)
		last_shot:tuple
			the last move they made
		"""
		self.move_history.append((latest_player, last_shot))
		# checks winner
		self.winner = self.check_winner()
		# advances current player tracker
		self.current_player += 1
		self.current_player %= len(self.players)
		# invokes AI if the player has an AI
		if 'AI-off' not in self.DEBUG:
			if 'AI' in self.players[self.current_player]:
				self.players[self.current_player]["AI"].attack()

	def check_winner(self) -> int:
		"""
		Checks if there's a winner

		Returns
		-------
		The winner
		"""
		sunk_players = []
		for player in self.players:
			if not ('TESTPLAYER' in self.DEBUG and player == 0):
				all_sunk = True
				for ship in self.players[player]["ships"]:
					all_sunk = all_sunk and ship.sunk() ## turns false if any ship is unsunk
				if all_sunk:
					sunk_players.append(player)

		if (len(self.players) - len(sunk_players)) == 1:
			return [player for player in self.players if player not in sunk_players][0]
		else:
			return -1

	def get_sunk_at_location(self, player:int, location:tuple) -> bool:
		"""
		Checks if the ship at a given location has been sunk
		"""
		for ship in self.players[player]['ships']:
			if location in ship.get_locations():
				return ship.sunk()

		return False

	def attack(self, player:int, location:tuple) -> bool:
		"""
		Changes hit board and ships hit status based on attacks.

		Parameters
		----------
		player : int
			The player being attacked
		location : tuple
			(x, y) of where you're hitting

		Returns
		-------
		If any ship was sunk this turn.
		"""
		if self.not_in_board(location):
			# checks if the hit is in the board
			raise ValueError(f"{location} is off the board")
		elif player == self.current_player: # error for self attack
			raise ValueError(f"Current player {self.current_player} is the same as attacked player {player}.")
		elif self.players[self.current_player]["hits board"][location[1]][location[0]] != 0 and not 'DOUBLEHITS' in self.DEBUG: # error for attacking the same square
			raise ValueError(f"Current player {self.current_player} has already attacked {location}.")
		else: # attack is valid
			for ship in self.players[player]["ships"]:
				if ship.hit(location):
					self.players[self.current_player]["hits board"][location[1]][location[0]] = 1
					self.advance_turn(self.current_player, location)

					return ship.sunk()

			self.players[self.current_player]["hits board"][location[1]][location[0]] = -1

		self.advance_turn(self.current_player, location)
		return False

	def get_move_history(self) -> tuple:
		"""
		Returns attack history as a tuple
		"""
		return tuple(self.move_history)

	def __str__(self) -> str:
		string = ""

		for player in self.players:
			# prints ships
			string += f"\n{player}:\nShips\n----\n"
			board = self.return_board_as_array(player)
			for row in board:
				string += f"{row}\n"
			# prints shots
			string += "Hits\n----\n"
			for row in self.players[player]["hits board"]:
				# not shot at is '*', hits are '@', misses are '#'
				string += f"{row}\n" .replace('0', '*').replace('-1', '#').replace('1', '@')

			string += '*' * self.width * 3
		return string

class AI:
	def __init__(self, game:Battleship, player:int = 1, difficulty:int = 0):
		self.player = player
		self.game = game
		self.status = False # False if you're hunting, True if you're targetting
		if difficulty == 0:
			self.mode = 'random'
			self.attacked_locations = []

	def attack(self):
		if self.mode == 'random':
			location = (random.randint(0, self.game.width - 1), random.randint(0, self.game.height - 1))

			while location in self.attacked_locations:
				location = (random.randint(0, self.game.width - 1), random.randint(0, self.game.height - 1))

			self.game.attack(0, location)
			self.attacked_locations.append(location)
		elif self.mode == 'hunt-target': # https://datagenetics.com/blog/december32011/index.html
			pass
