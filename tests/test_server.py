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
        result = client.read() #hello

        uid = int(re.search('Hello (?P<uid>\d+)!', result).groupdict()['uid'])
        client.uid = uid

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

    def test_join_game(self):
        client0 = self.clients[0]
        client0.write('create_game JungleRumble')
        result = client0.read()
        game_id = result.split(' ')[-1]

        client1 = self._new_client()
        client1.write('join_game %s' % game_id)

        result = client1.read()
        self.assertEqual('joined_to %s' % game_id, result)

        result = client0.read()
        self.assertEqual('new_opponent %s' % client1.uid, result)


class ServerPlayTest(TestCase):

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
        self._new_client()

        gid = server.create_game(self.clients[0].uid, 'JungleRumble')
        server.join_game(self.clients[1].uid, gid)

        result = self.clients[0].read() # new_opponent

    def tearDown(self):
        for client in self.clients:
            client.write('quit')
            # client.close() # quit do this!

        self.server.closeSocket(None, None)
        self.worker._Thread__stop() # force thread's stop

    def _new_client(self):
        client = MockClient(self.filename_temp)
        result = client.read() #hello

        uid = int(re.search('Hello (?P<uid>\d+)!', result).groupdict()['uid'])
        client.uid = uid

        self.clients.append(client)
        return client

    def test_play(self):
        client0 = self.clients[0]
        client0.write('play 0 0 0 1')

        result = client0.read()
        self.assertEqual('played 0 0 0 1', result)

        client1 = self.clients[1]
        result = client1.read()
        self.assertEqual('played 0 0 0 1', result)

    def test_play_turn_wrong_player(self):
        client1 = self.clients[1]
        client1.write('play 8 8 8 7')

        result = client1.read()
        self.assertEqual('invalid_movement "Invalid player"', result)

