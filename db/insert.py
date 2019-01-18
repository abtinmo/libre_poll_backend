import psycopg2


def makeConn():
    username = "abtin"
    password = "abtin021"
    host = "127.0.0.1"
    database = "librepoll"
    return  psycopg2.connect(host = host,database= database, user= username , password= password)


def insertUser(json):
    sql = "INSERT INTO poll(username , password , email)  VALUES(%s , %s , %s);"
    params =[json['username'] , json['password'],json['email']]
    conn = None
    try:
        conn = makeConn()
        cur = conn.cursor()
        cur.execute( sql, params  )
        cur.close()
        conn.commit()
        result = 0
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        result = 1
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return result
