

drop table if exists users;
    create table users (
    username text primary key not null,
    password text null,
    FOREIGN KEY(username) REFERENCES OwnedPokemon(owner)
);

drop table if exists OwnedPokemon;
    create table OwnedPokemon (
    type text not null,	
    name text not null,
    level int not null,
    owner text not null,
    PRIMARY KEY(owner,name)
 );

drop table if exists Pokemon;
    create table Pokemon (
	type text not null,
	name text not null,
	PRIMARY KEY(name),
	FOREIGN KEY(name)
	REFERENCES OwnedPokemon(pname)
);

