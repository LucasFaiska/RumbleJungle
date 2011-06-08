
import socket

import random
from threading import Thread as Worker
from game import BasicGame
from baseClient import GameClient, ProtocolError

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
    def _start_game(self, *args):
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
        game = self._start_game(cid)
        game.players = [cid]
        self.all_games[gid] = game
        self.all_players[cid].gid = gid
        return 'GAME:%s' % gid

    def join_game(self, cid, args):
        game = self.all_games.get(int(args[0]))

        if game is None:
            raise ProtocolError()

        game.join(cid)

        for c in game.players:
            self.all_players[c].write("NEW_PLAYER:%s" % cid)
        self.all_players[cid].gid = int(args[0])
        game.players.append(cid)

        return 'JOINED IN GAME %s' %args[0]

    def quit(self, cid):
        player = self.all_players[cid]
        if hasattr(player, 'gid'):
            self.left_game(cid)

    def left_game(self, cid):
        player = self.all_players[cid]
        gid = player.gid
        game = self.all_games.get(player.gid)
        # TODO threads
        game.left(cid)
        i = game.players.index(cid)
        game.players.pop(i)
        del(player.gid)

        for c in game.players:
            self.all_players[c].write("PLAYER_LEFT:%s" % cid)

        return 'LEFT %s' % gid

    def play(self, cid, command):
        player = self.all_players[cid]

        if not hasattr(player,'gid'):
            raise ProtocolError()

        game = self.all_games[player.gid]
        return game.execute(command);


if __name__ == '__main__':
    GameServer()

