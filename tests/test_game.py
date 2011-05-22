
import unittest
from game import BasicGame, Player

class TestPlayer(unittest.TestCase):
	'''
	Test player class and method - represents the player (and will be a
	client connection on a network)
	'''
	def test_new_player(self):
		p = Player(u"player 0")
		self.assertEqual(p._name, u"player 0")

class TestPlayerGame(unittest.TestCase):
	'''
	Test a Game class - player related methods
	'''

	def test_new_game(self):
		'''
		Start a new game
		'''
		player0 = Player(u"player 0")
		game = BasicGame(player0)

	def test_join_game(self):
		'''
		Join to a existing game
		'''
		player0 = Player(u"player 0")
		player1 = Player(u"player 1")
		game = BasicGame(player0)
		game.join(player1)

class TestBasicGame(unittest.TestCase):
	'''
	Test a Game class - is the implementation of the rules of the game (will
	be a server and need to validate every coup.
	'''

	def setUp(self):
		self.player0 = Player(u"player 0")
		self.player1 = Player(u"player 1")
		self.game = BasicGame(self.player0)
		self.game.join(self.player1)

	def test_pieces(self):
		'''
		Pieces on the board
		'''
		game = self.game
		self.assertTrue(game._pieces[(0,0)]._player == self.player0)
		self.assertTrue(game._pieces[(2,2)]._player == self.player1)

