drop table if exists ascii_art;
create table ascii_art (
  id integer primary key autoincrement,
  title text not null,
  art text not null,
  created timestamp not null,
  coords text
);
