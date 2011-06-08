
class Player:
	def __init__(self, name):
		self._name = name

class Piece:
	def __init__(self, player):
		self._player = player

	def can_catch(self, piece):
		return True

class InvalidAction(Exception):
	pass

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
		self._turn = 0

	def test(self):
		return "Teste"

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

	def playerTurn(self):
		playerNo = self._turn % len(self._players)
		return self._players[playerNo]

	def _checkTurn(self, piece):
		if piece._player != self.playerTurn():
			raise InvalidAction()

	def _checkMove(self, initial, final):
		if abs(initial[0]-final[0] + initial[1]-final[1]) > 1:
			raise InvalidAction()

	def move(self, initial, final):
		initial_piece = self._pieces.get(initial)
		final_piece = self._pieces.get(final)

		if initial_piece is None: raise InvalidAction()
		self._checkTurn(initial_piece)
		self._checkMove(initial, final)

		self._pieces.pop(initial) #remove
		if final_piece: self._pieces.pop(final) #remove, if exists
		self._pieces[final] = initial_piece
		self._turn += 1
		return True

	def win(self):
		player = set([piece._player for piece in self._pieces.values()])
		if len(player) == 1: return player.pop()
		return None

