__all__ = ['Cache', 'Database', 'Session', 'Storage']

from annotation import Class, Dictionary, List, Number, Serializable, String
from atexit import register as run_at_exit
from functools import partial
from json import dumps, loads
from minio import Minio
from psycopg.rows import dict_row
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
	def __getitem__(self, item) -> Serializable:
		return loads(self.get(item))

	def __setitem__(self, key, value: Serializable) -> None:
		self.set(key, dumps(value))


class DBPool(ConnectionPool):
	def __init__(self, **p):
		super().__init__('postgresql://%s:%s@%s:%s/%s' % (p['user'], p['password'], p['host'], p['port'], p['database']), min_size=int(p['minconn']), max_size=int(p['maxconn']), kwargs={"row_factory": dict_row})
		#super().__init__('postgresql://%s:%s@%s:%s/%s' % (p['user'], p['password'], p['host'], p['port'], p['database']), min_size=int(p['minconn']), max_size=int(p['maxconn']))
		# super().__init__(min_size=int(p['minconn']), max_size=int(p['maxconn']), kwargs={"row_factory": dict_row, ...})
		run_at_exit(self.close)

	def commit(self, query: String, parameters: List | None = None) -> None:
		with self.connection() as connection:
			connection.execute(query, parameters)

	def commits(self, query: String, parameters: List | None = None) -> None:
		with self.connection() as connection:
			connection.executemany(query, parameters)

	def row(self, query: String, parameters: List | None = None) -> Dictionary | None:
		with self.connection() as connection, connection.cursor() as cursor:
			cursor.execute(query, parameters)
			return cursor.fetchone()

	def rows(self, query: String, parameters: List | None = None) -> List:
		with self.connection() as connection, connection.cursor() as cursor:
			cursor.execute(query, parameters)
			return cursor.fetchall()


Cache = factory(Redis, 'CACHE')
Database = factory(DBPool, 'DB')
Session = factory(Redis, 'SESSION')
Storage = factory(Minio, 'STORAGE')
