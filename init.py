from config import SQL_CONFIG
from pathlib import Path
from psycopg2 import connect
from psycopg2.errors import DuplicateDatabase, DuplicateTable

connection = connect(**(SQL_CONFIG | {'database': 'postgres'}))
connection.autocommit = True
with connection.cursor() as cursor:
	try:
		cursor.execute('CREATE DATABASE %s ENCODING UTF8' % SQL_CONFIG['database'])
	except DuplicateDatabase:
		pass
connection.close()
with connect(**SQL_CONFIG) as connection:
	connection.autocommit = True
	with connection.cursor() as cursor:
		for script in sorted(Path('queries').glob('*.sql')):
			print('Executing: ' + script.name)
			for query in script.read_text(encoding='utf-8').split(';'):
				query = query.strip()
				if query:
					try:
						cursor.execute(query)
					except DuplicateTable:
						pass
					finally:
						connection.commit()
	connection.commit()
