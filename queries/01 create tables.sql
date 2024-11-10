CREATE TABLE users
(
	id	INTEGER PRIMARY KEY,
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
	id	INTEGER PRIMARY KEY,
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
	id	INTEGER PRIMARY KEY,
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
	id	INTEGER PRIMARY KEY,
	barber	INTEGER,
	comment	TEXT,
	customer	INTEGER,
	score	INTEGER,
	time	TIMESTAMP
);
CREATE TABLE requests
(
	id	INTEGER PRIMARY KEY,
	barber	INTEGER,
	customer	INTEGER,
	note	TEXT,
	service	INTEGER,
	time	TIMESTAMP
);
CREATE TABLE products
(
	id	INTEGER PRIMARY KEY,
	description	TEXT,
	photos	TEXT[10],
	price	INTEGER
);
CREATE TABLE attributes
(
	title	TEXT PRIMARY KEY,
	icon	TEXT,
	type	INTEGER
);
CREATE TABLE translations
(
	id	TEXT PRIMARY KEY,
	en	TEXT,
	fa	TEXT
);
CREATE SEQUENCE new_user;
CREATE SEQUENCE new_shop;
CREATE SEQUENCE new_service;
CREATE SEQUENCE new_proficiency;
CREATE SEQUENCE new_vote;
CREATE SEQUENCE new_request;
CREATE SEQUENCE new_product;
CREATE SEQUENCE new_attribute;