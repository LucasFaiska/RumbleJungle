
class InvalidMovement(Exception):
    pass

class Hole:
    '''
    A flag, like in "flag capture". The final objective into the game
    '''
    FIXED = True
    _value = -1 # anyone can catch a hole

    def __init__(self, player):
        self._player = player


class Piece:
    FIXED = False

    MOUSE = 1
    CAT = 2
    WOLF = 3
    DOG = 4
    PANTHER = 5
    TIGER = 6
    LION = 7
    ELEPHANT = 8

    def __init__(self, player, value):
        self._player = player
        self._original_value = self._value = value

    def can_catch(self, piece):
        if self._value == self.MOUSE and piece._value == self.ELEPHANT:
            return True

        if self._value == self.ELEPHANT and piece._value == self.MOUSE:
            return False

        return self._value >= piece._value

    def can_swim(self):
        '''
        If this piece can get into a lake
        '''
        return self._value == self.MOUSE

    def can_jump(self):
        '''
        If this piece can jump a lake
        '''
        return self._value in (self.TIGER, self.LION)

    def trap(self):
        self._value = 0

    def release(self):
        self._value = self._original_value

    def __eq__(self, piece):
        return self._player == piece._player and \
            self._value == piece._value

    def __repr__(self):
        return u'<Piece value=%i (%i), player=%s>' % (self._value,
            self._original_value, self._player)

from copy import copy
class Board:
    NBR_PLAYERS = 2

    HOLE = 0
    EARTH = 1
    TRAP = 2
    LAKE = 3

    INITIAL_BOARD = [
        [EARTH, EARTH, TRAP,  HOLE,  TRAP,  EARTH, EARTH],
        [EARTH, EARTH, EARTH, TRAP,  EARTH, EARTH, EARTH],
        [EARTH, EARTH, EARTH, EARTH, EARTH, EARTH, EARTH],
        [EARTH, LAKE,  LAKE , EARTH, LAKE,  LAKE,  EARTH],
        [EARTH, LAKE,  LAKE , EARTH, LAKE,  LAKE,  EARTH],
        [EARTH, LAKE,  LAKE , EARTH, LAKE,  LAKE,  EARTH],
        [EARTH, EARTH, EARTH, EARTH, EARTH, EARTH, EARTH],
        [EARTH, EARTH, EARTH, TRAP,  EARTH, EARTH, EARTH],
        [EARTH, EARTH, TRAP,  HOLE,  TRAP,  EARTH, EARTH],
    ]

    BOARD_DIMENTIONS = (9, 7)

    def __init__(self, owner_cid):
        self._players = [owner_cid]
        self._board = copy(self.INITIAL_BOARD)

    def join(self, owner_cid):
        self._players.append(owner_cid)
        if len(self._players) == self.NBR_PLAYERS:
            self._init_board()

    def _init_board(self):
        self.turn = 0
        player0, player1 = self._players

        self._pieces = {
            (0, 3): Hole(player0),
            (8, 3): Hole(player1),

            (0,0): Piece(player0, Piece.LION),
            (0,6): Piece(player0, Piece.TIGER),
            (1,1): Piece(player0, Piece.WOLF),
            (1,5): Piece(player0, Piece.CAT),
            (2,0): Piece(player0, Piece.MOUSE),
            (2,2): Piece(player0, Piece.PANTHER),
            (2,4): Piece(player0, Piece.DOG),
            (2,6): Piece(player0, Piece.ELEPHANT),

            (8,8): Piece(player1, Piece.LION),
            (8,0): Piece(player1, Piece.TIGER),
            (7,5): Piece(player1, Piece.WOLF),
            (7,1): Piece(player1, Piece.CAT),
            (6,6): Piece(player1, Piece.MOUSE),
            (6,4): Piece(player1, Piece.PANTHER),
            (6,2): Piece(player1, Piece.DOG),
            (6,0): Piece(player1, Piece.ELEPHANT),
        }

    def move(self, initial, final):
        # if the game is over, no movement are allowed
        if hasattr(self, '_winner'):
            raise InvalidMovement('We have a winner: %s' % self._winner)

        # get initial piece
        if initial not in self._pieces:
            raise InvalidMovement('Piece not found')

        piece = self._pieces[initial]

        if piece.FIXED:
            raise InvalidMovement('Cannot move this piece')

        # check player's turn
        player = self._players[self.turn % self.NBR_PLAYERS]
        if player != piece._player:
            raise InvalidMovement('Invalid player')

        # diagonally movements are forbidden
        if initial[0] != final[0] and initial[1] != final[1]:
            raise InvalidMovement('Diagonal movements are not allowed')

        # just special pieces can get into a lake
        line, column = final
        if not piece.can_swim() and self._board[line][column] == self.LAKE:
            raise InvalidMovement('Can\'t jump into a lake')

        piece_final = None
        if final in self._pieces:
            piece_final = self._pieces[final]

            # same team piece
            if piece._player == piece_final._player:
                raise InvalidMovement('Can\'t catch a same team piece')

            # check "can_catch" method
            if not piece.can_catch(piece_final):
                raise InvalidMovement('Can\'t catch this piece')

            # mouses can't catch and get into/out a lake at same time
            fline, fcolumn = final
            iline, icolumn = initial
            if self._board[fline][fcolumn] == self.LAKE and \
                    self._board[iline][icolumn] == self.EARTH:
                raise InvalidMovement('Can\'t catch and get into a lake at '
                    'same time')

            if self._board[fline][fcolumn] == self.EARTH and \
                    self._board[iline][icolumn] == self.LAKE:
                raise InvalidMovement('Can\'t catch and get out a lake at '
                    'same time')


        if abs(initial[0] - final[0]) > 1 or abs(initial[1] - final[1]) > 1:
            if piece.can_jump():
                # max size of a movement
                if initial[0] == final[0]:
                    # movement from "1" key (column)
                    for i in xrange(initial[1]+1, final[1]):
                        if self._board[initial[0]][i] != self.LAKE or \
                                (initial[0], i) in self._pieces:
                            # jump is just in a lake
                            # and nobody are into the lake
                            raise InvalidMovement('Too big movement')
                else:
                    # movement from "0" key (line)
                    for i in xrange(initial[0]+1, final[0]):
                        if self._board[i][initial[1]] != self.LAKE or \
                                (i, initial[1]) in self._pieces:
                            # jump is just in a lake
                            # and nobody are into the lake
                            raise InvalidMovement('Too big movement')
            else:
                # more then 2 squares and can't jump
                raise InvalidMovement('Too big movement')

        # get the piece
        piece = self._pieces.pop(initial)

        # get into a trap
        fline, fcolumn = final
        if self._board[fline][fcolumn] == self.TRAP:
            piece.trap()
        else:
            # get out a trap
            iline, icolumn = initial
            if self._board[iline][icolumn] == self.TRAP:
                piece.release()

        # execute the movement!
        self._pieces[final] = piece

        # is a winner?
        if isinstance(piece_final, Hole):
            # yes! you win!
            self.win(piece._player)

        # next turn!
        self.turn += 1

        return True

    def win(self, player):
        self._winner = player

class JungleRumbleGame:
    '''
    The "game" interface
    '''
    COMMANDS = ['join', 'left', 'play']

    def __init__(self, player):
        self.board = Board(player)

    def players(self):
        # copy because is at the moment:
        # without copy, "join" affect older calls of this method
        return copy(self.board._players)

    def join(self, player):
        self.board.join(player)

    def left(self, player):
        assert False, 'TODO' #TODO

    def play(self, *args):
        if len(args) != 4:
            assert False, args #TODO
        self.board.move(
            (args[0], args[1]),
            (args[2], args[3]),
        )

