from containers import Cache, Database
from utilities import jsonify


def load_languages() -> None:
	db = Database()
	cache = Cache()
	languages = [code for code in db.row('SELECT * FROM translations WHERE id=%s', ['LANGUAGE CODE']) if code != 'id']
	cache['languages'] = languages
	for language in languages:
		pairs = {pair['id']: pair[language] for pair in db.rows('SELECT id, %s FROM translations' % language)}
		with open('static/%s.js' % language, 'w') as file:
			print('document.translation = %s;' % jsonify(pairs), file=file)
		cache[language] = pairs

	tables = [row['table_name'] for row in db.rows('SELECT table_name FROM information_schema.tables WHERE table_schema=%s', ['public'])]
	cache['tables'] = tables
	for table in tables:
		pairs = {pair['column_name']: pair['data_type'] for pair in  db.rows('SELECT column_name, data_type FROM information_schema.columns WHERE table_name=%s and table_schema=%s', [table, 'public'])}
		print(table, '->>', pairs)






load_languages()
