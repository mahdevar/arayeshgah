__all__ = ['to_json']

from annotation import Dictionary, Number, String
from threading import Event
from functools import wraps
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


__STOP_SCHEDULER__ = Event()
__SCHEDULED_FUNCTIONS__ = []


def schedule(interval):
	def decorator(function):
		@wraps(function)
		def repeater(*args, **kwargs):
			while not __STOP_SCHEDULER__.wait(interval):
				function(*args, **kwargs)

		__SCHEDULED_FUNCTIONS__.append(repeater)
		return repeater

	return decorator

'''
@schedule(10 * ALLOWED_INACTIVITY)
def log_inactive_users_out():
	inactive_users = [user for user, data in USERS.items() if time() - data['last activity time'] > ALLOWED_INACTIVITY]
	for user in inactive_users:
		del USERS[user]
'''

'''
# Start scheduled tasks
for scheduled_function in __SCHEDULED_FUNCTIONS__:
	Thread(target=scheduled_function, daemon=True).start()
run_at_exit(__STOP_SCHEDULER__.set)
'''


class HTTP:
        ACCEPTED = EMPTY, 202
        CONFLICT = EMPTY, 409
        CREATED = EMPTY, 201
        FORBIDDEN = EMPTY, 403
        METHOD_NOT_ALLOWED = EMPTY, 405
        NOT_ACCEPTABLE = EMPTY, 406
        NO_CONTENT = EMPTY, 204
        OK = EMPTY, 200
        UNAUTHORIZED = EMPTY, 401

class HTTP:
    __slots__ = codes.keys()
for name, code in codes.items():
    setattr(HTTP, name, (EMPTY, code))


# Utility functions
hash_string = lambda string: b32hexencode(sha1(string.encode()).digest()).decode()
uuid = lambda prefix='': prefix + b32hexencode(urandom(20)).decode()