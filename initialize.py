from containers import Cache, Database
from psycopg.rows import dict_row
from utilities import jsonify


def load_languages():
	db = Database()
	translations = Cache()
	with db.connection() as connection, connection.cursor() as cursor:
		cursor.execute('SELECT * FROM translations WHERE id=\'LANGUAGE CODE\'')
		languages = cursor.fetchone()[1:]
		print('ALL:', languages)
		translations['languages'] = languages
		for language in languages:
			print('>>>>>>>>>>>', language)
			cursor.execute('SELECT id, %s FROM translations' % language)
			pairs = {key: value for key, value in cursor.fetchall()}
			print('????', language, pairs)
			with open('./static/%s.js' % language, 'w') as file:
				print('document.translation = %s;' % jsonify(pairs), file=file)
			translations[language] = pairs
	print('>>>>>>>DONE')

load_languages()
