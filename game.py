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

    INVALID_EXCEPTION = InvalidAction

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


    COMMANDS = {
        'move': _move, #is a classmethod, need self as parameter
    }

    def execute(self, cid, command):
        print '[execute]', repr(command)
        if command[0] in self.COMMANDS:
            return self.COMMANDS[command[0]](self, cid, *command[1:])
        raise InvalidAction()

