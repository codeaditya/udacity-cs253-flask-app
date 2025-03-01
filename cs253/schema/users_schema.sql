drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text unique not null,
  password text not null,
  creation_date timestamp not null,
  email text
);
