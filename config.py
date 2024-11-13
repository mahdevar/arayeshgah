from functools import partial
from psycopg2 import connect
from psycopg2.pool import ThreadedConnectionPool
from redis import Redis

S = {}
with open('.env') as file:
	for line in file:
		key, value = line.rstrip('\n').split('=')
		S[key] = value


def factory(cls, *required, **custom):
	return partial(cls, **{parameter: S[parameter.upper()] for parameter in required} | custom)


DB = partial(connect, database=S['DATABASE'], host=S['HOST'], password=S['PASSWORD'], port=8001, user=S['USER'])
DB = factory(connect, 'database', 'host', 'password', 'user', port=8001)


REDIS = partial(Redis, host=S['HOST'], password=S['PASSWORD'], port=8002)
REDIS = factory(Redis, 'host', 'password', port=8002)



POOL = factory(ThreadedConnectionPool, 'database', 'host',  'maxconn', 'minconn', 'password', 'user', port=8001)

# print(load(, 'host', 'database', 'password'))

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
