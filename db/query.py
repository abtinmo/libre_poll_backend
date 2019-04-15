from sanic import response
from .functions import buildToken, makeConn, tokenIsValid
import psycopg2
from psycopg2.extras import RealDictCursor
import json as js

def getGroupmembers(token, json):
    """
    get token and gp_id then return all group members
    """
    token_result = tokenIsValid(token)
    if token_result['status'] == 'OK':
        if 'gp_id' not in json:
            return response.json({'message': 'gp_id is  Empty'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=401)
        sql2 = "SELECT creator FROM gp WHERE gp_id = %s;"
        conn = None
        conn = makeConn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql2, (json["gp_id"],))
        creator = cur.fetchone()
        if creator["creator"] != token_result["user"]:
            return response.json({'message': 'Failure, You dont have acsess to this group'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=401)
        else:
            sql = "SELECT user_id FROM gp_users WHERE gp_id = %s;"
            conn = None
            conn = makeConn()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(sql, (json["gp_id"],))
            row = cur.fetchall()
            data = []
            while row is not None:
                data.append(row)
                row = cur.fetchone()
            cur.close()
            return response.json({"message": "OK", 'users': data},
                                 headers={'X-Served-By': 'sanic'},
                                 status=200)
    else:
        return response.json({'message': 'Failure, Token invalid '},
                             headers={'X-Served-By': 'sanic'},
                             status=401)
def getAllgroup(token):
    """
    get token and return all groups for user
    """
    token_result = tokenIsValid(token)
    if token_result['status'] == 'OK':
        sql = "SELECT name , gp_id FROM gp WHERE creator = %s;"
        conn = None
        conn = makeConn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, (token_result["user"], ))
        row = cur.fetchone()
        data = []
        while row is not None:
            data.append(row)
            row = cur.fetchone()
        cur.close()
        return response.json({"message": "OK", 'groups': data},
                             headers={'X-Served-By': 'sanic'},
                             status=200)
    else:
        return response.json({'message': 'Failure, Token invalid '},
                             headers={'X-Served-By': 'sanic'},
                             status=401)

def userIDToUsername(json):
    sql = '''SELECT username FROM users WHERE user_id = %s;'''
    if 'user_id' not in json:
        return response.json({'message': 'user_id is  Empty'},
                             headers={'X-Served-By': 'sanic'},
                             status=401)
    conn = None
    conn = makeConn()
    cur = conn.cursor()
    cur.execute(sql, [json["user_id"], ])
    user_id = cur.fetchone()[0]
    cur.close()
    return response.json({"message": "OK", "user_id": user_id},
                         headers={'X-Served-By': 'sanic'},
                         status=200)


def usernameToUserID(json):
    sql = '''SELECT user_id FROM users WHERE username = %s;'''
    if 'username' not in json:
        return response.json({'message': 'Username is  Empty'},
                             headers={'X-Served-By': 'sanic'},
                             status=401)
    conn = None
    conn = makeConn()
    cur = conn.cursor()
    cur.execute(sql, [json["username"], ])
    username = cur.fetchone()[0]
    cur.close()
    return response.json({"message": "OK", "username": username},
                         headers={'X-Served-By': 'sanic'},
                         status=200)


def getToken(json):
    sql = '''SELECT user_id FROM users WHERE username = %s and password = %s'''
    try:
        username = json['username']
    except KeyError:
        return response.json({'message': 'Username Empty'},
                             headers={'X-Served-By': 'sanic'},
                             status=401)
    try:
        password = json['password']
    except KeyError:
        return response.json({'message': 'Password Empty'},
                             headers={'X-Served-By': 'sanic'},
                             status=401)
    conn = None
    try:
        conn = makeConn()
        cur = conn.cursor()
        cur.execute(sql, (username, password))
        userid = cur.fetchone()[0]
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    print(userid)
    if(userid):
        return response.json({"message": "OK", "token": buildToken(userid)},
                             headers={'X-Served-By': 'sanic'},
                             status=200)
    else:
        return response.json({'message': 'Failure'},
                             headers={'X-Served-By': 'sanic'},
                             status=401)


def userExists(json):
    sql = '''SELECT username FROM users WHERE username = %s;'''
    try:
        username = json['username']
    except KeyError:
        return response.json({'message': 'Username Empty'},
                             headers={'X-Served-By': 'sanic'},
                             status=401)
    conn = None
    try:
        conn = makeConn()
        cur = conn.cursor()
        cur.execute(sql, (username,))
        username2 = cur.fetchone()
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    if username2 == None:
        return response.json({'userexists': False},
                             headers={'X-Served-By': 'sanic'},
                             status=200)
    else:
        return response.json({'userexists': True},
                             headers={'X-Served-By': 'sanic'},
                             status=200)


def emailExists(json):
    sql = '''SELECT email FROM users WHERE email= %s;'''
    try:
        email = json["email"]
    except KeyError:
        return response.json({'message': 'Email Empty'},
                             headers={'X-Served-By': 'sanic'},
                             status=401)
    conn = None
    try:
        conn = makeConn()
        cur = conn.cursor()
        cur.execute(sql, (email,))
        email2 = cur.fetchone()
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    # if email is in database return True
    if email2 == None:
        return response.json({'emailexists': False},
                             headers={'X-Served-By': 'sanic'},
                             status=200)
    else:
        return response.json({'emailexists': True},
                             headers={'X-Served-By': 'sanic'},
                             status=200)


def getPoll(token, json):
    token_result = tokenIsValid(token)
    if token_result['status'] == 'OK':
        if 'poll_id' not in json:
            return response.json({'message': 'poll_id  Empty'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=401)
        sql = "SELECT * FROM polls WHERE poll_id = %s ;"
        conn = makeConn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, [json["poll_id"], ])
        data = cur.fetchone()
        conn.close()
        data["options"] = js.loads(data["options"])
        return response.json(
            {'message': 'OK', 'data': data},
            headers={'X-Served-By': 'sanic'},
            status=200)
    else:
        return response.json({'message': 'Failure, Token invalid '},
                             headers={'X-Served-By': 'sanic'},
                             status=401)


def getPolls(token):
    token_result = tokenIsValid(token)
    if token_result['status'] == 'OK':
        sql = "SELECT poll_id , name , create_time FROM  polls where creator = %s order by create_time ;"
        conn = makeConn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, (token_result["user"], ))
        data = cur.fetchall()
        conn.close()
        return response.json(
            {'message': 'OK', 'data': data},
            headers={'X-Served-By': 'sanic'},
            status=200)
    else:
        return response.json({'message': 'Failure, Token invalid '},
                             headers={'X-Served-By': 'sanic'},
                             status=401)


def getVote(token, json):
    token_result = tokenIsValid(token)
    if 'poll_id' not in json:
        return response.json({'message': 'poll_id  Empty'},
                             headers={'X-Served-By': 'sanic'},
                             status=401)
    if token_result['status'] == 'OK':
        sql = "SELECT vote_id , user_id , poll , options FROM votes where user_id = %s and poll = %s"
        params = [token_result["user"],  json["poll_id"]]
        print(params)
        conn = makeConn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, params)
        data = cur.fetchone()
        conn.close()
        if data != None:
            return response.json(
                {'message': 'OK', 'data': data},
                headers={'X-Served-By': 'sanic'},
                status=200)
        else:
            return response.json(
                {'message': 'failure', 'data': None},
                headers={'X-Served-By': 'sanic'},
                status=200)
    else:
        return response.json({'message': 'Failure, Token invalid '},
                             headers={'X-Served-By': 'sanic'},
                             status=401)


def getVotes(token):
    token_result = tokenIsValid(token)
    if token_result['status'] == 'OK':
        sql = "SELECT * FROM votes WHERE user_id = %s ;"
        conn = makeConn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, (token_result["user"], ))
        data = cur.fetchall()
        conn.close()
        return response.json(
            {'message': 'OK', 'data': data},
            headers={'X-Served-By': 'sanic'},
            status=200)
    else:
        return response.json({'message': 'Failure, Token invalid '},
                             headers={'X-Served-By': 'sanic'},
                             status=401)
