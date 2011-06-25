# -*- coding: utf-8 -*-

from game import Piece, Board, InvalidMovement
from unittest import TestCase

class MockPlayer:
    pass

class PieceTest(TestCase):
    '''
    Piece related tests
    '''

    def test_capture(self):
        '''
        1. Mouse/rat
        2. Cat
        A catch is allowed to less or equal value. A cat can catch a mouse, but
        a mouse can't catch a cat
        '''
        player1 = MockPlayer()
        player2 = MockPlayer()

        piece1 = Piece(player1, 1)
        piece2 = Piece(player2, 2)

        self.failIf(piece1.can_catch(piece2))
        self.assertTrue(piece2.can_catch(piece1))

        piece2 = Piece(player2, 1)
        self.assertTrue(piece2.can_catch(piece1))
        self.assertTrue(piece1.can_catch(piece2))

    def test_elephant_capture(self):
        '''
        1. Mouse/rat
        8. Elephant
        The exception is rax x elephant: the elephant can't capture the mouse
        and the mouse can capture the elephant
        '''
        player1 = MockPlayer()
        player2 = MockPlayer()

        piece1 = Piece(player1, 1)
        piece8 = Piece(player2, 8)

        self.failIf(piece8.can_catch(piece1))
        self.assertTrue(piece1.can_catch(piece8))

    def test_trap_capture(self):
        '''
        If a piece are in a trap, your value is 0 and it can be captured by any
        other piece
        '''
        player1 = MockPlayer()
        player2 = MockPlayer()

        piece1 = Piece(player1, 1)
        piece2 = Piece(player2, 2)

        piece2.trap()
        self.assertTrue(piece1.can_catch(piece2))

        piece2.release()
        self.failIf(piece1.can_catch(piece2))

class BoardTest(TestCase):
    '''
    Board related test
    '''
    def test_board_init(self):
        '''
        When create a new board to play, the INITIAL_BOARD are copied to _board
        '''
        player = MockPlayer()

        board1 = Board(player)
        self.assertEqual(board1._board, Board.INITIAL_BOARD)

    def test_board_join(self):
        '''
        When player2 join to the game, the pieces are in the board.
        '''
        player1 = MockPlayer()
        player2 = MockPlayer()

        board1 = Board(player1)
        board1.join(player2)

        self.assertEqual(board1._pieces[ (0,0) ], Piece(player1, 7))

class BoardMoveTest(TestCase):
    '''
    Movement roules on the board
    '''
    def setUp(self):
        player1 = MockPlayer()
        player2 = MockPlayer()

        board1 = Board(player1)
        board1.join(player2)

        board1._pieces = {
            (0,0): Piece(player1, 7),
            (8,8): Piece(player2, 7)
        }

        self.board = board1
        self.player1 = player1
        self.player2 = player2

    def test_piece_move_horizontally(self):
        '''
        Move horizontal
        '''
        board1 = self.board
        board1.move( (0,0), (0,1) )
        self.assertTrue((0,1) in board1._pieces)

    def test_piece_move_vertically(self):
        '''
        Move vertically
        '''
        board1 = self.board
        board1.move( (0,0), (1,0) )
        self.assertTrue((1,0) in board1._pieces)

    def test_piece_move_diagonally(self):
        '''
        Move horizontal or vertically, but not diagonal
        '''
        board1 = self.board
        self.assertRaises(InvalidMovement, board1.move, (0,0), (1,1))
        self.assertTrue((0,0) in board1._pieces)

    def test_piece_wrong_player(self):
        '''
        First player begin the game
        '''
        board1 = self.board
        self.assertRaises(InvalidMovement, board1.move, (8,8), (8,7))

    def test_wrong_piece(self):
        '''
        Check the correct coordinator
        '''
        board1 = self.board
        self.assertRaises(InvalidMovement, board1.move, (5,5), (6,5))

    def test_capture(self):
        '''
        Test a piece capture
        '''
        board1 = self.board
        player1 = self.player1
        player2 = self.player2

        board1._pieces.update({
            (1,0): Piece(player2, 7),
        })
        board1.move( (0,0), (1,0) )
        self.assertEqual(board1._pieces[(1,0)], Piece(player1, 7))

    def test_not_capture(self):
        '''
        Test a piece capture, but with a larger value
        '''
        board1 = self.board
        player1 = self.player1
        player2 = self.player2

        board1._pieces.update({
            (1,0): Piece(player2, 8),
        })
        self.assertRaises(InvalidMovement, board1.move, (0,0), (1,0))

    def test_same_player_piece(self):
        '''
        Cannot capture a same team's piece
        '''
        board1 = self.board
        player1 = self.player1
        board1._pieces.update({
            (1,0): Piece(player1, 7),
        })
        self.assertRaises(InvalidMovement, board1.move, (0,0), (1,0))


class GameTest(TestCase):
    '''
    Game related tests
    '''
    pass

