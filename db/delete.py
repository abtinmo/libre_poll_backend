from sanic import response
from .functions import tokenIsValid , makeConn
import psycopg2


def removePoll(token ,json ):
    if 'uuid' not  in json:
        return response.json({'message': 'Username Empty'},
                    headers={'X-Served-By': 'sanic'},
                    status=406)
    token_result = tokenIsValid(token)
    if token_result['status'] == 'OK':
        sql = "DELETE FROM polls where creator = %s  and uuid = %s;"
        print(token_result['user'] , json['uuid'])
        params =[ token_result['user'] ,json['uuid']  ]
        conn = makeConn()
        cur = conn.cursor()
        cur.execute(sql , params )
        conn.commit()
        conn.close()
        return response.json(
                {'message':'OK'},
                headers={'X-Served-By':'sanic'},
                status=200)
    
    else:
        return response.json({'message': 'Failure, Token invalid '},
                    headers={'X-Served-By': 'sanic'},
                    status=401)

    
    

def removeUser(token):
    token_result = tokenIsValid(token)
    if token_result['status'] == 'OK':
        sql = "DELETE FROM users where username = %s ;"
        conn = makeConn()
        cur = conn.cursor()
        cur.execute(sql ,( token_result["user"], ))
        conn.commit()
        conn.close()
        return response.json(
                {'message':'OK'},
                headers={'X-Served-By':'sanic'},
                status=200)
    
    else:
        return response.json({'message': 'Failure, Token invalid '},
                    headers={'X-Served-By': 'sanic'},
                    status=401)

