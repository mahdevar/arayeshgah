from json import dumps

to_json = lambda data: '{}' if data is None else dumps(data, ensure_ascii=False, separators=(',', ':'))
