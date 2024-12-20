from contextlib import contextmanager
from functools import partial
from json import dumps, loads
from logging import basicConfig as logging_config, DEBUG
from os import chdir, getpid
from pathlib import Path
from sys import gettrace
from threading import Event, Semaphore, Thread
from time import time
from jdatetime import datetime as jdt, j_days_in_month
from flask import abort, Flask, g, render_template, request, send_file, make_response
from minio import Minio
from multiprocessing import Pool
from psycopg.rows import dict_row
from config import ALLOWED_INACTIVITY, DEFAULT_LANGUAGE
from containers import Cache, Database, Session

from utilities import easy_routing, HTTP, uuid

app = Flask(__name__)
app.jinja_env.line_statement_prefix = '#'

get = easy_routing(app, methods=['GET'])
post = easy_routing(app, methods=['POST'])

G = app.jinja_env.globals
#CONFIG = app.config
#CONFIG['DEBUG'] = True
#CONFIG['SEND_FILE_MAX_AGE_DEFAULT'] = 3600

CACHE = Cache()
SESSION = Session()
pool = Database()

@contextmanager
def get_db_connection():
	connection = pool.getconn()
	try:
		yield connection
	finally:
		pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
	with get_db_connection() as connection:
		cursor = connection.cursor()
		try:
			yield cursor
			if commit:
				connection.commit()
		finally:
			cursor.close()

#pool.autocommit = True

@contextmanager
def exec2(query, cursor_factory=None, commit=False):
	connection = pool.getconn()
	#connection.row_factory = dict_row
	#connection.autocommit = True
	print('>>>>>>>>>>>>>>>>>>>>>>>>', connection.autocommit)
	cursor = connection.cursor(row_factory=dict_row)
	cursor.execute(query)
	yield cursor
	cursor.close()
	#connection.commit()
	pool.putconn(connection)

@contextmanager
def exec(*query, row_factory=None, commit=False):
	with pool.connection() as connection:
		with connection.cursor(row_factory=row_factory) as cursor:
			cursor.execute(*query)
			yield cursor

		if commit:
			connection.commit()


#with get_db_cursor() as cursor:
#	cursor.execute()
	#cursor
#execute('INSERT INTO translations (id, en, fa) VALUES (0, 1, 2)', commit=True)
'''
with pool.connection() as connection, connection.cursor(row_factory=dict_row) as cursor:
	cursor.execute('select * from translations')
	a = cursor.fetchall()
	print('???', )
	for i in a:
		print(i, type(i))
'''
with pool.exec2('select * from users') as result:
	a = result.description
	b = result.pgresult
	print('description:', [[i.name, i.type_code] for i in a])
	print('pgresult:', b, result.rowcount)
	print('result;', result)


print('>>>>', r'INSERT INTO translations (' + ', '.join(['id', 'fa', 'en']) + ') VALUES (%s, %s, %s)', ['x', 'unknown', 'ناشاخته'])
#with pool['INSERT INTO translations (' + ', '.join(['id', 'fa', 'en']) + ') VALUES (%s, %s, %s)', ['x', 'unknown', 'ناشاخته']] as result:
#	result.connection.commit()
#	pass

pool['INSERT INTO translations (' + ', '.join(['id', 'fa', 'en']) + ') VALUES (%s, %s, %s)'] = [['a', 'unknown', 'ناشاخته'], ['b', 'unknown', 'ناشاخته'], ['c', 'unknown', 'ناشاخته']]

from dataclasses import dataclass
#a = pool.row('select * from translations', row_factory=dict_row)
#b = pool.rows('SELECT * FROM users WHERE id=%s', [0])
with pool['select * from translations where id like %s', ['%']] as result:
	n = [i.name for i in result.description]
	for i in result:
		print('<<', *zip(n, i))
with pool['select * from users where id=%s', [10]] as result:
	for i in result:
		print('<<', i)


'''
with pool['select * from users where id=%s', [0]] as result:
	n = result.pgresult.nfields
	print('___', n)
	for i in result:
		print('<<', i)
#for i, c in enumerate(pool.rows('select * from translations')):
#	print('>>',i, ' ->', c)

print('>>>', a, b)

'''
'''
with exec('select * from translations') as result:
	#a = result#.fetchall()
	print(type(result))
	#for i in result:
	#	print(i, type(i))

'''
@get
def aa():
	return 2/0

@app.route('/index')
@app.route('/')
@get
def home():
	return HTTP.OK

@app.route('/aaa')
def aaa():
	print('calling ccc')
	return 'سلام'



#exit()
'''if gettrace():
	logging_config(level=DEBUG)
LOG = app.logger.info
'''
chdir(app.root_path)

if __name__ == "__main__" :
	print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
	app.run(host=':8000', debug=True )

if 1 == 2:
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
			return CACHE[language or g.language][string]
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
				g.user = Session[g.uuid]
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
		if g.language not in CACHE:
			g.language = DEFAULT_LANGUAGE
	
	
	@app.before_request
	def csrf_protection():
		if request.method == 'POST':
			if g.user:
				if request.headers.get('CSRF') != g.user['CSRF']:
					return HTTP.EXPECTATION_FAILED
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
			response.headers['Content-Security-Policy'] = config.CSP
			# response.headers['Strict-Transport-Security'] = 'max-age=604800; includeSubDomains; preload'
			POOL.putconn(g.connection)
		return response
	
	
	
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
		return send_file('./static/favicon.svg')
	
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
			with open('./static/%s.js' % language, 'w', encoding='utf-8') as file:
				print('document.translation = %s;' % to_json(translation), file=file)
		G['LANGUAGES'] = TRANSLATIONS.keys()
		POOL.putconn(g.connection)
	
	'''
	
	with app.app_context():
		print('\n\n\n\n\n\n\n\n\n\n')
		print('>', type(G))
		for i, j in G.items():
			print(i, '->>', j)
	
	'''
