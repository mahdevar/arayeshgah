from containers import Cache, Database
from utilities import jsonify


def load_languages() -> None:
	db = Database()
	translations = Cache()
	languages = [code for code in db.row('SELECT * FROM translations WHERE id=%s', ['LANGUAGE CODE']) if code != 'id']
	for language in languages:
		pairs = {pair['id']: pair[language] for pair in db.rows('SELECT id, %s FROM translations' % language)}
		with open('static/%s.js' % language, 'w') as file:
			print('document.translation = %s;' % jsonify(pairs), file=file)
		translations[language] = pairs


load_languages()
