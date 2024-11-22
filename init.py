from containers import Cache, Database
from psycopg2.extras import RealDictCursor
from utilities import to_json

print('.....................')

DB = Database()
CONNECTION = DB.getconn()
TRANSLATIONS = Cache()
with CONNECTION.cursor(cursor_factory=RealDictCursor) as CURSOR:
	CURSOR.execute('SELECT * FROM translations WHERE id=\'LANGUAGE CODE\'')
	for language in [value for value in CURSOR.fetchone().values() if value != 'LANGUAGE CODE']:
		print('>>>>>>>>>>>', language)
		CURSOR.execute('SELECT id, %s FROM translations' % language)
		pairs = {key: value for key, value in [list(k.values()) for k in CURSOR.fetchall()]}
		with open('./file/%s.js' % language, 'w') as file:
			print('document.translation = %s;' % to_json(pairs), file=file)
		TRANSLATIONS[language] = pairs

DB.putconn(CONNECTION)
