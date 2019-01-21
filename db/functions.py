import jwt
from .config import secrect_key


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
    except Exception:
        result["status"] = "failure"
        return result
