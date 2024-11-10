SQL = \
{
	'host': 'localhost',
	'database': 'a'
}

REDIS = \
{
	'host': 'localhost',
	'port': 6379,
	'db': 5
}

MINIO = \
{
	'endpoint': '192.168.10.31:9000',
	'access_key': 'ACCESSMINIOMINIO',
	'secret_key': 'SECRETMINIOMINIO',
	'secure': False
}

MONGO = \
{
	'host': 'mongodb://developer_user:1YZ9o6GF0JMJ850Niv28@192.168.10.31:27017'
}


CSP_DIRECTIVES = \
{
	'connect-src': ['geolocation-db.com'],
	'font-src': ['fonts.gstatic.com'],
	'frame-ancestors': [],
	'img-src': [],
	'script-src': [],
	'style-src': ['fonts.googleapis.com']
}