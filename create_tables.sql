CREATE TABLE IF NOT EXISTS book (
book_id text PRIMARY KEY ,
author text NOT NULL,
name text NOT NULL,
company text NOT NULL,
pages integer NOT NULL,
year integer NOT NULL,
book_photo BLOB NOT NULL,
view integer NOT NULL
);

CREATE TABLE IF NOT EXISTS user (
user_id integer PRIMARY KEY AUTOINCREMENT,
username text NOT NULL,
email text NOT NULL,
password text NOT NULL,
avatar BLOB
);

CREATE TABLE IF NOT EXISTS massages (
massage_id integer PRIMARY KEY AUTOINCREMENT,
user_id integer NOT NULL,
time text NOT NULL,
text text NOT NULL,
book_id integer NOT NULL
);