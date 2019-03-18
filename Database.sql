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
 user_id VARCHAR(25) REFERENCES users(user_id) ON DELETE CASCADE,
 gp_id VARCHAR(25) REFERENCES gp(gp_id) ON DELETE CASCADE );

CREATE TABLE user_poll_access(
 user_id VARCHAR(25) REFERENCES users(user_id) ON DELETE CASCADE ,
 poll_id VARCHAR(25) REFERENCES polls(poll_id) ON DELETE CASCADE );


CREATE OR REPLACE FUNCTION ChangeCanAdd( inputUserID varchar(25) )
 RETURNS INTEGER AS $$
 BEGIN
 IF (SELECT can_add FROM users WHERE users.user_id = inputUserID) > 0 THEN
 	UPDATE users SET can_add = 0 WHERE user_id = inputUserID ;
 ELSE
        UPDATE users SET can_add = 1 WHERE user_id = inputUserID ;
 END IF;
 RETURN 0;
 END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION AddUserToGroup(inputGroupID varchar(25), inputUserID varchar(25), inputCreatorID varchar(25))
 RETURNS TABLE(
 user_id varchar
 ) AS $$
 BEGIN
 IF ( (SELECT count(*) FROM gp WHERE creator = inputCreatorID AND gp_id = inputGroupID ) > 0  AND  (SELECT can_add FROM users WHERE users.user_id = inputUserID) > 0  )THEN
 	INSERT INTO gp_users(user_id, gp_id) VALUES (inputUserID, inputGroupID);
 END IF;
 RETURN QUERY SELECT gp_users.user_id::varchar(25)
 FROM gp_users WHERE gp_users.gp_id = inputGroupID ;
 END;
$$ LANGUAGE plpgsql;

