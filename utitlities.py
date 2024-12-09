from threading import Event
from functools import wraps

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