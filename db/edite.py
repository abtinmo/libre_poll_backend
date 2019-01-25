from sanic import response
from .functions import tokenIsValid , makeConn

def editePoll(token, json) :
    token_result = tokenIsValid(token)
    if token_result['status'] == 'OK':
        sql = "UPDATE polls SET name = %s , description = %s, place = %s,options = %s,last_edit = now() WHERE uuid = %s;"
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
        if 'uuid' not in json:
            return response.json({'message': 'UUID Empty'},
                                 headers={'X-Served-By': 'sanic'},
                                 status=401)
        params = [json['name'], json['description'], json['place'], json['options'], json['uuid']]
        conn = makeConn()
        cur = conn.cursor()
        cur.execute(sql, params,)
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
