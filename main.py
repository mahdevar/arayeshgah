from redis import Redis
#m = Redis()
#m.keys()
from containers import Cache
c = Cache()
for i in c.keys():
	print(i)


exit()

from atexit import register as run_at_exit
from base64 import b32hexencode
from functools import wraps
from hashlib import sha1
from json import dumps, loads
from logging import basicConfig as logging_config, DEBUG
from os import chdir, urandom, getpid
from pathlib import Path
from sys import gettrace
from threading import Event, Semaphore, Thread
from time import time
from jdatetime import datetime as jdt, j_days_in_month
from flask import abort, Flask, g, render_template, request, send_file
from flask.wrappers import Response
#from minio import Minio
from psycopg2 import connect, OperationalError
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool as CreatePool
#from pymongo import MongoClient
import config

#mongo = MongoClient(**CONFIG.MONGO)['a']
#mongo['c'].insert_one({'_id': 1, 'a': 'hello', 'b': 3.14})
from datetime import datetime

#from pickle import dumps, loads

#minio = Minio(**MINIO_CONFIG)
#minio_ = minio.fput_object('data', 'a', 'D:\\Download\\windowsdesktop-runtime-8.0.8-win-x64.exe')
#minio_ = minio.fput_object('data', 'b', 'D:\\Download\\vidisco\\Vidisco ADMINISTRATION.rar')
#exit()

#redis.set_response_callback('hmget', lambda i: [loads(v) for v in i])
#d = {'a': '31'}
#d = mongo['c'].find_one({'_id': 1})#, {'_id': 0})

#d = 3.14
#redis['a'] = 3.14 #{'a': '31'}
#redis['a'] = dumps(d)
#v = loads(redis['a'])
#redis.hset('a',{'b': 3.14})
#print(v)
#exit()
#redis['b'] = 'aa' #dumps(332)
#b = redis['b']
#print(redis.hmget('a'))
#print(b)
#print(b == 'hello')
#print(redis.)
#exit()
'''
def _execute_(*args, **kwargs):
	g.cursor.execute(*args, **kwargs)
	return g.cursor

def _execute_many_(*args, **kwargs):
	g.cursor.executemany(*args, **kwargs)
	return g.cursor


read_row = lambda *query: _execute_(*query).fetchone()
read_table = lambda *query: _execute_(*query).fetchall()


connection = connect(**CONFIG.SQL)
connection.autocommit = True
#connection.cursor(cursor_factory=RealDictCursor)
with connection.cursor() as cursor:
	cursor.execute('SELECT * FROM users')
	print(cursor.fetchall())


#		g.connection = POOL.getconn()
#		g.cursor = g.connection.cursor(cursor_factory=RealDictCursor)


exit()

'''


app = Flask(__name__, static_folder='file')
app.jinja_env.line_statement_prefix = '#'
G = app.jinja_env.globals
#CONFIG = app.config
DEFAULT_LANGUAGE = 'fa'
ALLOWED_INACTIVITY = 6 * 60
# Database specific configurations
# CONFIG['SEND_FILE_MAX_AGE_DEFAULT'] = 3600
# Initialize
TRANSLATIONS = {}

#exit()
print('>>>>>>>>>>>>>PID:', getpid())
POOL = None
if gettrace():
	logging_config(level=DEBUG)
LOG = app.logger.info
new_user_lock = Semaphore()
chdir(app.root_path)
# Allowed resources
CSP = 'default-src \'none\'; ' + ' '.join('%s %s;' % (name, ' '.join(['\'self\''] + value)) for name, value in config.csp_directives.items())
#CSP = ''


# Utility functions
hash_string = lambda string: b32hexencode(sha1(string.encode()).digest()).decode()
uuid = lambda prefix='': prefix + b32hexencode(urandom(20)).decode()



to_json = lambda data: '{}' if data is None else dumps(data, ensure_ascii=False, separators=(',', ':'))
json_response = lambda data: Response(to_json(data), mimetype='application/json')
EMPTY = json_response({})


def get_nearby_requests():
	# SELECT ST_ASTEXT(T.LOC) AS POINT,	ST_DISTANCE(LOC, POINT(49, 49)) AS DIST FROM T ORDER BY ST_DISTANCE(LOC, POINT(49, 49)) LIMIT 2;
	read_table('SELECT ST_ASTEXT(T.LOC) AS POINT, ST_DISTANCE(LOC, POINT(49, 49)) AS DIST FROM T ORDER BY ST_DISTANCE(LOC, POINT(49, 49)) LIMIT 2')


# Simple scheduler
__STOP_SCHEDULER__ = Event()
__SCHEDULED_FUNCTIONS__ = []


def schedule(interval):
	def decorator(function):
		@wraps(function)
		def repeater(*args, **kwargs):
			while not __STOP_SCHEDULER__.wait(interval):
				function(*args, **kwargs)

		__SCHEDULED_FUNCTIONS__.append(repeater)
		return repeater

	return decorator


@schedule(10 * ALLOWED_INACTIVITY)
def log_inactive_users_out():
	inactive_users = [user for user, data in USERS.items() if time() - data['last activity time'] > ALLOWED_INACTIVITY]
	for user in inactive_users:
		del USERS[user]


# Global macros for accessing the database
def _execute_(*args, **kwargs):
	g.cursor.execute(*args, **kwargs)
	return g.cursor


def _execute_many_(*args, **kwargs):
	g.cursor.executemany(*args, **kwargs)
	return g.cursor


read_row = lambda *query: _execute_(*query).fetchone()
read_table = lambda *query: _execute_(*query).fetchall()
write = lambda *query: _execute_(*query)
write_many = lambda *query: _execute_many_(*query)
new_id = lambda entity: read_row('SELECT nextval(\'new_%s\')' % entity)['nextval']


@app.template_global()
def _(string, language=None):
	try:
		return TRANSLATIONS[language or g.language][string]
	except KeyError:
		return string


@app.before_request
def get_connected():
	"""Connecting to the DB; if necessary"""
	if request.endpoint == 'static':
		return send_file('.' + request.path)
	else:
		g.connection = POOL.getconn()
		g.cursor = g.connection.cursor(cursor_factory=RealDictCursor)
		return None


@app.before_request
def load_user():
	g.uuid = request.cookies.get('UUID')
	if g.uuid:
		try:
			g.user = USERS[g.uuid]
		# Invalid UUID! Perhaps it is forged
		except KeyError:
			g.user = None
			g.uuid = 'INVALID'
		else:
			if time() - g.user['last activity time'] > ALLOWED_INACTIVITY:
				sign_out()
	else:
		g.user = None
	g.language = request.cookies.get('LANGUAGE') or request.headers.get('accept-language')[:2]
	if g.language not in TRANSLATIONS:
		g.language = DEFAULT_LANGUAGE


@app.before_request
def csrf_protection():
	if request.method == 'POST':
		if g.user:
			if request.headers.get('CSRF') != g.user['CSRF']:
				return EMPTY, 417
			g.user['CSRF'] = uuid()
		else:
			if request.endpoint not in ('sign_in', 'sign_up'):
				return EMPTY, 412
	if g.user:
		G['CSRF'] = g.user['CSRF']
	else:
		G['CSRF'] = ''


@app.after_request
def finalize_response(response):
	print('>>>>>DONE BY:', getpid())

	#if 'Content-Type' in response.headers:
	#	print('>', request.url, [i for i in request.headers.keys()])
	if request.endpoint == 'static':
		response.headers['X-Content-Type-Options'] = 'nosniff'
	else:
		if g.user:
			g.user['last activity time'] = time()
			if not g.uuid or g.uuid == 'INVALID':
				g.uuid = uuid('USER')
				while g.uuid in USERS:
					g.uuid = uuid('USER')
				# Add an entry to the UUID-->ID map
				USERS[g.uuid] = g.user
				response.set_cookie('UUID', g.uuid)  # secure=True, samesite='None', httponly=True
		else:
			if g.uuid:
				if g.uuid in USERS:
					del USERS[g.uuid]
				if 'Set-Cookie' not in response.headers:
					response.delete_cookie('UUID')
		#response.headers['X-Frame-Options'] = 'SAMEORIGIN'
		response.headers['Content-Security-Policy'] = CSP
		# response.headers['Strict-Transport-Security'] = 'max-age=604800; includeSubDomains; preload'
		POOL.putconn(g.connection)
	return response


def route(**m):
	"""Route creation
	:param m: parameters used to build a decorator
	:return: a decorator"""

	def decorator(f):
		rule = '/' + f.__name__.replace('_', '-')
		for name, t in f.__annotations__.items():
			rule += '/<%s:%s>' % (t.__name__, name)
		app.add_url_rule(rule, f.__name__, f, **m)
		return f

	return decorator


post = route(methods=['POST'])
get = route(methods=['GET'])


@post
def sign_in():
	if g.user:
		sign_out()
	if data := read_row('SELECT * FROM users WHERE user_name=%s AND password=%s', [request.json['user_name'], hash_string(request.json['password'])]):
		data['CSRF'] = uuid()
		del data['password']
		g.user = data
		return json_response(data), 200
	else:
		return EMPTY, 401


@post
def sign_out():
	if g.user:
		g.user = None
		return EMPTY, 200
	else:
		return EMPTY, 406


@post
def sign_up():
	if read_row('SELECT id FROM users WHERE user_name=%s', [request.json['user_name']]):
		return EMPTY, 409
	else:
		request.json['password'] = hash_string(request.json['password'])
		write('INSERT INTO users (id, %s) VALUES (%s)' % (', '.join(request.json.keys()), ', '.join([r'%s'] * (len(request.json.keys()) + 1))), [new_id('user'), *request.json.values()])
		g.connection.commit()
		return EMPTY, 201


@post
def users(i: int):
	if data := read_row('SELECT * FROM users WHERE id=%s', [i]):
		if data['role'] == 1:
			return EMPTY, 403
		else:
			del data['password']
			return json_response(data), 200
	else:
		return EMPTY, 404


@get
def user_data():
	return json_response(g.user), 200

@get
def u():
	return 2/0, 200


@get
def user_data2():
	if g.user:
		return json_response(g.user), 200
	else:
		return EMPTY, 412


@post
def shop(i: int):
	if data := read_row('SELECT * FROM shop WHERE id=%s', [i]):
		return json_response(data), 200
	else:
		return EMPTY, 404


@post
def user_shops(i: int):
	if data := read_table('SELECT * FROM shop WHERE owner=%s', [i]):
		return json_response(data), 200
	else:
		return EMPTY, 404


@get
def profile():
	if g.user:
		return render_template('profile.html')
	else:
		abort(401)


@get
def search():
	abort(501)


@app.route('/index')
@app.route('/')
@get
def home():
	return render_template('home.html')


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
	return send_file('.' + request.path)


@app.route('/favicon.ico')
@app.route('/favicon.svg')
def fav():
	return send_file('./file/favicon.svg')

POOL = CreatePool(1, 100, **config.sql)
with app.app_context():
	# Install error handlers
	for code in 401, 404, 501:
		app.register_error_handler(code, lambda e: render_template('error.html', error=e))
	# Get connected
	g.connection = POOL.getconn()
	g.cursor = g.connection.cursor(cursor_factory=RealDictCursor)

	a = read_row('SELECT * FROM translations WHERE id=%s', ['USER']).values()
	print('>>>', a)
	# Write translations
	for language in [value for value in read_row('SELECT * FROM translations WHERE id=\'LANGUAGE CODE\'').values() if value != 'LANGUAGE CODE']:
		TRANSLATIONS[language] = {key: value for key, value in [list(k.values()) for k in read_table('SELECT id, %s FROM translations' % language)]}
	for language, translation in TRANSLATIONS.items():
		with open('./file/%s.js' % language, 'w', encoding='utf-8') as file:
			print('document.translation = %s;' % to_json(translation), file=file)
	G['LANGUAGES'] = TRANSLATIONS.keys()
	POOL.putconn(g.connection)
# Start scheduled tasks
for scheduled_function in __SCHEDULED_FUNCTIONS__:
	Thread(target=scheduled_function, daemon=True).start()
run_at_exit(__STOP_SCHEDULER__.set)

'''

with app.app_context():
	print('\n\n\n\n\n\n\n\n\n\n')
	print('>', type(G))
	for i, j in G.items():
		print(i, '->>', j)

'''

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
	#from waitress import serve
	#serve(app, listen='*:80')
