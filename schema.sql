drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  Folder text not null,
  Password text not null,
  Hostnames text not null,
  Receivers text not null
);
