__all__ = ['Cache', 'Database', 'Session', 'Storage']

from atexit import register as run_at_exit
from annotation import Class, Number, String
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


class DBPool:
	def __new__(cls, **p):
		pool = ConnectionPool('postgresql://%s:%s@%s:%s/%s' % (p['user'], p['password'], p['host'], p['port'], p['database']), min_size=int(p['minconn']), max_size=int(p['maxconn']))
		run_at_exit(pool.close)
		return pool


Cache = factory(Redis, 'CACHE')
Database = factory(DBPool, 'DB')
Session = factory(Redis, 'SESSION')
Storage = factory(Minio, 'STORAGE')
