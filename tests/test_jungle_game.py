# -*- coding: utf-8 -*-

from game import Piece, Hole, Board, InvalidMovement
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

        piece1 = Piece(player1, Piece.MOUSE)
        piece2 = Piece(player2, 2)

        self.failIf(piece1.can_catch(piece2))
        self.assertTrue(piece2.can_catch(piece1))

        piece2 = Piece(player2, Piece.MOUSE)
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

        piece1 = Piece(player1, Piece.MOUSE)
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

        piece1 = Piece(player1, Piece.MOUSE)
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
            (8,8): Piece(player2, 7),

            (0, 3): Hole(player1),
            (8, 3): Hole(player2),
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

    def test_piece_move_2(self):
        '''
        Movement are allowed just for 1 square by time
        '''
        board1 = self.board
        self.assertRaises(InvalidMovement, board1.move, (0,0), (2,0))
        self.assertTrue((0,0) in board1._pieces)
        self.assertRaises(InvalidMovement, board1.move, (0,0), (0,2))
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

    def test_mouse_into_lake(self):
        '''
        Mouses (and just Mouses) can get into a lake
        '''
        board1 = self.board
        player1 = self.player1
        board1._pieces.update({
            (2,1): Piece(player1, 2),
        })
        self.assertRaises(InvalidMovement, board1.move, (2,1), (3,1))

        board1._pieces.update({
            (2,1): Piece(player1, Piece.MOUSE),
        })
        board1.move( (2,1), (3,1) )
        self.assertEqual(board1._pieces[(3,1)], Piece(player1, Piece.MOUSE))

    def test_mouse_into_lake_capture(self):
        '''
        Mouses can't get into (or out) a lake and capture in same movement
        '''
        board1 = self.board
        player1 = self.player1
        player2 = self.player2

        board1._pieces.update({
            (3,1): Piece(player1, Piece.MOUSE),
            (2,1): Piece(player2, Piece.MOUSE),
        })
        self.assertRaises(InvalidMovement, board1.move, (3,1), (2,1))

        board1._pieces.update({
            (2,1): Piece(player1, Piece.MOUSE),
            (3,1): Piece(player2, Piece.MOUSE),
        })
        self.assertRaises(InvalidMovement, board1.move, (2,1), (3,1))

        board1._pieces.update({
            (3,2): Piece(player1, Piece.MOUSE),
            (3,1): Piece(player2, Piece.MOUSE),
        })
        board1.move((3,2), (3,1))
        self.assertEqual(board1._pieces[(3,1)], Piece(player1, Piece.MOUSE))

    def test_jump_lake(self):
        '''
        Tigers and lions can jump the lakes
        '''
        board1 = self.board
        player1 = self.player1

        board1._pieces.update({
            (3,0): Piece(player1, Piece.LION),
        })
        board1.move( (3,0), (3,3) )
        self.assertEqual(board1._pieces[(3,3)], Piece(player1, Piece.LION))

        board1._pieces.update({
            (2,1): Piece(player1, Piece.LION),
        })

        # player1 can play againt
        board1.turn = 0

        board1.move( (2,1), (6,1) )
        self.assertEqual(board1._pieces[(6,1)], Piece(player1, Piece.LION))


    def test_cant_jump_not_lake(self):
        '''
        If aren't a lake, can't jump
        Or even have EARTH between lakes
        '''
        board1 = self.board
        player1 = self.player1

        board1._pieces.update({
            (2,0): Piece(player1, Piece.LION),
        })
        self.assertRaises(InvalidMovement, board1.move, (2,0), (6,0))
        self.assertEqual(board1._pieces[(2,0)], Piece(player1, Piece.LION))

        board1._pieces.update({
            (3,0): Piece(player1, Piece.LION),
        })
        self.assertRaises(InvalidMovement, board1.move, (3,0), (3,6))
        self.assertEqual(board1._pieces[(3,0)], Piece(player1, Piece.LION))


    def test_cant_jump(self):
        '''
        Elephants can't jump
        '''
        board1 = self.board
        player1 = self.player1

        board1._pieces.update({
            (3,0): Piece(player1, Piece.ELEPHANT),
        })
        self.assertRaises(InvalidMovement, board1.move, (3,0), (3,3))
        self.assertEqual(board1._pieces[(3,0)], Piece(player1, Piece.ELEPHANT))

    def test_cant_jump_if_mouses(self):
        '''
        If mouses are into the lake, tigers and lions can't jump
        '''
        board1 = self.board
        player1 = self.player1

        board1._pieces.update({
            (3,0): Piece(player1, Piece.TIGER),
            (3,1): Piece(player1, Piece.MOUSE)
        })
        self.assertRaises(InvalidMovement, board1.move, (3,0), (3,3))
        self.assertEqual(board1._pieces[(3,0)], Piece(player1, Piece.TIGER))

        board1._pieces.update({
            (2,1): Piece(player1, Piece.TIGER),
            (3,1): Piece(player1, Piece.MOUSE)
        })
        self.assertRaises(InvalidMovement, board1.move, (2,1), (3,1))
        self.assertEqual(board1._pieces[(2,1)], Piece(player1, Piece.TIGER))

    def test_move_hole(self):
        '''
        A player cannot move the hole
        '''
        board1 = self.board
        player1 = self.player1

        self.assertRaises(InvalidMovement, board1.move, (0,3), (1,3))

    def test_move_to_hole(self):
        '''
        A piece can't move to your player's hole
        '''
        board1 = self.board
        player1 = self.player1

        board1._pieces.update({
            (0,2): Piece(player1, Piece.TIGER),
        })
        self.assertRaises(InvalidMovement, board1.move, (0,2), (0,3))
        self.assertEqual(board1._pieces[(0,2)], Piece(player1, Piece.TIGER))

    def test_hole_capture(self):
        '''
        When a piece capture the enemy's hole, the game is over
        '''
        board1 = self.board
        player1 = self.player1

        board1._pieces.update({
            (8,2): Piece(player1, Piece.TIGER),
        })
        board1.move((8,2), (8,3))

        self.assertEqual(board1._winner, player1)
        self.assertRaises(InvalidMovement, board1.move, (8,3), (8,4))

    def test_into_trap(self):
        '''
        When a piece get into a trap, lose all your force (value=0)
        When get out a trap, get your force back
        '''
        board1 = self.board
        player1 = self.player1

        board1._pieces.update({
            (0,1): Piece(player1, Piece.TIGER),
        })
        board1.move((0,1), (0,2))

        piece = board1._pieces[(0,2)]
        self.assertEqual(piece._value, 0)

        # reset turn, player1 can play again
        board1.turn = 0

        board1.move((0,2), (0,1))
        piece = board1._pieces[(0,1)]
        self.assertEqual(piece._value, Piece.TIGER)

    def test_into_trap_catch(self):
        '''
        When a piece get into a trap, anyone can catch it
        '''
        board1 = self.board
        player1 = self.player1
        player2 = self.player2

        board1._pieces.update({
            (0,1): Piece(player1, Piece.TIGER),

            # normaly, a mouse can't catch a tiger
            (0,3): Piece(player2, Piece.MOUSE),
        })

        board1.move((0,1), (0,2)) # Tiger into a trap
        board1.move((0,3), (0,2)) # Mouse catch a Tiger

        piece = board1._pieces[(0,2)]

        # piece are from player2
        self.assertEqual(piece._player, player2)

        # and now mouse are in a trap
        self.assertEqual(piece._value, 0)


class GameTest(TestCase):
    '''
    Game related tests
    '''
    pass

