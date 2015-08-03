use simon;
create table Scores(id int not null primary key auto_increment, score bigint not null, player int not null, recorded timestamp not null default current_timestamp);
