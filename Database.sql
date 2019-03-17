CREATE TABLE users (
 user_id VARCHAR(25) PRIMARY KEY ,
 can_add INTEGER DEFAULT 0 ,
 username VARCHAR(100) NOT NULL UNIQUE ,
 password VARCHAR(200) NOT NULL ,
 email VARCHAR(200) UNIQUE ,
 createtime TIMESTAMP DEFAULT NOW() ) ;


CREATE TABLE polls(
 creator VARCHAR(100) REFERENCES  users(user_id) ON DELETE CASCADE ,
 poll_id VARCHAR(25) PRIMARY KEY ,
 type INTEGER  default 1 ,
 name VARCHAR(300) NOT NULL ,
 description TEXT ,
 place VARCHAR(500) ,
 options TEXT NOT NULL ,
 create_time TIMESTAMP DEFAULT NOW() ,
 last_edit TIMESTAMP DEFAULT NOW() ) ;


CREATE TABLE votes(
 vote_id VARCHAR(25) PRIMARY KEY ,
 user_id  VARCHAR(100) REFERENCES users(user_id) ON DELETE CASCADE ,
 poll varchar(25) REFERENCES polls(poll_id) ON DELETE CASCADE ,
 options VARCHAR(500)[100] );

CREATE TABLE gp(
 gp_id VARCHAR(25) PRIMARY KEY,
 creator VARCHAR(25) REFERENCES users(user_id) ON DELETE CASCADE ,
 name VARCHAR(200) );

CREATE TABLE gp_users(
 user_id VARCHAR(25) ,
 gp_id VARCHAR(25) );

CREATE TABLE user_poll_access(
 user_id VARCHAR(25) REFERENCES users(user_id) ON DELETE CASCADE ,
 poll_id VARCHAR(25) REFERENCES polls(poll_id) ON DELETE CASCADE );


CREATE OR REPLACE FUNCTION ChangeCanAdd( inputUserID varchar(25) )
 RETURNS INTEGER AS $$
 BEGIN
 IF (SELECT can_add FROM users WHERE user_id = inputUserID) > 0 THEN
 	UPDATE users SET can_add = 0 WHERE user_id = inputUserID ;
 ELSE
        UPDATE users SET can_add = 1 WHERE user_id = inputUserID ;
 END IF;
 RETURN 0;
 END;
$$ LANGUAGE plpgsql;

