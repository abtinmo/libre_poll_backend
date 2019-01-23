CREATE TABLE users (
 user_id VARCHAR(25) PRIMARY KEY ,
 username VARCHAR(100) NOT NULL UNIQUE , 
 password VARCHAR(200) NOT NULL ,
 email VARCHAR(200) UNIQUE ,
 createtime TIMESTAMP DEFAULT NOW() ) ;


CREATE TABLE polls(
 creator VARCHAR(100) REFERENCES  users(username) ON DELETE CASCADE ,
 uuid UUID PRIMARY KEY , 
 name VARCHAR(300) NOT NULL, 
 description TEXT , 
 options TEXT NOT NULL ,
 create_time TIMESTAMP DEFAULT NOW() ,
 last_edit TIMESTAMP DEFAULT NOW() ) ;


CREATE TABLE votes(
 uuid UUID PRIMARY KEY ,
 username  VARCHAR(100) REFERENCES users(username) ON DELETE CASCADE ,
 poll UUID REFERENCES polls(uuid) ON DELETE CASCADE ,
 options TEXT );
