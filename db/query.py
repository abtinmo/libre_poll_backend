from .config import db_config
import psycopg2
from sanic import response
from .functions import buildToken

def makeConn():
    return  psycopg2.connect(db_config)

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
        cur.execute( sql, (username , password))
        userid = cur.fetchone()
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    print(userid)
    if(userid):
        return response.json({"message":"OK","token":buildToken(username) },
            headers={'X-Served-By': 'sanic'},
            status=200)
    else:
        return response.json({'message': 'Failure'},
        headers={'X-Served-By': 'sanic'},
        status=401)


