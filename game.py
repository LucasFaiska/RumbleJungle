
class Piece:
    def __init__(self, player, value):
        self._player = player
        self._value = value

    def can_catch(self, piece):
        return True

class InvalidAction(Exception):
    pass

from copy import copy
class BasicGame:
    
    TOTAL_PLAYERS = 2

    INITIAL_BOARD = [
        ['Earth', 'Earth', 'Trap',  'Hole',  'Trap',  'Earth', 'Earth'],
        ['Earth', 'Earth', 'Earth', 'Trap',  'Earth', 'Earth', 'Earth'],
        ['Earth', 'Earth', 'Earth', 'Earth', 'Earth', 'Earth', 'Earth'],
        ['Earth', 'Lake',  'Lake' , 'Earth', 'Lake',  'Lake',  'Earth'],
        ['Earth', 'Lake',  'Lake' , 'Earth', 'Lake',  'Lake',  'Earth'],
        ['Earth', 'Lake',  'Lake' , 'Earth', 'Lake',  'Lake',  'Earth'],
        ['Earth', 'Earth', 'Earth', 'Earth', 'Earth', 'Earth', 'Earth'],
        ['Earth', 'Earth', 'Earth', 'Trap',  'Earth', 'Earth', 'Earth'],
        ['Earth', 'Earth', 'Trap',  'Hole',  'Trap',  'Earth', 'Earth']
    ]

    ANIMAL_VALUE = {'Mice':1, 'Cat':2, 'Wolf':3, 'Dog':4, 'Panther':5, 'Tiger':6, 'Lion':7, 'Elephant':8}
    VALUE_ANIMAL = {1:'Mice', 2:'Cat', 3:'Wolf', 4:'Dog', 5:'Panther', 6:'Tiger', 7:'Lion', 8:'Elephant'}

    INVALID_EXCEPTION = InvalidAction

    BOARD_DIMENTIONS = (9, 7)

    def __init__(self, owner_cid):
        self._pieces = {}
        self._players = [owner_cid]
        self._board = copy(self.INITIAL_BOARD)
        self._turn = 0

    def test(self):
        return "Teste"

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
        self._pieces[ (0,0) ] = Piece(player0,self.ANIMAL_VALUE['Lion'])
        self._pieces[ (0,6) ] = Piece(player0,self.ANIMAL_VALUE['Tiger'])
        self._pieces[ (1,1) ] = Piece(player0,self.ANIMAL_VALUE['Wolf'])
        self._pieces[ (1,5) ] = Piece(player0,self.ANIMAL_VALUE['Cat'])
        self._pieces[ (2,0) ] = Piece(player0,self.ANIMAL_VALUE['Mice'])
        self._pieces[ (2,2) ] = Piece(player0,self.ANIMAL_VALUE['Panther'])
        self._pieces[ (2,4) ] = Piece(player0,self.ANIMAL_VALUE['Dog'])
        self._pieces[ (2,6) ] = Piece(player0,self.ANIMAL_VALUE['Elephant'])

        self._pieces[ (8,6) ] = Piece(player1,self.ANIMAL_VALUE['Lion'])
        self._pieces[ (8,0) ] = Piece(player1,self.ANIMAL_VALUE['Tiger'])
        self._pieces[ (7,5) ] = Piece(player1,self.ANIMAL_VALUE['Wolf'])
        self._pieces[ (7,1) ] = Piece(player1,self.ANIMAL_VALUE['Cat'])
        self._pieces[ (6,6) ] = Piece(player1,self.ANIMAL_VALUE['Mice'])
        self._pieces[ (6,4) ] = Piece(player1,self.ANIMAL_VALUE['Panther'])
        self._pieces[ (6,2) ] = Piece(player1,self.ANIMAL_VALUE['Dog'])
        self._pieces[ (6,0) ] = Piece(player1,self.ANIMAL_VALUE['Elephant'])

    def playerTurn(self):
        playerNo = self._turn % len(self._players)
        return self._players[playerNo]

    def _checkTurn(self, piece):
        if piece._player != self.playerTurn():
            raise InvalidAction()

    def _checkMove(self, initial, final):
        if abs(initial[0]-final[0] + initial[1]-final[1]) > 1:
            raise InvalidAction()

    # Game Rules
    def caugth_by_a_trap(self):
        pass

    def catch_the_hole(self):
        pass

    def catch_a_enemy(self):
        pass

    def on_lake(self):
        pass

    def on_earth(self):
        pass

    def move(self, initial, final):
        initial_piece = self._pieces.get(initial)
        final_piece = self._pieces.get(final)

        if initial_piece is None: raise InvalidAction()
        self._checkTurn(initial_piece)
        self._checkMove(initial, final)

        #check if the final_piece is an enemy or a friend
        if isinstance(final_piece,Piece):
           if initial_piece.player == final_piece.player:
              raise InvalidAction()
           else:
              return catch_a_enemy(initial_piece,final_piece)
        elif:
           if self._board[final[0]][final[1]] == "Lake":
              return self.on_lake()
           elif self._board[final[0]][final[1]] == "Trap":
              return self.caugth_by_a_trap()
           elif self._board[final[0]][final[1]] == "Earth":
              return self.on_earth()
           elif self._board[final[0]][final[1]] == "Hole":
              return self.catch_the_hoke()

        #self._pieces.pop(initial) #remove
        #if final_piece: self._pieces.pop(final) #remove, if exists
        #self._pieces[final] = initial_piece
        self._turn += 1

        return 'moved_from %ix%i to %ix%i' % (initial+final)

    def win(self):
        return 'no_winner_yet'

    def _move(self, cid, *args):
        if len(args) != 4:
            print '[InvalidAction]', repr(args)
            raise InvalidAction
        initial = (int(args[0]), int(args[1]))
        final = (int(args[2]), int(args[3]))
        return self.move(initial, final)

    def _board(self, cid, *args):
        out = ['%s %s' % self.BOARD_DIMENTIONS]

        for x in xrange(self.BOARD_DIMENTIONS[0]):
            a_row = []
            for y in xrange(self.BOARD_DIMENTIONS[1]):
                pos = x * self.BOARD_DIMENTIONS[1] + y
                row = 6 * '_'
                if (x,y) in self._pieces:
                    piece = self._pieces[(x,y)]
                    player_id = '%0.3i' % piece._player
                    piece_value = '%s' % self.VALUE_ANIMAL[piece._value]
                    row = player_id + piece_value
                else:
                    row = self._board[x][y]
                a_row.append(row.rjust(11))
            out.append('|'.join(a_row))
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

