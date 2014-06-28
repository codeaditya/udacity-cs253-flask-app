drop table if exists blog;
create table blog (
  id integer primary key autoincrement,
  subject text not null,
  content text not null,
  posted timestamp not null
);
