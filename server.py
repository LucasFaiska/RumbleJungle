
import socket
import random
from threading import Lock, Thread as Worker

from game import JungleRumbleGame

class ProtocolError(Exception):
    pass

class Connection:
    '''
    Every client connection
    '''
    COMMANDS = ['quit', # allow exit
        'list_game_types', 'create_game', 'list_game', 'join_game',
    ]

    def __init__(self, server, sock):
        self.socket = sock
        self.server = server
        self.uid = id(self.socket)

    def hello(self):
        '''
        Say hello to the client
        '''
        self.write("Hello %s! Welcome to the jungle!" % self.uid)

    def read(self):
        return self.socket.recv(1024).strip()

    def write(self, data):
        return self.socket.send("%s\n" % data.strip())

    def run(self):
        '''
        "play" the game
        '''
        self.hello()
        data = None
        while data != 'quit':
            data = self.read() # even "quit" has a implementation

            try:
                return_data = self.execute(data)
                if return_data: self.write(return_data)
            except ProtocolError, exception:
                self.write(unicode(exception))
            except TypeError, exception:
                print exception
                self.write(u'Wrong arguments')

    def execute(self, data):
        commands = data.split(' ')
        if hasattr(self, 'game'):
            assert False
        else:
            # not in a game yet
            if commands[0] in self.COMMANDS:
                method = getattr(self, commands[0])
                return method(*commands[1:])
            else:
                raise ProtocolError('command misunderstood:%s' % (
                    repr(commands[0])))
        assert False, data

    def disconnect(self):
        '''
        Close socket
        '''
        self.socket.close()
        self.server.all_players.pop(self.uid) #TODO check thread problems

    quit = disconnect

    ## external methods - called by protocol
    def list_game_types(self):
        '''
        Return a list of allowed games in this server
        '''
        games = self.server.GAMES.keys()
        return '%i\n%s' % (
                len(games),
                '\n'.join(games),
            )

    def create_game(self, game_type):
        '''
        Received a game type, create it and return the game ID
        '''
        if game_type not in self.server.GAMES.keys():
            raise ProtocolError('game misunderstood:%s' % (
                repr(game_type)))

        gid = self.server.create_game(self.uid, game_type)
        return 'new_game %s' % gid

    def list_game(self, game_type):
        '''
        List all instances os a game type
        '''
        if game_type not in self.server.GAMES.keys():
            raise ProtocolError('game misunderstood:%s' % (
                repr(game_type)))

        game_class = self.server.GAMES.get(game_type)
        gids = [str(gid) for gid,game in self.server.all_games.items()
            if isinstance(game, game_class)]

        return '%i\n%s' % (len(gids), '\n'.join(gids))

    def join_game(self, game_id):
        '''
        Join to a game
        '''
        try:
            gid = int(game_id)
        except ValueError:
            raise ProtocolError('gameid misunderstood:%s' % game_id)

        if gid not in self.server.all_games.keys():
            raise ProtocolError('gameid not found:%s' % game_id)

        return 'joined_to %i' % self.server.join_game(self.uid, gid)

class Server:
    '''
    Our server
    '''
    SOCKET_ATTR = (socket.AF_INET, socket.SOCK_STREAM,)
    SOCKET_HOST = ('127.0.0.1', 8000)

    GAMES = {
        'JungleRumble': JungleRumbleGame,
    }

    def __init__(self):
        self.all_players = {}
        self.all_games = {}
        self._all_games_lock = Lock()
        self._process = []

    def installSignal(self):
        import signal
        signal.signal(signal.SIGINT, self.closeSocket)

    def closeSocket(self, signal_number, stack_frame):
        '''
        When Ctrl+C or SIGINT is received, or at the end of connection, the
        server need to be closed
        '''
        server = self._server_socket

        # tell all connected clients
        for kclient in self.all_players.keys():
            client = self.all_players[kclient]
            client.write('Server are down and waiting for you to disconnect...')

        # TODO how to force all clients to disconnect?

        # wait all threads
        for process in self._process:
            process.join()

        # close the socket server
        server.close()

    def initSocket(self):
        server = socket.socket(*self.SOCKET_ATTR)

        # http://stackoverflow.com/questions/2351465/socket-shutdown-and-rebind-how-to-avoid-long-wait
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server.bind(self.SOCKET_HOST)
        server.listen(5)

        self._server_socket = server

        # to stop:
        # kill -SIGINT <PID>

        while 1:
            # wait a connection
            conn, addr = server.accept()

            # connected!
            # add player connection
            client = Connection(self, conn)

            # add a player to the index
            self.all_players[client.uid] = client

            # start a thread to play the game
            process = Worker(target=client.run)
            self._process.append(process)
            process.start()

        self.closeSocket(self, None, None)

    def create_game(self, player, game_type):
        # create a new game
        game_class = self.GAMES.get(game_type)
        game = game_class(player)

        # lock, generate unique ID and append to all_games index
        self._all_games_lock.acquire()
        gid = random.randint(1, 100000)
        while gid in self.all_games.keys():
            gid = random.randint(1, 100000)
        self.all_games[gid] = game
        self._all_games_lock.release()

        # return the generated gid
        return gid

    def join_game(self, player, gid):
        # join "player" into "gid" game
        game = self.all_games[gid]
        players = game.players()
        game.join(player)

        # notify all other players
        for player_id in players:
            player_connection = self.all_players[player_id]
            player_connection.write('new_opponent %s' % player)

        return gid


if __name__ == '__main__':
    server = Server()
    server.initSocket()
