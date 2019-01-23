import jwt
import psycopg2
from .config import db_config , secrect_key


def makeConn():
    return  psycopg2.connect(db_config)


def buildToken(username):
    """
    get a username and builds token for the user
    """
    return jwt.encode({'sub':username},secrect_key , algorithm='HS256').decode('utf-8') 


def tokenIsValid(token):
    """
    get token an decodes username , if invalid returns False
    """
    result = {
            "status":"OK"
            }
    try:
        result["user"] =  jwt.decode(token ,secrect_key , algorithms='HS256')['sub']
        return result
    except Exception:
        result["status"] = "failure"
        return result
