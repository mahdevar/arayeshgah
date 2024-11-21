__all__ = ['to_json']

from annotation import Dictionary, Number, String

from json import dumps


def to_json(data: Dictionary | Number | String) -> String:
	if data:
		return dumps(data, ensure_ascii=False, separators=(',', ':'))
	else:
		return '{}'
