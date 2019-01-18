import psycopg2
from sanic import response


def makeConn():
    username = "abtin"
    password = "abtin021"
    host = "127.0.0.1"
    database = "librepoll"
    return  psycopg2.connect(host = host,database= database, user= username , password= password)


def insertUser(json):
    sql = "INSERT INTO poll(username , password , email)  VALUES(%s , %s , %s);"
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
    try:
        email = json['email']
    except KeyError:
        email = None
    conn = None
    try:
        conn = makeConn()
        cur = conn.cursor()
        cur.execute( sql, (username , password , email) )
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
        return response.json({'message': 'OK!'},
                    headers={'X-Served-By': 'sanic'},
                    status=200)
    else:
        return response.json({'message': 'Failure'},
                    headers={'X-Served-By': 'sanic'},
                    status=401)

