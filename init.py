__all__ = ['load_languages']
from containers import Cache, Database
from psycopg2.extras import RealDictCursor
from utilities import jsonify


def load_languages():
	db = Database()
	connection = db.getconn()
	translations = Cache()
	with connection.cursor(cursor_factory=RealDictCursor) as cursor:
		cursor.execute('SELECT * FROM translations WHERE id=\'LANGUAGE CODE\'')
		languages = [value for value in cursor.fetchone().values() if value != 'LANGUAGE CODE']
		translations['languages'] = languages
		for language in languages:
			print('>>>>>>>>>>>', language)
			cursor.execute('SELECT id, %s FROM translations' % language)
			pairs = {key: value for key, value in [list(k.values()) for k in cursor.fetchall()]}
			with open('./file/%s.js' % language, 'w') as file:
				print('document.translation = %s;' % jsonify(pairs), file=file)
			translations[language] = pairs
	db.putconn(connection)
