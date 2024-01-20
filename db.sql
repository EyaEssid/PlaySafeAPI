create table users ( username varchar(20) , password varchar(50) , country varchar(30) , phone_number varchar(15) , email varchar(50),  birthdate date );
create table players ( username varchar(20) , level int , games_played int , games_won int);
insert into users values ( 'leuheul','Eyaessid2001*','Tunisia','94937391','eyayouta2001@gmail.com','2001-12-26'),
('samir','SAMEER','Tunisia','94937391','eyayouta2001@gmail.com','2002-12-26');
insert into players values('leuheul' , 1 , 10 , 4 ) , ('samir' , 2 , 15 , 6 ) ; 
ALTER TABLE users ADD CONSTRAINT pk_users PRIMARY KEY (username);
ALTER TABLE players ADD constraint pk_players PRIMARY KEY (username);
ALTER TABLE players ADD CONSTRAINT fk_players FOREIGN KEY (username)  REFERENCES users(username);
create table report ( username varchar(20) , reports int)
ALTER TABLE report ADD CONSTRAINT fk_player FOREIGN KEY (username)  REFERENCES users(username);
