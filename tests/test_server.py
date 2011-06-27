import tempfile
import socket
import re
from unittest import TestCase
from threading import Thread as Worker

from server import Server

class MockClient:
    def __init__(self, socket_file):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(socket_file)
        self._socket = sock

    def read(self):
        return self._socket.recv(1024).strip()

    def write(self, data):
        return self._socket.send('%s\n' % data.strip())

    def close(self):
        self._socket.close()


class ServerTest(TestCase):
    def setUp(self):
        temp = tempfile.NamedTemporaryFile()
        filename_temp = temp.name
        temp.close()

        Server.SOCKET_ATTR = (socket.AF_UNIX, socket.SOCK_STREAM)
        Server.SOCKET_HOST = filename_temp

        server = Server()
        worker = Worker(target=server.initSocket)
        worker.start()
        self.server = server
        self.worker = worker
        self.filename_temp = filename_temp

        # wait socket up
        while not hasattr(server, '_server_socket'):
            pass

        self.clients = []
        self._new_client()

    def _new_client(self):
        client = MockClient(self.filename_temp)
        client.read() #hello
        self.clients.append(client)
        return client

    def tearDown(self):
        for client in self.clients:
            client.write('quit')
            # client.close() # quit do this!

        self.server.closeSocket(None, None)
        self.worker._Thread__stop() # force thread's stop

    def test_list_types_games(self):
        client = self.clients[0]
        client.write('list_game_types')
        result = client.read().split('\n')

        self.assertEqual(result, ['1', 'JungleRumble'])

    def test_create_new_game(self):
        client = self.clients[0]
        client.write('create_game JungleRumble')
        result = client.read()

        self.assertTrue(bool(re.match('^new_game \d+$', result)))

        game_id = result.split(' ')[-1]

        client.write('list_game JungleRumble')
        result = client.read().split('\n')

        self.assertEqual(result, ['1', game_id])


