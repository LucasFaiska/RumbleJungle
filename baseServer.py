
import socket
from multiprocessing import Process, Manager

from game import Player, BasicGame
from copy import copy

class ProtocolError(Exception):
	pass

unique_id = id

class BaseServer:

	def __init__(self):
		pass

	def _my_id(self):
		return 'My Id is:: %i' % self._player_id

	def _get_player_game(self):
		game_id = self._player_game.get(self._player_id)
		if game_id: return self._games[game_id]

	def _create(self):
		player = self._players[self._player_id]

		if self._get_player_game() is not None:
			return 'YOU ARE PLAYING ANOTHER GAME'

		ng = copy(BasicGame(player))
		game_id = unique_id(ng)
		self._games[game_id] = ng

		# self._join
		self._game_player[game_id] = [self._player_id]

		print 'CREATE A NEW %s GAME IN %i' % (ng, unique_id(self._games))
		print self._games

		return 'NEW GAME CREATED::%i' % game_id


	def _list(self):
		games = self._games.keys()
		return 'GAMES::%(nro)i\n%(games)s' % {
			'nro': len(games),
			'games': '\n'.join([str(g) for g in games]),
		}

	def _join(self, game_id, notify=True):
		try:
			game_id = int(game_id)
		except ValueError:
			raise ProtocolError()
		game = self._games.get(game_id)
		player = self._players[self._player_id]

		if game is None:
			raise ProtocolError()

		# TODO check is player are in another game

		game.join(player)
		self._player_game[self._player_id] = game_id

		if notify:
			for player_id in self._game_player[game_id]:
				# self._players[player_id].sock.send('NEW PLAYER ARE IN')
				# FIXME how notificate other players about new player in the board?
				pass

		self._game_player[game_id].append(self._player_id)

		return 'YOU ARE IN'
	
	def _play(self):
		game = self._get_player_game()
		if game is None:
			return 'PLAYER NOT JOINED TO A GAME'
		else:
			return game.test()

	def execute(self, cmd, args):
		method_name = '_%s' %cmd.lower()
		if hasattr(self, method_name):
			method = getattr(self, '_%s' %cmd)
			return method(*args)
		else:
			raise ProtocolError()

	def _connect(self, games, players, player_game, game_player, conn, addr):
		print 'connected!', conn, addr, unique_id(conn)
		self._games = games
		self._players = players
		self._player_game = player_game
		self._game_player = game_player
		
		self._player_id = player_id = unique_id(conn)

		player = Player(player_id)
		self._players[player_id] = player

		print '[C]games=', self._games
		print '[C]players=', self._players

		data = conn.recv(1024).strip()
		while data != 'QUIT':
			try:
				print repr(data)
				cmd = data.split(' ')
				try:
					result = self.execute(cmd[0], cmd[1:])
					conn.send(result)
				except ProtocolError:
					conn.send('PROTOCOL ERROR!')

			except Exception, p:
				raise
				break

			data = conn.recv(1024).strip()

		conn.close()
		print 'close!', conn, addr
		
	def buildSocket(self):
		# to shared memory: to see how Manager() works, see
		# http://docs.python.org/dev/library/multiprocessing#sharing-state-between-processes
		manager = Manager()
		_games = manager.dict()
		_players = manager.dict()
		_player_game = manager.dict()
		_game_player = manager.dict()

		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		port = 8000
		while 1:
			try:
				server.bind(('127.0.0.1', port))
				break
			except socket.error:
				port +=1

		print 'PORT', port
		server.listen(5)

		while 1:
			conn, addr = server.accept()

			p = Process(target=self._connect, args=(_games, _players, _player_game, _game_player,
				conn, addr))
			p.start()
			conn.close()

		server.close()


if __name__ == '__main__':
	BaseServer().buildSocket()
