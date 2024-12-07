__all__ = ['to_json']

from annotation import Dictionary, Number, String
from flask import blueprints
from json import dumps


def to_json(data: Dictionary | Number | String) -> String:
	if data:
		return dumps(data, ensure_ascii=False, separators=(',', ':'))
	else:
		return '{}'


def routing(blueprints, **m):
	"""Route creation
	:param m: parameters used to build a decorator
	:return: a decorator"""

	def decorator(f):
		rule = '/' + f.__name__.replace('_', '-')
		for name, t in f.__annotations__.items():
			rule += '/<%s:%s>' % (t.__name__, name)
		blueprints.add_url_rule(rule, f.__name__, f, **m)
		return f

	return decorator
