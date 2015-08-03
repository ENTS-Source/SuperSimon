-- Version 1.0 - Initial database structure
create table if not exists Scores(id int not null primary key auto_increment, score bigint not null, player int not null, recorded timestamp not null default current_timestamp);
