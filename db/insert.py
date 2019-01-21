import psycopg2
from sanic import response
from .config import db_config , secrect_key
from .functions import tokenIsValid
import uuid
import jwt

def makeConn():
    return  psycopg2.connect(db_config)


def insertUser(json):
    sql = "INSERT INTO users( user_id , username , password , email)  VALUES(%s ,%s, %s , %s);"
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
    if (len(username) < 1) or (len(password) <1):
        return response.json({'message': 'Username or Password is to Short'},
                   headers={'X-Served-By': 'sanic'},
                   status=401)

    try:
        email = json['email']
    except KeyError:
        email = None
    user_id = "User" + uuid.uuid4().hex[:15]


    conn = None
    try:
        conn = makeConn()
        cur = conn.cursor()
        cur.execute( sql, (user_id , username , password , email) )
        cur.close()
        conn.commit()
        result = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        result = False
    finally:
        if conn is not None:
            conn.close()
    if result:
        return response.json(
                    {'message':'OK!'},
                    headers={'X-Served-By': 'sanic'},
                    status=200)
    else:
        return response.json({'message': 'Failure'},
                    headers={'X-Served-By': 'sanic'},
                    status=401)


def setEmail(token , email):

    token_result = tokenIsValid(token)
    if token_result["status"] == "OK":
        sql = "UPDATE users SET email = %s WHERE username = %s"
        conn = makeConn()
        cur = conn.cursor()
        cur.execute(sql ,(email , token_result["user"]))
        conn.commit()
        conn.close()
        return response.json(
                {'message':'OK'},
                headers={'X-Served-By':'sanic'},
                status=200)
    
    else:
        return response.json({'message': 'Failure'},
                    headers={'X-Served-By': 'sanic'},
                    status=401)

    
