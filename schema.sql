create table if not exists users (
id integer primary key autoincrement,
name text not null,
binary text not null,
status boolean not null
);
create table if not exists log (
id integer primary key autoincrement,
date text not null,
name text not null,
binary text not null,
status boolean not null
);
