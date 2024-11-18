__all__ = ['CSP']

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
