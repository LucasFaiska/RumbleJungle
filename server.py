
import socket
from threading import Lock, Thread as Worker

from game import JungleRumbleGame

class ProtocolError(Exception):
    pass

class Connection:
    '''
    Every client connection
    '''
    COMMANDS = ['quit', 'list_game_types', ]

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
                raise ProtocolError('command misunderstood:%s' % repr(commands[0]))
        assert False, data

    def list_game_types(self):
        '''
        Return a list of allowed games in this server
        '''
        games = self.server.GAMES.keys()
        return '%i\n%s' % (
                len(games),
                '\n'.join(games),
            )


    def disconnect(self):
        '''
        Close socket
        '''
        self.socket.close()
        self.server.all_players.pop(self.uid) #TODO check thread problems

    quit = disconnect

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

if __name__ == '__main__':
    server = Server()
    server.initSocket()
