# -*- coding: utf-8 -*-

from game import Piece, Board
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

class GameTest(TestCase):
    '''
    Game related tests
    '''
    pass

