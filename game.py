
class Player:
	def __init__(self, name):
		self._name = name
		
class Piece:
	def __init__(self, player):
		self._player = player

	def can_catch(self, piece):
		return True

from copy import copy
class BasicGame:
	'''
	A very basic functional game, used to test features
	-------------
	| 0 |   |   |
	-------------
	|   |   |   |
	-------------
	|   |   | 1 |
	-------------
	'''
	TOTAL_PLAYERS = 2

	INITIAL_BOARD = [
		None, None, None,
		None, None, None,
		None, None, None,
	]

	def __init__(self, hostPlayer):
		self._pieces = {}
		self._board = copy(self.INITIAL_BOARD)
		self._players = [hostPlayer,]

	def join(self, player):
		# TODO check max game players
		# TODO check same player twice
		self._players.append(player)
		if len(self._players) == self.TOTAL_PLAYERS:
			self.initPlayerPieces()

	def initPlayerPieces(self):
		player0, player1 = self._players
		self._pieces[ (0,0) ] = Piece(player0)
		self._pieces[ (2,2) ] = Piece(player1)

	def move(self, initial, final):
		initial_piece = self._pieces.get(initial)
		final_piece = self._pieces.get(final)
		# FIXME
		
