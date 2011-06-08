
class Player:
    def __init__(self, name):
        self._name = name

class ProtocolError(Exception):
	pass

class GameClient:
    def __init__(self, server, socket):
        self._socket = socket
        self._server = server
        self.uid = self._socket.fileno()

        self._player = Player('Player %i' % self.uid) # FIXME

    def super_supimpa(self):
        return '42'

    def read(self):
        return self._socket.recv(1024).strip()

    def write(self, data):
        return self._socket.send(data)

    def run(self):
        data = None
        while data != 'quit':
            data = self.read() # even "quit" has a implementation
            try:
                result = self._server.execute(self.uid, data)
            except ProtocolError:
                result = 'PROTOCOL_ERROR'
            if result:
                self.write(result)

        self._socket.close()
        self._server.client_out(self.uid)