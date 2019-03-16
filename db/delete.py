from sanic import response
from .functions import tokenIsValid, makeConn
import psycopg2
import json as js


def removeGroup(token, json):
    if 'gp_id' not in json:
        return response.json({'message': 'gp_id Empty'},
                             headers={'X-Served-By': 'sanic'},
                             status=406)
    token_result = tokenIsValid(token)
    if token_result['status'] == 'OK':
        sql = "DELETE FROM gp where creator = %s  and gp_id = %s;"
        params = [token_result['user'], json['gp_id']]
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


def removePoll(token, json):
    if 'poll_id' not in json:
        return response.json({'message': 'poll_id Empty'},
                             headers={'X-Served-By': 'sanic'},
                             status=406)
    token_result = tokenIsValid(token)
    if token_result['status'] == 'OK':
        sql = "DELETE FROM polls where creator = %s  and poll_id = %s;"
        params = [token_result['user'], json['poll_id']]
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


def removeUser(token):
    token_result = tokenIsValid(token)
    if token_result['status'] == 'OK':
        sql = "DELETE FROM users where user_id = %s ;"
        conn = makeConn()
        cur = conn.cursor()
        cur.execute(sql, (token_result["user"], ))
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


def removeVote(token, json):
    token_result = tokenIsValid(token)
    if token_result['status'] == 'OK':
        sql = "update "
        if 'poll_id' not in json:
            return response.json({'message': 'UUID Empty'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=406)
        poll_id = json['poll_id']
        # db part
        sql = "select options from polls where poll_id = %s;"
        sql0 = "select count(*) from votes where user_id = %s and poll = %s;"
        sql11 = "select options from votes where user_id = %s and poll = %s ;"
        sql1 = "update polls SET options = %s where poll_id = %s ;"
        sql2 = "  DELETE FROM votes WHERE user_id = %s  AND poll = %s ; "
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
        if vote_exists[0] == 0:
            return response.json({'message': 'user did\'nt vote befor'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=401)

        try:
            conn = makeConn()
            cur = conn.cursor()
            cur.execute(sql11, [token_result["user"], poll_id])
            user_options = cur.fetchone()[0]
            cur.close()
            result = True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            result = False
        finally:
            if conn is not None:
                conn.close()
        print(user_options)
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
        options = js.loads(options[0])
        try:
            for key in user_options:
                options[key] -= 1
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
        params = [token_result['user'], poll_id]
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
