__all__ = ['DB', 'CACHE', 'STORAGE', 'USERS']

from functools import partial
from minio import Minio
from psycopg2.pool import ThreadedConnectionPool
from redis import Redis

S = {}
with open('.env') as file:
	for line in file:
		line = line.rstrip()
		print(line)
		if line:
			key, value = line.split('=')
			S[key] = value


def factory(cls, prefix, **custom):
	return partial(cls, **{secret[len(prefix) + 1:].lower(): S[secret] for secret in S if secret.startswith(prefix)} | custom)

DB = factory(ThreadedConnectionPool, 'SQL')
CACHE = factory(Redis, 'CACHE')
STORAGE = factory(Minio, 'STORAGE')
USERS = factory(Redis, 'CACHE')

# POOL = factory(ThreadedConnectionPool, 'database', 'host',  'maxconn', 'minconn', 'password', 'user', port=8001)

# print(load(, 'host', 'database', 'password'))
'''
e = DB(database='postgres')
print(e)
exit()

DB = connect(**(sql | {'database': 'postgres', 'user': 'postgres'}))
print(secrets)

exit()

pool_size = 100
host = 'localhost'
sql = {'host': host, 'database': secrets['DB'], 'password': secrets['PASSWORD']}
# , 'minconn': 1, 'maxconn': pool_size

redis = {'host': host, 'password': secrets['PASSWORD']}

# from utilities import Redis
# from functools import partial


minio = \
	{
		'endpoint': host + ':9000',
		'access_key': 'accessminiominio',
		'secret_key': 'secretminiominio',
		'secure': False
	}

csp_directives = \
	{
		'connect-src': ['geolocation-db.com'],
		'font-src': ['fonts.gstatic.com'],
		'frame-ancestors': [],
		'img-src': [],
		'script-src': [],
		'style-src': ['fonts.googleapis.com']
	}
'''
