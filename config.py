secrets = {}
with open('.env') as file:
	for line in file:
		key, value = line.rstrip('\n').split('=')
		secrets[key] = value

from functools import partial

def form(cls, *parameters, **custom):
	return partial(cls, **{parameter: secrets[parameter.upper()] for parameter in parameters} | custom)


from psycopg2 import connect

DB = form(connect, 'database', 'host', 'password', 'user')

#print(load(, 'host', 'database', 'password'))

e =DB(database='postgres')
exit()

DB = connect(**(sql | {'database': 'postgres', 'user': 'postgres'}))
print(secrets)

exit()

pool_size = 100
host = 'localhost'
sql = {'host': host, 'database': secrets['DB'], 'password': secrets['PASSWORD']}
#, 'minconn': 1, 'maxconn': pool_size

redis = {'host': host, 'password': secrets['PASSWORD']}


#from utilities import Redis
#from functools import partial


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
