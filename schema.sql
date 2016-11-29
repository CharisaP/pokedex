

drop table if exists users;
    create table users (
    username text primary key not null,
    password text null
);
