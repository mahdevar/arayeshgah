__all__ = ['Cache', 'Database', 'Storage', 'Users']
from functools import partial
from redis import Redis as OriginalRedis
from minio import Minio
from json import dumps, loads
from psycopg2.pool import ThreadedConnectionPool

S = {}
with open('.env') as file:
	for line in file:
		line = line.rstrip()
		if line:
			key, value = line.split('=')
			S[key] = value

S['STORAGE_ENDPOINT'] += ':' + S['STORAGE_PORT']  
del S['STORAGE_PORT']

def factory(cls, prefix, **custom):
	return partial(cls, **{secret[len(prefix) + 1:].lower(): S[secret] for secret in S if secret.startswith(prefix)} | custom)

class Redis(OriginalRedis):
	def __getitem__(self, item):
		return loads(self.get(item))

	def __setitem__(self, key, value: [float, int, str, dict]):
		self.set(key, dumps(value))
Cache = factory(Redis, 'CACHE')
Database = factory(ThreadedConnectionPool, 'DB')
Storage = factory(Minio, 'STORAGE')
Users = factory(Redis, 'USERS')
