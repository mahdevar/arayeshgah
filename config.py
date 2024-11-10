pool_size = 100
host = 'localhost'
sql = {'host': host, 'database': 'a'}
#, 'minconn': 1, 'maxconn': pool_size

redis = {'host': host}


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


redis2 = \
{
	'host': '127.0.0.1',
	'port': 6379,
	'password': 'fgh3y9mwxglk5vp3783l',
	#'decode_responses': true,
	'db': 5
}
