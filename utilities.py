from redis import Redis as OriginalRedis
from json import dumps, loads
from psycopg2.pool import ThreadedConnectionPool as CreatePool
import config

__all__ = ['SETTING', 'USERS']


class Redis(OriginalRedis):
	def __getitem__(self, item):
		return loads(self.get(item))

	def __setitem__(self, key, value: [float, int, str, dict]):
		self.set(key, dumps(value))


USERS = Redis(**config.redis, db=0)
SETTING = Redis(**config.redis, db=1)
SQL = CreatePool(1, 100, **config.sql)
