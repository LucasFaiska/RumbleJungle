
import socket

import random
from threading import Thread as Worker
from threading import Lock

from game import BasicGame
from baseClient import GameClient, ProtocolError

class BaseServer:
    def __init__(self):
        self.all_players = {}
        self.all_games = {}
        self._all_games_lock = Lock()
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
            conn, addr = server.accept()

            client = GameClient(self, conn)
            self.all_players[client.uid] = client

            process = Worker(target=client.run)
            process.start()

        server.close()

    def client_out(self, cid):
        self.all_players.pop(cid)

    def _notify_players(self, gid, message, exclude_cid=None):
        game = self.all_games.get(gid)
        for player_cid in game.players:
            if player_cid != exclude_cid:
                player = self.all_players[player_cid]
                player.write(message)

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
        game = BasicGame(*args)
        game._lock = Lock()
        return game

    def _build_game_uid(self):
        # FIXME max clients
        if len(self.all_games.keys()) >= 100:
            assert False

        uid = random.randint(1, 101)
        while uid in self.all_games.keys():
            uid = random.randint(1, 101)
        return uid

    def check_end_game(self, cid):
        player = self.all_players[cid]
        if not hasattr(player, 'gid'):
            return False

        gid = player.gid
        game = self.all_games[gid]
        if game.ended():
            # finished game
            result = game.game_finished_status()
            print result
            for player in result:
                msg = 'END_GAME - YOU %s' % result[player]
                self.all_players[player].write(msg)
            return True
        return False

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
        # lock to avoid problems between generate "uid" as set game dict
        self._all_games_lock.acquire()

        gid = self._build_game_uid()
        game = self._start_game(cid)
        game.players = [cid]
        self.all_games[gid] = game
        self.all_players[cid].gid = gid

        self._all_games_lock.release() # THREAD CONTROL

        return 'GAME %s' % gid

    def join_game(self, cid, args):
        gid = int(args[0])
        game = self.all_games.get(gid)

        if game is None:
            raise ProtocolError()

        game.join(cid)

        self._notify_players(gid, "NEW_PLAYER %s" % cid)
        self.all_players[cid].gid = gid
        game.players.append(cid)

        return 'JOINED IN GAME %s' %args[0]

    def quit(self, cid):
        player = self.all_players[cid]
        if hasattr(player, 'gid'):
            self.left_game(cid)

    def my_game(self, cid):
        player = self.all_players[cid]
        if hasattr(player, 'gid'):
            return 'IN_GAME %s' % player.gid
        else:
            return 'NOT_IN_A_GAME'

    def left_game(self, cid):
        player = self.all_players[cid]
        gid = player.gid
        game = self.all_games.get(player.gid)
        # lock to avoid 2 players change the "game.players" list at same time
        # or between "index()" and "pop()" callers
        game._lock.acquire()
        game.left(cid)
        i = game.players.index(cid)
        game.players.pop(i)
        game._lock.release() # THREAD CONTROL

        del(player.gid)

        for c in game.players:
            self.all_players[c].write("PLAYER_LEFT %s" % cid)

        # remove game if all players left
        if not game.players:
            del self.all_games[gid]

        return 'LEFT %s' % gid

    def play(self, cid, command):
        player = self.all_players[cid]

        if not hasattr(player,'gid'):
            raise ProtocolError()

        game = self.all_games[player.gid]
        try:
            result, send_to_all = game.execute(cid, command)
        except game.INVALID_EXCEPTION, exception:
            raise ProtocolError('Invalid game action!')
        if send_to_all:
            self._notify_players(player.gid, result, exclude_cid=cid)
        return result

if __name__ == '__main__':
    GameServer()

