

drop table if exists users;
    create table users (
    username text primary key not null,
    password text  null
);

drop table if exists pokemon;
    create table pokemon (

    pname text not null,
    pid integer primary key not null,
    ptype text not null,
    owner text not null

    );

    
