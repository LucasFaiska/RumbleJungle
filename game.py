
class InvalidMovement(Exception):
    pass


class Piece:
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
        self._value = value

    def can_catch(self, piece):
        if self._value == self.MOUSE and piece._value == self.ELEPHANT:
            return True

        if self._value == self.ELEPHANT and piece._value == self.MOUSE:
            return False

        return self._value >= piece._value

    def trap(self):
        self._original_value = self._value
        self._value = 0

    def release(self):
        self._value = self._original_value

    def __eq__(self, piece):
        return self._player == piece._player and \
            self._value == piece._value

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

        if initial not in self._pieces:
            raise InvalidMovement('Piece not found')

        piece = self._pieces[initial]

        player = self._players[self.turn % self.NBR_PLAYERS]
        if player != piece._player:
            raise InvalidMovement('Invalid player')

        if initial[0] != final[0] and initial[1] != final[1]:
            raise InvalidMovement('Diagonal movements are not allowed')

        if final in self._pieces:
            piece_final = self._pieces[final]
            if piece._player == piece_final._player:
                raise InvalidMovement('Can\'t catch a same team piece')

            if not piece.can_catch(piece_final):
                raise InvalidMovement('Can\'t catch this piece')

        piece = self._pieces.pop(initial)
        self._pieces[final] = piece

        return True


class InvalidAction(Exception):
    pass

from copy import copy
class BasicGame:

    TOTAL_PLAYERS = 2

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

    PIECE_TYPES = [
        ('Mice', 1,),
        ('Cat', 2,),
        ('Wolf', 3,),
        ('Dog', 4,),
        ('Panther', 5,),
        ('Tiger', 6,),
        ('Lion', 7,),
        ('Elephant', 8,),
    ]

    ANIMAL_VALUE = dict([(x[0], x[1]) for x in PIECE_TYPES])
    VALUE_ANIMAL = dict([(x[1], x[0]) for x in PIECE_TYPES])

    INVALID_EXCEPTION = InvalidAction

    BOARD_DIMENTIONS = (9, 7)

    def __init__(self, owner_cid):
        self._pieces = {}
        self._players = [owner_cid]
        self._board = copy(self.INITIAL_BOARD)
        self._turn = 0

    def even_or_odd(self):
        pass

    def join(self, player_cid):
        # TODO check max game players
        # TODO check same player twice
        self._players.append(player_cid)
        if len(self._players) == self.TOTAL_PLAYERS:
            #TODO implement even_or_odd method, before initialize game
            self.initPlayerPieces()

    def left(self, player_cid):
        i = self._players.index(player_cid)
        self._players.pop(i)

    def initPlayerPieces(self):
        player0, player1 = self._players

        # Automathize this, and change the numbers for MACROS
        self._pieces[ (0,0) ] = Piece(player0, self.ANIMAL_VALUE['Lion'])
        self._pieces[ (0,6) ] = Piece(player0, self.ANIMAL_VALUE['Tiger'])
        self._pieces[ (1,1) ] = Piece(player0, self.ANIMAL_VALUE['Wolf'])
        self._pieces[ (1,5) ] = Piece(player0, self.ANIMAL_VALUE['Cat'])
        self._pieces[ (2,0) ] = Piece(player0, self.ANIMAL_VALUE['Mice'])
        self._pieces[ (2,2) ] = Piece(player0, self.ANIMAL_VALUE['Panther'])
        self._pieces[ (2,4) ] = Piece(player0, self.ANIMAL_VALUE['Dog'])
        self._pieces[ (2,6) ] = Piece(player0, self.ANIMAL_VALUE['Elephant'])

        self._pieces[ (8,8) ] = Piece(player1, self.ANIMAL_VALUE['Lion'])
        self._pieces[ (8,0) ] = Piece(player1, self.ANIMAL_VALUE['Tiger'])
        self._pieces[ (7,5) ] = Piece(player1, self.ANIMAL_VALUE['Wolf'])
        self._pieces[ (7,1) ] = Piece(player1, self.ANIMAL_VALUE['Cat'])
        self._pieces[ (6,6) ] = Piece(player1, self.ANIMAL_VALUE['Mice'])
        self._pieces[ (6,4) ] = Piece(player1, self.ANIMAL_VALUE['Panther'])
        self._pieces[ (6,2) ] = Piece(player1, self.ANIMAL_VALUE['Dog'])
        self._pieces[ (6,0) ] = Piece(player1, self.ANIMAL_VALUE['Elephant'])

    def playerTurn(self):
        playerNo = self._turn % len(self._players)
        return self._players[playerNo]

    def _check_turn(self, piece):
        if piece._player != self.playerTurn():
            print 'Not your turn, %s!' % piece._player
            raise InvalidAction()

    def _check_move(self, initial, final):
        piece = self._pieces.get(initial)
        x, y = final
        destination_board = self._board[x][y]
        destination_piece = self._pieces.get(final)

        if destination_board == self.LAKE:
            if piece._value not in (self.ANIMAL_VALUE['Mice'],self.ANIMAL_VALUE['Tiger'],self.ANIMAL_VALUE['Lion']):
                print 'You cannot move to a lake!'
                raise InvalidAction()
            else:
                self.on_lake(piece, initial, final)

        if destination_board == self.TRAP:
            self.caugth_by_a_trap(piece)

        if destination_piece is not None:
            if destination_piece._player == piece._player:
                print 'You cannot move over your own piece'
                raise InvalidAction()
            else:
                print piece.can_catch(destination_piece)

    # Game Rules
    def caugth_by_a_trap(self, piece):
        piece._captured = True

    def catch_the_hole(self, piece):
        pass

    def on_lake(self, piece, initial, final):
        if(piece._value == self.ANIMAL_VALUE['Mice']):
           #Mice can Enter in the Lake
           pass
        else:
           #Tiger and Lion jump Over the Lake
           if( initial[0] != final[0] ):
              #Vertical move allow 3 spaces jump
              if( abs(final[0] - initial[0]) != 4 ):
                 raise InvalidAction()
           if( initial[1] != final[1] ):
              #Horizontal move allow 2 spaces jump
              if( abs(final[1] - initial[1]) != 3 ):
                 raise InvalidAction()

    def on_earth(self):
        pass

    def move(self, initial, final):
        initial_piece = self._pieces.get(initial)
        final_piece = self._pieces.get(final)

        if initial_piece is None:
            print 'No piece on %s %s'  %initial[0] %initial[1]
            raise InvalidAction()

        self._check_turn(initial_piece) # is the right player?
        self._check_move(initial, final) # is this move allowed?

        self._pieces.pop(initial) #remove
        self._pieces[final] = initial_piece
        self._turn += 1

        return 'moved_from %ix%i to %ix%i' % (initial+final)

    def _move(self, cid, *args):
        if len(args) != 4:
            print '[InvalidAction]', repr(args)
            raise InvalidAction
        initial = (int(args[0]), int(args[1]))
        final = (int(args[2]), int(args[3]))
        return self.move(initial, final)

    def _board(self, cid, *args):
        out = ['%s %s' % self.BOARD_DIMENTIONS]

        # 3 char player.uid (or _ if no piece)
        # 3 char piece (or _ if no piece)
        # 3 char of board
        for x in xrange(self.BOARD_DIMENTIONS[0]):
            a_row = []
            for y in xrange(self.BOARD_DIMENTIONS[1]):
                pos = x * self.BOARD_DIMENTIONS[1] + y
                row = 6 * '_'
                if (x,y) in self._pieces:
                    piece = self._pieces[(x,y)]
                    player_id = '%0.3i' % piece._player
                    piece_value = '%0.3i' % piece._value
                    row = player_id + piece_value

                row += '%0.3i' % self._board[x][y]
                a_row.append(row)

            out.append(' '.join(a_row))
        return unicode('\n'.join(out))

    def _get_players(self):
        players = set([p._player for p in self._pieces.values()])
        return players

    def ended(self):
        return False
        #return len(self._get_players()) == 1 # 1 player, the WINNER

    def game_finished_status(self):
        if not self.ended():
            return False

        result = {}
        winner = self._get_players().pop()
        for player in self._players:
            result[player] = 'won' if winner == player else 'lose'
        return result

    # COMMANDS and STAUS are classmethods, need self as parameter
    COMMANDS = { # do actions, send confirmation to all players
        'move': _move,
    }
    STATUS = { # get information/status about game, sent to requested player
        'board': _board,
    }

    def execute(self, cid, command):
        if command[0] in self.COMMANDS:
            return self.COMMANDS[command[0]](self, cid, *command[1:]), True
        if command[0] in self.STATUS:
            return self.STATUS[command[0]](self, cid, *command[1:]), False

        raise InvalidAction()

