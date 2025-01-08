from containers import Cache, Database
from utilities import jsonify

db = Database()
cache = Cache()


def load_languages() -> None:
	languages = [code for code in db.row('SELECT * FROM translations WHERE id=%s', ['language code']) if code != 'id']
	cache['languages'] = languages
	for language in languages:
		pairs = {pair['id']: pair[language] for pair in db.rows('SELECT id, %s FROM translations' % language)}
		with open('static/%s.js' % language, 'w') as file:
			print('document.translation = %s;' % jsonify(pairs), file=file)
		cache[language] = pairs


def load_tables() -> None:
	tables = [row['name'] for row in db.rows('SELECT table_name AS name FROM information_schema.tables WHERE table_schema=%s', ['public'])]
	cache['tables'] = tables
	for table in tables:
		cache[table] = [attribute['name'] for attribute in db.rows('SELECT column_name AS name FROM information_schema.columns WHERE table_name=%s AND table_schema=%s', [table, 'public'])]


def load_attributes() -> None:
	cache['attributes'] = db.rows('SELECT * FROM attributes')


load_languages()
load_tables()
load_attributes()
