__all__ = ['ALLOWED_INACTIVITY', 'CSP', 'DEFAULT_LANGUAGE']

ALLOWED_INACTIVITY = 6 * 60

# Allowed resources
CSP_DIRECTIVES = \
{
	'connect-src': ['geolocation-db.com'],
	'font-src': ['fonts.gstatic.com'],
	'frame-ancestors': [],
	'img-src': [],
	'script-src': [],
	'style-src': ['fonts.googleapis.com']
}

CSP = 'default-src \'none\'; ' + ' '.join('%s %s;' % (name, ' '.join(['\'self\''] + value)) for name, value in CSP_DIRECTIVES.items())

DEFAULT_LANGUAGE = 'fa'
