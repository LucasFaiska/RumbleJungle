
class Piece:
    def __init__(self, player):
        self._player = player
        self._id = 'B'

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

    INVALID_EXCEPTION = InvalidAction

    BOARD_DIMENTIONS = (3, 3)

    def __init__(self, owner_cid):
        self._pieces = {}
        self._players = [owner_cid]
        self._board = copy(self.INITIAL_BOARD)
        self._turn = 0

    def test(self):
        return "Teste"

    def join(self, player_cid):
        # TODO check max game players
        # TODO check same player twice
        self._players.append(player_cid)
        print len(self._players), self.TOTAL_PLAYERS, len(self._players) == self.TOTAL_PLAYERS
        if len(self._players) == self.TOTAL_PLAYERS:
            self.initPlayerPieces()

    def left(self, player_cid):
        i = self._players.index(player_cid)
        self._players.pop(i)

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
        return 'moved_from %ix%i to %ix%i' % (initial+final)

    def win(self):
        return 'no_winner_yet'

    def _move(self, cid, *args):
        if len(args) != 4:
            print repr(args)
            raise InvalidAction
        initial = (int(args[0]), int(args[1]))
        final = (int(args[2]), int(args[3]))

        return self.move(initial, final)

    def _board(self, cid):
        out = ['%s %s' % self.BOARD_DIMENTIONS]
        for x in xrange(self.BOARD_DIMENTIONS[0]):
            a_row = []
            for y in xrange(self.BOARD_DIMENTIONS[1]):
                pos = x * self.BOARD_DIMENTIONS[1] + y
                row = 6 * '_'
                print self._pieces, (x,y), (x,y) in self._pieces
                if (x,y) in self._pieces:
                    piece = self._pieces[(x,y)]
                    player_id = '%0.3i' % piece._player
                    piece_id = '%3s' % piece._id
                    row = player_id + piece_id
                a_row.append(row)
            out.append('|'.join(a_row))
        return unicode('\n'.join(out))


    # COMMANDS and STAUS are classmethods, need self as parameter
    COMMANDS = { # do actions, send confirmation to all players
        'move': _move,
    }
    STATUS = { # get information/status about game, sent to requested player
        'board': _board,
    }

    def execute(self, cid, command):
        print '[execute]', repr(command)
        if command[0] in self.COMMANDS:
            return self.COMMANDS[command[0]](self, cid, *command[1:]), True
        if command[0] in self.STATUS:
            return self.STATUS[command[0]](self, cid, *command[1:]), False

        raise InvalidAction()

