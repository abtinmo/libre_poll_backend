import jwt
from .config import secrect_key


def buildToken(username):
    """
    get a username and builds token for the user
    """
    return jwt.encode({'sub':username},secrect_key , algorithm='HS256').decode('utf-8') 


def tokenIsValid():
    """
    get token an decodes username , if invalid returns False
    """
    pass
