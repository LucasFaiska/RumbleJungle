
import unittest
from game import BasicGame, Player, InvalidAction

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
		self.assertEqual(game._pieces[(0,0)]._player, self.player0)
		self.assertEqual(game._pieces[(2,2)]._player, self.player1)

	def test_turn(self):
		'''
		After moving, it changes the player turn (not when runs 
		"playerTurn()")
		'''
		game = self.game
		self.assertEqual(game.playerTurn(), self.player0)
		self.assertEqual(game.playerTurn(), self.player0)
		game.move((0,0), (0,1))
		self.assertEqual(game.playerTurn(), self.player1)
		game.move((2,2), (2,1))
		self.assertEqual(game.playerTurn(), self.player0)

	def test_move(self):
		'''
		Move pieces on the board
		'''
		game = self.game
		self.assertTrue(game.move(initial=(0,0), final=(0,1)))
		self.assertEqual(game._pieces[(0,1)]._player, self.player0)

	def test_move_without_piece(self):
		'''
		Raises exception when no piece in initial place
		'''
		game = self.game
		self.assertRaises(InvalidAction, game.move, (1,1), (2,1))

	def test_move_wrong_player(self):
		'''
		Raises exception when wrong player try a movement
		(2,2) is a player1 piece, but player0 starts
		'''
		game = self.game
		self.assertRaises(InvalidAction, game.move, (2,2), (2,1))

	def test_move_wrong_destination(self):
		'''
		Game not allow go 2 squares long
		'''
		game = self.game
		self.assertRaises(InvalidAction, game.move, (0,0), (0,2))
		self.assertRaises(InvalidAction, game.move, (0,0), (2,0))
		self.assertRaises(InvalidAction, game.move, (0,0), (2,2))

	def test_win(self):
		'''
		Test when some player win the game
		'''
		game = self.game
		self.assertEqual(game.win(), None)
		game.move( (0,0), (0,1) )
		self.assertEqual(game.win(), None)
		game.move( (2,2), (2,1) )
		self.assertEqual(game.win(), None)
		game.move( (0,1), (1,1) )
		self.assertEqual(game.win(), None)
		game.move( (2,1), (1,1) ) # eat and win!
		self.assertEqual(game.win(), self.player1)

