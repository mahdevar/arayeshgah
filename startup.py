from utilities import SETTING

from json import dumps
from config import redis, sql
from psycopg2 import connect

translation = {}
with connect(**sql) as connection:
	with connection.cursor() as cursor:
		cursor.execute('SELECT * FROM translations WHERE id=\'LANGUAGE CODE\'')
		languages = [value for value in cursor.fetchone() if value != 'LANGUAGE CODE']
		for language in languages:
			cursor.execute('SELECT id, %s FROM translations' % language)
			translation[language] = {key: value for key, value in cursor.fetchall()}

for language, values in translation.items():
	with open('./file/%s.js' % language, 'w', encoding='utf-8') as file:
		print('document.translation = %s;' % dumps(values, ensure_ascii=False), file=file)
SETTING['translation'] = translation

