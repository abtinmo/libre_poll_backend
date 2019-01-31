CREATE TABLE users (
 user_id VARCHAR(25) PRIMARY KEY ,
 username VARCHAR(100) NOT NULL UNIQUE , 
 password VARCHAR(200) NOT NULL ,
 email VARCHAR(200) UNIQUE ,
 createtime TIMESTAMP DEFAULT NOW() ) ;


CREATE TABLE polls(
 creator VARCHAR(100) REFERENCES  users(username) ON DELETE CASCADE ,
 poll_id VARCHAR(25) PRIMARY KEY , 
 name VARCHAR(300) NOT NULL , 
 description TEXT , 
 place VARCHAR(500) ,
 options TEXT NOT NULL ,
 create_time TIMESTAMP DEFAULT NOW() ,
 last_edit TIMESTAMP DEFAULT NOW() ) ;


CREATE TABLE votes(
 vote_id VARCHAR(25) PRIMARY KEY ,
 username  VARCHAR(100) REFERENCES users(username) ON DELETE CASCADE ,
 poll varchar(25) REFERENCES polls(poll_id) ON DELETE CASCADE ,
 options VARCHAR(500)[100] );
