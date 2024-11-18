from psycopg2.extras import RealDictCursor
from containers import Cache, Database 
from json import dumps, loads



to_json = lambda data: '{}' if data is None else dumps(data, ensure_ascii=False, separators=(',', ':'))

DB = Database()

TRANSLATIONS = Cache()

CONNECTION = DB.getconn()
CURSOR = CONNECTION.cursor(cursor_factory=RealDictCursor)
CURSOR.execute('SELECT * FROM translations WHERE id=\'LANGUAGE CODE\'')



for language in [value for value in CURSOR.fetchone().values() if value != 'LANGUAGE CODE']:
	print('>>', language)

'''
	CURSOR.execute('SELECT id, %s FROM translations' % language)
	TRANSLATIONS[language] = {key: value for key, value in [list(k.values()) for k in CURSOR.fetchall()]}
	for language, translation in TRANSLATIONS.items():
		with open('./file/%s.js' % language, 'w', encoding='utf-8') as file:
			print('document.translation = %s;' % to_json(translation), file=file)
	G['LANGUAGES'] = TRANSLATIONS.keys()
	POOL.putconn(g.connection)

'''
