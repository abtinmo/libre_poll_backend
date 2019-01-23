from sanic import response
from .functions import tokenIsValid , makeConn
import psycopg2
import uuid
import json as js



def insertUser(json):
    sql = "INSERT INTO users( user_id , username , password , email)  VALUES(%s ,%s, %s , %s);"
    try:
        username = json['username']
    except KeyError:
        return response.json({'message': 'Username Empty'},
                    headers={'X-Served-By': 'sanic'},
                    status=406)
    try:
        password = json['password']
    except KeyError:
        return response.json({'message': 'Password Empty'},
                   headers={'X-Served-By': 'sanic'},
                   status=406)
    if (len(username) < 1) or (len(password) <1):
        return response.json({'message': 'Username or Password is to Short'},
                   headers={'X-Served-By': 'sanic'},
                   status=406)

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
        return response.json({'message': 'Somthing went wrong'},
                    headers={'X-Served-By': 'sanic'},
                    status=500)


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


def addPoll(token , json):
    result = tokenIsValid(token)
    if 'user' in result :
        sql = "INSERT INTO polls(name ,description ,place ,options ,creator,uuid)  VALUES(%s , %s , %s, %s, %s , %s);"
        if 'name' not in json:
            return response.json({'message': 'Name Empty'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=401)
        if 'options' not in json:
            return response.json({'message': 'Options Empty'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=401)
        if 'place' not in json:
            json['plcae'] = None
        if 'description' not in json:
            json['description'] = None
        Uuid = str(uuid.uuid4())
        conn = None
        opts = js.dumps({k: 0 for k in json['options'] } )
        params = [ json['name'] , json['description'] , json['place'] , opts ,
                 result['user'] , Uuid  ]
        try:
            conn = makeConn()
            cur = conn.cursor()
            cur.execute(sql, params )
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
                {'message': 'OK!'},
                headers={'X-Served-By': 'sanic'},
                status=200)
        else:
            return response.json({'message': 'Failure , somthing went wrong'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=500)
    else:
        return response.json({'message': 'Failure , Token invalid'},
                             headers={'X-Served-By': 'sanic'},
                             status=401)
