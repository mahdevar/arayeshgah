__all__ = ['Cache', 'Database', 'Session', 'Storage']

from atexit import register as run_at_exit

from psycopg import Cursor

from annotation import Class, Number, String
from contextlib import contextmanager
from functools import partial
from json import dumps, loads
from minio import Minio
from psycopg_pool import ConnectionPool
from redis import Redis as OriginalRedis

S = {}
with open('.env') as file:
	for line in file:
		line = line.rstrip()
		if line:
			key, value = line.split('=')
			S[key] = value


def factory(cls: Class, prefix: String, **custom: Number | String) -> Class:
	return partial(cls, **{secret[len(prefix) + 1:].lower(): S[secret] for secret in S if secret.startswith(prefix)} | custom)


class Redis(OriginalRedis):
	def __getitem__(self, item):
		return loads(self.get(item))

	def __setitem__(self, key, value: [float, int, str, dict]):
		self.set(key, dumps(value))


class DBPool(ConnectionPool):
	def __init__(self, **p):
		super().__init__('postgresql://%s:%s@%s:%s/%s' % (p['user'], p['password'], p['host'], p['port'], p['database']), min_size=int(p['minconn']), max_size=int(p['maxconn']))
		run_at_exit(self.close)

	@contextmanager
	def exec2(self, query, row_factory=None, commit=False) -> Cursor:
		with self.connection() as connection:
			with connection.cursor(row_factory=row_factory) as cursor:
				cursor.execute(query)
				yield cursor
			if commit:
				connection.commit()

	@contextmanager
	def __getitem__(self, query) -> Cursor:
		print('TO GET:', query)
		with self.connection() as connection:
			#connection.autocommit = True
			with connection.cursor() as cursor:
				if type(query) == str:
					cursor.execute(query)
				else:
					cursor.execute(query[0], query[1])
				yield cursor

	def __contains__(self, item):
		print('TO CONTAIN:', item)
		with self[item] as result:
			return result.rowcount > 0

	def __setitem__(self, query, values):
		with self.connection() as connection, connection.cursor() as cursor:
			cursor.execute(query, values)
			#connection.commit()

	@contextmanager
	def __getitemmmmmmmmm__(self, query) -> Cursor:
		print('query===========', query)
		print('p===============', p)
		print('type======', type(query))
		print('0-------', query[0])
		print('1-------', query[1])
		with self.connection() as connection:
			#connection.autcommit = True
			with connection.cursor() as cursor:
				cursor.execute(query)
				yield cursor

	def exec(self, function, query, parameters=None, row_factory=None, commit=False):
		with self.connection() as connection:
			with connection.cursor(row_factory=row_factory) as cursor:
				cursor.execute(query, parameters)
				return getattr(cursor, function)()

	def row(self, query, parameters=None, row_factory=None):
		return self.exec('fetchone', query, parameters, row_factory=row_factory)

	def rows(self, query, parameters=None, row_factory=None):
		return self.exec('fetchall', query, parameters, row_factory=row_factory)



Cache = factory(Redis, 'CACHE')
Database = factory(DBPool, 'DB')
Session = factory(Redis, 'SESSION')
Storage = factory(Minio, 'STORAGE')
