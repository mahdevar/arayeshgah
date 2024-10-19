CREATE SEQUENCE new_id START WITH 100 CACHE 1;
CREATE TABLE users
(
	id	INTEGER,
	accuracy	INTEGER,
	family	TEXT,
	gender	INTEGER,
	location	POINT,
	mobile	TEXT,
	name	TEXT,
	password	TEXT,
	role    INTEGER,
	user_name	TEXT
);
CREATE TABLE shops
(
	id	INTEGER,
	accuracy	INTEGER,
	address	TEXT,
	description	TEXT,
	location	POINT,
	multiplier	NUMERIC,
	phones	TEXT[10],
	photos	TEXT[10],
	title	TEXT,
 	owner	INTEGER
);
CREATE TABLE services
(
	id	INTEGER,
	description	TEXT,
	duration	INTEGER,
	photos	TEXT[10],
	price	INTEGER
);
CREATE TABLE proficiencies
(
	barber	INTEGER,
	service	INTEGER
);
CREATE TABLE votes
(
	id	INTEGER,
	barber	INTEGER,
	comment	TEXT,
	customer	INTEGER,
	score	INTEGER,
	time	TIMESTAMP
);
CREATE TABLE requests
(
	id	INTEGER,
	barber	INTEGER,
	customer	INTEGER,
	note	TEXT,
	service	INTEGER,
	time	TIMESTAMP
);
CREATE TABLE products
(
	id	INTEGER,
	description	TEXT,
	photos	TEXT[10],
	price	INTEGER
);
CREATE TABLE attributes
(
	title	TEXT,
	icon	TEXT,
	type	INTEGER
);
CREATE TABLE translations
(
	id	TEXT,
	en	TEXT,
	fa	TEXT
);