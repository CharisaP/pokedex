

drop table if exists users;
    create table users (
    username text primary key not null,
    password text null,
    FOREIGN KEY(username) REFERENCES OwnedPokemon(owner)
);

drop table if exists OwnedPokemon;
    create table OwnedPokemon (
    type text,	
    pname text not null,
    level int,
    owner text
    PRIMARY KEY(owner,pname)
    );

drop table if exists PokemonDB;
    create table PokemonDB (
	type text,
	name text,
	PRIMARY KEY(name,type),
	FOREIGN KEY(name)
	REFERENCES OwnedPokemon(pname)
	);
