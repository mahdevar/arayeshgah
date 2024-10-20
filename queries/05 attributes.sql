/*
1	INTEGER		2	TEXT		3	NUMERIC
4	PASSWORD	5	ROLE		6	GENDER
7	POINT		8	TIMESTAMP	9	PHONES
10	PHOTOS		11	DURATION
*/
INSERT INTO attributes(title, icon, type) VALUES
	('ACCURACY',	'straighten',	1),
	('ADDRESS',	'location_city',	2),
	('BARBER',	'styler',	1),
	('COMMENT',	'comment',	2),
	('CUSTOMER',	'face',	1),
	('DESCRIPTION',	'description',	2),
	('DURATION',	'timer',	11),
	('FAMILY',	'edit',	2),
	('GENDER',	'wc',	1),
	('ID',	'fingerprint',	1),
	('LOCATION',	'map',	1),
	('MOBILE',	'smartphone',	1),
	('MULTIPLIER',	'percent',	1),
	('NAME',	'edit',	2),
	('NOTE',	'note',	2),
	('OWNER',	'store',	1),
	('PASSWORD',	'password',	4),
	('PHONES',	'call',	9),
	('PHOTOS',	'image',	10),
	('PRICE',	'credit_card',	1),
	('ROLE',	'group',	5),
	('SCORE',	'score',	3),
	('SERVICE',	'dry_cleaning',	1),
	('TIME',	'av_timer',	8),
	('TITLE',	'title',	1),
	('LAST ACTIVITY TIME',	'history',	8),
	('USER_NAME',	'person',	1) ON CONFLICT DO NOTHING;
