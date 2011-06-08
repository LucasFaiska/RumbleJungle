
import socket

import random
from threading import Thread as Worker
from game import Player, BasicGame
from baseClient import GameClient

class ProtocolError(Exception):
	pass

class BaseServer:
    def __init__(self):
        self.all_players = {}
        self.all_games = {}
        self.initSocket()

    def initSocket(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # port: TODO
        port = 8000
        while 1:
            try:
                server.bind(('127.0.0.1', port))
                break
            except socket.error:
                port += 1

        print '[PORT]', port
        server.listen(5)

        while 1:
            print '[HERE]'
            conn, addr = server.accept()

            client = GameClient(self, conn)
            self.all_players[client.uid] = client

            process = Worker(target=client.run)
            process.start()

        server.close()

    def client_out(self, cid):
        self.all_players.pop(cid)

    def execute(self, cid, command):
        commands = command.split(' ')

        command = commands[0]
        if hasattr(self, command):
            method = getattr(self, command)
        else:
            raise ProtocolError()

        args = commands[1:]
        if args:
            return method(cid, args)
        return method(cid)


class GameServer(BaseServer):
    def start_game(self, *args):
        return BasicGame(*args)

    def _build_game_uid(self):
        # FIXME max clients
        if len(self.all_games.keys()) > 100:
            assert False

        # FIXME threads problem?!
        uid = random.randint(1, 101)
        while uid in self.all_games.keys():
            uid = random.randint(1, 101)
        return uid

    def list_games(self, cid):
        out = ''
        out += '%i\n' % len(self.all_games.keys())
        for key in self.all_games.keys():
            out += '%s\n' % key
        return out

    def list_players(self, cid):
        out = ''
        out += '%i\n' % len(self.all_players.keys())
        for key in self.all_players.keys():
            if key == cid:
                out += '%s:%s\n' % (key, self.all_players[cid].super_supimpa())
        return out

    def create_game(self, cid):
        gid = self._build_game_uid()
        self.all_games[gid] = self.start_game(self.all_players[cid]._player)
        return 'GAME:%s' % gid

    def join_game(self, cid):
        raise NotImplementedError


if __name__ == '__main__':
    GameServer()

