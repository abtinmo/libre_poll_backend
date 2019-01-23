from sanic import response
from .functions import buildToken , makeConn
import psycopg2


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
        cur.execute(sql,(username,))
        username2 = cur.fetchone()
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    if username2 == None :
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
    if email2== None:
        return response.json({'emailexists': False},
                             headers={'X-Served-By': 'sanic'},
                             status=200)
    else:
        return response.json({'emailexists': True},
                             headers={'X-Served-By': 'sanic'},
                             status=200)
