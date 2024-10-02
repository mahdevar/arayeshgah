from atexit import register as run_at_exit
from base64 import b32hexencode
from functools import wraps
from hashlib import sha1
from json import dumps
from logging import basicConfig as logging_config, DEBUG
from os import chdir, urandom
from pathlib import Path
from sys import gettrace
from threading import Event, Semaphore, Thread
from time import time

from flask import abort, Flask, g, render_template, request, send_file
from flask.wrappers import Response
from psycopg2 import connect, OperationalError
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool as CreatePool

from config import SQL_CONFIG

# minio = Minio(**MINIO_CONFIG)
# minio_ = minio.fput_object('users', 'a', 'D:\\Download\\3fe778a1f6c50712435d03d157149b8028339aeab5fd925044ad8d6b7232a30a.jpg')

# redis = Redis(**REDIS_CONFIG)
# redis['a'] = 'Hello'
# print(redis['a'])

app = Flask(__name__, static_folder='file')
app.jinja_env.line_statement_prefix = '#'
G = app.jinja_env.globals
CONFIG = app.config
DEFAULT_LANGUAGE = 'fa'
ALLOWED_INACTIVITY = 6 * 60
# Database specific configurations
# CONFIG['SEND_FILE_MAX_AGE_DEFAULT'] = 3600
# Initialize
TRANSLATIONS = {}
USERS = {}
POOL = None
if gettrace():
	logging_config(level=DEBUG)
LOG = app.logger.info
new_user_lock = Semaphore()
chdir(app.root_path)
# Allowed resources
CSP_DIRECTIVES = {'connect': ['geolocation-db.com'], 'img': [], 'font': ['fonts.gstatic.com'], 'script': [], 'style': ['fonts.googleapis.com']}
CONFIG['Content-Security-Policy'] = 'default-src \'none\';' + ' '.join('%s-src %s;' % (name, ' '.join(['\'self\''] + value)) for name, value in CSP_DIRECTIVES.items())
# CONFIG['Content-Security-Policy'] = ''
# Utility functions
hash_string = lambda string: str(b32hexencode(sha1(string.encode('utf-8')).digest()))[2:-1]
uuid = lambda prefix='': prefix + str(b32hexencode(urandom(20)))[2:-1]
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
new_id = lambda: read_row('SELECT nextval(\'new_id\')')['nextval']


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
		response.headers['X-Frame-Options'] = 'SAMEORIGIN'
		response.headers['Content-Security-Policy'] = CONFIG['Content-Security-Policy']
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
		write('INSERT INTO users (id, %s) VALUES (%s)' % (', '.join(request.json.keys()), ', '.join([r'%s'] * (len(request.json.keys()) + 1))), [new_id(), *request.json.values()])
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


def create_database():
	"""Create database, if necessary"""
	connection = connect(**(SQL_CONFIG | {'database': 'postgres'}))
	connection.autocommit = True
	with connection.cursor() as cursor:
		cursor.execute('CREATE DATABASE %s ENCODING UTF8' % SQL_CONFIG['database'])
	connection.close()
	with connect(**SQL_CONFIG) as connection:
		with connection.cursor() as cursor:
			for script in sorted(Path('queries').glob('*.sql')):
				print('Executing: ' + script.name)
				for query in script.read_text(encoding='utf-8').split(';'):
					query = query.strip()
					if query:
						cursor.execute(query)
		connection.commit()


try:
	POOL = CreatePool(1, 100, **SQL_CONFIG)
except OperationalError:
	# DB does not exist
	create_database()
	POOL = CreatePool(1, 100, **SQL_CONFIG)
with app.app_context():
	# Install error handlers
	for code in 401, 404, 501:
		app.register_error_handler(code, lambda e: render_template('error.html', error=e))
	# Get connected
	g.connection = POOL.getconn()
	g.cursor = g.connection.cursor(cursor_factory=RealDictCursor)
	# Write translations
	for language in [value for value in read_row('SELECT * FROM translation WHERE id=\'LANGUAGE CODE\'').values() if value != 'LANGUAGE CODE']:
		TRANSLATIONS[language] = {key: value for key, value in [list(k.values()) for k in read_table('SELECT id, %s FROM translation' % language)]}
	for language, translation in TRANSLATIONS.items():
		with open('./file/%s.js' % language, 'w', encoding='utf-8') as file:
			print('document.translation = %s;' % to_json(translation), file=file)
	G['LANGUAGES'] = TRANSLATIONS.keys()
	POOL.putconn(g.connection)
# Start scheduled tasks
for scheduled_function in __SCHEDULED_FUNCTIONS__:
	Thread(target=scheduled_function, daemon=True).start()
run_at_exit(__STOP_SCHEDULER__.set)

if __name__ == '__main__':
	# app.run(debug=True)
	print('!!!!!!!')
	from waitress import serve

	serve(app, listen='*:80')
