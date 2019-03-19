from sanic import response
from .functions import tokenIsValid, makeConn
from .query import getVote
import psycopg2
import uuid
import json as js



def addUserToPoll(token, json):
    token_result = tokenIsValid(token)
    if "user_id" not in json:
        return response.json({'message': 'user_id Empty'},
                             headers={'X-Served-By': 'sanic'},
                             status=406)
    if "poll_id" not in json:
        return response.json({'message': 'poll_id Empty'},
                             headers={'X-Served-By': 'sanic'},
                             status=406)
    if token_result["status"] == 'OK':
        try:
            params = [json["poll_id"], json["user_id"], token_result["user"]]
            conn = makeConn()
            cur = conn.cursor()
            cur.callproc('AddUserToPoll', params)
            data = cur.fetchall()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            data = error
        finally:
            if conn is not None:
                conn.close()
        return response.json(
                {'message': 'OK!',"data":data},
            headers={'X-Served-By': 'sanic'},
            status=200)
    else:
        return response.json({'message': 'Token invalid'},
                             headers={'X-Served-By': 'sanic'},
                             status=500)


def addUserToGroup(token, json):
    token_result = tokenIsValid(token)
    if "user_id" not in json:
        return response.json({'message': 'user_id Empty'},
                             headers={'X-Served-By': 'sanic'},
                             status=406)
    if "gp_id" not in json:
        return response.json({'message': 'gp_id Empty'},
                             headers={'X-Served-By': 'sanic'},
                             status=406)
    if token_result["status"] == 'OK':
        try:
            params = [json["gp_id"], json["user_id"], token_result["user"]]
            conn = makeConn()
            cur = conn.cursor()
            cur.callproc('AddUserToGroup', params)
            data = cur.fetchall()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            data = error
        finally:
            if conn is not None:
                conn.close()
        return response.json(
                {'message': 'OK!',"data":data},
            headers={'X-Served-By': 'sanic'},
            status=200)
    else:
        return response.json({'message': 'Token invalid'},
                             headers={'X-Served-By': 'sanic'},
                             status=500)
    

def changeCanAdd(token):
    token_result = tokenIsValid(token)
    print(token)
    conn = None
    if token_result['status'] == 'OK':
        print("token is valid")
        try:
            conn = makeConn()
            cur = conn.cursor()
            cur.callproc('ChangeCanAdd',[token_result["user"], ])
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return response.json(
            {'message': 'OK!'},
            headers={'X-Served-By': 'sanic'},
            status=200)
    else:
        return response.json({'message': 'Token invalid'},
                             headers={'X-Served-By': 'sanic'},
                             status=500)
    

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
    if (len(username) < 1) or (len(password) < 1):
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
        cur.execute(sql, (user_id, username, password, email))
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
        return response.json({'message': 'Somthing went wrong'},
                             headers={'X-Served-By': 'sanic'},
                             status=500)


def setEmail(token, email):
    token_result = tokenIsValid(token)
    if token_result["status"] == "OK":
        sql = "UPDATE users SET email = %s WHERE username = %s"
        conn = makeConn()
        cur = conn.cursor()
        cur.execute(sql, (email, token_result["user"]))
        conn.commit()
        conn.close()
        return response.json(
            {'message': 'OK'},
            headers={'X-Served-By': 'sanic'},
            status=200)
    else:
        return response.json({'message': 'Failure'},
                             headers={'X-Served-By': 'sanic'},
                             status=401)


def addPoll(token, json):
    result = tokenIsValid(token)
    if 'user' in result:
        sql = "INSERT INTO polls(name ,description ,place ,options ,creator,poll_id)  VALUES(%s , %s , %s, %s, %s , %s);"
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
        poll_id = "Poll" + uuid.uuid4().hex[:15]
        conn = None
        opts = js.dumps({k: 0 for k in json['options']})
        params = [json['name'], json['description'], json['place'], opts,
                  result['user'], poll_id]
        try:
            conn = makeConn()
            cur = conn.cursor()
            cur.execute(sql, params)
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


def doVote(token, json):
    """
    this is dirty code , i can't do better so commits are welcome
    gets token , next checks if the vote exists , than gets options from database ,
    adds value to new options , commits new values to database Done.
    """
    token_result = tokenIsValid(token)
    if token_result['status'] == 'OK':
        if ('poll_id' not in json) or ('options' not in json):
            return response.json({'message': 'Poll_id or Options are  Empty'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=401)
        user_options = json['options']
        poll_id = json['poll_id']
        # db part
        sql = "select options from polls where poll_id = %s;"
        sql0 = "select count(*) from votes where user_id = %s and poll = %s;"
        sql1 = "update polls SET options = %s where poll_id = %s ;"
        sql2 = "insert into votes(vote_id , user_id , poll , options) values(%s ,%s ,%s ,%s );"
        conn = None
        try:
            conn = makeConn()
            cur = conn.cursor()
            cur.execute(sql0, [token_result["user"], poll_id])
            vote_exists = cur.fetchone()
            cur.close()
            result = True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            result = False
        finally:
            if conn is not None:
                conn.close()
        print(vote_exists)
        if vote_exists[0] > 0:
            return response.json({'message': 'user voted befor'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=401)

        try:
            conn = makeConn()
            cur = conn.cursor()
            cur.execute(sql, (poll_id,))
            options = cur.fetchone()
            cur.close()
            result = True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            result = False
        finally:
            if conn is not None:
                conn.close()
        print("\n\noptions befor add\n\n", options, "\n\n", user_options)
        options = js.loads(options[0])
        print(options)
        try:
            for key in user_options:
                options[key] += 1
        except KeyError:
            return response.json({'message': 'bad options'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=401)
        options = js.dumps(options)
        print("\n\noptions after add\n\n", options, "\n\n")
        params = [options, poll_id]
        try:
            conn = makeConn()
            cur = conn.cursor()
            cur.execute(sql1, params)
            conn.commit()
            cur.close()
            result = True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            result = False
        finally:
            if conn is not None:
                conn.close()
        params = ["Vote" + uuid.uuid4().hex[:15], token_result['user'], poll_id, user_options]
        print(params)
        try:
            conn = makeConn()
            cur = conn.cursor()
            cur.execute(sql2, params)
            conn.commit()
            cur.close()
            result = True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            result = False
        finally:
            if conn is not None:
                conn.close()
        return response.json(
            {'message': 'OK!'},
            headers={'X-Served-By': 'sanic'},
            status=200)
    else:
        return response.json({'message': 'Failure , Token invalid'},
                             headers={'X-Served-By': 'sanic'},
                             status=401)


def editPoll(token, json):
    token_result = tokenIsValid(token)
    if token_result['status'] == 'OK':
        sql = "UPDATE polls SET name = %s , description = %s, place = %s,options = %s,last_edit = now() WHERE poll_id = %s AND creator = %s  ;"
        if 'name' not in json:
            return response.json({'message': 'Name Empty'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=401)
        if 'options' not in json:
            return response.json({'message': 'Options Empty'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=401)
        if 'poll_id' not in json:
            return response.json({'message': 'UUID Empty'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=401)
        if 'place' not in json:
            json['plcae'] = None
        if 'description' not in json:
            json['description'] = None
        opts = js.dumps({k: 0 for k in json['options']})
        params = [json['name'], json['description'], json['place'],
                  opts, json['poll_id'], token_result['user']]
        conn = makeConn()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        conn.close()
        return response.json(
            {'message': 'OK'},
            headers={'X-Served-By': 'sanic'},
            status=200)

    else:
        return response.json({'message': 'Failure, Token invalid '},
                             headers={'X-Served-By': 'sanic'},
                             status=401)


def addGroup(token, json):
    token_result = tokenIsValid(token)
    sql = '''INSERT INTO gp(gp_id, creator, name ) VALUES (%s, %s, %s)'''
    if token_result['status'] == 'OK':
        if 'name' not in json:
            return response.json({'message': 'Name Empty'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=401)
        gp_id = "Group" + uuid.uuid4().hex[:15]
        params = [gp_id, token_result["user"], json["name"]]
        try:
            conn = makeConn()
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            cur.close()
            result = "OK"
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            result = error
        finally:
            if conn is not None:
                conn.close()
        return response.json(
            {'message': result},
            headers={'X-Served-By': 'sanic'},
            status=200)
    else:
        return response.json({'message': 'Failure , Token invalid'},
                             headers={'X-Served-By': 'sanic'},
                             status=401)
